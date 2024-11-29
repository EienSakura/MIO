from pathlib import Path
from typing import List

import aiohttp
import httpx
from nonebot import get_bot, get_driver, require, get_plugin_config
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from playwright.async_api import async_playwright

from .config import Config
from ...MioCore import logger
from ...MioCore.core.hook import on_startup
from ...MioCore.core.permission import group_white_list

try:
    import ujson as json
except ModuleNotFoundError:
    import json

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_alconna")

from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_alconna import on_alconna, UniMessage
from arclet.alconna import Option, Alconna, Args

# 读取配置文件
subscribe = Path(__file__).parent / "subscribe.json"
subscribe_list = json.loads(subscribe.read_text(
    "utf-8")) if subscribe.is_file() else {}


def save_subscribe():
    """保存订阅配置"""
    subscribe.write_text(json.dumps(subscribe_list), encoding="utf-8")


# 加载配置
daily_news_config: Config = get_plugin_config(Config)
wechat_oa_cookie = daily_news_config.daily_news_cookie
wechat_oa_token = daily_news_config.daily_news_token

driver = get_driver()

__plugin_meta__ = PluginMetadata(
    name="新闻",
    description="每日60秒新闻",
    usage="@我 新闻/60s/news",
    type="application",
    extra={
        "example": "@我 新闻 / @我 60s / @我 news",
        "管理员设置": "在当前群聊配置新闻推送时间：\n" +
                 "@我 新闻配置 设置 小时:分钟 \n" +
                 "查看状态： \n" +
                 "@我 新闻配置 状态" +
                 "取消订阅：\n" +
                 "@我 新闻配置 取消订阅"
    },
)

daily_news = on_alconna(
    Alconna("新闻"),
    aliases={"60s","news"},
    block=True,
    rule=to_me(),
    permission=group_white_list,
)

daily_news_config = on_alconna(
    Alconna("新闻配置",
            Option("set|设置", Args["time", str]),
            Option("state|状态"),
            Option("close|取消推送|关闭推送|取消订阅|关闭订阅")
            ),
    aliases={"60sSet", "newsSet"},
    block=True,
    rule=to_me(),
    permission=group_white_list | SUPERUSER
)


@daily_news.handle()
async def moyu(matcher: Matcher):
    await UniMessage("澪正在为您爬取新闻中...").send(reply_to=True)
    try:
        moyu_img = await get_news_image_by_url()
    except ValueError:
        moyu_img = await get_news_image(wechat_oa_cookie, wechat_oa_token)
    await matcher.finish(MessageSegment.image(moyu_img))


@daily_news_config.assign("set")
async def setting(time: str, event: GroupMessageEvent):
    """新闻设置"""
    if not time or len(time_list := time.split(":")) != 2 or not time_check(time_list):
        await UniMessage("输入时间格式为 小时:分钟，当前格式不符请重新输入") \
            .finish(at_sender=True, reply_to=True)
    daily_news_subscribe(str(event.group_id), time_list[0], time_list[1])
    await UniMessage(fr"已设置新闻订阅时间{time_list[0]}:{time_list[1]}").send(at_sender=True, reply_to=True)


@daily_news_config.assign("state")
async def state(event: GroupMessageEvent):
    """新闻状态"""
    push_state = scheduler.get_job(f"daily_news_{event.group_id}")
    daily_news_state = "当前群聊每日新闻状态：\n每日推送: " + ("已开启" if push_state else "已关闭")
    if push_state:
        group_id_info = subscribe_list[str(event.group_id)]
        daily_news_state += (
            f"\n推送时间: {group_id_info['hour']}:{group_id_info['minute']}"
        )
    await UniMessage(daily_news_state).send(at_sender=True, reply_to=True)


