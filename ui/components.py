import streamlit as st

def header():
    st.title("whooLog")
    st.caption("Streamlit UI サンプル")

def input_area():
    email = st.text_input("メールアドレス")
    password = st.text_input("パスワード", type="password")

    show_extra = st.checkbox("追加情報を入力する")

    extras = []

    if show_extra:
        st.subheader("変更入力")
        extras.append(st.text_input("緯度", key="extra1"))
        extras.append(st.text_input("経度", key="extra2"))
        extras.append(st.text_input("滞在時間", key="extra3"))
        extras.append(st.text_input("バッテリー残量", key="extra4"))
        extras.append(st.text_input("移動スピード", key="extra4"))

    return email, password,extras, show_extra
