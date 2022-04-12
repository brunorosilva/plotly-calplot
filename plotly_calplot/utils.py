from datetime import date

import pandas as pd
from pandas.core.frame import DataFrame


def fill_empty_with_zeros(
    selected_year_data: DataFrame, x: str, dark_theme: bool, year: int
) -> pd.DataFrame:
    year_min_date = date(year=year, month=1, day=1)
    year_max_date = date(year=year, month=12, day=31)
    df = pd.DataFrame({x: pd.date_range(year_min_date, year_max_date)})
    final_df = df.merge(selected_year_data, how="left")
    if not dark_theme:
        final_df = final_df.fillna(0)
    return final_df
