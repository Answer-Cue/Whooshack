import streamlit as st
from ui.components import header, input_area
import trader

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

trader.runling.test("HI")
