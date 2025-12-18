import streamlit as st
from WhooPy.client import Client, BatteryState

def run(data):
    try:
        # ログイン
        client = Client(email=data["email"], password=data["password"])
        me = client.info()
        user = me["user"]

        st.success("ログイン成功！")

        # コンパクト表示
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(user["profile_image"], width=80)
        with col2:
            st.markdown(f"**表示名:** {user['display_name']}")
            st.markdown(f"**ユーザー名:** {user['username']}")
            st.markdown(f"**ID:** {user['id']}")
            st.markdown(f"**生年月日:** {user['birthday']}")
            st.markdown(f"**オンライン:** {'✅' if user['online'] else '❌'}")
            st.markdown(f"**プライベート:** {'ON' if user['private_mode'] else 'OFF'}")
            st.markdown(f"**友達:** {user['friend_count']}")

        # 位置情報更新（任意）
        if data.get("use_location") and data.get("lat") is not None and data.get("lon") is not None:
            client.update_location(
                location={"latitude": data["lat"], "longitude": data["lon"]},
                state=BatteryState.CHARGING,
            )
            st.info(f"位置情報更新: 緯度 {data['lat']}, 経度 {data['lon']}")
        elif data.get("use_location"):
            st.warning("位置情報ONだが座標が未選択")

        return {"ok": True}

    except Exception as e:
        st.error("ログイン失敗")
        st.write(str(e))
        return {"ok": False}


