import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium
import trader

st.set_page_config(page_title="Whooshack", layout="centered")
header()

email, password, extras, checkbox = input_area()

# --------------------
# セッション状態初期化
# --------------------
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = None
if "lat" not in st.session_state:
    st.session_state.lat = ""
if "lon" not in st.session_state:
    st.session_state.lon = ""

# --------------------
# 地図
# --------------------
st.subheader("地図")
center = st.session_state.clicked_latlon or [35.68, 139.76]
zoom = 13 if st.session_state.clicked_latlon else 10
m = folium.Map(location=center, zoom_start=zoom)

if st.session_state.clicked_latlon:
    folium.Marker(
        location=st.session_state.clicked_latlon,
        icon=folium.Icon(color="red")
    ).add_to(m)

result = st_folium(m, width=700, height=500)

# --------------------
# 地図クリック → 緯度経度テキストボックスに反映
# --------------------
if result and result.get("last_clicked"):
    clicked = result["last_clicked"]
    st.session_state.lat = str(clicked["lat"])
    st.session_state.lon = str(clicked["lng"])
    st.session_state.clicked_latlon = [clicked["lat"], clicked["lng"]]

# --------------------
# 緯度経度テキストボックス
# --------------------
lat_input = st.text_input("緯度 (自由に変更可能)", value=st.session_state.lat, key="lat")
lon_input = st.text_input("経度 (自由に変更可能)", value=st.session_state.lon, key="lon")

# --------------------
# 送信
# --------------------
if st.button("偽装実行"):
    form_data = {
        "email": email,
        "password": password,
        "use_location": checkbox,
        "latitude": float(lat_input) if lat_input else None,
        "longitude": float(lon_input) if lon_input else None,
        "stayed_at": extras.get("stayed_at"),
        "battery_level": extras.get("battery_level"),
        "speed": extras.get("speed")
    }

    trader.run(form_data)
    st.success("送信しました")

