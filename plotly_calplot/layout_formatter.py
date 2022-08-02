from typing import Any, List, Optional

import pandas as pd
from plotly import graph_objects as go


def decide_layout(
    dark_theme: bool,
    title: str,
    month_names: List[str],
    month_positions: Any,
) -> go.Layout:
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

    return layout


def create_month_lines(
    cplt: List[go.Figure],
    month_lines_color: str,
    month_lines_width: int,
    data: pd.DataFrame,
    weekdays_in_year: List[float],
    weeknumber_of_dates: List[int],
) -> go.Figure:
    kwargs = dict(
        mode="lines",
        line=dict(color=month_lines_color, width=month_lines_width),
        hoverinfo="skip",
    )
    for date, dow, wkn in zip(data, weekdays_in_year, weeknumber_of_dates):
        if date.day == 1:
            cplt += [go.Scatter(x=[wkn - 0.5, wkn - 0.5], y=[dow - 0.5, 6.5], **kwargs)]
            if dow:
                cplt += [
                    go.Scatter(
                        x=[wkn - 0.5, wkn + 0.5], y=[dow - 0.5, dow - 0.5], **kwargs
                    ),
                    go.Scatter(x=[wkn + 0.5, wkn + 0.5], y=[dow - 0.5, -0.5], **kwargs),
                ]
    return cplt


def update_plot_with_current_layout(
    fig: go.Figure,
    cplt: go.Figure,
    row: int,
    layout: go.Layout,
    total_height: Optional[int],
) -> go.Figure:
    fig.update_layout(layout)
    fig.update_xaxes(layout["xaxis"])
    fig.update_yaxes(layout["yaxis"])
    fig.update_layout(height=total_height)
    fig.add_traces(cplt, rows=[(row + 1)] * len(cplt), cols=[1] * len(cplt))
    return fig


def apply_general_colorscaling(data: pd.DataFrame, y: str, fig: go.Figure) -> go.Figure:
    return fig.update_traces(selector=dict(type="heatmap"), zmax=data[y].max(), zmin=0)


def showscale_of_heatmaps(fig: go.Figure) -> go.Figure:
    return fig.update_traces(
        showscale=True,
        selector=dict(type="heatmap"),
    )
