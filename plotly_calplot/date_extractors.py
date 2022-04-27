from typing import Any, List, Tuple

import numpy as np
import pandas as pd


def get_month_names(data: pd.DataFrame, x: str) -> List[str]:
    return list(data[x].dt.month_name().unique())


def get_date_coordinates(
    data: pd.DataFrame, x: str
) -> Tuple[Any, List[float], List[int]]:
    month_days = []
    for m in data[x].dt.month.unique():
        month_days.append(data.loc[data[x].dt.month == m].max()[x].day)

    month_positions = (np.cumsum(month_days) - 15) / 7
    weekdays_in_year = [i.weekday() for i in data[x]]

    # sometimes the last week of the current year conflicts with next year's january
    # pandas will give those weeks the number 52 or 53, but this is bad news for this plot
    # therefore we need a correction, for a more in-depth explanation check
    # https://stackoverflow.com/questions/44372048/python-pandas-timestamp-week-returns-52-for-first-day-of-year

    weeknumber_of_dates = (
        data[x].apply(lambda x: get_weeknumber_of_date(x)).values.tolist()
    )

    return month_positions, weekdays_in_year, weeknumber_of_dates


def get_weeknumber_of_date(d: pd.Timestamp) -> int:
    """
    Pandas week returns ISO week number, this function
    returns gregorian week date
    """
    return int(d.strftime("%W"))
