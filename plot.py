import datetime

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# select time and location (3 segments)

# showing the speed visualization by heatmap (or something else) -> only selected time

# show the FD

# output some parameters from the FD


# =============================================================================
# set the title of the page
# =============================================================================
st.title('Fundamental Diagram Visualizer')
st.text("@ MYTraffiCZeal")

# =============================================================================
# starting date time
# =============================================================================
s_date = st.sidebar.date_input(
    "Select your starting date:",
    datetime.date(2020, 1, 1)
)
s_time = st.sidebar.time_input(
    "Select your starting time:",
    datetime.time(6, 30)
)

# =============================================================================
# ending date time
# =============================================================================
e_date = st.sidebar.date_input(
    "Select your ending date:",
    datetime.date(2020, 1, 5)
)
e_time = st.sidebar.time_input(
    "Select your ending date:",
    datetime.time(12, 30)
)

'You selected starting time: ', s_date, s_time
'You selected ending time: ', e_date, e_time

# =============================================================================
# show the data
# =============================================================================
'The data:'
st.write(pd.DataFrame({
    'Flow': [10, 20, 30, 40],
    'Speed': [34.5, 26.0, 30.2, 41.0]
}))

# =============================================================================
# button for showing FD scatter
# =============================================================================
if st.button('Show FD scatter'):
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    st.pyplot(fig)
else:
     st.write('Nothing to show.')

# =============================================================================
# button for showing fitted FD (scatter and the triangle)
# =============================================================================
if st.button('Show FD fitted'):
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    st.pyplot(fig)
else:
     st.write('Nothing to show.')