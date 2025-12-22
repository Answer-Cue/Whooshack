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
                st.write(friend)
                st.markdown("---")


def run(data):
    try:
        client = Client(email=data["email"], password=data["password"])
        me = client.info()
        st.write(client)
        
        st.success("ログイン成功！")
        st.write(me)
        show_my_profile_card(me)

        friends = client.get_friends()
        show_friends_cards(friends)

        # 位置情報更新
        if data.get("use_location"):
            if data.get("latitude") is not None and data.get("longitude") is not None:
                location = {"latitude": float(data["latitude"]), "longitude": float(data["longitude"])}
                client.update_location(location=location, state=BatteryState.CHARGING)
                st.write(f"位置情報更新: {location}")
            else:
                st.warning("位置情報ONだが座標が未選択")

        # 追加情報反映
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
