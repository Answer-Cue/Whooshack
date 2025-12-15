"""Whoo API にアクセスするためのクライアントモジュール。

このモジュールでは ``Client`` クラスを中心に、アカウントの作成や更新、
位置情報の送信といった Whoo API との通信機能を提供します。
``requests`` を利用しており、認証トークンの保持や自動リトライの仕組みも
備えています。
"""

import logging
from uuid import uuid4
from enum import IntEnum
from typing import Callable, Dict, Optional
from functools import wraps
from urllib.parse import urljoin

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import requests
from pydantic import BaseModel, field_validator, ValidationError

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class BatteryState(IntEnum):
    """バッテリー状態を表すEnum"""

    UNKNOWN = 0
    CHARGING = 1
    FULL = 2
    DISCHARGING = 3


class HttpStatus(IntEnum):
    """HTTPステータスコードを表すEnum"""

    UNAUTHORIZED = 401


# その他の定数
# km/h -> m/s 変換に掛ける比率
MPS_PER_KMH = 1 / 3.6
DEFAULT_BATTERY_LEVEL = 100
DEFAULT_BATTERY_LEVEL_RATIO = 1.0
DEFAULT_BATTERY_STATE = BatteryState.UNKNOWN
DEFAULT_TIMEOUT = 10


def _create_session() -> requests.Session:
    """自動リトライ設定済みの ``requests.Session`` を返す。"""
    sess = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=(500, 502, 503, 504))
    sess.mount("https://", HTTPAdapter(max_retries=retry))
    return sess


def _json_or_empty(res: requests.Response) -> Dict:
    """JSON レスポンスを辞書で返す。空の場合は空辞書。"""

    try:
        return res.json()
    except ValueError:
        return {}


class WhooError(Exception):
    """Whoo ライブラリ共通の基底例外"""


class AuthError(WhooError):
    """認証に関するエラー"""


class APIError(WhooError):
    """API 通信に関するエラー"""


