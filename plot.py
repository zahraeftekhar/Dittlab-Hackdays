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

show_data = st.checkbox('Show data')
show_fd_scatter = st.checkbox('Show FD scatter')
show_params = st.checkbox('Show identified parameters')

flow = np.array(data['data']['flow'])[loc]
speed = np.array(data['data']['speed'])[loc]
density = flow / speed

# =============================================================================
# show the data
# =============================================================================
if show_data:
    st.header('Data for detector #' + str(loc) + ':')
    st.warning('Density is calculated from flow and speed. Be careful to use!')
    df = pd.DataFrame({
        'Flow': flow,
        'Speed': speed,
        'Density': flow / speed
    })
    'The data:'
    st.write(df)
    
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='data_' + str(loc) + '.csv',
        mime='text/csv',
    )


# =============================================================================
# button for showing FD scatter
# =============================================================================
if show_fd_scatter:
    st.header('FD scatter plot for detector #' + str(loc) + ':')
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


# =============================================================================
# button for showing identified parameters
# =============================================================================
if show_params:
    st.header('Identified parameters for detector #' + str(loc) + ':')
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






import folium
from streamlit_folium import folium_static
import pandas as pd 
import numpy as np

#     import streamlit as st
# from streamlit import session_state
linestring_fn = 'A4-1.txt'
with open (linestring_fn, 'r') as f:
    linestring = f.read()
linestring = json.loads(linestring)


coordinatess = np.asarray(pd.DataFrame.from_dict(linestring['geometry']['coordinates']))
def create_basic_map():
    basic_map = folium.Map(location=list(coordinatess[0]), tiles='openstreetmap', zoom_start=5)
    folium.Marker(list(coordinatess[0])).add_to(basic_map)
    return folium_static(basic_map, width=500, height=300)



if st.button('Map'):
    # session_state.key = True
    create_basic_map()
    st.write("Map")