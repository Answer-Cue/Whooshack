import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, checkbox = input_area()

# --------------------
# 状態の初期化
# --------------------
if "clicked_latlon" not in st.session_state:
    st.session_state.clicked_latlon = None

# --------------------
# 地図
# --------------------
st.subheader("地図")

if st.session_state.clicked_latlon:
    center = st.session_state.clicked_latlon
    zoom = 13
else:
    center = [35.68, 139.76]
    zoom = 10

m = folium.Map(location=center, zoom_start=zoom)

if st.session_state.clicked_latlon:
    folium.Marker(
        location=st.session_state.clicked_latlon,
        popup="選択した位置",
        icon=folium.Icon(color="red"),
    ).add_to(m)

result = st_folium(m, width=700, height=500)

# クリックされたら「保存だけ」
if result and result.get("last_clicked"):
    lat = result["last_clicked"]["lat"]
    lon = result["last_clicked"]["lng"]
    st.session_state.clicked_latlon = [lat, lon]

# --------------------
# 送信ボタン
# --------------------
if st.button("送信"):
    st.write("メールアドレス:", email)
    st.write("パスワード:", "●" * len(password))

    if st.session_state.clicked_latlon:
        st.success("位置情報")
        st.write("緯度:", st.session_state.clicked_latlon[0])
        st.write("経度:", st.session_state.clicked_latlon[1])
    else:
        st.warning("地図をクリックして位置を選択してください")
