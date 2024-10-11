from abc import ABC, abstractmethod
from collections import defaultdict
from itertools import pairwise

from mfire.text.wind.reducers.wind_summary_builder.case3.wind_direction import Pcd
from mfire.text.wind.reducers.wind_summary_builder.helpers import (
    SummaryKeysMixin,
    WindSummaryBuilderMixin,
)
from mfire.text.wind.reducers.wind_summary_builder.wind_intensity import Pci
from mfire.utils.date import Datetime

from .wind_block import WindBlock


class BlockSummaryBuilder(WindSummaryBuilderMixin, SummaryKeysMixin, ABC):
    def __init__(self, blocks: list[WindBlock]):
        super().__init__()
        self._pci: list[Pci] = []  # Period with Common wind Intensity
        self._pcd: list[Pcd] = []  # Period with Common wind Direction
        self._counters: defaultdict = defaultdict(int)

        self._preprocess(blocks)

    @property
    def pci_cnt(self) -> int:
        return self._counters["pci"]

    @property
    def pcd_cnt(self) -> int:
        return self._counters["pcd"]

    @property
    def extra_condition(self) -> str:
        return "simultaneous_change"

    def _get_extra_condition(self) -> str:
        if (
            self.pci_cnt == 2
            and self.pcd_cnt == 2
            and self._pci[1].begin_time == self._pcd[1].begin_time
        ):
            return self.extra_condition
        return ""

    @classmethod
    def pci_sorted_key(cls, period: Pci):
        return period.wi.interval[0], period.begin_time

    def _process_pci(self) -> None:
        self._counters["pci"] = len(self._pci)

        if self.pci_cnt > 2:
            interval_upper_bounds: list[int] = [pci.wi.interval[0] for pci in self._pci]

            # If self.pci is not sorted along wind_intensity, then do it
            if not all(x < y for x, y in pairwise(interval_upper_bounds)) and not all(
                x > y for x, y in pairwise(interval_upper_bounds)
            ):
                self._pci.sort(key=self.pci_sorted_key)
            # Else, it's like if there are only 2 periods
            else:
                # Keep only the 1st and the last period
                self._pci = [self._pci[i] for i in (0, -1)]
                self._counters["pci"] = 2

        if self.pci_cnt == 2 and self._pci[0].has_same_intensity_than(self._pci[1]):
            self._pci[0].update(self._pci[1])
            self._pci = [self._pci[0]]
            self._counters["pci"] = 1

    @abstractmethod
    def _process_pcd(self) -> None:
        pass

    @abstractmethod
    def _preprocess(self, blocks: list[WindBlock]) -> None:
        """Compute pci and pcd periods and set the case."""
        pass

    def _build_and_set_case(self, extra_condition: str, *elts) -> None:
        if extra_condition != "":
            elts += (extra_condition,)
        case: str = "_".join(elts)
        self._set_summary_case(case)

    def compute(self, reference_datetime: Datetime) -> dict:
        """Compute the block summary."""

        # Update the summary with the pci and pcd summarizes
        self._summary.update(
            {
                # If more than 2 PCI, get only the summary of the 1st and the last PCI
                # Else,
                self.PCI_K: [
                    self._pci[i].summarize(reference_datetime)
                    for i in range(0, -min(self.pci_cnt, 2), -1)
                ],
                # Get summary of all PCD
                self.PCD_K: [p.summarize(reference_datetime) for p in self._pcd],
            }
        )

        return self._summary
