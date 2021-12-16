import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from plotly import graph_objects as go
from plotly.subplots import make_subplots

# mock setup
dummy_start_date = "2019-01-01"
dummy_end_date = "2021-10-03"
dummy_df = pd.DataFrame(
    {
        "ds": pd.date_range(dummy_start_date, dummy_end_date),
        "y": np.random.randint(
            0,
            30,
            (pd.to_datetime(dummy_end_date) - pd.to_datetime(dummy_start_date)).days
            + 1,
        ),
    }
)


def year_calplot(data: DataFrame, month_lines, fig, row, title="", height=250):
    month_names = list(data["ds"].dt.month_name().unique())
    month_days = []
    for month in data["ds"].dt.month.unique():
        month_days.append(data.loc[data["ds"].dt.month == month].max()["ds"].day)

    month_positions = (np.cumsum(month_days) - 15) / 7

    weekdays_in_year = [i.weekday() for i in data["ds"]]

    # sometimes the last week of the current year conflicts with next year's january
    # pandas will give those weeks the number 52 or 53, but this is bad news for this plot
    # therefore we need a correction, for a more in-depth explanation check
    # https://stackoverflow.com/questions/44372048/python-pandas-timestamp-week-returns-52-for-first-day-of-year
    weeknumber_of_dates = [
        i.week if not (i.month == 1 and i.week > 50) else 0 for i in data["ds"]
    ]
    # 4cc417 green #347c17 dark green
    colorscale = [[False, "#eeeeee"], [True, "#76cf63"]]

    # handle end of year

    cplt = [
        go.Heatmap(
            x=weeknumber_of_dates,
            y=weekdays_in_year,
            z=data["y"],
            xgap=3,  # this
            ygap=3,  # and this is used to make the grid-like apperance
            showscale=False,
            colorscale=colorscale,
            hovertemplate="%{customdata}, <br>z=%{z}",
            customdata=(data["ds"].astype(str),),
        )
    ]

    if month_lines:
        kwargs = dict(
            mode="lines", line=dict(color="#9e9e9e", width=1), hoverinfo="skip"
        )
        for date, dow, wkn in zip(data["ds"], weekdays_in_year, weeknumber_of_dates):
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

    if row == 0:
        layout = go.Layout(
            title=title,
            height=height,
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
            margin=dict(t=40),
            showlegend=False,
        )
        fig.update_layout(layout)
        fig.update_xaxes(layout["xaxis"])
        fig.update_yaxes(layout["yaxis"])

    fig.add_traces(cplt, rows=[(row + 1)] * len(cplt), cols=[1] * len(cplt))

    return fig


def fill_empty_with_zeros(selected_year_data: DataFrame, year: int):
    year_min_date = "01-01-" + str(year)
    year_max_date = "31-12-" + str(year)
    df = pd.DataFrame({"ds": pd.date_range(year_min_date, year_max_date)})
    final_df = df.merge(selected_year_data, how="left")
    final_df = final_df.fillna(0)
    return final_df


def calplot(data: DataFrame):
    unique_years = data["ds"].dt.year.unique()
    unique_years_amount = len(unique_years)
    fig = make_subplots(unique_years_amount, 1, subplot_titles=unique_years.astype(str))
    for i, year in enumerate(unique_years):
        selected_year_data = data.loc[data["ds"].dt.year == year]
        selected_year_data = fill_empty_with_zeros(selected_year_data, year)

        year_calplot(selected_year_data, month_lines=True, fig=fig, row=i)
        fig.update_layout(height=250 * len(unique_years))

    return fig


def twelve_months_calplot():
    pass


fig = calplot(dummy_df)
fig.show()
