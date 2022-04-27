from datetime import datetime
from unittest import TestCase

import pandas as pd
from plotly import graph_objects as go

from plotly_calplot import month_calplot


class TestMonthCalplot(TestCase):
    def setUp(self) -> None:
        # Data copied on 2022-04-27 from test_calplot.py
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
        cp = month_calplot(self.one_year_sample_dataframe, "ds", "value")

        self.assertEqual(len(cp.data), 1)  # Only one figure
        self.assertEqual(cp.layout.yaxis.tickvals, [2019])  # Only one year
        self.assertIsInstance(cp, go.Figure)
        self.assertIsInstance(cp.data, tuple)

    def test_should_create_multi_year(self) -> None:
        cp = month_calplot(self.multi_year_sample_dataframe, "ds", "value")

        self.assertEqual(len(cp.data), 1)  # Only one figure
        self.assertEqual(len(cp.layout.yaxis.tickvals), 7)
        self.assertIsInstance(cp, go.Figure)
        self.assertIsInstance(cp.data, tuple)

    def test_should_create_black_theme_multi_year(self) -> None:
        cp = month_calplot(
            self.multi_year_sample_dataframe, "ds", "value", dark_theme=True
        )

        self.assertEqual(len(cp.data), 1)  # Only one figure
        self.assertEqual(len(cp.layout.yaxis.tickvals), 7)
        self.assertIsInstance(cp, go.Figure)
        self.assertIsInstance(cp.data, tuple)
        self.assertEqual(cp.layout["paper_bgcolor"], "#333")
