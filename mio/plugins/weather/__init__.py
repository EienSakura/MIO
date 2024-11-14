from nonebot import require
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata, get_plugin_config
from nonebot.rule import to_me

from mio.MioCore import logger
from mio.MioCore.core.hook import on_startup, on_bot_connect
from mio.MioCore.core.permission import group_white_list
from mio.plugins.weather.config import Config, WeatherConfig

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_alconna import on_alconna, UniMessage, Alconna, Args, Target, Text
from mio.plugins.weather.render_pic import render
from mio.plugins.weather.weather import Weather, FutureNotRain

__plugin_meta__ = PluginMetadata(
    name="天气",
    description="天气预报",
    usage=(
        "获取默认城市天气：\n"
        "@我 + 天气\n"
        "查询天气：\n"
        "@我 + xx天气 或 @我 + 天气xx\n"
    ),
    extra={
        "example": "@bot 天气\n" +
        "@bot 杭州天气\n" +
        "@bot 天气杭州\n"
    },
)

weather_config: WeatherConfig = get_plugin_config(Config).weather

weather = on_alconna(
    Alconna("天气", Args["city;?", str, ""]),
    rule=to_me(),
    permission=group_white_list,
    block=True,
    priority=30
)
weather.shortcut(r"^(?P<city>.+)天气$", {"args": ["{city}"], "fuzzy": False})
weather.shortcut(r"^天气(?P<city>.+)$", {"args": ["{city}"], "fuzzy": False})


@weather.handle()
async def _(matcher: Matcher, city: str):
    if weather_config.api_key is None:
        await matcher.finish("天气配置文件未填写完善，无法使用该功能")
    if not city:
        city = weather_config.default_city
    if not city:
        await matcher.finish("请在配置文件中输入默认城市或者在使用该功能时提供城市")
    try:
        weather_data = await Weather(city=city, api_key=weather_config.api_key).load_data()
    except:
        await matcher.finish("天气信息获取失败")
    await UniMessage.image(raw=await render(weather_data)).send()


@on_bot_connect
async def _():
    """天气提醒"""
    alert_time = weather_config.alert_time
    if alert_time is None:
        logger.info(f"天气提醒模块未启用")
        return
    try:
        hour, minute, second = alert_time.split(":")
        scheduler.add_job(weather_alert, "cron",
                          hour=hour, minute=minute, second=second, id="weather_alert")
        logger.info(f"天气提醒模块已加载，将于每日{hour}:{minute}:{second}启动")
    except Exception as e:
        logger.error("Weather的天气提醒模块出现错误,请查看配置文件是否完善")
        logger.error(e)


async def weather_alert():
    """下雨、雪 提醒"""
    time, weather_text = "", ""
    try:
        time, weather_text = await Weather(api_key=weather_config.api_key).check_future24_rain()
    except FutureNotRain:
        return
    msg = UniMessage(Text(f"澪酱提醒您将于{time}时会下{weather_text}，请注意带伞哦"))
    for user in weather_config.alert_users_id:
        target = Target(id=user, private=True)
        await msg.send(target=target)
    for group in weather_config.alert_groups_id:
        target = Target(id=group)
        await msg.send(target=target)
