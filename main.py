import folium
import geopandas as gpd
import streamlit as st

from map_utils import show_map

st.set_page_config(page_title="Geoviz", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    footer {visibility: hidden;}
    </style>
    
    """, unsafe_allow_html=True)

sidebar = st.sidebar

uploaded_file = sidebar.file_uploader("", type=['geojson', 'json'], width=500)

m = folium.Map(zoom_start=20, control_scale=True, tiles='OpenStreetMap')

if uploaded_file is not None:
    gdf = gpd.read_file(uploaded_file)
    show_polygons = sidebar.checkbox("Show polygons", value=False)

    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    if show_polygons:
        sidebar.write(gdf.head(100))

    folium.GeoJson(gdf, name="JSON Features").add_to(m)

    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    show_map(m)
else:
    show_map(m)
