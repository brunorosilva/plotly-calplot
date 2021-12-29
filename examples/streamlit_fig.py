import numpy as np
import pandas as pd
import streamlit as st

from plotly_calplot.calplot import calplot

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
fig = calplot(
    dummy_df,
    x="ds",
    y="value",
)

st.plotly_chart(fig)
