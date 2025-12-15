# ui/components.py
import streamlit as st

def header():
    st.title("ヘッダー")

def input_area():
    email = st.text_input("メール")
    password = st.text_input("パスワード", type="password")
    return email, password
