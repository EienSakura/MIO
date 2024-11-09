from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.rule import to_me

from mio.MioCore.core.permission import group_white_list

heart_reply = on_command("", rule=to_me(), permission=group_white_list)


@heart_reply.handle()
async def handle_heart_reply(bot: Bot, event: GroupMessageEvent):
    """
    空指令at
    :param bot:
    :param event:
    :return:
    """
    if event.is_tome and event.get_plaintext() == "":
        await heart_reply.send("这里是高性能萝卜子[澪(みおMio)]!\n如有需要，可使用[@我 帮助]查看澪的功能哦 ")
