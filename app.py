import streamlit as st
from ui.components import header, input_area
from map_component import map_component

st.set_page_config(page_title="Whooshack", layout="centered")

header()

email, password, extras, checkbox = input_area()

if st.button("送信"):
    st.write("メールアドレス:", email)
    st.write("パスワード:", "●" * len(password))
    st.write(checkbox)

    if extras:
        st.write("追加情報:")
        for i, ex in enumerate(extras, 1):
            st.write(f"{i}:", ex)

st.divider()
st.subheader("地図から位置を選択")

location = map_component()

if location:
    st.success("位置情報を受信しました")
    st.write("緯度:", location["lat"])
    st.write("経度:", location["lng"])
