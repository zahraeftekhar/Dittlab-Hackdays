import json
import datetime

import streamlit as st
from streamlit_folium import folium_static
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from PIL import Image



# =============================================================================
# load the data
# =============================================================================
with open('./data_A4_2019-11-26.json', 'r') as f:
    data = json.load(f)

# =============================================================================
# set the title of the page
# =============================================================================
st.title('Fundamental Diagram Visualizer')
st.subheader('by MYtraffiCZeal ([@DiTTlab](https://dittlab.tudelft.nl/index.php))')
image = Image.open('logo.png')
st.image(image)

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
st.warning('Density is calculated from flow and speed. Be careful to use!')

show_map = st.checkbox('Show map')
show_data = st.checkbox('Show data')
show_fd_scatter = st.checkbox('Show FD scatter')
show_params = st.checkbox('Show identified parameters')

flow = np.array(data['data']['flow'])[loc]
speed = np.array(data['data']['speed'])[loc]
density = flow / speed

# =============================================================================
# show the map
# =============================================================================
if show_map:
    linestring_fn = 'A4-1.txt'
    with open (linestring_fn, 'r') as f:
        linestring = f.read()
    linestring = json.loads(linestring)

    coordinatess = np.asarray(pd.DataFrame.from_dict(linestring['geometry']['coordinates']))
    def create_basic_map():
        basic_map = folium.Map(location=list(coordinatess[0]), tiles='openstreetmap', zoom_start=5)
        for i in coordinatess:
            folium.Marker(list(i)).add_to(basic_map)
        return folium_static(basic_map, width=500, height=300)

    # session_state.key = True
    st.header('Map')
    create_basic_map()


# =============================================================================
# show the data
# =============================================================================
if show_data:
    st.header('Data for detector #' + str(loc) + ':')
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
    fig = plt.figure(figsize=(16,14))
    plt.rcParams["font.size"] = 16

    plt.subplot(2, 2, 1)
    plt.scatter(flow[240:-360], speed[240:-360], marker='o', s=10, c='r', label='6am-8pm')
    plt.scatter(flow[:240], speed[:240], marker='o', s=10, c='lightsalmon', label='4~6am, 8~10pm')
    plt.scatter(flow[-360:], speed[-360:], marker='o', s=10, c='lightsalmon')
    plt.legend()
    plt.xlabel('Flow (veh/hr/lane)')
    plt.ylabel('Speed (km/hr)')
    plt.title('Flow vs Speed')

    plt.subplot(2, 2, 2)
    plt.scatter(density[240:-360], flow[240:-360], marker='^', s=10, c='b', label='6am-8pm')
    plt.scatter(density[:240], flow[:240], marker='^', s=10, c='skyblue', label='4~6am, 8~10pm')
    plt.scatter(density[-360:], flow[-360:], marker='^', s=10, c='skyblue')
    plt.legend()
    plt.xlabel('Density (veh/km/lane)')
    plt.ylabel('Flow (veh/hr/lane)')
    plt.title('Density vs Flow')

    plt.subplot(2, 2, 3)
    plt.scatter(density[240:-360], speed[240:-360], marker='+', s=10, c='g', label='6am-8pm')
    plt.scatter(density[:240], speed[:240], marker='+', s=10, c='lightgreen', label='4~6am, 8~10pm')
    plt.scatter(density[-360:], speed[-360:], marker='+', s=10, c='lightgreen')
    plt.legend()
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

# =============================================================================
# Other resources
# =============================================================================
st.subheader('Other resources:')
st.write('Fundamental diagram (wiki): click [here](https://en.wikipedia.org/wiki/Fundamental_diagram_of_traffic_flow)')
st.write('Traffic wave (wiki): click [here](https://en.wikipedia.org/wiki/Traffic_wave)')
st.write('TU Delft open course material (fundamental diagram): click [here](https://ocw.tudelft.nl/wp-content/uploads/Chapter-4.-Fundamental-diagrams.pdf)')
st.write('TU Delft open course material (shockwave analysis): click [here](https://ocw.tudelft.nl/wp-content/uploads/Chapter-8.-Shock-wave-analysis.pdf)')

