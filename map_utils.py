from streamlit_folium import st_folium


def show_map(map):
    st_folium(map, width=1000, height=850, use_container_width=True)