import pydeck as pdk
import streamlit as st


def show_map(layer, lat=-20.8789, lon=55.4481):

    layers = []
    if layer is not None:
        layers.append(layer)

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=10,
        pitch=45,
        bearing=0
    )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        height=900,
        map_style=None
    )

    st.pydeck_chart(deck, height=900)