from datetime import datetime
from unittest import TestCase

import pandas as pd
import pytz

from plotly_calplot.utils import fill_empty_with_zeros, validate_date_column


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

    def test_validate_date_column_datetime64(self) -> None:
        date_column = pd.Series(
            [
                datetime(2022, 1, 1),
                datetime(2022, 1, 2),
                datetime(2022, 1, 3),
            ]
        )
        date_fmt = "%Y-%m-%d"

        result = validate_date_column(date_column, date_fmt)

        self.assertEqual(result.dtype, "datetime64[ns]")

    def test_validate_date_column_object(self) -> None:
        date_column = pd.Series(["2022-01-01", "2022-01-02", "2022-01-03"])
        date_fmt = "%Y-%m-%d"

        result = validate_date_column(date_column, date_fmt)

        self.assertEqual(result.dtype, "datetime64[ns]")

    def test_validate_date_column_invalid_format(self) -> None:
        date_column = pd.Series(["2022-01-01", "2022-01-02", "2022-01-03"])
        date_fmt = "%d-%m-%Y"

        with self.assertRaises(ValueError):
            validate_date_column(date_column, date_fmt)

    def test_validate_date_column_invalid_type(self) -> None:
        date_column = pd.Series([1, 2, 3])
        date_fmt = "%Y-%m-%d"

        with self.assertRaises(Exception):
            validate_date_column(date_column, date_fmt)

    def test_validate_date_column_utc_tz(self) -> None:
        tz = pytz.UTC
        date_column = pd.Series(
            [
                datetime(2022, 1, 1, tzinfo=tz),
                datetime(2022, 1, 2, tzinfo=tz),
                datetime(2022, 1, 3, tzinfo=tz),
            ]
        )
        date_fmt = "%Y-%m-%d"

        self.assertTrue(
            validate_date_column(date_column, date_fmt).dtype == "datetime64[ns]"
        )

    def test_validate_date_column_singapore_tz(self) -> None:
        tz = pytz.timezone("Singapore")
        date_column = pd.Series(
            [
                datetime(2022, 1, 1, tzinfo=tz),
                datetime(2022, 1, 2, tzinfo=tz),
                datetime(2022, 1, 3, tzinfo=tz),
            ]
        )
        date_fmt = "%Y-%m-%d"

        self.assertTrue(
            validate_date_column(date_column, date_fmt).dtype == "datetime64[ns]"
        )
