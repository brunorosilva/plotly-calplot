from datetime import date, datetime, timedelta

import pandas as pd
from pandas.core.frame import DataFrame


def fill_empty_with_zeros(
    selected_year_data: DataFrame,
    x: str,
    year: int,
    start_month: int,
    end_month: int,
) -> pd.DataFrame:
    """
    Fills empty dates with zeros in the selected year data.

    Args:
        selected_year_data (DataFrame): The data for the selected year.
        x (str): The column name for the date values.
        year (int): The year for which the data is being filled.
        start_month (int): The starting month of the year.
        end_month (int): The ending month of the year.

    Returns:
        pd.DataFrame: The final DataFrame with empty dates filled with zeros.
    """
    if end_month != 12:
        last_date = datetime(year, end_month + 1, 1) + timedelta(days=-1)
    else:
        last_date = datetime(year, 1, 1) + timedelta(days=-1)
    year_min_date = date(year=year, month=start_month, day=1)
    year_max_date = date(year=year, month=end_month, day=last_date.day)
    df = pd.DataFrame({x: pd.date_range(year_min_date, year_max_date)})
    final_df = df.merge(selected_year_data, how="left")
    return final_df


def validate_date_column(date_column: pd.Series, date_fmt: str) -> pd.Series:
    """
    Validate the date column from a DataFrame.

    Parameters:
        data (DataFrame): The input DataFrame.
        x (str): The name of the column containing the date values.

    Returns:
        pd.Series: The date column extracted from the DataFrame.

    Raises:
        ValueError: If the column is not in datetime format.
    """
    if date_column.dtype == "datetime64[ns]":
        return date_column
    elif date_column.dtype == "object":
        try:
            return pd.to_datetime(date_column, format=date_fmt)
        except ValueError:
            raise ValueError(
                f"Date column is not in the {date_fmt} format. Use change date_fmt parameter to match your dates."  # noqa
            )
    try:
        if date_column.dt.tz is not None:
            return date_column.dt.tz_localize(None)
    except Exception as e:
        raise Exception(
            f"Exception {e}\nDate column is not in datetime format or not in the right string format. Please convert it to datetime format first or use the date_fmt parameter."  # noqa
        )
