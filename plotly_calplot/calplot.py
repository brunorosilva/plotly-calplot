from pandas.core.frame import DataFrame
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from plotly_calplot.layout_formatter import (
    apply_general_colorscaling,
    showscale_of_heatmaps,
)
from plotly_calplot.single_year_calplot import year_calplot
from plotly_calplot.utils import fill_empty_with_zeros


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
    width: int = 800,
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

    width : int = 800
        controls the width of the plot

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
            width=width,
            gap=gap,
            title=title,
            row=i,
            total_height=total_height,
        )

    fig = apply_general_colorscaling(data, y, fig)
    if showscale:
        fig = showscale_of_heatmaps(fig)

    return fig
