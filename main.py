import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

st.set_page_config(page_title="Geoviz", layout="wide")

st.title("Geoviz")

uploaded_file = st.sidebar.file_uploader("Choisir un fichier GeoJSON", type=['geojson', 'json'])

if uploaded_file is not None:
    gdf = gpd.read_file(uploaded_file)

    if st.checkbox("Afficher les données du tableau"):
        st.write(gdf.head())

    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=10, control_scale=True)

    folium.GeoJson(
        gdf,
        name="Mes Données",
        tooltip=folium.GeoJsonTooltip(fields=[gdf.columns[0]], aliases=["Nom :"]),
        popup=folium.GeoJsonPopup(fields=list(gdf.columns[:-1]))
    ).add_to(m)

    st_folium(m, width=1000, height=600)
else:
    st.info("En attente d'un fichier GeoJSON...")