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

center = st.session_state.clicked_latlon or [35.68, 139.76]
zoom = 13 if st.session_state.clicked_latlon else 10

m = folium.Map(location=center, zoom_start=zoom)

if st.session_state.clicked_latlon:
    folium.Marker(location=st.session_state.clicked_latlon, icon=folium.Icon(color="red")).add_to(m)

result = st_folium(m, width=700, height=500)

if result and result.get("last_clicked"):
    st.session_state.clicked_latlon = [
        result["last_clicked"]["lat"],
        result["last_clicked"]["lng"],
    ]

# --------------------
# 送信
# --------------------
if st.button("送信"):
    if checkbox and not st.session_state.clicked_latlon:
        st.warning("位置情報を有効にしている場合は、地図をクリックしてください")
        st.stop()

    # --------------------
    # trader.py に渡すデータ作成
    # --------------------
    form_data = {
        "email": email,
        "password": password,
        "use_location": checkbox,
        "latitude": st.session_state.clicked_latlon[0] if st.session_state.clicked_latlon else (extras[0] if len(extras) > 0 else None),
        "longitude": st.session_state.clicked_latlon[1] if st.session_state.clicked_latlon else (extras[1] if len(extras) > 1 else None),
        "stayed_at": extras[2] if len(extras) > 2 else None,
        "battery_level": extras[3] if len(extras) > 3 else None,
        "speed": extras[4] if len(extras) > 4 else None,
    }

    trader.run(form_data)
    st.success("送信しました")


