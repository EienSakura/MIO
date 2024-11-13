"""自定义钩子"""
import datetime
import os
import platform
from pathlib import Path


import nonebot
from nonebot import require

from mio.MioCore import logger, bot_config

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Target, UniMessage, SupportScope


class CustomHooks():
    def __init__(self):
        pass


bot = nonebot.get_driver()


@bot.on_bot_connect
async def start_notification():
    """启动通知"""
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot = nonebot.get_driver()
    superusers: set() = nonebot.get_driver().config.superusers
    for superuser in superusers:
        target = Target(id=superuser, private=True, scope=SupportScope.qq_client)
        await UniMessage(f"您的高性能萝卜子mio\n已于[{now_time}启动]").send(target=target)
    logger.info("已向所有超级用户发送启动通知")


@bot.on_bot_connect
async def restart_script_generator():
    """自动生成重启脚本"""
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
            logger.info("已自动生成 restart.sh 重启脚本，请检查脚本是否与本地指令符合..")
