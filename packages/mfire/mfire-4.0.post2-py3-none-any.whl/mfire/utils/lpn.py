from __future__ import annotations

from functools import cached_property
from typing import List, Optional

import numpy as np

from mfire.composite.base import BaseModel
from mfire.settings import SPACE_DIM
from mfire.utils import mfxarray as xr
from mfire.utils.calc import round_to_previous_multiple
from mfire.utils.date import Period, PeriodDescriber


class Lpn(BaseModel):
    da: xr.DataArray
    period_describer: PeriodDescriber

    @cached_property
    def extremums_da(self) -> Optional[xr.DataArray]:
        """
        Returns the extremums DataArray of LPN values

        Returns:
            Optional[xr.DataArray]: DataArray containing only the extremums or None if
                no extremums were found
        """
        # Calculation of minimum values
        lpn_da = self.da.min(dim=SPACE_DIM)
        lpn_da = lpn_da.where(~np.isnan(lpn_da), drop=True)
        if lpn_da.size == 0:
            return None

        # Calculation of local extremums
        diffs = np.sign(lpn_da[1:].to_numpy() - lpn_da[:-1].to_numpy())
        extremums, idx_prev_extremum = [], -1
        for idx, diff in enumerate(diffs):
            if diff != 0:
                if idx_prev_extremum != -1 and diffs[idx_prev_extremum] == diff:
                    extremums[idx_prev_extremum] = False
                idx_prev_extremum = idx
                extremums.append(True)
            else:
                extremums.append(False)
        lpn_da = lpn_da[[True] + extremums]

        # Keep 3 variations maximally >= 200
        while (diffs := np.diff(lpn_da)).size > 0 and (
            diffs.size > 3 or min(abs(diffs)) < 200
        ):
            idx = np.argmin(abs(diffs))
            if idx == 0:
                lpn_da[0] = (lpn_da[0] + lpn_da[1]) / 2
                lpn_da = lpn_da.drop_isel(valid_time=1)
            elif idx == len(diffs) - 1:
                lpn_da[-1] = (lpn_da[-1] + lpn_da[-2]) / 2
                lpn_da = lpn_da.drop_isel(valid_time=-2)
            else:
                lpn_da = lpn_da.drop_isel(valid_time=[idx, idx + 1])

        # Keep 3 hours at least
        while (diffs := np.diff(lpn_da.valid_time)).size > 0 and (
            min(diffs).astype("timedelta64[h]") < 3
        ):
            idx = np.argmin(abs(diffs))
            lpn_da[idx] = (lpn_da[idx] + lpn_da[idx + 1]) / 2
            lpn_da = lpn_da.drop_isel(valid_time=idx + 1)

        return round_to_previous_multiple(lpn_da, 100).astype(int)

    @property
    def extremums(self) -> List[int]:
        """Returns the lst of extremum values"""
        return self.extremums_da.values.tolist()

    @property
    def template_key(self) -> Optional[str]:
        """
        Returns the template key correspond to extremum values

        Returns:
            str: template key
        """
        extremums_da = self.extremums_da
        if extremums_da is None:
            return None

        return (
            (
                f"{len(extremums_da)}xlpn"
                f"{'+' if extremums_da[1] > extremums_da[0] else '-'}"
            )
            if extremums_da.size > 1
            else "1xlpn"
        )

    @property
    def temporalities(self) -> List[str]:
        """
        Returns the description of temporalities of extremums values

        Returns:
            List[str]: List of the descriptions of extremums

        """
        return [
            self.period_describer.describe(Period(x.valid_time))
            for x in self.extremums_da
        ]
