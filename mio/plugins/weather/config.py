from typing import Optional, List, Set

import nonebot
from nonebot import get_plugin_config
from pydantic import BaseModel, Field, field_validator

from mio.MioCore.core.permission import WhiteListGroupConfig


class WeatherConfig(BaseModel):
    api_key: Optional[str] = Field(default=None)
    default_city: Optional[str] = Field(default=None)
    alert_time: Optional[str] = Field(default=None)
    alert_groups_id: Set[str] = Field(default=get_plugin_config(WhiteListGroupConfig).white_list)
    alert_users_id: Set[str] = Field(default=nonebot.get_driver().config.superusers)


class Config(BaseModel):
    weather: WeatherConfig


