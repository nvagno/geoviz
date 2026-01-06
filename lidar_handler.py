import streamlit as st
import pydeck as pdk
import laspy
import numpy as np
import pandas as pd
import geopandas as gpd

from map_utils import show_map


@st.cache_data
def _read_file(file):
    las = laspy.read(file)

    sampling_factor = 50

    points = np.vstack((las.x[::sampling_factor],
                        las.y[::sampling_factor],
                        las.z[::sampling_factor])).transpose()

    class_codes = np.array(las.classification[::sampling_factor])

    df = pd.DataFrame(points, columns=['x', 'y', 'z'])
    df['class_code'] = class_codes

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.x, df.y), crs="EPSG:2154"
    )
    gdf = gdf.to_crs("EPSG:4326")

    df_final = pd.DataFrame({
        'lon': gdf.geometry.x,
        'lat': gdf.geometry.y,
        'elevation': gdf['z'],
        'class_code': gdf['class_code']
    })

    unique_classes = df_final['class_code'].unique()

    np.random.seed(42)
    color_dict = {
        cls: [np.random.randint(0, 255) for _ in range(3)]
        for cls in unique_classes
    }

    df_final['r'] = df_final['class_code'].map(lambda x: color_dict[x][0])
    df_final['g'] = df_final['class_code'].map(lambda x: color_dict[x][1])
    df_final['b'] = df_final['class_code'].map(lambda x: color_dict[x][2])

    return df_final


def process_lidar(uploaded_file):
    df_lidar = _read_file(uploaded_file)

    target_layer = pdk.Layer(
        "PointCloudLayer",
        df_lidar,
        get_position="[lon, lat, elevation]",
        get_color="[r, g, b, 200]",
        point_size=3,
    )

    mean_lat = df_lidar['lat'].mean()
    mean_lon = df_lidar['lon'].mean()

    show_map(target_layer, mean_lat, mean_lon)