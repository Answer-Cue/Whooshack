import streamlit as st

def header():
    st.title("whooLog")
    st.caption("Streamlit UI サンプル")

def input_area():
    email = st.text_input("メールアドレス")
    password = st.text_input("パスワード", type="password")

    show_extra = st.checkbox("追加情報を入力する")

    # 初期化
    if "lat" not in st.session_state:
        st.session_state["lat"] = ""
    if "lon" not in st.session_state:
        st.session_state["lon"] = ""
    if "stayed_at" not in st.session_state:
        st.session_state["stayed_at"] = ""
    if "battery_level" not in st.session_state:
        st.session_state["battery_level"] = ""
    if "speed" not in st.session_state:
        st.session_state["speed"] = ""

    if show_extra:
        st.subheader("変更入力")
        lat = st.text_input("緯度", key="lat")
        lon = st.text_input("経度", key="lon")
        stayed_at = st.text_input("滞在時間", key="stayed_at")
        battery_level = st.text_input("バッテリー残量", key="battery_level")
        speed = st.text_input("移動スピード", key="speed")
    else:
        lat = st.session_state["lat"]
        lon = st.session_state["lon"]
        stayed_at = st.session_state["stayed_at"]
        battery_level = st.session_state["battery_level"]
        speed = st.session_state["speed"]

    extras = {
        "lat": lat,
        "lon": lon,
        "stayed_at": stayed_at,
        "battery_level": battery_level,
        "speed": speed,
    }

    return email, password, extras, show_extra
