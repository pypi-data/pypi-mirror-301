from __future__ import annotations

import re
from typing import Optional

import numpy as np
from pydantic import model_validator

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseModel
from mfire.composite.component import RiskComponentComposite
from mfire.localisation.spatial_localisation import SpatialLocalisation
from mfire.localisation.table_localisation import TableLocalisation
from mfire.localisation.temporal_localisation import TemporalLocalisation
from mfire.settings import N_CUTS, get_logger
from mfire.utils.exception import LocalisationWarning

# Logging
LOGGER = get_logger(name="localisation", bind="localisation")

# seuil pour considérer qu'un ensemble de zones recouvre l'axe
GENERALISATION_THRESHOLD = 0.9


class RiskLocalisation(BaseModel):
    """
    Class representing the localisation of a risk.

    Args:
        risk_component: The associated risk component.
        geo_id: The geographical identifier of the localisation.
        alt_min: The minimum altitude of the localisation (in meters).
        alt_max: The maximum altitude of the localisation (in meters).
    """

    risk_component: RiskComponentComposite
    geo_id: str

    alt_min: Optional[int] = None
    alt_max: Optional[int] = None

    spatial_localisation: Optional[SpatialLocalisation] = None
    table_localisation: Optional[TableLocalisation] = None

    def compute(self):
        """
        Compute the localized risk.

        This method performs the spatial and temporal localisation of the risk.
        """

        # Perform the spatial localisation.
        self.spatial_localisation = SpatialLocalisation(
            component=self.risk_component, geo_id=self.geo_id
        ).compute()
        areas_with_occ = self.spatial_localisation.areas_with_occurrence

        # Perform the temporal localisation.
        cover = (
            self.spatial_localisation.areas.sel(id=areas_with_occ.id).count()
            / self.spatial_localisation.domain.count()
        )

        table_3p = TemporalLocalisation(data=areas_with_occ).compute()

        # If the coverage is below the generalization threshold, we need to handle the
        # case where not all areas are covered by the risk.
        if cover < GENERALISATION_THRESHOLD:
            # we need to add a zero-risk area to the division.
            if len(areas_with_occ.id) < N_CUTS:
                # If there are only two or fewer areas with occurrence, add one
                table_3p = xr.concat(
                    [
                        table_3p,
                        xr.DataArray(
                            np.zeros((1, table_3p.period.size)),
                            coords={
                                "id": ["zero"],
                                "period": table_3p.period.values,
                                "areaName": (["id"], ["Zone Zero"]),
                                "altAreaName": (["id"], ["Zone Zero"]),
                                "areaType": (["id"], [""]),
                            },
                            dims=["id", "period"],
                            name="elt",
                        ),
                    ],
                    dim="id",
                )
                self.spatial_localisation.areas = xr.concat(
                    [
                        self.spatial_localisation.areas,
                        xr.DataArray(
                            coords={
                                "id": ["zero"],
                                "areaName": (["id"], ["Zone Zero"]),
                                "altAreaName": (["id"], ["Zone Zero"]),
                                "areaType": (["id"], [""]),
                            },
                            dims=["id"],
                        ),
                    ],
                    dim="id",
                )
            else:
                # zero the last one
                table_3p = table_3p.copy()
                table_3p[:, -1] = 0
                LOGGER.warning(
                    f"Truncated last zone {areas_with_occ.id[-1].data}"
                    f" to avoid general axe {self.geo_id}"
                )
        # If all the temporal periods are on the same areas and those areas cover almost
        # the entire axis, we can set the risk to be monozone.
        identical_period = True
        for zones_idx in range(1, table_3p.sizes["period"]):
            if (table_3p[0, :] != table_3p[zones_idx, :]).any() and (
                table_3p[zones_idx, :] != 0
            ).any():
                identical_period = False
                break
        if identical_period and cover > GENERALISATION_THRESHOLD:
            raise LocalisationWarning("Localised zones merely cover axe.")

        # Finally, aggregate the risk temporally.
        self.table_localisation = TableLocalisation(
            data=table_3p,
            spatial_localisation=self.spatial_localisation,
            alt_min=self.alt_min,
            alt_max=self.alt_max,
        ).compute()
        return self

    @model_validator(mode="after")
    def init_alt_min_and_alt_max(self) -> RiskLocalisation:
        """
        Initializes the `alt_min` and `alt_max` attributes of the `RiskLocalisation`
        instance.

        Returns:
            dict: A dictionary containing the updated values of the `RiskLocalisation`
                instance.
        """
        max_level = self.risk_component.final_risk_max_level(self.geo_id)
        levels = self.risk_component.levels
        if max_level > 0:
            levels = self.risk_component.risks_of_level(level=max_level)

        self.alt_min = min((lvl.alt_min for lvl in levels), default=None)
        self.alt_max = max((lvl.alt_max for lvl in levels), default=None)
        return self

    @property
    def periods_name(self) -> list:
        """Get the names of periods."""
        return list(self.table_localisation.data.period.values.tolist())

    @property
    def unique_name(self) -> str:
        """Get the unique name."""
        return self.table_localisation.name

    @property
    def is_multizone(self) -> bool:
        """
        Check whether the localized risk is multizone.

        A localized risk is multizone if it covers multiple areas.

        Returns:
            bool: True if the localized risk is multizone, False otherwise.
        """
        return (
            self.table_localisation is not None
            and len(self.table_localisation.table) > 1
        )

    @property
    def template_type(self) -> str:
        """
        Returns the template type based on the variables encountered at the given level.
        Only the variables at this level are taken into account.

        Returns:
            str: The template type.

        Raises:
            ValueError: If the level does not exist.
        """
        # Get the level.
        risk_level = self.spatial_localisation.risk_level
        level = self.risk_component.risks_of_level(level=risk_level)
        if len(level) == 0:
            raise ValueError(f"Level {risk_level} does not exist.")

        # Get the comparison dictionary of the level.
        dict_comparison = level[0].get_comparison()

        # Get the list of variable prefixes.
        l_prefix = []
        for variable in dict_comparison.keys():
            prefix = variable.split("_")[0]
            pattern = r"[0-9]"
            l_prefix.append(re.sub(pattern, "", prefix))

        # Get the set of variable prefixes.
        variable_set = set(l_prefix)

        # If there is only one variable, return its type.
        if len(variable_set) == 1:
            variable = list(variable_set)[0]
            if variable in ["PRECIP", "EAU"]:
                return "precip"
            if variable in ["NEIPOT"]:
                return "snow"

        # Otherwise, return "GENERIC".
        return "generic"

    @property
    def all_name(self) -> str:
        data = self.table_localisation.data
        if data.raw[0] == "0":
            areas_idx = [str(i + 2) for i in range(len(data) - 1)]
        else:
            areas_idx = [str(i + 1) for i in range(len(data))]

        return self.table_localisation.table["zone" + "_".join(areas_idx)]
