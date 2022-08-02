from pandas.core.frame import DataFrame
from plotly import graph_objects as go

from plotly_calplot.date_extractors import get_date_coordinates, get_month_names
from plotly_calplot.layout_formatter import (
    create_month_lines,
    decide_layout,
    update_plot_with_current_layout,
)
from plotly_calplot.raw_heatmap import create_heatmap_without_formatting


def year_calplot(
    data: DataFrame,
    x: str,
    y: str,
    fig: go.Figure,
    row: int,
    year: int,
    name: str = "y",
    dark_theme: bool = False,
    month_lines_width: int = 1,
    month_lines_color: str = "#9e9e9e",
    gap: int = 1,
    colorscale: str = "greens",
    title: str = "",
    month_lines: bool = True,
    total_height: int = None,
) -> go.Figure:
    """
    Each year is subplotted separately and added to the main plot
    """

    month_names = get_month_names(data, x)
    month_positions, weekdays_in_year, weeknumber_of_dates = get_date_coordinates(
        data, x
    )

    # the calendar is actually a heatmap :)
    cplt = create_heatmap_without_formatting(
        data, x, y, weeknumber_of_dates, weekdays_in_year, gap, year, colorscale, name
    )

    if month_lines:
        cplt = create_month_lines(
            cplt,
            month_lines_color,
            month_lines_width,
            data[x],
            weekdays_in_year,
            weeknumber_of_dates,
        )

    layout = decide_layout(dark_theme, title, month_names, month_positions)
    fig = update_plot_with_current_layout(fig, cplt, row, layout, total_height)

    return fig
