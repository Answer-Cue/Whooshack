import streamlit as st

def header():
    st.title("whooLog")
    st.caption("Streamlit UI サンプル")

def input_area():
    email = st.text_input("メールアドレス")
    password = st.text_input("パスワード", type="password")

    show_extra = st.checkbox("追加情報を入力する")

    extras = {}

    if show_extra:
        st.subheader("変更入力")
        extras["latitude"] = st.text_input("緯度", key="lat")
        extras["longitude"] = st.text_input("経度", key="lon")
        extras["stayed_at"] = st.text_input("滞在時間", key="stayed_at")
        extras["battery_level"] = st.text_input("バッテリー残量", key="battery_level")
        extras["speed"] = st.text_input("移動スピード", key="speed")

    return email, password, extras, show_extra
