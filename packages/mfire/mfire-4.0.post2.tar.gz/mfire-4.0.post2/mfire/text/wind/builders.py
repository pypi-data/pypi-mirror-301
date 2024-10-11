from __future__ import annotations

from typing import Optional

from mfire.settings import get_logger
from mfire.text.wind import const
from mfire.text.wind.base import BaseMultiParamsBuilder, BaseParamBuilder
from mfire.text.wind.selectors import GustSelector, WindSelector

# Logging
LOGGER = get_logger(name=__name__, bind="wind_builders")


class WindParamBuilder(BaseParamBuilder):
    """WindParamBuilder class."""

    PARAM_NAME = "wind"
    ERROR_CASE: str = const.ERROR_CASE
    SELECTOR_KEY = WindSelector.KEY


class GustParamBuilder(BaseParamBuilder):
    """GustParamBuilder class."""

    PARAM_NAME = "gust"
    DEFAULT_OUTPUT = WindParamBuilder.DEFAULT_OUTPUT
    ERROR_CASE: str = const.ERROR_CASE
    SELECTOR_KEY = GustSelector.KEY


class WindBuilder(BaseMultiParamsBuilder):
    """WindBuilder class."""

    PARAM_BUILDER_CLASSES = [WindParamBuilder, GustParamBuilder]

    def compute(
        self, summary: dict, with_extra: bool = False
    ) -> tuple[Optional[str], Optional[str]]:
        """Compute the synthesis text from a dict summary."""
        text, extra_content = super().compute(summary, with_extra)

        if text is None:
            text = self.DEFAULT_OUTPUT

        return text, extra_content
