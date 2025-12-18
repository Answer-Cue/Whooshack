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
        st.subheader("追加情報")
        extras.append(st.text_input("追加①", key="extra1"))
        extras.append(st.text_input("追加②", key="extra2"))
        extras.append(st.text_input("追加③", key="extra3"))
        extras.append(st.text_input("追加④", key="extra4"))

    return email, password, show_extras
