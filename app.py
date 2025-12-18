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

# --- 状態保存 ---
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = None

# 表示中心
if st.session_state.clicked_latlon:
    center = st.session_state.clicked_latlon
    zoom = 13
else:
    center = [35.68, 139.76]
    zoom = 10

# 地図作成
m = folium.Map(location=center, zoom_start=zoom)

# ピン表示
if st.session_state.clicked_latlon:
    folium.Marker(
        location=st.session_state.clicked_latlon,
        popup="選択した位置",
        icon=folium.Icon(color="red"),
    ).add_to(m)

# 表示 & クリック取得
result = st_folium(m, width=700, height=500)

# クリック処理
if result and result.get("last_clicked"):
    lat = result["last_clicked"]["lat"]
    lon = result["last_clicked"]["lng"]
    st.session_state.clicked_latlon = [lat, lon]

    st.success("位置を更新しました")
    st.write("緯度:", lat)
    st.write("経度:", lon)
