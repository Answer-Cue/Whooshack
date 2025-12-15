import streamlit as st

def input_area():
    email = st.text_input("メールアドレス")
    password = st.text_input("パスワード", type="password")

    show_extra = st.checkbox("追加情報を入力する")

    extra_values = []

    if show_extra:
        st.markdown("### 追加情報")
        extra_values.append(st.text_input("追加①"))
        extra_values.append(st.text_input("追加②"))
        extra_values.append(st.text_input("追加③"))
        extra_values.append(st.text_input("追加④"))

    return email, password, extra_values
