from abc import ABC
from typing import Optional

import mfire.utils.mfxarray as xr
from mfire.composite.component import SynthesisComposite
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name=__name__, bind="base_reducers")


class BaseReducer(ABC):
    """BaseReducer class.

    Its is used to compute a data summary as a dictionary.
    """

    PARAM_SUMMARIES_KEY = "params"
    META_KEY = "meta"

    def __init__(self):
        self.data: Optional[xr.DataArray] = None
        self.summary: dict = {}

    def reset(self):
        """Reset data attribute."""
        self.data = None
        self.summary: dict = {}

    def compute(self, geo_id: str, composite: SynthesisComposite) -> dict:
        """Build a summary as a dictionary."""
        self.reset()
        self.data = composite.compute(geo_id=geo_id, force=True)

        return self.summary
