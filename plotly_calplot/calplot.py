import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from plotly import graph_objects as go
from plotly.subplots import make_subplots


def get_weeknumber_of_date(d):
    """
    Pandas week returns some strange values, this function fixes'em
    """
    if d.month == 1 and d.week > 50:
        return 0
    elif d.month == 12 and d.week < 10:
        return 53
    else:
        return d.week


def year_calplot(
    data: DataFrame,
    x,
    y,
    name,
    year,
    fig,
    row,
    month_lines,
    month_lines_width,
    month_lines_color,
    colorscale,
    gap,
    title,
    dark_theme,
    width,
    each_plot_height=None,
):
    """
    Each year is subplotted separately and added to the main plot
    """
    month_names = list(data[x].dt.month_name().unique())
    month_days = []
    for month in data[x].dt.month.unique():
        month_days.append(data.loc[data[x].dt.month == month].max()[x].day)

    month_positions = (np.cumsum(month_days) - 15) / 7

    weekdays_in_year = [i.weekday() for i in data[x]]

    # sometimes the last week of the current year conflicts with next year's january
    # pandas will give those weeks the number 52 or 53, but this is bad news for this plot
    # therefore we need a correction, for a more in-depth explanation check
    # https://stackoverflow.com/questions/44372048/python-pandas-timestamp-week-returns-52-for-first-day-of-year

    weeknumber_of_dates = (
        data[x].apply(lambda x: get_weeknumber_of_date(x)).values.tolist()
    )

    # the calendar is actually a heatmap :)
    cplt = [
        go.Heatmap(
            x=weeknumber_of_dates,
            y=weekdays_in_year,
            z=data[y],
            xgap=gap,  # this
            ygap=gap,  # and this is used to make the grid-like apperance
            showscale=False,
            colorscale=colorscale,  # user can setup their colorscale
            hovertemplate="%{customdata[0]} <br>%{customdata[1]}=%{z} <br>Week=%{x}",
            customdata=np.stack((data[x].astype(str), [name] * data.shape[0]), axis=-1),
            name=str(year),
        )
    ]

    if month_lines:
        kwargs = dict(
            mode="lines",
            line=dict(color=month_lines_color, width=month_lines_width),
            hoverinfo="skip",
        )
        for date, dow, wkn in zip(data[x], weekdays_in_year, weeknumber_of_dates):
            if date.day == 1:
                cplt += [
                    go.Scatter(x=[wkn - 0.5, wkn - 0.5], y=[dow - 0.5, 6.5], **kwargs)
                ]
                if dow:
                    cplt += [
                        go.Scatter(
                            x=[wkn - 0.5, wkn + 0.5], y=[dow - 0.5, dow - 0.5], **kwargs
                        ),
                        go.Scatter(
                            x=[wkn + 0.5, wkn + 0.5], y=[dow - 0.5, -0.5], **kwargs
                        ),
                    ]

    #    if row == 0:
    if dark_theme:
        layout = go.Layout(
            title=title,
            yaxis=dict(
                showline=False,
                showgrid=False,
                zeroline=False,
                tickmode="array",
                ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                tickvals=[0, 1, 2, 3, 4, 5, 6],
                autorange="reversed",
            ),
            xaxis=dict(
                showline=False,
                showgrid=False,
                zeroline=False,
                tickmode="array",
                ticktext=month_names,
                tickvals=month_positions,
            ),
            font={"size": 10, "color": "#fff"},
            paper_bgcolor=("#333"),
            plot_bgcolor=("#333"),
            margin=dict(t=20, b=20),
            showlegend=False,
        )
        fig.update_layout(layout)
        fig.update_xaxes(layout["xaxis"])
        fig.update_yaxes(layout["yaxis"])

    else:
        layout = go.Layout(
            title=title,
            yaxis=dict(
                showline=False,
                showgrid=False,
                zeroline=False,
                tickmode="array",
                ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                tickvals=[0, 1, 2, 3, 4, 5, 6],
                autorange="reversed",
            ),
            xaxis=dict(
                showline=False,
                showgrid=False,
                zeroline=False,
                tickmode="array",
                ticktext=month_names,
                tickvals=month_positions,
            ),
            font={"size": 10, "color": "#9e9e9e"},
            plot_bgcolor=("#fff"),
            margin=dict(t=20, b=20),
            showlegend=False,
        )
    fig.update_layout(layout)
    fig.update_xaxes(layout["xaxis"])
    fig.update_yaxes(layout["yaxis"])
    fig.update_layout(width=width, height=each_plot_height)
    fig.add_traces(cplt, rows=[(row + 1)] * len(cplt), cols=[1] * len(cplt))

    return fig


def fill_empty_with_zeros(selected_year_data: DataFrame, x, dark_theme, year: int):
    year_min_date = "01-01-" + str(year)
    year_max_date = "31-12-" + str(year)
    df = pd.DataFrame({x: pd.date_range(year_min_date, year_max_date)})
    final_df = df.merge(selected_year_data, how="left")
    if not dark_theme:
        final_df = final_df.fillna(0)
    return final_df


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
):
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
    """
    unique_years = data[x].dt.year.unique()
    unique_years_amount = len(unique_years)
    if years_title:
        subplot_titles = unique_years.astype(str)
    else:
        subplot_titles = None

    if total_height is None:
        total_height = 500 * unique_years_amount

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
            each_plot_height=int(total_height / unique_years_amount),
        )

    return fig
