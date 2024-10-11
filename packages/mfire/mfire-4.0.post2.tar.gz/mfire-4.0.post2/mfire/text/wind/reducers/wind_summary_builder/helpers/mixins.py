from mfire.text.wind.reducers.mixins import BaseSummaryBuilderMixin
from mfire.text.wind.selectors import WindSelector


class WindSummaryBuilderMixin(BaseSummaryBuilderMixin):
    SELECTOR_KEY: str = WindSelector.KEY


class SummaryKeysMixin:
    """SummaryKeysMixin class."""

    START_K: str = "start"
    STOP_K: str = "stop"
    WD_K: str = "wd"
    WI_K: str = "wi"
    PCD_K: str = "pcd"
    PCI_K: str = "pci"
