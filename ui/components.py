import streamlit as st

def header():
    st.title("My App")

def input_area():
    email = st.number_input("メールアドレス", value=0)
    passQ = st.number_input("パスワード", value=0)
    return emal, passQ
