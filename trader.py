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
        me = client.info()
        username = me.get("username", "")
        display_name = me.get("display_name", "")

        st.success("ログイン成功！")
        st.write("ユーザー名:", username)
        st.write("表示名:", display_name)

        # 位置情報は「使うときだけ」
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
