from sys import platform

import os
import platform
from pathlib import Path

import nonebot
from nonebot import get_driver
from nonebot_plugin_alconna import UniMessage, Target

from ..core.log import logger
from ..config import bot_config
from ..core.hook import on_bot_connect


@on_bot_connect
def on_bot_connected():
    print("\n\n\n\n澪\n\n\n\n")
    bot = nonebot.get_bot()
    superusers: set() = nonebot.get_driver().config.superusers
    await UniMessage.text("澪已在线!").send(target=Target(id="844451749"),bot=bot)



@on_bot_connect
async def remind():
    if str(platform.system()).lower() != "windows":
        restart = Path() / "restart.sh"
        if not restart.exists():
            with open(restart, "w", encoding="utf8") as f:
                f.write(
                    "pid=$(netstat -tunlp | grep "
                    + str(bot_config.port)
                    + " | awk '{print $7}')\n"
                    "pid=${pid%/*}\n"
                    "kill -9 $pid\n"
                    "sleep 3\n"
                    "python3 bot.py"
                )
            os.system("chmod +x ./restart.sh")
            logger.info("配置", "已自动生成 restart.sh 重启脚本，请检查脚本是否与本地指令符合..")