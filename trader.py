import streamlit as st
from WhooPy.client import Client, BatteryState

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
    try:
        # ログイン
        client = Client(email=data["email"], password=data["password"])
        me = client.info()  # JSON形式で取得

        user = me["user"]
        st.success("ログイン成功！")
        st.write("ユーザー名:", user["username"])
        st.write("表示名:", user["display_name"])
        st.write("ID:", user["id"])
        st.write("生年月日:", user["birthday"])
        st.write("オンライン:", "はい" if user["online"] else "いいえ")
        st.image(user["profile_image"], width=100)

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

