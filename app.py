import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, checkbox = input_area()

if st.button("送信"):
    st.write("メールアドレス:", email)
    st.write("パスワード:", "●" * len(password))

st.subheader("地図")

# 地図作成
m = folium.Map(location=[35.68, 139.76], zoom_start=10)

# 地図表示 & クリック情報取得
result = st_folium(
    m,
    width=700,
    height=500,
)

# クリックされたら座標が入る
if result and result.get("last_clicked"):
    lat = result["last_clicked"]["lat"]
    lon = result["last_clicked"]["lng"]

    st.success("位置が選択されました")
    st.write("緯度:", lat)
    st.write("経度:", lon)
