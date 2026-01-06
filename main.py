import folium
import geopandas as gpd
import streamlit as st

from map_utils import show_map
from sidebar import show_side_bar

st.set_page_config(page_title="Geoviz", layout="wide")

st.markdown("""
<style>
.block-container {
    padding: 0rem;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


m = folium.Map(zoom_start=20, control_scale=True, tiles="OpenStreetMap")

_, uploaded_file = show_side_bar()

if uploaded_file is not None:
    gdf = gpd.read_file(uploaded_file)

    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    folium.GeoJson(
        gdf,
        name="GeoJSON",
        tooltip=folium.GeoJsonTooltip(
            fields=[c for c in gdf.columns if c != "geometry"]
        )
    ).add_to(m)

    bounds = gdf.total_bounds
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    show_map(m)

else:
    show_map(m)
