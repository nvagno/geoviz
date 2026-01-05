import folium
import geopandas as gpd
import streamlit as st

from map_utils import show_map

st.set_page_config(page_title="Geoviz", layout="wide")

st.markdown("""
<style>
.block-container {
    padding: 0rem;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

sidebar = st.sidebar
uploaded_file = sidebar.file_uploader("", type=["geojson", "json"])

m = folium.Map(zoom_start=20, control_scale=True, tiles="OpenStreetMap")

if uploaded_file is not None:
    gdf = gpd.read_file(uploaded_file)

    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    with sidebar.expander("General information", expanded=True):
        st.write(f"**Features:** {len(gdf)}")
        st.write(f"**Columns:** {len(gdf.columns)}")
        st.write(f"**CRS:** {gdf.crs}")
        st.write(f"**Geometry type(s):** {gdf.geometry.geom_type.unique()}")

    with sidebar.expander("Bounding Box"):
        bounds = gdf.total_bounds
        st.write("**(minx, miny, maxx, maxy)**")
        st.code(bounds)

    with sidebar.expander("Data types"):
        st.dataframe(
            gdf.dtypes.reset_index()
            .rename(columns={"index": "Column", 0: "Type"})
        )

    with sidebar.expander("Statistics"):
        st.write(gdf.describe())

    with sidebar.expander("GeoDataFrame"):
        st.write(gdf)

    folium.GeoJson(
        gdf,
        name="GeoJSON",
        tooltip=folium.GeoJsonTooltip(
            fields=[c for c in gdf.columns if c != "geometry"]
        )
    ).add_to(m)

    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    show_map(m)

else:
    show_map(m)
