import streamlit as st

def header():
    st.title("My App")

def input_area():
    email = st.number_input("メールアドレス", value=1)
    passQ = st.number_input("パスワード", value=0)
    return email, passQ
