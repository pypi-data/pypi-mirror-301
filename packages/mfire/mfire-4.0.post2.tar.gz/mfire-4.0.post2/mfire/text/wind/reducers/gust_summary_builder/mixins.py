from mfire.text.wind.reducers.mixins import BaseSummaryBuilderMixin
from mfire.text.wind.selectors import GustSelector


class GustSummaryBuilderMixin(BaseSummaryBuilderMixin):
    SELECTOR_KEY: str = GustSelector.KEY
