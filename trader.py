# trader.py
from whoo-main.src.WhooPy.client import Client, BatteryState

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

    # ① ここで必ずログインする
    client = Client(
        email=data["email"],
        password=data["password"],
    )

    # ② ログイン成功確認（任意）
    me = client.info()
    print("ログイン成功:", me.get("username"))

    # ③ 位置情報は「使うときだけ」
    if data.get("use_location"):
        if data.get("lat") is not None and data.get("lon") is not None:
            client.update_location(
                location={
                    "latitude": data["lat"],
                    "longitude": data["lon"],
                },
                state=BatteryState.CHARGING,
            )
        else:
            print("位置情報ONだが座標が未選択")

    return {
        "ok": True,
        "used_location": data.get("use_location", False),
    }
