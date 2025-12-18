import streamlit as st
from map_component import map_component

st.set_page_config(layout="wide")
st.title("Leaflet × Streamlit Component")

result = map_component()

if result:
    st.success("位置が更新されました")
    st.write("緯度:", result["lat"])
    st.write("経度:", result["lon"])

