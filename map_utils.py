import folium
from streamlit_folium import st_folium


def show_map(map):
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(map)
    folium.LayerControl(position='bottomright', collapsed=False).add_to(map)
    st_folium(map, width=1000, height=900, use_container_width=True)