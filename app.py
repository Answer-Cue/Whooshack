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
    st.session_state.clicked_latlon = None

# --------------------
# 地図
# --------------------
st.subheader("地図")

center = [35.68, 139.76]
zoom = 10

m = folium.Map(location=center, zoom_start=zoom)

# 既にクリックした位置がある場合マーカー表示
if st.session_state.clicked_latlon:
    folium.Marker(location=st.session_state.clicked_latlon, icon=folium.Icon(color="red")).add_to(m)

result = st_folium(m, width=700, height=500)

# 地図クリック時に session_state の lat/lon を更新
if result and result.get("last_clicked"):
    st.session_state.clicked_latlon = [result["last_clicked"]["lat"], result["last_clicked"]["lng"]]
    st.session_state["lat"] = str(result["last_clicked"]["lat"])
    st.session_state["lon"] = str(result["last_clicked"]["lng"])

# --------------------
# 送信
# --------------------
if st.button("送信"):
    # チェックボックスがオンで地図も入力なしの場合
    if checkbox and not (st.session_state["lat"] and st.session_state["lon"]):
        st.warning("位置情報を有効にしている場合は、地図をクリックするか緯度・経度を入力してください")
        st.stop()

    # trader.py に渡すデータ作成
    form_data = {
        "email": email,
        "password": password,
        "use_location": checkbox,
        "lat": st.session_state["lat"] if st.session_state["lat"] else None,
        "lon": st.session_state["lon"] if st.session_state["lon"] else None,
        "stayed_at": st.session_state["stayed_at"] or None,
        "battery_level": st.session_state["battery_level"] or None,
        "speed": st.session_state["speed"] or None,
    }

    trader.run(form_data)
    st.success("送信しました")



