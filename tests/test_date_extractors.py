from datetime import datetime
from unittest import TestCase

import numpy as np
import pandas as pd

from plotly_calplot.date_extractors import get_date_coordinates, get_month_names


class TestUtils(TestCase):
    def setUp(self) -> None:
        self.sample_dataframe = pd.DataFrame(
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

    def test_should_get_month_names(self) -> None:
        expected_result = ["January", "March", "April", "May"]
        month_names = get_month_names(self.sample_dataframe, "ds")

        self.assertTrue(len(month_names) == 4)
        self.assertEqual(month_names, expected_result)

    def test_should_get_date_right_coordinates(self) -> None:
        month_positions, weekdays_in_year, weeknumber_of_dates = get_date_coordinates(
            self.sample_dataframe, "ds"
        )

        self.assertEqual(len(month_positions), 12)
        self.assertTrue(type(month_positions) == np.ndarray)
        self.assertEqual(len(weekdays_in_year), self.sample_dataframe.shape[0])
        self.assertTrue(max(weekdays_in_year) <= 6)
        self.assertTrue(min(weekdays_in_year) >= 0)
        self.assertEqual(len(weeknumber_of_dates), self.sample_dataframe.shape[0])
        self.assertTrue(max(weeknumber_of_dates) <= 53)
        self.assertTrue(min(weeknumber_of_dates) >= 0)
