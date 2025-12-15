import modules.client


import WhooPy as whoo

client=whoo.Client()
# ログイン
data=client.email_login(
    email="example@example.com", # メールアドレス
    password="password" # パスワード
)
