import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium
import trader

# --------------------
# ページ設定
# --------------------
st.set_page_config(page_title="Whooshack", layout="centered")
header()

# --------------------
# 入力フォーム
# --------------------
email, password, extras, checkbox = input_area()

# --------------------
# セッションステート初期化
# --------------------
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = None

# --------------------
# 地図表示
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

# 地図クリックの結果を取得
result = st_folium(m, width=700, height=500)
if result and result.get("last_clicked"):
    lat_click = result["last_clicked"]["lat"]
    lon_click = result["last_clicked"]["lng"]
    # テキストボックスに反映する
    st.session_state.lat = str(lat_click)
    st.session_state.lon = str(lon_click)
    st.session_state.clicked_latlon = [lat_click, lon_click]

# --------------------
# 緯度経度テキストボックス
# --------------------
lat_input = st.text_input("緯度", value=st.session_state.get("lat", ""))
lon_input = st.text_input("経度", value=st.session_state.get("lon", ""))

# --------------------
# 送信ボタン
# --------------------
if st.button("送信"):
    # 位置情報ONだがテキストボックスが空なら警告
    if checkbox and (not lat_input or not lon_input):
        st.warning("位置情報を有効にする場合は、緯度・経度を入力してください")
        st.stop()

    # trader.py に渡すデータ
    form_data = {
        "email": email,
        "password": password,
        "use_location": checkbox,
        "lat": lat_input if lat_input else None,
        "lon": lon_input if lon_input else None,
        "stayed_at": extras[2] if len(extras) > 2 else None,
        "battery_level": extras[3] if len(extras) > 3 else None,
        "speed": extras[4] if len(extras) > 4 else None,
    }

    trader.run(form_data)
    st.success("送信しました")

