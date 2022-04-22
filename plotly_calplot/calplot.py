from datetime import date
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from plotly import graph_objects as go
from plotly.subplots import make_subplots


def _get_weeknumber_of_date(d):
    """
    Pandas week returns ISO week number, this function
    returns gregorian week date
    """
    return int(d.strftime('%W'))


def _get_subplot_layout(**kwargs) -> go.Layout:
    """
    Combines the default subplot layout with the customized parameters
    """
    dark_theme = kwargs.pop('dark_theme', False)
    yaxis = kwargs.pop('yaxis', {})
    xaxis = kwargs.pop('xaxis', {})

    def _dt(b, a):
        return a if dark_theme else b

    return go.Layout(**{
        'yaxis': {
            'showline': False,
            'showgrid': False,
            'zeroline': False,
            'tickmode': 'array',
            'autorange': 'reversed',
            **yaxis,
        },
        'xaxis': {
            'showline': False,
            'showgrid': False,
            'zeroline': False,
            'tickmode': 'array',
            **xaxis,
        },
        'font': {'size': 10, 'color': _dt('#9e9e9e', '#fff')},
        'plot_bgcolor': _dt('#fff', '#333'),
        'paper_bgcolor': _dt(None, '#333'),
        'margin': {'t': 20, 'b': 20},
        'showlegend': False,
        **kwargs,
    })


def _year_subplot(
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
    total_height,
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
        data[x].apply(lambda x: _get_weeknumber_of_date(x)).values.tolist()
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

    layout = _get_subplot_layout(
        dark_theme=dark_theme,
        title=title,
        yaxis=dict(
            ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            tickvals=[0, 1, 2, 3, 4, 5, 6],
        ),
        xaxis=dict(
            ticktext=month_names,
            tickvals=month_positions,
        ),
        width=width,
        height=total_height
    )

    fig.update_layout(layout)
    fig.update_xaxes(layout["xaxis"])
    fig.update_yaxes(layout["yaxis"])
    fig.add_traces(cplt, rows=[(row + 1)] * len(cplt), cols=[1] * len(cplt))

    return fig


def fill_empty_with_zeros(selected_year_data: DataFrame, x, dark_theme, year: int):
    year_min_date = date(year=year, month=1, day=1)
    year_max_date = date(year=year, month=12, day=31)
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

        _year_subplot(
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

    return fig

def month_calplot(
    data: DataFrame = None,
    x: str = "x",
    y: str = "y",
    name: str = "y",
    dark_theme: bool = False,
    gap: int = 2,
    width: int = 400,
    colorscale: str = "greens",
    title: str = "",
    year_height: int = 30,
    total_height: int = None,
    showscale: bool = False,
):
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

    width : int = 400
        controls the width of the plot

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
        if not isinstance(x, pd.Series):
            x = pd.Series(x, dtype='datetime64[ns]', name='x')

        if not isinstance(y, pd.Series):
            y = pd.Series(y, dtype='float64', name='y')

        data = pd.DataFrame({x.name: x, y.name: y})

        x = x.name
        y = y.name

    gData = data.set_index(x)[y].groupby(pd.Grouper(freq='M')).sum()
    unique_years = gData.index.year.unique()
    unique_years_amount = len(unique_years)

    if total_height is None:
        total_height = 20+max(10, year_height * unique_years_amount)

    layout = _get_subplot_layout(
        dark_theme=dark_theme,
        width=width,
        height=total_height,
        title=title,
        yaxis={
            'tickvals': unique_years,
        },
        xaxis={
            'tickvals': list(range(12))
        },
    )

    cplt = go.Heatmap(
        x=gData.index.month,
        y=gData.index.year,
        z=gData,
        name=title,
        showscale=showscale,
        xgap=gap,
        ygap=gap,
        colorscale=colorscale,
        customdata=np.stack((gData.index.astype(str), [name] * gData.shape[0]), axis=-1),
        hovertemplate="%{customdata[0]} <br>%{customdata[1]}=%{z} <br>Month=%{x}",
    )

    fig = go.Figure(data=cplt, layout=layout)

    return fig
