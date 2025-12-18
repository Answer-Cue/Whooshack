import streamlit as st
from ui.components import header, input_area
from streamlit.components.v1 import html
import trader

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, checkbox = input_area()

if st.button("送信"):
    st.write("メールアドレス:", email)
    st.write("パスワード:", "●" * len(password))
    st.write(checkbox)

    if extras:
        st.write("追加情報:")
        for i, ex in enumerate(extras, 1):
            st.write(f"{i}:", ex)

# =========================
# ここから地図
# =========================

st.divider()
st.subheader("地図から位置を選択")

with open("map.html", encoding="utf-8") as f:
    map_html = f.read()

location = html(map_html, height=600)

if location:
    st.success("位置情報を取得しました")
    st.write("緯度:", location["lat"])
    st.write("経度:", location["lng"])
