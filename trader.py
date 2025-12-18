import streamlit as st
from WhooPy.client import Client, BatteryState

def run(data):
    try:
        # ログイン
        client = Client(email=data["email"], password=data["password"])
        me = client.info()
        user = me["user"]

        st.success("ログイン成功！")

        # 左に画像、右に情報
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(user["profile_image"], width=120)
        with col2:
            st.subheader(user["display_name"])
            st.write(f"ユーザー名: {user['username']}")
            st.write(f"ID: {user['id']}")
            st.write(f"生年月日: {user['birthday']}")
            st.write(f"オンライン: {'✅' if user['online'] else '❌'}")
            st.write(f"プライベートモード: {'ON' if user['private_mode'] else 'OFF'}")
            st.write(f"友達数: {user['friend_count']}")

        # 追加情報をカードでまとめる
        st.subheader("アプリアイコン")
        for icon in user.get("user_app_icons", []):
            icon_type = icon["app_icon"]["icon_type"]
            state = icon["icon_state"]
            st.write(f"{icon_type} : {state}")

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


