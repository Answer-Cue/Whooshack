import streamlit as st
from ui.components import header, input_area
from map_component import map_component

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, checkbox = input_area()

if st.button("送信"):
    st.write("メールアドレス:", email)
    st.write("パスワード:", "●" * len(password))

st.subheader("地図")
location = map_component()

if location is not None:
    st.write("緯度:", location["lat"])
    st.write("経度:", location["lng"])
