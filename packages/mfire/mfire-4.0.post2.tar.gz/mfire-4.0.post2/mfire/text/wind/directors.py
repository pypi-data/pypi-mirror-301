"""WindDirector submodule."""

from mfire.settings import get_logger
from mfire.text.wind.base.directors import BaseDirector
from mfire.text.wind.builders import WindBuilder
from mfire.text.wind.reducers.wind_reducer import WindReducer

# Logging
LOGGER = get_logger(name=__name__, bind="wind_directors")


class WindDirector(BaseDirector):
    """WindDirector class."""

    REDUCER: WindReducer = WindReducer
    BUILDER: WindBuilder = WindBuilder
    WITH_EXTRA: bool = False
