from typing import Optional

from mfire.composite.component import SynthesisComposite
from mfire.settings import get_logger
from mfire.text.base.reducer import BaseReducer
from mfire.utils.date import PeriodDescriber

LOGGER = get_logger(name="synthesis_reducer.mod", bind="synthesis_reducer")


class SynthesisReducer(BaseReducer):
    """
    SynthesisBuilder class that must make the reduction for synthesis texts
    """

    composite: Optional[SynthesisComposite]

    @property
    def period_describer(self) -> PeriodDescriber:
        return self.composite.component.period_describer

    def has_risk(self, risk_name: str) -> Optional[bool]:
        """
        Checks if a specific risk occurred within a given geographical area and
        timeframe.

        Args:
            risk_name (str): The name of the risk to check for.

        Returns:
            Optional[bool]:
                - True if the specified risk occurred within the area and timeframe.
                - False if the risk does not occurre.
                - None if there is no risk within the given geographical area and
                    timeframe.
        """
        valid_times = self.composite_data["valid_time"].data
        return self.composite.interface.has_risk(
            risk_name,
            self.composite.geos.all_sub_areas(self.geo_id),
            slice(valid_times[0], self.composite_data["valid_time"][-1]),
        )
