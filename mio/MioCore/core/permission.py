from nonebot import get_plugin_config
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from mio.MioCore.config import BaseConfig


async def group_white_list(event: GroupMessageEvent):
    white_list = get_plugin_config(WhiteListGroupConfig).white_list
    if not white_list:
        return True
    group_id = event.group_id
    return group_id in white_list


class WhiteListGroupConfig(BaseConfig):
    white_list: list[str] = []
