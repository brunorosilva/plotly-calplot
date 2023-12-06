import numpy as np
import pandas as pd

from plotly_calplot.calplot import calplot, month_calplot

# mock setup
dummy_start_date = "2019-01-01"
dummy_end_date = "2022-10-03"
dummy_df = pd.DataFrame(
    {
        "ds": pd.date_range(dummy_start_date, dummy_end_date, tz="Singapore"),
        "value": np.random.randint(
            -10,
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
)

fig1.show()

# same example by month
fig2 = month_calplot(
    dummy_df,
    x="ds",
    y="value",
)
fig2.show()
