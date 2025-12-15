import streamlit as st

def header():
    st.title("My App")

def input_area():
    a = st.number_input("A", value=0)
    b = st.number_input("B", value=0)
    return a, b
