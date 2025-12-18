import streamlit as st
from WhooPy.client import Client, BatteryState

def show_profile(user):
    """自分のプロフィールをコンパクトに表示"""
    st.subheader("自分のプロフィール")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(user.get("profile_image"), width=70)
    with col2:
        st.markdown(f"**表示名:** {user.get('display_name')}")
        st.markdown(f"**ユーザー名:** {user.get('username')}")
        st.markdown(f"**オンライン:** {'✅' if user.get('online') else '❌'}")
        st.markdown(f"**フレンド数:** {user.get('friend_count')}")

def show_friends(friends: list):
    """友達情報をコンパクトに表示"""
    if not friends:
        st.info("友達はいません")
        return

    st.subheader("友達リスト")
    for friend in friends:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(friend.get("profile_image"), width=50)
        with col2:
            st.markdown(f"**表示名:** {friend.get('display_name')}")
            st.markdown(f"**ユーザー名:** {friend.get('username')}")
            st.markdown(f"**オンライン:** {'✅' if friend.get('online') else '❌'}")

def run(data):
    """
    data = {
        "email": str,
        "password": str,
        "use_location": bool,
        "lat": float | None,
        "lon": float | None,
    }
    """

    # ログイン
    client = Client(email=data["email"], password=data["password"])
    
    # 自分のプロフィール
    try:
        me = client.info()
        show_profile(me)
    except Exception as e:
        st.error(f"プロフィール取得失敗: {e}")
        return

    # 位置情報更新
    if data.get("use_location") and data.get("lat") is not None and data.get("lon") is not None:
        try:
            client.update_location(
                location={"latitude": data["lat"], "longitude": data["lon"]},
                state=BatteryState.CHARGING
            )
        except Exception as e:
            st.warning(f"位置情報更新に失敗: {e}")

    # 友達リスト取得
    try:
        friends_data = client.get_friends()
        friends_list = [v["user"] for k, v in friends_data.items()]
        show_friends(friends_list)
    except Exception as e:
        st.warning(f"友達情報の取得に失敗しました: {e}")


