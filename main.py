import folium
import streamlit as st

from geojson_handler import process_geojson
from lidar_handler import process_lidar
from map_utils import show_map
from sidebar import show_side_bar

st.set_page_config(page_title="Geoviz 3D", layout="wide")

st.markdown("""
<style>
.block-container { padding: 0rem; }
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


m = folium.Map(zoom_start=20, control_scale=True, tiles="OpenStreetMap")
_, uploaded_file = show_side_bar()

if uploaded_file is not None:
    file_name = uploaded_file.name.lower()

    if file_name.endswith(('.las', '.laz')):
        process_lidar(uploaded_file)

    else:
        process_geojson(m, uploaded_file)
else:
    show_map(m)