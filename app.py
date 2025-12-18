import streamlit as st
from map_component import map_component

st.title("Map Test")

location = map_component()

if location:
    st.write(location)
