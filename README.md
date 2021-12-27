# Calendar Heatmap with Plotly
Making it easier to visualize and costumize time relevant or time series data with plotly interaction.

This plot is a very similar to the contribuitions available on Github and Gitlab profile pages and to [Calplot](https://github.com/tomkwok/calplot) - which is a pyplot implementation of the calendar heatmap, thus it is not interactive right off the bat.

The first mention I could find of this plot being made with plotly was in [this forum post](https://community.plotly.com/t/colored-calendar-heatmap-in-dash/10907/16) and it got my attention as something it should be easily available to anyone.

# Installation
TODO: upload the package to pypi

# Examples
TODO: write usage examples
```
from plotlycalplot import calplot
import plotly.graph_objects as go

fig = go.Figure()
fig.add_traces(calplot(df, x="date", y="value"))
fig.show()
```
