import streamlit as st
from ui.components import header, input_area
from logic.calc import add

st.set_page_config(layout="wide")

header()
x, y, z = input_area()
st.write(x, y, z)
