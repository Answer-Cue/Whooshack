import streamlit as st
from ui.components import header, input_area

st.set_page_config(page_title="My App")

header()

email, password, extras = input_area()

st.write("email:", email)
st.write("password:", password)
st.write("extras:", extras)
