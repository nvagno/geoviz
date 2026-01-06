import streamlit as st
import geopandas as gpd
import pydeck as pdk

from map_utils import show_map


def process_geojson(uploaded_file):
    gdf = gpd.read_file(uploaded_file)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()

    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        gdf,
        opacity=0.8,
        stroked=True,
        filled=True,
        get_fill_color="[200, 30, 0, 160]",
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
        pickable=True,
    )

    show_map(geojson_layer, center_lat, center_lon)