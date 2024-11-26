from pydantic import BaseModel


class Config(BaseModel):
    daily_news_cookie: str = ""    # 填写微信公众号的cookie
    daily_news_token: int = 0   # 填写微信公众号的token
