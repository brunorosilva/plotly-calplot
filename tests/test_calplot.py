from datetime import datetime
from unittest import TestCase

import pandas as pd
from plotly import graph_objects as go

from plotly_calplot.calplot import calplot


class TestCalplot(TestCase):
    def setUp(self) -> None:
        self.one_year_sample_dataframe = pd.DataFrame(
            [
                (datetime(2019, 1, 1), 13),
                (datetime(2019, 1, 1), 16),
                (datetime(2019, 1, 3), 5),
                (datetime(2019, 3, 31), 2),
                (datetime(2019, 4, 1), 27),
                (datetime(2019, 4, 2), 29),
                (datetime(2019, 4, 3), 20),
                (datetime(2019, 4, 4), 13),
                (datetime(2019, 4, 5), 23),
                (datetime(2019, 5, 30), 0),
            ],
            columns=["ds", "value"],
        )
        self.multi_year_sample_dataframe = pd.DataFrame(
            [
                (datetime(2019, 1, 1), 13),
                (datetime(2019, 1, 1), 16),
                (datetime(2020, 1, 3), 5),
                (datetime(2020, 3, 31), 2),
                (datetime(2021, 4, 1), 27),
                (datetime(2022, 4, 2), 29),
                (datetime(2023, 4, 3), 20),
                (datetime(2024, 4, 4), 13),
                (datetime(2024, 4, 5), 23),
                (datetime(2025, 5, 30), 0),
            ],
            columns=["ds", "value"],
        )

    def test_should_create_one_year_only(self) -> None:
        cp = calplot(self.one_year_sample_dataframe, "ds", "value")
        self.assertTrue(len(cp.data) == 36)
        self.assertTrue(type(cp.data) == tuple)
        self.assertTrue(type(cp) == go.Figure)

    def test_should_create_multi_year(self) -> None:
        cp = calplot(self.multi_year_sample_dataframe, "ds", "value")

        self.assertTrue(len(cp.data) == 236)
        self.assertTrue(type(cp.data) == tuple)
        self.assertTrue(type(cp) == go.Figure)

    def test_should_create_black_theme_multi_year(self) -> None:
        cp = calplot(self.multi_year_sample_dataframe, "ds", "value", dark_theme=True)

        self.assertTrue(len(cp.data) == 236)
        self.assertTrue(type(cp.data) == tuple)
        self.assertTrue(type(cp) == go.Figure)
        self.assertTrue(cp.layout["paper_bgcolor"] == "#333")

    def test_should_create_with_years_title(self) -> None:
        cp = calplot(self.multi_year_sample_dataframe, "ds", "value", years_title=True)

        self.assertTrue(len(cp.data) == 236)
        self.assertTrue(type(cp.data) == tuple)
        self.assertTrue(type(cp) == go.Figure)
