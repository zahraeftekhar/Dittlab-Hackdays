import json
import datetime

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# =============================================================================
# load the data
# =============================================================================
with open('./data_A4_2019-11-26.json', 'r') as f:
    data = json.load(f)

# =============================================================================
# set the title of the page
# =============================================================================
st.title('Fundamental Diagram Visualizer')
st.text("@ MYTraffiCZeal")

# =============================================================================
# select the location
# =============================================================================
loc = st.sidebar.selectbox(
    'Location of detector',
    tuple(list(range(152)))
)

# =============================================================================
# starting date time
# =============================================================================
s_date = st.sidebar.date_input(
    "Select your starting date:",
    datetime.date(2019, 11, 26)
)
s_time = st.sidebar.time_input(
    "Select your starting time:",
    datetime.time(4, 0)
)

# =============================================================================
# ending date time
# =============================================================================
e_date = st.sidebar.date_input(
    "Select your ending date:",
    datetime.date(2019, 11, 26)
)
e_time = st.sidebar.time_input(
    "Select your ending date:",
    datetime.time(22, 0)
)

'You selected starting time: ', s_date, s_time
'You selected ending time: ', e_date, e_time
'You selected loop detector:', '#', loc

# =============================================================================
# show the data
# =============================================================================
flow = np.array(data['data']['flow'])[loc]
speed = np.array(data['data']['speed'])[loc]
density = flow / speed
if st.button('Show the data'):
    'The data:'
    st.write(pd.DataFrame({
        'Flow': flow,
        'Speed': speed,
        'Density': flow / speed
    }))
else:
     st.write('Loading data...')


# =============================================================================
# button for showing FD scatter
# =============================================================================
if st.button('Show FD scatter'):
    flow = np.array(data['data']['flow'])[loc]
    speed = np.array(data['data']['speed'])[loc]
    density = flow / speed

    fig = plt.figure(figsize=(14,14))
    plt.subplot(2, 2, 1)
    plt.scatter(flow, speed, marker='o', s=10, c='r')
    plt.xlabel('Flow (veh/hr/lane)')
    plt.ylabel('Speed (km/hr)')
    plt.title('Flow vs Speed')

    plt.subplot(2, 2, 2)
    plt.scatter(density, flow, marker='^', s=10, c='b')
    plt.xlabel('Density (veh/km/lane)')
    plt.ylabel('Flow (veh/hr/lane)')
    plt.title('Density vs Flow')

    plt.subplot(2, 2, 3)
    plt.scatter(density, speed, marker='+', s=10, c='g')
    plt.xlabel('Density (veh/km/lane)')
    plt.ylabel('Speed (km/hr)')
    plt.title('Density vs Speed')
    st.pyplot(fig)
else:
     st.write('Plotting...')

# =============================================================================
# button for showing identified parameters
# =============================================================================
if st.button('Identify parameters'):
    k = 20.9
    s = 93.7
    c = 1704.5
    v = 105.9
    w1, w2 = 103.6, -12.3
    'Critical density:', k, 'veh/km/lane'
    'Speed at critical density:', s, 'km/hr'
    'Capacity:', c, 'veh/hr/lane'
    'Free-fow speed:', v, 'km/hr'
    'Forward wave speed:', w1, 'km/hr'
    'Backward wave speed:', w2, 'km/hr'
else:
     st.write('Identifying...')