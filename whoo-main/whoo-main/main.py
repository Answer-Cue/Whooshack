from dotenv import load_dotenv
import os

from src.WhooPy import Client


def main() -> None:
    """ログインユーザーの情報を表示する簡単なスクリプト"""

    load_dotenv()
    token = os.getenv("TOKEN")
    client = Client(access_token=token)
    data = client.info()
    print(data)


if __name__ == "__main__":
    main()