@daily_news_config.assign("close")
async def close(event: GroupMessageEvent):
    """取消订阅"""
    try:
        del subscribe_list[str(event.group_id)]
        save_subscribe()
        scheduler.remove_job(f"daily_news_{event.group_id}")
    except:
        await UniMessage("取消订阅，请通过状态查看当前群是否订阅新闻").finish(at_sender=True, reply_to=True)
    await UniMessage("当前群聊已取消订阅").send(at_sender=True, reply_to=True)


async def get_url(cookie: str, token: str):
    """获取公众号文章url"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Cookie": cookie,
            "User-Agent": 'Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.64 HuaweiBrowser/10.0.1.335 Mobile Safari/537.36'
        }

        ID = '每日60s简报'  # 公众号的名字
        search_url = f'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=5&query={ID}&token={token}&lang=zh_CN&f=json&ajax=1'
        # 发起搜索公众号请求
        async with session.get(search_url, headers=headers) as response:
            doc = await response.text()
        jstext = json.loads(doc)
        fakeid = jstext['list'][0]['fakeid']

        data = {
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "action": "list_ex",
            "begin": 0,
            "count": "5",
            "query": "",
            "fakeid": fakeid,
            "type": "9",
        }
        url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
        # 发起获取文章列表的请求
        async with session.get(url, headers=headers, params=data) as response:
            json_test = await response.text()
        json_test = json.loads(json_test)
        page = json_test["app_msg_list"]
        page = page[0]['link']
        return page


async def get_news_image_by_url() -> bytes:
    """根据URL获取图片"""
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as client:
        response = await client.get(
            "https://api.03c3.cn/zb"
        )
        if response.is_error:
            raise ValueError(f"60s日历获取失败，错误码：{response.status_code}")
        return response.content


@on_startup
async def subscribe_jobs():
    """根据配置文件在启动时订阅新闻"""
    for group_id, info in subscribe_list.items():
        scheduler.add_job(
            push_news,
            "cron",
            args=[group_id],
            id=f"daily_news_{group_id}",
            replace_existing=True,
            hour=info["hour"],
            minute=info["minute"],
        )
        logger.info(fr"群{group_id}将在每日{info['hour']}:{info['minute']}推送每日新闻")


async def push_news(group_id: str):
    bot = get_bot()
    try:
        moyu_img = await get_news_image_by_url()
    except ValueError:
        moyu_img = await get_news_image(wechat_oa_cookie, wechat_oa_token)
    await bot.send_group_msg(
        group_id=int(group_id), message=MessageSegment.image(moyu_img)
    )


def daily_news_subscribe(group_id: str, hour: str, minute: str) -> None:
    """新闻订阅"""
    subscribe_list[group_id] = {"hour": hour, "minute": minute}
    save_subscribe()
    scheduler.add_job(
        push_news,
        "cron",
        args=[group_id],
        id=f"daily_news_{group_id}",
        replace_existing=True,
        hour=hour,
        minute=minute,
    )
    logger.debug(f"群[{group_id}]设置60s日历推送时间为：{hour}:{minute}")


async def get_news_image(cookie, token) -> bytes:
    """获取新闻图片"""
    url = await get_url(cookie, token)
    return await capture_element_screenshot(url, "#js_content > section > section > section:nth-child(4)")


async def capture_element_screenshot(url, selector) -> bytes:
    """网页截图"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="zh-CN")
        page = await context.new_page()
        # 设置网页宽度 来适合截图
        await page.set_viewport_size({"width": 574, "height": 1165})
        # 打开指定 URL
        await page.goto(url, timeout=60000)

        # 查找元素并截图
        element = page.locator(selector)
        image: bytes = await element.screenshot(timeout=60000)

        await browser.close()
        return image


def time_check(time_list: List):
    """时间校验"""
    if not all(str(x).isdigit() for x in time_list):
        return False
    if int(time_list[0]) > 24 or int(time_list[0]) < 0:
        return False
    if int(time_list[1]) > 59 or int(time_list[1]) < 0:
        return False
    return True
