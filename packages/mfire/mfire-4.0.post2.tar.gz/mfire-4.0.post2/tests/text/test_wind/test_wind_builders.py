import pytest

from mfire.text.wind.builders import GustParamBuilder, WindBuilder, WindParamBuilder
from mfire.text.wind.const import ERROR_CASE


class TestWindBuilder:
    @staticmethod
    def check_builder_with_bad_summary(summary: dict, builder_class):
        builder = builder_class()
        text, _ = builder.compute(summary)

        assert text == "Erreur dans la génération de la synthèse du vent."

    @staticmethod
    def check_builder(summary: dict, builder_class, assert_equals_result):
        builder = builder_class()
        text, _ = builder.compute(summary)

        assert_equals_result(text)

    @pytest.mark.parametrize(
        "summary",
        [
            # Unknown case for wind
            (
                {
                    "params": {
                        "gust": {
                            "bound_inf": 80,
                            "bound_sup": 100,
                            "gust_max": 110,
                            "period": "lundi après-midi",
                            "case": "2",
                            "units": "km/h",
                        },
                        "wind": {"case": "unknown_case"},
                    }
                }
            ),
            # Error case for wind
            (
                {
                    "params": {
                        "gust": {
                            "bound_inf": 80,
                            "bound_sup": 100,
                            "gust_max": 110,
                            "period": "lundi après-midi",
                            "case": "2",
                            "units": "km/h",
                        },
                        "wind": {"case": ERROR_CASE},
                    }
                }
            ),
            # Unknown selector for wind
            (
                {
                    "params": {
                        "gust": {
                            "bound_inf": 80,
                            "bound_sup": 100,
                            "gust_max": 110,
                            "period": "lundi après-midi",
                            "case": "2",
                            "units": "km/h",
                        },
                        "wind": {"unknown_selector": "2"},
                    }
                }
            ),
            # Unknown case for gust
            (
                {
                    "params": {
                        "gust": {"case": "unknown_case"},
                        "wind": {
                            "case": "2",
                            "units": "km/h",
                            "wi": "modéré",
                            "wd_periods": [],
                        },
                    }
                }
            ),
            # Error case for gust
            (
                {
                    "params": {
                        "gust": {"case": ERROR_CASE},
                        "wind": {
                            "case": "2",
                            "units": "km/h",
                            "wi": "modéré",
                            "wd_periods": [],
                        },
                    }
                }
            ),
            # Unknown selector for gust
            (
                {
                    "params": {
                        "gust": {"unknown_selector": "2"},
                        "wind": {
                            "case": "2",
                            "units": "km/h",
                            "wi": "modéré",
                            "wd_periods": [],
                        },
                    }
                }
            ),
            # Gust summary is missing
            (
                {
                    "params": {
                        "wind": {
                            "case": "2",
                            "units": "km/h",
                            "wi": "modéré",
                            "wd_periods": [],
                        }
                    }
                }
            ),
            # Wind summary is missing
            (
                {
                    "params": {
                        "gust": {
                            "bound_inf": 80,
                            "bound_sup": 100,
                            "gust_max": 110,
                            "period": "lundi après-midi",
                            "case": "2",
                            "units": "km/h",
                        }
                    }
                }
            ),
        ],
    )
    def test_wind_builder_with_bad_summary(self, summary):
        self.check_builder_with_bad_summary(summary, WindBuilder)

    @pytest.mark.parametrize(
        "summary",
        [{"case": "unknown_case"}, {"case": ERROR_CASE}, {"unknown_selector": "2"}],
    )
    def test_wind_param_builder_with_bad_summary(self, summary):
        self.check_builder_with_bad_summary(summary, WindParamBuilder)

    @pytest.mark.parametrize(
        "summary",
        [{"case": "unknown_case"}, {"case": ERROR_CASE}, {"unknown_selector": "2"}],
    )
    def test_gust_param_builder_with_bad_summary(self, summary):
        self.check_builder_with_bad_summary(summary, GustParamBuilder)

    def test_wind_builder(self, assert_equals_result):
        summary = {
            "params": {
                "gust": {
                    "bound_inf": 80,
                    "bound_sup": 100,
                    "gust_max": 110,
                    "period": "lundi après-midi",
                    "case": "2",
                    "units": "km/h",
                },
                "wind": {
                    "case": "2",
                    "units": "km/h",
                    "wi": "modéré",
                    "wd_periods": [],
                },
            }
        }

        self.check_builder(summary, WindBuilder, assert_equals_result)

    def test_wind_param_builder(self, assert_equals_result):
        summary = {"case": "2", "units": "km/h", "wi": "modéré", "wd_periods": []}

        self.check_builder(summary, WindParamBuilder, assert_equals_result)

    def test_gust_param_builder(self, assert_equals_result):
        summary = {
            "bound_inf": 80,
            "bound_sup": 100,
            "gust_max": 110,
            "period": "lundi après-midi",
            "case": "2",
            "units": "km/h",
        }

        self.check_builder(summary, GustParamBuilder, assert_equals_result)
