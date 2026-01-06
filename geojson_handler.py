import folium
import geopandas as gpd

from map_utils import show_map


def process_geojson(map, uploaded_file):
    gdf = gpd.read_file(uploaded_file)

    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    folium.GeoJson(
        gdf,
        name="GeoJSON",
        tooltip=folium.GeoJsonTooltip(
            fields=[c for c in gdf.columns if c != "geometry"]
        )
    ).add_to(map)

    bounds = gdf.total_bounds
    map.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    show_map(map)