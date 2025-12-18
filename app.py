import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium
import trader

st.set_page_config(page_title="Whooshack", layout="centered")

header()

# --------------------
# 入力欄
# --------------------
email, password, extras, checkbox = input_area()

# --------------------
# 状態初期化
# --------------------
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = [35.68, 139.76]  # 東京を初期値
if "lat_map" not in st.session_state:
    st.session_state.lat_map = ""
if "lon_map" not in st.session_state:
    st.session_state.lon_map = ""

# --------------------
# 地図表示
# --------------------
st.subheader("地図")
center = st.session_state.clicked_latlon
zoom = 13 if st.session_state.clicked_latlon else 10

m = folium.Map(location=center, zoom_start=zoom)

# クリック位置マーカー
if st.session_state.clicked_latlon:
    folium.Marker(
        location=st.session_state.clicked_latlon,
        icon=folium.Icon(color="red"),
    ).add_to(m)

# foliumレンダリング
result = st_folium(m, width=700, height=500)

# --------------------
# 地図クリックで session_state 更新
# --------------------
if result and result.get("last_clicked"):
    lat_click = result["last_clicked"]["lat"]
    lon_click = result["last_clicked"]["lng"]
    st.session_state.lat_map = str(lat_click)
    st.session_state.lon_map = str(lon_click)
    st.session_state.clicked_latlon = [lat_click, lon_click]

# --------------------
# 地図下の緯度・経度入力欄
# --------------------
st.subheader("緯度・経度を直接入力")
lat_input = st.text_input("緯度", key="lat_map", value=st.session_state.lat_map)
lon_input = st.text_input("経度", key="lon_map", value=st.session_state.lon_map)

# --------------------
# 送信
# --------------------
if st.button("送信"):
    # 位置情報が必要なら入力チェック
    if checkbox and (not lat_input or not lon_input):
        st.warning("位置情報を有効にしている場合は、緯度と経度を入力してください")
        st.stop()

    # trader に渡すデータ作成
    form_data = {
        "email": email,
        "password": password,
        "use_location": checkbox,
        "lat": float(lat_input) if lat_input else None,
        "lon": float(lon_input) if lon_input else None,
        "stayed_at": extras[2] if len(extras) > 2 else None,
        "battery_level": extras[3] if len(extras) > 3 else None,
        "speed": extras[4] if len(extras) > 4 else None,
    }

    trader.run(form_data)
    st.success("送信しました")


