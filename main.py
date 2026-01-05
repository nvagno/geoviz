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


if uploaded_file is not None:
    gdf = gpd.read_file(uploaded_file)
    show_polygons = sidebar.checkbox("Show polygons", value=False)

    if show_polygons:
        sidebar.write(gdf.head(100))

    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=20, control_scale=True)

    folium.GeoJson(
        gdf,
        name="Mes Données",
        tooltip=folium.GeoJsonTooltip(fields=[gdf.columns[0]], aliases=["Nom :"]),
        popup=folium.GeoJsonPopup(fields=list(gdf.columns[:-1]))
    ).add_to(m)

    show_map(m)
else:
    m = folium.Map(location=[0, 0], zoom_start=3, control_scale=True)
    show_map(m)
