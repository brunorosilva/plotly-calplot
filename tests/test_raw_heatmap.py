from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pandas as pd

from plotly_calplot.raw_heatmap import create_heatmap_without_formatting


class TestRawHeatmap(TestCase):
    def setUp(self) -> None:
        self.weeknumber_of_dates = [0, 0, 0, 12, 13, 13, 13, 13, 13, 21]
        self.weekdays_in_year = [1.0, 1.0, 3.0, 6.0, 0.0, 1.0, 2.0, 3.0, 4.0, 3.0]

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

    @patch("plotly_calplot.raw_heatmap.go")
    def test_should_create_raw_heatmap(self, hm_mock: MagicMock) -> None:
        hm = create_heatmap_without_formatting(
            self.sample_dataframe,
            "ds",
            "value",
            self.weeknumber_of_dates,
            self.weekdays_in_year,
            1,
            2020,
            "greens",
            "y",
        )
        hm_mock.Heatmap.assert_called()
        self.assertTrue(type(hm), list)