def require_token(func: Callable) -> Callable:
    """トークンが存在するかを確認するデコレータ"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """トークンが無い場合 ``AuthError`` を送出する。"""
        if not getattr(self, "_token", None):
            raise AuthError("Token is required.")
        return func(self, *args, **kwargs)

    return wrapper


class LocationModel(BaseModel):
    """位置情報を検証するための Pydantic モデル。"""

    latitude: float
    longitude: float
    speed: float = 0.0
    horizontal_accuracy: Optional[float] = None

    @field_validator("latitude")
    @classmethod
    def check_latitude(cls, v: float) -> float:
        """緯度のバリデーションを行う。"""
        if not (-90 <= v <= 90):
            raise ValueError("latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def check_longitude(cls, v: float) -> float:
        """経度のバリデーションを行う。"""
        if not (-180 <= v <= 180):
            raise ValueError("longitude must be between -180 and 180")
        return v

    @field_validator("horizontal_accuracy")
    @classmethod
    def check_accuracy(cls, v: Optional[float]) -> Optional[float]:
        """水平精度のバリデーションを行う。"""
        if v is not None and v < 0:
            raise ValueError("horizontal_accuracy must be >= 0")
        return v

    @field_validator("speed")
    @classmethod
    def check_speed(cls, v: float) -> float:
        """速度値のバリデーションを行う。"""
        if v < 0:
            raise ValueError("speed must be >= 0")
        return v


class Client:
    """Whoo API と通信するためのクライアントクラス。"""

    def __init__(
        self,
        access_token: Optional[str] = None,
        *,
        email: Optional[str] = None,
        password: Optional[str] = None,
        session: Optional[requests.Session] = None,
        on_unauthorized: Optional[Callable[[], Optional[str]]] = None,
    ) -> None:
        """クライアントを初期化する。

        Args:
            access_token: 既存のアクセストークン。
            email: メールアドレス。 ``access_token`` がない場合に使用。
            password: パスワード。 ``access_token`` がない場合に使用。
            session: カスタム ``requests.Session``。
            on_unauthorized: 認証エラー時に呼び出されるコールバック。
        """
        self.base = "https://www.wh00.ooo/"
        self.session = session or _create_session()
        self._token: Optional[str] = None
        self._on_unauthorized = on_unauthorized
        self._base_headers = {
            "Accept": "application/json",
            "User-Agent": "app.whoo/0.13.4 iOS/17.0",
            "Accept-Language": "ja-JP",
        }

        if access_token is None and email and password:
            data = self.email_login(email, password)
            access_token = data["access_token"]

        if access_token:
            self._token = access_token
            logger.info("Login successful!")

    @property
    def token(self) -> Optional[str]:
        """現在保持しているアクセストークンを返す。"""
        return self._token

    @property
    def headers(self) -> Dict[str, str]:
        """リクエスト送信時に使用するヘッダーを返す。"""
        headers = self._base_headers.copy()
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def close(self) -> None:
        """セッションを閉じる"""
        self.session.close()

    def __enter__(self) -> "Client":
        """with 文で使用するためのエントリポイント。"""
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """with 文の終了時にセッションを閉じる。"""
        self.close()

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        """API へリクエストを送りレスポンスを返す内部メソッド。"""
        url = urljoin(self.base, path.lstrip("/"))
        for attempt in range(2):
            try:
                res = self.session.request(
                    method, url, headers=self.headers, timeout=DEFAULT_TIMEOUT, **kwargs
                )
            except requests.RequestException as exc:
                raise APIError(str(exc)) from exc

            if res.status_code == HttpStatus.UNAUTHORIZED and self._on_unauthorized and attempt == 0:
                new_token = self._on_unauthorized()
                if new_token:
                    self._token = new_token
                    continue

            break

        if not res.ok:
            try:
                message = res.json().get("message", res.text)
            except ValueError:
                message = res.text
            raise APIError(f"{res.status_code}: {message[:200]}")
        return res

    def _paginate(self, path: str, key: str):
        """ページネーションされたエンドポイントを走査して要素を取得する。"""
        next_page = 1
        items = []
        while next_page:
            res = self._request("GET", f"{path}?page={next_page}").json()
            items.extend(res[key])
            next_page = res.get("next_page")
        return items

    ##############  アカウントの設定関連   ##############
    def email_login(self, email: str, password: str) -> Dict:
        """メールアドレスとパスワードでログインする。"""
        data = {"email": email, "password": password}
        res = self._request("POST", "api/email/login", data=data)
        self._token = res.json()["access_token"]
        return res.json()

    def create_account(
        self,
        email: str,
        password: str,
        name: str,
        profile_image: str,
        username: str,
        location: Optional[Dict] = None,
    ) -> Dict:
        """新しいアカウントを作成する。"""
        data = {
            "user[email]": email,
            "user[password]": password,
            "user[display_name]": name,
            "user[profile_image]": profile_image,
            "user[username]": username,
        }
        res = self._request("POST", "api/email/users", data=data)

        if location is None:
            return res.json()

        headers = {
            "Accept": "application/json",
            "User-Agent": "app.whoo/0.13.4 iOS/17.0",
            "Authorization": f"Bearer {res.json()['access_token']}",
            "Accept-Language": "ja-JP",
        }
        data = {
            "user_location[latitude]": str(location["latitude"]),
            "user_location[longitude]": str(location["longitude"]),
            "user_location[speed]": 0,
            "user_battery[level]": DEFAULT_BATTERY_LEVEL_RATIO,
            "user_battery[state]": BatteryState.CHARGING,
        }
        self._request("PATCH", "api/user/location", headers=headers, data=data)
        return res.json()

    @require_token
    def update_account(
        self,
        name: Optional[str] = None,
        profile_image: Optional[str] = None,
        username: Optional[str] = None,
    ) -> Dict:
        """アカウント情報を更新する。"""

        data = {
            "user[display_name]": name,
            "user[profile_image]": profile_image,
            "user[username]": username,
        }
        res = self._request("PATCH", "api/user", data=data)
        return _json_or_empty(res)

    @require_token
    def delete_account(self, alert: bool = False) -> Dict:
        """アカウントを削除する。"""

        if alert:
            logger.warning("Account deletion requested.")

        res = self._request("DELETE", "api/user")
        return _json_or_empty(res)

    ##############  バックグラウンド処理   ##############
    @require_token
    def info(self) -> Dict:
        """ログイン中のユーザー情報を取得する。"""
        res = self._request("GET", "api/my")
        return _json_or_empty(res)

    @require_token
    def get_requested(self) -> Dict:
        """自分宛ての友達申請リストを取得する。"""
        res = self._request("GET", "api/friends/requested")
        return _json_or_empty(res)

    @require_token
    def get_friends(self) -> Dict:
        """友達リストを取得する。"""
        res = self._request("GET", "api/friends")
        return _json_or_empty(res)

    @require_token
    def get_user(self, user_id, friends: bool = False) -> Dict:
        """指定ユーザーの情報を取得する。"""

        res = self._request("GET", f"api/v2/users/{user_id}")
        js = _json_or_empty(res)

        if not friends:
            del js["friends"], js["next_page"]
            return js

        if js.get("next_page"):
            js["friends"] = self._paginate(f"api/v2/users/{user_id}/friends", "friends")
            js["next_page"] = None
        return js

    @require_token
    def reacquire_location(self, user_id) -> Dict:
        """指定ユーザーに位置情報の再送信を要求する。"""
        res = self._request("GET", f"api/users/{user_id}/location_request")
        return _json_or_empty(res)

    @require_token
    def update_location(
        self,
        location: Dict,
        level: int = DEFAULT_BATTERY_LEVEL,
        state: BatteryState = DEFAULT_BATTERY_STATE,
        speed: float = 0.0,
        stayed_at: Optional[str] = None,
        horizontal_accuracy: Optional[float] = None,
    ) -> Dict:
        """ユーザーの位置情報を更新する。

        Args:
            location (Dict): 位置情報辞書 (latitude, longitudeを含む)
            level (int): バッテリーレベル (0-100)。デフォルトは100。
            state (int): バッテリー状態 (0:不明, 1:充電中, 2:充電完了, 3:放電中)。デフォルトは0。
            speed (float): 速度 (km/h)。デフォルトは0.0。
            stayed_at (Optional[str]): 滞在時間。省略可能。
            horizontal_accuracy (Optional[float]): 水平精度。省略可能。

        Returns:
            Dict: 更新結果

        Raises:
            Exception: リクエストエラーが発生した場合、またはトークンがない場合
        """
        try:
            loc = LocationModel(
                latitude=location["latitude"],
                longitude=location["longitude"],
                speed=speed,
                horizontal_accuracy=horizontal_accuracy,
            )
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

        data = {
            "user_location[latitude]": str(loc.latitude),
            "user_location[longitude]": str(loc.longitude),
            "user_location[speed]": str(loc.speed * MPS_PER_KMH),
            "user_battery[level]": str(level / 100),
            "user_battery[state]": str(state.value),
        }
        if loc.horizontal_accuracy is not None:
            data["user_location[horizontal_accuracy]"] = str(loc.horizontal_accuracy)
        if stayed_at:
            data["user_location[stayed_at]"] = str(stayed_at)

        res = self._request("PATCH", "api/user/location", data=data)
        return _json_or_empty(res)

    @require_token
    def get_locations(self, user_id: Optional[str] = None) -> Dict:
        """友達の位置情報を取得する。"""

        res = self._request("GET", "api/locations")

        js = {}
        for loc in res.json()["locations"]:
            name = loc["user"]["username"]
            del loc["user"]["username"]

            if user_id and user_id != loc["user"]["id"]:
                continue

            loc["map"] = (
                f"https://maps.google.com/maps?q={loc['latitude']},{loc['longitude']}&t=k&z=24"
            )
            loc["pano"] = (
                f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={loc['latitude']},{loc['longitude']}"
            )
            js[name] = loc

        return js

    @require_token
    def online(self) -> Dict:
        """ステータスをオンラインにする。"""
        res = self._request("PATCH", "api/user/online")
        return _json_or_empty(res)

    @require_token
    def offline(self) -> Dict:
        """ステータスをオフラインにする。"""
        res = self._request("PATCH", "api/user/offline")
        return _json_or_empty(res)

    ##############  基本操作   ##############
    @require_token
    def send_stamp(self, user_id, stamp_id, quantity) -> Dict:
        """スタンプを送信する。"""

        data = {
            "message[user_id]": user_id,
            "message[stamp_id]": stamp_id,
            "message[stamp_count]": quantity,
        }
        res = self._request("POST", "api/stamp_messages", data=data)
        return _json_or_empty(res)

    @require_token
    def send_message(self, room_id, content) -> Dict:
        """メッセージを送信する。"""

        data = {
            "message[uid]": str(uuid4()),
            "message[body]": content,
        }
        res = self._request("POST", f"api/rooms/{room_id}/messages", data=data)
        return _json_or_empty(res)

    @require_token
    def request_friend(self, user_id) -> Dict:
        """友達申請を送信する。"""

        data = {"user_id": user_id}
        res = self._request("POST", "api/friends", data=data)
        return _json_or_empty(res)

    @require_token
    def delete_requested(self, user_id) -> Dict:
        """送信済みの友達申請を取り消す。"""

        res = self._request("DELETE", f"api/friendships/{user_id}/retire")
        return _json_or_empty(res)
