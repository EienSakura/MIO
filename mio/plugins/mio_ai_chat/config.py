from nonebot import get_plugin_config
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    baidu_access_key: str
    baidu_secret_key: str

    @field_validator("baidu_access_key", "baidu_secret_key")
    @classmethod
    def validate_api_keys(cls, value: str) -> str:
        # 判断值是否为空
        if not value:
            raise ValueError("Baidu API keys cannot be empty")
        return value


baidu_config = get_plugin_config(Config)
