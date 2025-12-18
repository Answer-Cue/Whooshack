import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium
import trader

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, show_extra = input_area()

# --------------------
# 状態初期化
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

# クリック位置にマーカー
if st.session_state.clicked_latlon:
    folium.Marker(
        location=st.session_state.clicked_latlon,
        icon=folium.Icon(color="red"),
    ).add_to(m)

# Folium マップを描画
result = st_folium(m, width=700, height=500)

# クリック時に session_state を更新
if result and result.get("last_clicked"):
    lat_click = str(result["last_clicked"]["lat"])
    lon_click = str(result["last_clicked"]["lng"])
    st.session_state["lat"] = lat_click
    st.session_state["lon"] = lon_click
    st.session_state.clicked_latlon = [float(lat_click), float(lon_click)]

# --------------------
# 送信ボタン処理
# --------------------
if st.button("送信"):
    # 位置情報チェック
    if show_extra and (not extras["lat"] or not extras["lon"]):
        st.warning("位置情報を有効にしている場合は、地図をクリックするか緯度経度を入力してください")
        st.stop()

    # trader.py に渡すデータ作成
    form_data = {
        "email": email,
        "password": password,
        "use_location": show_extra,
        "lat": float(extras["lat"]) if extras["lat"] else None,
        "lon": float(extras["lon"]) if extras["lon"] else None,
        "stayed_at": extras.get("stayed_at"),
        "battery_level": extras.get("battery_level"),
        "speed": extras.get("speed"),
    }

    trader.run(form_data)

    st.success("送信しました")


