import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium
import trader

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, checkbox = input_area()

# --------------------
# 状態初期化
# --------------------
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = [35.68, 139.76]  # 初期地図位置
if "lat" not in st.session_state:
    st.session_state.lat = ""
if "lon" not in st.session_state:
    st.session_state.lon = ""

# --------------------
# 地図
# --------------------
st.subheader("地図")
center = st.session_state.clicked_latlon
zoom = 13 if st.session_state.clicked_latlon != [35.68, 139.76] else 10

m = folium.Map(location=center, zoom_start=zoom)

# 既にクリックした場所があればマーカー
if st.session_state.clicked_latlon != [35.68, 139.76]:
    folium.Marker(
        location=st.session_state.clicked_latlon,
        icon=folium.Icon(color="red"),
    ).add_to(m)

result = st_folium(m, width=700, height=500)

# 地図クリックで更新
if result and result.get("last_clicked"):
    lat_click = result["last_clicked"]["lat"]
    lon_click = result["last_clicked"]["lng"]
    st.session_state.clicked_latlon = [lat_click, lon_click]
    st.session_state.lat = str(lat_click)
    st.session_state.lon = str(lon_click)

# --------------------
# 緯度・経度テキストボックス
# --------------------
st.subheader("緯度・経度")
lat_input = st.text_input("緯度", value=st.session_state.lat, key="lat")
lon_input = st.text_input("経度", value=st.session_state.lon, key="lon")

# --------------------
# 送信
# --------------------
if st.button("送信"):
    # 緯度経度はテキストボックスから取得
    lat_val = float(lat_input) if lat_input else None
    lon_val = float(lon_input) if lon_input else None

    # 位置情報ONだけど座標なしは警告
    if checkbox and (lat_val is None or lon_val is None):
        st.warning("位置情報を有効にしている場合は、緯度・経度を入力してください")
        st.stop()

    # trader.py に渡すデータ作成
    form_data = {
        "email": email,
        "password": password,
        "use_location": checkbox,
        "lat": lat_val,
        "lon": lon_val,
        "stayed_at": extras[0] if len(extras) > 0 else None,
        "battery_level": extras[1] if len(extras) > 1 else None,
        "speed": extras[2] if len(extras) > 2 else None,
    }

    trader.run(form_data)
    st.success("送信しました")

