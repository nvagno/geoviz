import streamlit as st

def show_side_bar():
    sidebar = st.sidebar

    sidebar.image("logo.png")

    uploaded_file = sidebar.file_uploader("", type=["geojson", "json"])

    return sidebar, uploaded_file