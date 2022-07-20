from datetime import date
from typing import Any, Dict

from pandas import DataFrame, Grouper, Series
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from plotly_calplot.layout_formatter import (
    apply_general_colorscaling,
    showscale_of_heatmaps,
)
from plotly_calplot.single_year_calplot import year_calplot
from plotly_calplot.utils import fill_empty_with_zeros


def _get_subplot_layout(**kwargs: Any) -> go.Layout:
    """
    Combines the default subplot layout with the customized parameters
    """
    dark_theme: bool = kwargs.pop("dark_theme", False)
    yaxis: Dict[str, Any] = kwargs.pop("yaxis", {})
    xaxis: Dict[str, Any] = kwargs.pop("xaxis", {})

    def _dt(b: Any, a: Any) -> Any:
        return a if dark_theme else b

    return go.Layout(
        **{
            "yaxis": {
                "showline": False,
                "showgrid": False,
                "zeroline": False,
                "tickmode": "array",
                "autorange": "reversed",
                **yaxis,
            },
            "xaxis": {
                "showline": False,
                "showgrid": False,
                "zeroline": False,
                "tickmode": "array",
                **xaxis,
            },
            "font": {"size": 10, "color": _dt("#9e9e9e", "#fff")},
            "plot_bgcolor": _dt("#fff", "#333"),
            "paper_bgcolor": _dt(None, "#333"),
            "margin": {"t": 20, "b": 20},
            "showlegend": False,
            **kwargs,
        }
    )


def calplot(
    data: DataFrame,
    x: str,
    y: str,
    name: str = "y",
    dark_theme: bool = False,
    month_lines_width: int = 1,
    month_lines_color: str = "#9e9e9e",
    gap: int = 1,
    years_title: bool = False,
    colorscale: str = "greens",
    title: str = "",
    month_lines: bool = True,
    total_height: int = None,
    space_between_plots: float = 0.08,
    showscale: bool = False,
) -> go.Figure:
    """
    Yearly Calendar Heatmap

    Parameters
    ----------
    data : DataFrame
        Must contain at least one date like column and
        one value column for displaying in the plot

    x : str
        The name of the date like column in data

    y : str
        The name of the value column in data

    dark_theme : bool = False
        Option for creating a dark themed plot

    month_lines: bool = True
        if true will plot a separation line between
        each month in the calendar

    month_lines_width : int = 1
        if month_lines this option controls the width of
        the line between each month in the calendar

    month_lines_color : str = "#9e9e9e"
        if month_lines this option controls the color of
        the line between each month in the calendar

    gap : int = 1
        controls the gap bewteen daily squares

    years_title : bool = False
        if true will add a title for each subplot with the
        correspondent year

    colorscale : str = "greens"
        controls the colorscale for the calendar, works
        with all the standard Plotly Colorscales and also
        supports custom colorscales made by the user

    title : str = ""
        title of the plot

    total_height : int = None
        if provided a value, will force the plot to have a specific
        height, otherwise the total height will be calculated
        according to the amount of years in data

    space_between_plots: float = 0.08
        controls the vertical space between the plots

    showscale: bool = False
        if True, a color legend will be created.
        Thanks to @ghhar98!
    """
    unique_years = data[x].dt.year.unique()
    unique_years_amount = len(unique_years)
    if years_title:
        subplot_titles = unique_years.astype(str)
    else:
        subplot_titles = None

    if total_height is None:
        total_height = 150 * unique_years_amount

    fig = make_subplots(
        unique_years_amount,
        1,
        subplot_titles=subplot_titles,
        vertical_spacing=space_between_plots,
    )
    for i, year in enumerate(unique_years):
        selected_year_data = data.loc[data[x].dt.year == year]
        selected_year_data = fill_empty_with_zeros(
            selected_year_data, x, dark_theme, year
        )

        year_calplot(
            selected_year_data,
            x,
            y,
            name=name,
            month_lines=month_lines,
            month_lines_width=month_lines_width,
            month_lines_color=month_lines_color,
            colorscale=colorscale,
            year=year,
            fig=fig,
            dark_theme=dark_theme,
            gap=gap,
            title=title,
            row=i,
            total_height=total_height,
        )

    fig = apply_general_colorscaling(data, y, fig)
    if showscale:
        fig = showscale_of_heatmaps(fig)

    return fig


def month_calplot(
    data: DataFrame = None,
    x: str = "x",
    y: str = "y",
    name: str = "y",
    dark_theme: bool = False,
    gap: int = 2,
    colorscale: str = "greens",
    title: str = "",
    year_height: int = 30,
    total_height: int = None,
    showscale: bool = False,
) -> go.Figure:
    """
    Yearly Calendar Heatmap by months (12 cols per row)

    Parameters
    ----------
    data : DataFrame | None
        Must contain at least one date like column and
        one value column for displaying in the plot. If data is None, x and y will
        be used

    x : str | Iterable
        The name of the date like column in data or the column if data is None

    y : str | Iterable
        The name of the value column in data or the column if data is None

    dark_theme : bool = False
        Option for creating a dark themed plot

    gap : int = 2
        controls the gap bewteen monthly squares

    colorscale : str = "greens"
        controls the colorscale for the calendar, works
        with all the standard Plotly Colorscales and also
        supports custom colorscales made by the user

    title : str = ""
        title of the plot

    year_height: int = 30
        the height per year to be used if total_height is None

    total_height : int = None
        if provided a value, will force the plot to have a specific
        height, otherwise the total height will be calculated
        according to the amount of years in data

    showscale : bool = False
        wether to show the scale of the data
    """
    if data is None:
        if not isinstance(x, Series):
            x = Series(x, dtype="datetime64[ns]", name="x")

        if not isinstance(y, Series):
            y = Series(y, dtype="float64", name="y")

        data = DataFrame({x.name: x, y.name: y})

        x = x.name
        y = y.name

    gData = data.set_index(x)[y].groupby(Grouper(freq="M")).sum()
    unique_years = gData.index.year.unique()
    unique_years_amount = len(unique_years)

    if total_height is None:
        total_height = 20 + max(10, year_height * unique_years_amount)

    layout = _get_subplot_layout(
        dark_theme=dark_theme,
        height=total_height,
        title=title,
        yaxis={
            "tickvals": unique_years,
        },
        xaxis={
            "tickvals": list(range(1, 13)),
            "ticktext": [date(1900, i, 1).strftime("%b") for i in range(1, 13)],
            "tickangle": 45,
        },
    )

    # hovertext = _gen_hoverText(gData.index.month, gData.index.year, gData)
    hovertext = gData.apply(lambda x: f"{x:.0f}")

    cplt = go.Heatmap(
        x=gData.index.month,
        y=gData.index.year,
        z=gData,
        name=title,
        showscale=showscale,
        xgap=gap,
        ygap=gap,
        colorscale=colorscale,
        hoverinfo="text",
        text=hovertext,
    )

    fig = go.Figure(data=cplt, layout=layout)

    return fig
