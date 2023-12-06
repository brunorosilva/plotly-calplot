from datetime import datetime
from unittest import TestCase

import pandas as pd
from plotly import graph_objects as go

from plotly_calplot.layout_formatter import (
    create_month_lines,
    decide_layout,
    update_plot_with_current_layout,
)


class TestLayouting(TestCase):
    def setUp(self) -> None:
        self.sample_dataframe = pd.DataFrame(
            [
                (datetime(2019, 1, 1), 13),
                (datetime(2019, 1, 1), 16),
                (datetime(2019, 1, 3), 5),
                (datetime(2019, 3, 31), 2),
                (datetime(2019, 4, 1), 27),
                (datetime(2019, 4, 2), 29),
                (datetime(2019, 4, 3), 20),
                (datetime(2019, 4, 4), 13),
                (datetime(2019, 4, 5), 23),
                (datetime(2019, 5, 30), 0),
            ],
            columns=["ds", "value"],
        )

        self.weeknumber_of_dates = [0, 0, 0, 12, 13, 13, 13, 13, 13, 21]
        self.weekdays_in_year = [1.0, 1.0, 3.0, 6.0, 0.0, 1.0, 2.0, 3.0, 4.0, 3.0]

    def test_should_create_layout_with_black_theme(self) -> None:
        result_layout = decide_layout(
            True, "title", ["January", "March", "April"], [0, 1, 2]
        )
        self.assertTrue(type(result_layout) == go.Layout)

    def test_should_create_layout_with_light_theme(self) -> None:
        result_layout = decide_layout(
            False, "title", ["January", "March", "April"], [0, 1, 2]
        )
        self.assertTrue(type(result_layout) == go.Layout)

    def test_should_create_month_lines(self) -> None:
        result_layout = create_month_lines(
            [],
            "#333",
            1,
            self.sample_dataframe["ds"],
            self.weekdays_in_year,
            self.weeknumber_of_dates,
        )
        self.assertTrue(type(result_layout) == list)
        self.assertTrue(type(result_layout[0]) == go.Scatter)
        self.assertTrue(result_layout[0]["line"]["color"] == "#333")
        self.assertTrue(result_layout[0]["line"]["width"] == 1)
        self.assertTrue(result_layout[0]["mode"] == "lines")

    def test_should_update_plot(self) -> None:
        layout = go.Layout(
            {
                "font": {"color": "#9e9e9e", "size": 10},
                "margin": {"b": 20, "t": 20},
                "plot_bgcolor": "#fff",
                "showlegend": False,
                "title": {"text": "title"},
                "xaxis": {
                    "showgrid": False,
                    "showline": False,
                    "tickmode": "array",
                    "ticktext": ["January", "March", "April"],
                    "tickvals": [0, 1, 2],
                    "zeroline": False,
                },
                "yaxis": {
                    "autorange": "reversed",
                    "showgrid": False,
                    "showline": False,
                    "tickmode": "array",
                    "ticktext": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    "tickvals": [0, 1, 2, 3, 4, 5, 6],
                    "zeroline": False,
                },
            }
        )
        result = update_plot_with_current_layout(go.Figure(), [], 0, layout, 100, False)
        self.assertEqual(result.layout.font, layout.font)
        self.assertEqual(result.layout.margin, layout.margin)
        self.assertEqual(result.layout.plot_bgcolor, layout.plot_bgcolor)
        self.assertEqual(result.layout.showlegend, layout.showlegend)
        self.assertEqual(result.layout.title, layout.title)
        self.assertEqual(result.layout.xaxis, layout.xaxis)
        self.assertEqual(result.layout.yaxis, layout.yaxis)
        self.assertTrue(type(result) == go.Figure)
