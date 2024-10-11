from __future__ import annotations

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers import (
    BaseCaseSummaryBuilder,
    WindSummaryBuilderMixin,
)
from mfire.text.wind.reducers.wind_summary_builder.wind_enum import WindCase

LOGGER = get_logger(name=__name__, bind="case1_summary_builder")


class Case1SummaryBuilder(WindSummaryBuilderMixin, BaseCaseSummaryBuilder):
    """Case1SummaryBuilder class."""

    def run(self):
        """Run the summary builder."""
        self._set_summary_case(WindCase.CASE_1.value)
        return self._summary
