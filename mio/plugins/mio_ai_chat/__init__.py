from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import Event, Bot, MessageSegment, Message, MessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown, extract_image_urls
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from ...MioCore.core.permission import group_white_list

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import UniMessage

from .baidu_ai import BaiduAi



__plugin_meta__ = PluginMetadata(
    name="问答",
    description="AI问答和AI识图",
    usage=(
        "ai问答：\n"
        "@我 + ai + 问答内容；\n"
        "ai识图：\n"
        "@我 + 识图\n"
        "发送识图后mio会发送应答，再发送所需图片即可"
    ),
    extra={
        "example": "@bot ai 1+2等于几",
    },
)

# ai对话
ai_chat = on_command("ai", rule=to_me(), permission=group_white_list)


@ai_chat.handle()
async def handle_mio_ai_chat(bot: Bot, event: Event, args: Message = CommandArg()):
    """
    ai对话
    :param args:
    :param bot:
    :param event:
    :return:
    """
    msg = args.extract_plain_text()
    msg_id: str = UniMessage.get_message_id(event, bot)

    if not msg:
        await ai_chat.finish("请告诉澪你想问的问题！")
    await ai_chat.finish(MessageSegment.reply(msg_id) + MessageSegment.at(event.get_user_id()) + " " +
                         BaiduAi().get_ai_response(msg)['result'])


# ai识图
ai_image_recognition = on_command("识图",rule=to_me(), permission=group_white_list)


@ai_image_recognition.got("ai_rec_image", "图来!", [Cooldown(5, prompt=["5s cd中.."])])
async def handle_mio_ai_image_recognition(bot: Bot, event: MessageEvent):
    """
    ai识图
    :param args:
    :param bot:
    :param event:
    :return:
    """
    user_id = event.get_user_id()
    img = extract_image_urls(event.message)
    if not img:
        await ai_image_recognition.finish("你是在糊弄澪吗？\n请发送图片！！")
    await bot.send(event, "正在识别中...")
    baidu_ai = BaiduAi()
    result = f"> {MessageSegment.at(user_id)}\n" + baidu_ai.en_to_ch(
        baidu_ai.get_ai_image_recognition(img[0]))
    await ai_image_recognition.finish(Message(result))



