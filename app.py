import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium
import trader

st.set_page_config(page_title="Whooshack", layout="centered")
header()

email, password, extras, show_extra = input_area()

# --------------------
# 初期化
# --------------------
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = [None, None]

if "lat_input" not in st.session_state:
    st.session_state.lat_input = extras.get("lat", "")
if "lon_input" not in st.session_state:
    st.session_state.lon_input = extras.get("lon", "")

# --------------------
# 地図
# --------------------
st.subheader("地図")
center = st.session_state.clicked_latlon if all(st.session_state.clicked_latlon) else [35.68, 139.76]
zoom = 13 if all(st.session_state.clicked_latlon) else 10

m = folium.Map(location=center, zoom_start=zoom)

if all(st.session_state.clicked_latlon):
    folium.Marker(
        location=st.session_state.clicked_latlon,
        icon=folium.Icon(color="red"),
    ).add_to(m)

result = st_folium(m, width=700, height=500)

# クリック時にウィジェットの初期値を更新
if result and result.get("last_clicked"):
    lat_click = str(result["last_clicked"]["lat"])
    lon_click = str(result["last_clicked"]["lng"])
    st.session_state.lat_input = lat_click
    st.session_state.lon_input = lon_click
    st.session_state.clicked_latlon = [float(lat_click), float(lon_click)]

# --------------------
# 緯度経度テキストボックス
# --------------------
if show_extra:
    st.text_input("緯度", key="lat_input")
    st.text_input("経度", key="lon_input")

# --------------------
# 送信
# --------------------
if st.button("送信"):
    form_data = {
        "email": email,
        "password": password,
        "use_location": show_extra,
        "lat": float(st.session_state.lat_input) if st.session_state.lat_input else None,
        "lon": float(st.session_state.lon_input) if st.session_state.lon_input else None,
        "stayed_at": extras.get("stayed_at"),
        "battery_level": extras.get("battery_level"),
        "speed": extras.get("speed"),
    }

    trader.run(form_data)
    st.success("送信しました")


    st.success("送信しました")


