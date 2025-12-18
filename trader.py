# trader.py
from WhooPy.client import Client, BatteryState
import streamlit as st

def show_profile(user: dict):
    """ユーザー情報をコンパクトに表示"""
    if not user:
        st.warning("ユーザー情報がありません")
        return

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(user.get("profile_image"), width=80)
    with col2:
        st.markdown(f"**表示名:** {user.get('display_name')}")
        st.markdown(f"**ユーザー名:** {user.get('username')}")
        st.markdown(f"**ID:** {user.get('id')}")
        st.markdown(f"**生年月日:** {user.get('birthday')}")
        st.markdown(f"**オンライン:** {'✅' if user.get('online') else '❌'}")
        st.markdown(f"**プライベート:** {'ON' if user.get('private_mode') else 'OFF'}")
        st.markdown(f"**友達:** {user.get('friend_count')}")

def run(data: dict):
    """
    メインループとして動作。
    data = {
        "email": str,
        "password": str,
        "use_location": bool,
        "lat": float | None,
        "lon": float | None,
    }
    """

    try:
        # ① ログイン
        client = Client(email=data["email"], password=data["password"])
        me = client.info()
        st.success("ログイン成功！")

        # ② プロフィール表示
        show_profile(me["user"])

        # ③ 位置情報更新（必要なら）
        if data.get("use_location"):
            lat = data.get("lat")
            lon = data.get("lon")
            if lat is not None and lon is not None:
                client.update_location(
                    location={"latitude": lat, "longitude": lon},
                    state=BatteryState.CHARGING,
                )
                st.info(f"位置情報を更新しました: ({lat}, {lon})")
            else:
                st.warning("位置情報ONだが座標が未選択")
                
        return {"ok": True, "used_location": data.get("use_location", False)}

    except Exception as e:
        st.error(f"ログインまたは処理中にエラーが発生: {e}")
        return {"ok": False}

