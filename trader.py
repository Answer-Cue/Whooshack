import streamlit as st
from WhooPy.client import Client, BatteryState

def run(data):
    # ① ログイン
    try:
        client = Client(email=data["email"], password=data["password"])
        me = client.info()
    except Exception as e:
        st.error(f"ログイン失敗: {e}")
        return

    st.success(f"ログイン成功: {me.get('display_name')} (@{me.get('username')})")

    # ② 自分のプロフィールは以前送ってもらった構造を参照
    st.subheader("自分のプロフィール")
    st.json(me)  # まずは全体をJSONで確認

    # ③ 友達情報を取得
    try:
        friends = client.get_friends()  # 多くの場合、辞書かリストの辞書
        st.subheader("友達のデータ構造")
        st.json(friends)  # とりあえず生データ表示
    except Exception as e:
        st.warning(f"友達情報取得失敗: {e}")


