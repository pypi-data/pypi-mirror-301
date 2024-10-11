from collections import defaultdict
from functools import cached_property
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

import mfire.utils.mfxarray as xr
from mfire.localisation.altitude import AltitudeInterval
from mfire.localisation.area_algebra import compute_IoL
from mfire.settings import Settings, get_logger
from mfire.text.synthesis.builder import SynthesisBuilder
from mfire.text.synthesis.reducer import SynthesisReducer
from mfire.utils.calc import (
    all_combinations_and_remaining,
    combinations_and_remaining,
    round_to_previous_multiple,
)
from mfire.utils.date import Period, Periods
from mfire.utils.string import _, concatenate_string, decapitalize
from mfire.utils.unit_converter import from_w1_to_wwmf
from mfire.utils.wwmf import (
    WWMF_SUBGRP,
    is_precipitation,
    is_severe,
    is_snow,
    is_visibility,
    wwmf_families,
    wwmf_label,
    wwmf_subfamilies,
)

# Logging
LOGGER = get_logger(name="weather.mod", bind="weather")


class WeatherReducer(SynthesisReducer):
    """WeatherReducer  class for the weather module."""

    # Structure of computed data
    _ts: defaultdict = defaultdict(lambda: {"temp": Periods()})

    # Dictionary giving the minimum values to be considered not isolated
    # The keys are the corresponding WWMF codes
    densities: dict = {
        "DT": {
            "required": defaultdict(lambda: 0.05),
            "precipitation": 0.0,
            "visibility": 0.0,
        },
        "DHmax": {
            "required": defaultdict(lambda: 0.05),
            "precipitation": 0.0,
            "visibility": 0.0,
        },
    }

    def has_required_density(self, density: str) -> bool:
        return (
            self.densities["DT"][density] >= self.densities["DT"]["required"][density]
            or self.densities["DHmax"][density]
            >= self.densities["DHmax"]["required"][density]
        )

    @cached_property
    def has_risk_fog(self) -> Optional[bool]:
        return self.has_risk("Brouillard dense et/ou givrant")

    @cached_property
    def has_risk_snow(self) -> Optional[bool]:
        return self.has_risk("Neige")

    def _pre_process(self):
        """Pre-processing step."""
        # Clean old values
        self._ts.clear()

        # Convert if necessary
        if self.composite_data["wwmf"].units == "w1":
            self.composite_data["wwmf"] = from_w1_to_wwmf(self.composite_data["wwmf"])

        # Replace current codes with nebulosity
        replacing_codes = {72: 71, 73: 70, 78: 77, 82: 81, 83: 80}
        for old, new in replacing_codes.items():
            self.composite_data["wwmf"] = self.composite_data["wwmf"].where(
                self.composite_data["wwmf"] != old, other=new
            )

        # Replace some values when it’s riding with D+3/D+4 (#39102)
        if 50 in self.composite_data["wwmf"]:
            self.composite_data["wwmf"] = self.composite_data["wwmf"].where(
                ~self.composite_data["wwmf"].isin([51, 52, 53, 58]), other=50
            )
        if 60 in self.composite_data["wwmf"]:
            self.composite_data["wwmf"] = self.composite_data["wwmf"].where(
                ~self.composite_data["wwmf"].isin([61, 62, 63]), other=60
            )
        if 90 in self.composite_data["wwmf"]:
            self.composite_data["wwmf"] = self.composite_data["wwmf"].where(
                ~self.composite_data["wwmf"].isin([91, 92, 93]), other=90
            )

        # Handle the inconsistency problem with LPN and Alpha
        if "lpn" in self.composite_data:
            consistencies_map = ~is_snow(self.composite_data["wwmf"]) | (
                self.composite_data["lpn"] < self.composite.altitude("lpn")
            )
            if not consistencies_map.all():
                LOGGER.warning(
                    "Some inconsistencies with snow and LPN were found and fixed"
                )
                self.composite_data["wwmf"] = self.composite_data["wwmf"].where(
                    consistencies_map, other=50
                )

    def _process(self):
        """
        Process the reduction by retrieving sensitive TS codes and storing their
        valid_time information.
        """
        self.densities["DT"]["precipitation"] = 0
        self.densities["DHmax"]["precipitation"] = 0
        self.densities["DT"]["visibility"] = 0
        self.densities["DHmax"]["visibility"] = 0

        previous_time = self.first_time
        for time in self.times:
            data_for_fixed_time: xr.DataArray = self.composite_data.wwmf.sel(
                valid_time=time.as_np_dt64
            )
            all_ts, counts = np.unique(data_for_fixed_time, return_counts=True)

            dh_visibility, dh_precipitation = 0.0, 0.0
            for ts, count in zip(all_ts, counts):
                # Mist is not considered in order to avoid over-representation of the
                # Alpha model
                if ts == 31:
                    continue

                ts_families = wwmf_families(ts)
                if not ts_families:  # Skip if it's not a TS
                    continue

                self._ts[ts]["temp"].append(
                    Period(begin_time=previous_time, end_time=time)
                )

                # Store the DHMax to remove isolated phenomenon later
                dh = (count / data_for_fixed_time.count()).item()

                if is_visibility(ts):
                    dh_visibility += dh
                else:
                    dh_precipitation += dh

            self.densities["DT"]["visibility"] += dh_visibility / len(self.times)
            self.densities["DT"]["precipitation"] += dh_precipitation / len(self.times)
            self.densities["DHmax"]["visibility"] = max(
                self.densities["DHmax"]["visibility"], dh_visibility
            )
            self.densities["DHmax"]["precipitation"] = max(
                self.densities["DHmax"]["precipitation"], dh_precipitation
            )

            previous_time = time

        # Apply different rules
        self._process_densities()
        self._process_temporalities()

    def _process_densities(self):
        """Process all densities to remove isolated phenomena"""
        ts_to_exclude = []
        if not any(is_severe(ts) for ts in self._ts) and not self.has_required_density(
            "precipitation"
        ):
            ts_to_exclude += [ts for ts in self._ts if is_precipitation(ts)]

        if not self.has_required_density("visibility") and not self.has_risk_fog:
            ts_to_exclude += [ts for ts in self._ts if is_visibility(ts)]

        for ts in ts_to_exclude:
            del self._ts[ts]

    def _process_temporalities(self):
        """
        Process all temporalities to remove short phenomena and apply grouping rules.

        This method reduces the temporalities and removes short phenomena from the data.
        It helps generate sentences and apply grouping rules accordingly.
        """
        ts_to_remove = []

        # Calculate the number of temporalities to keep based on the time range
        nbr_temporalities_to_keep = 2 + (self.times[-1] - self.times[0]).days

        for ts, info in self._ts.items():
            # Reduce the temporality using PeriodDescriber
            info["temp"] = self.period_describer.reduce(
                info["temp"], n=nbr_temporalities_to_keep
            )

            # Let temporalities with total hours greater than 3
            if info["temp"].total_hours >= 3:
                continue

            if is_visibility(ts) and self.has_risk_fog:
                continue

            ts_to_remove.append(ts)

        # Remove the temporalities marked for removal
        for ts in ts_to_remove:
            del self._ts[ts]

    def _describe(self, *args) -> List[Dict]:
        """
        Generate a dictionary of descriptions based on the list of TS codes.

        Args:
            *args: List of TS codes.

        Returns:
            List[Dict]: Dictionaries of reduced data.
        """
        # Merge groups of TS with same labels
        labels = defaultdict(lambda: ([], {"temp": Periods()}))
        for ts_group, info in args:
            label = wwmf_label(*ts_group)
            labels[label] = (
                labels[label][0] + ts_group,
                self._concat_infos(
                    info, labels[label][1], is_severe=info.get("is_severe", False)
                ),
            )

        # Sort the TS codes based on the begin_time of temporality
        tuples = sorted(
            labels.values(),
            key=lambda x: (x[1]["temp"].begin_time, -x[1]["temp"].total_hours),
        )

        main_TS, severe_TS = [], []
        period_describer = self.period_describer

        for ts_group, info in tuples:
            if info.get("is_severe"):  # Handling of severe phenomenon
                severe_TS.append(
                    {
                        "key": "severe",
                        "lab": decapitalize(wwmf_label(*ts_group)),
                        "loc": self._process_localisation(ts_group, info["temp"]),
                    }
                )
                continue

            label = wwmf_label(*ts_group)

            # Handle fog - see 38534
            if all(is_visibility(ts) for ts in ts_group):
                if self.has_risk_fog is False:
                    label = wwmf_label(*ts_group, labels=Settings().wwmf_labels_no_risk)
                elif not self.has_required_density("visibility"):
                    label = _("{label} possible localement").format(
                        label=decapitalize(label)
                    )
                elif info["temp"].total_hours < 3:
                    label = _("temporairement {label}").format(
                        label=decapitalize(label)
                    )

            # Check if there are multiple temporalities or if the first temporality
            # doesn't cover the entire requested time range
            if (
                len(info["temp"]) > 1
                or info["temp"][0].begin_time > self.first_time
                or info["temp"][0].end_time < self.times[-1]
            ):
                temporality = period_describer.describe(info["temp"])
            else:
                temporality = None

            main_TS.append(
                {
                    "lab": label if temporality is None else decapitalize(label),
                    "loc": self._process_localisation(ts_group, info["temp"]),
                    "key": "1xTS" if temporality is None else "1xTS_temp",
                    "temp": temporality.capitalize()
                    if temporality is not None
                    else None,
                }
            )

        return (main_TS or [{"key": "0xTS"}]) + severe_TS

    def _concat_infos(self, *args, is_severe: bool = False) -> dict:
        """
        Concatenate information by summing the temporalities.

        Args:
            *args: List of TS codes.
            is_severe (bool): Flag indicating if it's a severe phenomenon.

        Returns:
            dict: Concatenated information.
        """

        # Combine all the temporalities of the TS codes
        all_temporalities = Periods()
        for arg in args:
            all_temporalities += (arg if isinstance(arg, dict) else self._ts[arg])[
                "temp"
            ]

        result = {"temp": self.period_describer.reduce(all_temporalities)}
        if is_severe:
            result["is_severe"] = True

        return result

    def _process_localisation(self, wwmfs: List[int], temp: Periods) -> str:
        """
        Process localisation based on given wwmfs codes.

        This method processes the localisation based on data.
        It determines the location based on the map and altitude information.
        The determined location is assigned to the corresponding time series.
        """
        wwmfs = [ts for ts in wwmfs if ts not in [30, 31, 32]]
        if not wwmfs:
            return ""

        # If there are snow and other kind of precipitations, only the snow is localized
        any_snow = any(is_snow(ts) for ts in wwmfs)
        if any_snow and any(not is_snow(ts) for ts in wwmfs):
            wwmfs = [ts for ts in wwmfs if is_snow(ts)]

        precipitation_map = (
            self.composite_data["wwmf"]
            .isin(wwmfs)
            .sel(
                valid_time=slice(
                    temp.begin_time.without_tzinfo, temp.end_time.without_tzinfo
                )
            )
            .sum("valid_time")
            > 0
        )

        geos_data = self.composite.geos_data(self.geo_id)
        geos_data_size = geos_data.sum().data

        # Determine the location based on map and altitude information
        if precipitation_map.sum().data / geos_data_size >= 0.9:
            return geos_data.altAreaName.item()

        ratio_iol = compute_IoL(
            self.composite.geos_descriptive(self.geo_id), precipitation_map
        )
        if ratio_iol is not None:
            return (
                concatenate_string(ratio_iol.areaName.values)
                if ratio_iol.sum().data / geos_data_size < 0.9
                else geos_data.altAreaName.item()
            )

        if not any_snow:
            return ""

        min_altitude = round_to_previous_multiple(
            self.composite.altitude("wwmf").where(precipitation_map).min(), 100
        )
        if min_altitude - self.composite.altitude("wwmf").where(geos_data).min() < 100:
            # Take into account the minimum altitude of an area for localisation #38200
            return geos_data.altAreaName.item()

        return (
            AltitudeInterval((min_altitude, np.inf)).name() if min_altitude > 0 else ""
        )

    def _merge_same_ts_family(self, *args) -> List[Tuple[List[int], dict]]:
        """
        This function takes a list of TS of the same family as an argument, merges them,
        and returns a list of tuples (list of TS, info) for all descriptions.

        Args:
            *args: Variable-length list of TS.

        Returns:
            List[Tuple[List[int], dict]]: List of tuples containing the TS code and
            information for each merged description.
        """
        ts1, ts2 = args[0], args[1]
        info1, info2 = self._ts[ts1], self._ts[ts2]

        if len(args) == 2:
            # If TS are considered to have different temporalities
            if (
                any(is_severe(wwmf) for wwmf in args)
                and info1["temp"].hours_of_intersection(info2["temp"])
                / info1["temp"].hours_of_union(info2["temp"])
                < 0.75
            ) or not info1["temp"].are_same_temporalities(info2["temp"]):
                return [([ts1], info1), ([ts2], info2)]

            return [([ts1, ts2], self._concat_infos(ts1, ts2))]

        # In this case we have three args
        ts3 = args[2]

        # We try to gather two of them according to the same possible temporality
        # and TS
        for [_ts1, _ts2], [_ts3] in combinations_and_remaining([ts1, ts2, ts3], 2):
            _temp1 = self._ts[_ts1]["temp"]
            _temp2 = self._ts[_ts2]["temp"]
            _temp3 = self._ts[_ts3]["temp"]

            if (
                _temp1.are_same_temporalities(_temp2)
                and not _temp1.are_same_temporalities(_temp3)
                and not _temp2.are_same_temporalities(_temp3)
            ):
                return [
                    ([_ts1, _ts2], self._concat_infos(_ts1, _ts2)),
                    ([_ts3], self._ts[_ts3]),
                ]

        # If we can't gather two of them with the same temporality and TS
        return [([ts1, ts2, ts3], self._concat_infos(ts1, ts2, ts3))]

    def _post_process(self) -> List[Dict]:
        """
        Post-processes the data to be treated by the template key selector.

        Returns:
            List[Dict]: Post-processed data.
        """
        nbr_ts = len(self._ts)
        if nbr_ts == 0:
            return [{"key": "0xTS"}]
        if nbr_ts == 1:
            return self._post_process_1_ts()
        if nbr_ts == 2:
            return self._post_process_2_ts()
        if nbr_ts == 3:
            return self._post_process_3_ts()
        return self._post_process_more_than_3_ts()

    def _post_process_1_ts(self) -> List[Dict]:
        """
        Post-processes data when there is only one TS.

        Returns:
            List[Dict]: Post-processed data.
        """
        items_iter = iter(self._ts.items())
        ts1, info1 = next(items_iter)
        return self._describe(([ts1], info1))

    def _post_process_2_ts(self) -> List[Dict]:
        """
        Post-processes data when there are two TS.

        Returns:
            List[Dict]: Post-processed data.
        """
        items_iter = iter(self._ts.keys())
        ts1 = next(items_iter)
        ts2 = next(items_iter)

        # If families are different we don't merge even if temporalities are the same
        if is_visibility(ts1) ^ is_visibility(ts2):
            info1, info2 = [self._ts[ts] for ts in [ts1, ts2]]
            return self._describe(([ts1], info1), ([ts2], info2))

        descriptions = self._merge_same_ts_family(ts1, ts2)
        return self._describe(*descriptions)

    def _post_process_3_ts(self) -> List[Dict]:
        """
        Post-processes data when there are three TS.

        Returns:
            List[Dict]: Post-processed data.
        """
        items_iter = iter(self._ts.items())
        ts1, _ = next(items_iter)
        ts2, _ = next(items_iter)
        ts3, _ = next(items_iter)

        # Handle TS of same family
        if all(is_visibility(ts) for ts in [ts1, ts2, ts3]) or all(
            is_precipitation(ts) for ts in [ts1, ts2, ts3]
        ):
            descriptions = self._merge_same_ts_family(ts1, ts2, ts3)
            return self._describe(*descriptions)

        # Handle TS of different families
        if all(is_visibility(ts) for ts in [ts1, ts2]) or all(
            is_precipitation(ts) for ts in [ts1, ts2]
        ):
            same_family, other_family = [ts1, ts2], ts3
        elif all(is_visibility(ts) for ts in [ts1, ts3]) or all(
            is_precipitation(ts) for ts in [ts1, ts3]
        ):
            same_family, other_family = [ts1, ts3], ts2
        else:
            same_family, other_family = [ts2, ts3], ts1
        return self._describe(
            (same_family, self._concat_infos(*same_family)),
            ([other_family], self._ts[other_family]),
        )

    def _post_process_more_than_3_ts(self) -> List[Dict]:
        description_args = []

        visibility_codes, precipitation_codes = [], []
        for wwmf in self._ts.keys():
            (visibility_codes, precipitation_codes)[int(is_precipitation(wwmf))].append(
                wwmf
            )

        if len(visibility_codes) > 0:
            visibility_infos = (
                self._concat_infos(*(wwmf for wwmf in visibility_codes if wwmf != 31))
                if visibility_codes != [31]
                else self._ts[31]
            )

            if len(visibility_codes) == 2 and 31 in visibility_codes:
                visibility_codes = [
                    visibility_codes[0]
                    if visibility_codes[0] != 31
                    else visibility_codes[1]
                ]
            description_args.append((visibility_codes, visibility_infos))

        nb_precipitation = len(precipitation_codes)
        if nb_precipitation == 1:
            description_args.append(
                ([precipitation_codes[0]], self._ts[precipitation_codes[0]])
            )
        elif nb_precipitation in [2, 3]:
            description_args += self._merge_same_ts_family(*precipitation_codes)
        elif nb_precipitation > 3:
            # We try to not treat severe phenomenon as distinct
            if nb_precipitation > 10:
                LOGGER.warning(
                    f"Grand nombre de précipitations : {nb_precipitation}"
                    f" {precipitation_codes}"
                )
                # too much time with precipitation_code
                rr_families = wwmf_subfamilies(*precipitation_codes)
                all_combi = all_combinations_and_remaining(
                    rr_families, is_symmetric=True
                )
            else:
                all_combi = all_combinations_and_remaining(
                    precipitation_codes, is_symmetric=True
                )
            for combined_ts1, combined_ts2 in all_combi:
                if nb_precipitation > 10:
                    # recreate combined_ts from combined subfamilies
                    combined_rr1 = [subfam.value for subfam in combined_ts1]
                    combined_rr2 = [subfam.value for subfam in combined_ts2]
                    combined_ts1 = list(set(combined_rr1) & set(precipitation_codes))
                    combined_ts2 = list(set(combined_rr2) & set(precipitation_codes))

                if (
                    all(ts in WWMF_SUBGRP.B_group for ts in combined_ts1)
                    and all(ts not in WWMF_SUBGRP.B_group for ts in combined_ts2)
                ) or (
                    all(ts not in WWMF_SUBGRP.B_group for ts in combined_ts1)
                    and all(ts in WWMF_SUBGRP.B_group for ts in combined_ts2)
                ):
                    continue  # Otherwise it could be treated as distinct

                if (
                    wwmf_label(*combined_ts1, concatenate=False) is None
                    or wwmf_label(*combined_ts2, concatenate=False) is None
                ):
                    continue

                combined_temp1 = [self._ts[ts]["temp"] for ts in combined_ts1]
                combined_temp2 = [self._ts[ts]["temp"] for ts in combined_ts2]
                if not combined_temp1[0].are_same_temporalities(
                    *combined_temp1[1:]
                ) or not combined_temp2[0].are_same_temporalities(*combined_temp2[1:]):
                    continue

                if not sum(combined_temp1, start=Periods()).are_same_temporalities(
                    sum(combined_temp2, start=Periods())
                ):
                    description_args.append(
                        (combined_ts1, self._concat_infos(*combined_ts1))
                    )
                    description_args.append(
                        (combined_ts2, self._concat_infos(*combined_ts2))
                    )
                    break
            else:
                if wwmf_label(*precipitation_codes, concatenate=False) is not None:
                    description_args.append(
                        (precipitation_codes, self._concat_infos(*precipitation_codes))
                    )
                else:
                    # Otherwise, we treat severe phenomenon if present as distinct
                    A_group, B_group = [], []
                    for ts in precipitation_codes:
                        if ts in WWMF_SUBGRP.B_group:
                            B_group.append(ts)
                        else:
                            A_group.append(ts)

                    if A_group:
                        description_args.append((A_group, self._concat_infos(*A_group)))
                    if B_group:
                        description_args.append(
                            (B_group, self._concat_infos(*B_group, is_severe=True))
                        )
        return self._describe(*description_args)

    def _process_lpn(self) -> List[Dict]:
        if (
            "lpn" not in self.composite_data
            or all(not is_snow(wwmf) for wwmf in self._ts)
            or self.has_risk_snow
        ):
            return []

        lpn = int(
            round_to_previous_multiple(
                self.composite_data["lpn"]
                .where(is_snow(self.composite_data["wwmf"]))
                .min()
                .item(),
                100,
            )
        )
        if lpn <= self.composite.altitude("lpn").min().data:
            return [{"key": "LPN_ground"}]
        return [{"key": "LPN", "low": lpn}]

    def _compute(self) -> List[Dict]:
        self._pre_process()
        self._process()
        return self._post_process() + self._process_lpn()


class WeatherBuilder(SynthesisBuilder):
    """
    BaseBuilder class that must build texts for weather
    """

    reducer_class: type = WeatherReducer

    @property
    def template_name(self) -> str:
        """Get the template name."""
        return "weather"

    @property
    def template_key(self) -> Union[str, List[str]]:
        """Get the template key."""
        return [reduction["key"] for reduction in self.reduction]
