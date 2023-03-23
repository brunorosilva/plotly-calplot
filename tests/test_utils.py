from datetime import datetime
from unittest import TestCase

import pandas as pd

from plotly_calplot.utils import fill_empty_with_zeros


class TestUtils(TestCase):
    def test_fill_empty_with_zeros_light_theme(self) -> None:
        selected_year_data = pd.DataFrame(
            {
                "ds": [
                    datetime(2019, 1, 5),
                    datetime(2019, 2, 1),
                    datetime(2019, 3, 1),
                ],
                "y": [3231, 43415, 23123],
            }
        )

        final_df = fill_empty_with_zeros(selected_year_data, "ds", 2019, 1, 12)
        self.assertEqual(final_df.shape[0], 365)

    def test_fill_empty_with_zeros_dark_theme(self) -> None:
        selected_year_data = pd.DataFrame(
            {
                "ds": [
                    datetime(2019, 1, 5),
                    datetime(2019, 2, 1),
                    datetime(2019, 3, 1),
                ],
                "y": [3231, 43415, 23123],
            }
        )
        final_df = fill_empty_with_zeros(selected_year_data, "ds", 2019, 1, 12)

        self.assertEqual(final_df.shape[0], 365)
