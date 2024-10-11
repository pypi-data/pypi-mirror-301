from mfire.settings import get_logger
from mfire.text.wind.base.selectors import BaseSelector

# Logging
LOGGER = get_logger(name=__name__, bind="wind_selectors")


class WindSelector(BaseSelector):
    """WindSelector class."""


class GustSelector(BaseSelector):
    """GustSelector class."""
