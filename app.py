import streamlit as st
from ui.components import header, input_area
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, checkbox = input_area()

if st.button("送信"):
    st.write("メールアドレス:", email)
    st.write("パスワード:", "●" * len(password))

st.subheader("地図")

# 初期中心
center = [35.68, 139.76]

# クリック結果を保存
clicked_latlon = None

# 先に空の地図を作る
m = folium.Map(location=center, zoom_start=10)

# 表示 & クリック取得
result = st_folium(
    m,
    width=700,
    height=500,
)

# クリックされたら
if result and result.get("last_clicked"):
    lat = result["last_clicked"]["lat"]
    lon = result["last_clicked"]["lng"]
    clicked_latlon = [lat, lon]

    st.success("位置が選択されました")
    st.write("緯度:", lat)
    st.write("経度:", lon)
    
# 🔽 ピン付き地図を再描画
if clicked_latlon:
    m2 = folium.Map(location=clicked_latlon, zoom_start=13)

    folium.Marker(
        location=clicked_latlon,
        popup="選択した位置",
        icon=folium.Icon(color="red", icon="map-marker"),
    ).add_to(m2)

    st_folium(m2, width=700, height=500)
