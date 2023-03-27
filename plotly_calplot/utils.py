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
    if end_month != 12:
        last_date = datetime(year, end_month + 1, 1) + timedelta(days=-1)
    else:
        last_date = datetime(year, 1, 1) + timedelta(days=-1)
    year_min_date = date(year=year, month=start_month, day=1)
    year_max_date = date(year=year, month=end_month, day=last_date.day)
    df = pd.DataFrame({x: pd.date_range(year_min_date, year_max_date)})
    final_df = df.merge(selected_year_data, how="left")
    return final_df
