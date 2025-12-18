import streamlit as st

def receive_form_data(data: dict):
    """
    data に全部入ってくる想定
    """
    print("受け取ったデータ:")
    for k, v in data.items():
        print(f"{k}: {v}")
        st.success(f"{k}: {v}")

    # ここでDB保存・API送信など
    return True
