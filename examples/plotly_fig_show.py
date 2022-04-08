import numpy as np
import pandas as pd

from plotly_calplot.calplot import calplot, month_calplot

# mock setup
dummy_start_date = "2019-01-01"
dummy_end_date = "2021-10-03"
dummy_df = pd.DataFrame(
    {
        "ds": pd.date_range(dummy_start_date, dummy_end_date),
        "value": np.random.randint(
            0,
            30,
            (pd.to_datetime(dummy_end_date) - pd.to_datetime(dummy_start_date)).days
            + 1,
        ),
    }
)
fig1 = calplot(
    dummy_df,
    x="ds",
    y="value",
    dark_theme=True
)

fig1.show()

# same example by month
fig2 = month_calplot(
    dummy_df,
    x="ds",
    y="value",
    dark_theme=True,
    showscale=True,
)
fig2.show()
