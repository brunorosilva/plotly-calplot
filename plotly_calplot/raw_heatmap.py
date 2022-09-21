from typing import List, Optional

import numpy as np
import pandas as pd
from plotly import graph_objects as go


def create_heatmap_without_formatting(
    data: pd.DataFrame,
    x: str,
    y: str,
    weeknumber_of_dates: List[int],
    weekdays_in_year: List[float],
    gap: int,
    year: int,
    colorscale: str,
    name: str,
    text: Optional[List[str]] = None,
    text_name: Optional[str] = None,
) -> List[go.Figure]:
    hovertemplate_extra = ""
    if text is not None:
        hovertemplate_extra = " <br>"
        if text_name is not None:
            hovertemplate_extra += f"{text_name}="
        hovertemplate_extra += "%{text}"
    raw_heatmap = [
        go.Heatmap(
            x=weeknumber_of_dates,
            y=weekdays_in_year,
            z=data[y],
            xgap=gap,  # this
            ygap=gap,  # and this is used to make the grid-like apperance
            showscale=False,
            colorscale=colorscale,  # user can setup their colorscale
            text=text,
            hovertemplate=(
                "%{customdata[0]} <br>Week=%{x} <br>%{customdata[1]}=%{z}"
                + hovertemplate_extra
            ),
            customdata=np.stack((data[x].astype(str), [name] * data.shape[0]), axis=-1),
            name=str(year),
        )
    ]
    return raw_heatmap
