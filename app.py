import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium
import trader

st.set_page_config(page_title="Whooshack", layout="centered")
header()

# 入力フォーム取得
email, password, extras, checkbox = input_area()

# --------------------
# 状態初期化
# --------------------
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = None

# --------------------
# 地図
# --------------------
st.subheader("地図")
center = st.session_state.clicked_latlon or [35.68, 139.76]
zoom = 13 if st.session_state.clicked_latlon else 10
m = folium.Map(location=center, zoom_start=zoom)

if st.session_state.clicked_latlon:
    folium.Marker(location=st.session_state.clicked_latlon, icon=folium.Icon(color="red")).add_to(m)

result = st_folium(m, width=700, height=500)

# 地図クリックで session_state 更新
if result and result.get("last_clicked"):
    st.session_state.clicked_latlon = [result["last_clicked"]["lat"], result["last_clicked"]["lng"]]
    # テキストボックスの初期値に反映（すでに extras にある場合は書き換えない）
    if "latitude" in extras and not extras["latitude"]:
        extras["latitude"] = str(result["last_clicked"]["lat"])
    if "longitude" in extras and not extras["longitude"]:
        extras["longitude"] = str(result["last_clicked"]["lng"])

# --------------------
# 緯度・経度のテキストボックスを表示（編集可能）
# --------------------
lat_input = st.text_input("緯度 (自由に変更可能)", value=extras.get("latitude", ""), key="lat")
lon_input = st.text_input("経度 (自由に変更可能)", value=extras.get("longitude", ""), key="lon")

# --------------------
# 送信ボタン
# --------------------
if st.button("送信"):
    # 位置情報が必要かチェック
    if checkbox and not (lat_input and lon_input):
        st.warning("位置情報を有効にしている場合は、緯度経度を入力してください")
        st.stop()

    # trader.py に渡すデータ作成
    form_data = {
        "email": email,
        "password": password,
        "use_location": checkbox,
        "lat": float(lat_input) if lat_input else None,
        "lon": float(lon_input) if lon_input else None,
        "stayed_at": extras.get("stayed_at"),
        "battery_level": extras.get("battery_level"),
        "speed": extras.get("speed"),
    }

    trader.run(form_data)
    st.success("送信しました")

