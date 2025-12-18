from WhooPy.client import Client, BatteryState
import streamlit as st

def show_my_profile_card(me):
    user = me["user"]
    with st.container():
        cols = st.columns([1, 3])
        with cols[0]:
            st.image(user.get("profile_image"), width=80)
        with cols[1]:
            st.markdown(f"**{user.get('display_name')} (@{user.get('username')})**")
            st.write(f"- 誕生日: {user.get('birthday')}")
            st.write(f"- オンライン: {user.get('online')}")
            st.write(f"- フレンド数: {user.get('friend_count')}")
            st.write(f"- ログイン日数: {user.get('login_days')} / {user.get('max_login_days')}")
            st.write(f"- 国: {user.get('country_code')}")
            st.write(f"- 自己紹介: {user.get('introduction') or 'なし'}")
        st.markdown("---")

def show_friends_cards(friends_data, cols_per_row=3):
    friends = friends_data.get("friends", [])
    st.subheader(f"友達一覧 ({len(friends)})")
    for i in range(0, len(friends), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, friend in enumerate(friends[i:i+cols_per_row]):
            with cols[j]:
                st.image(friend.get("profile_image"), width=60)
                st.markdown(f"**{friend.get('display_name')} (@{friend.get('username')})**")
                st.write(f"- 誕生日: {friend.get('birthday') or '不明'}")
                st.write(f"- オンライン: {friend.get('online')}")
                st.write(f"- フレンドシップID: {friend.get('friendship', {}).get('id')}")
                st.markdown("---")

def run(data):
    """
    data = {
        "email": str,
        "password": str,
        "use_location": bool,
        "latitude": float | None,
        "longitude": float | None,
        "stayed_at": str | None,
        "battery_level": str | None,
        "speed": str | None,
    }
    """
    try:
        client = Client(email=data["email"], password=data["password"])
        me = client.info()
        st.success("ログイン成功！")
        show_my_profile_card(me)

        # 友達情報取得
        friends = client.get_friends()
        show_friends_cards(friends)

        # 位置情報はチェックボックスがオンのときだけ反映
        if data.get("use_location"):
            lat = data.get("latitude")
            lon = data.get("longitude")
            if lat is not None and lon is not None:
                client.update_location(
                    location={"latitude": float(lat), "longitude": float(lon)},
                    state=BatteryState.CHARGING,
                )
                st.write(f"位置情報を更新: 緯度 {lat}, 経度 {lon}")
            else:
                st.warning("位置情報ONだが座標が未選択")

        # 追加情報の反映（滞在時間・バッテリー・移動速度）
        if data.get("use_location"):
            stayed_at = data.get("stayed_at")
            battery_level = data.get("battery_level")
            speed = data.get("speed")

            if stayed_at or battery_level or speed:
                st.write("追加情報を反映:")
                if stayed_at: st.write(f"- 滞在時間: {stayed_at}")
                if battery_level: st.write(f"- バッテリー残量: {battery_level}")
                if speed: st.write(f"- 移動スピード: {speed}")

    except Exception as e:
        st.error(f"ログイン失敗: {e}")

