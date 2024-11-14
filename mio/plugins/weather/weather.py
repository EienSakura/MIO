import asyncio
from datetime import datetime
from typing import Optional, List

from httpx import Response, AsyncClient
from nonebot import get_plugin_config, Config

from mio.MioCore import logger
from mio.plugins.weather.model import NowWeather, DailyWeather, AirQuality, WeatherDisasterWarning, HourlyWeather, \
    HourlyType, Hourly


class APIError(Exception): ...


class ConfigError(Exception): ...


class CityNotFoundError(Exception): ...


class FutureNotRain(Exception): ...


class Weather:
    """天气"""

    def __init__(self, city: str = None, api_key: str = None):
        """
        :param city: 城市
        :param api_key: 秘钥
        """
        if not city:
            city = get_plugin_config(Config).weather['default_city']
        self.city = city
        """城市名字"""
        if not city:
            api_key = get_plugin_config(Config).weather['apikey']
        self.apikey = api_key
        """api_key"""
        self.forecast_days = 3
        """天气预报天数（3-7）"""
        self.hourly_type = HourlyType.current_24h
        """天气预报小时显示类型"""
        self.url_geoapi = "https://geoapi.qweather.com/v2/city/lookup"
        """城市搜索"""
        self.url_weather_api = "https://devapi.qweather.com/v7/weather/"
        self.url_weather_warning = "https://devapi.qweather.com/v7/warning/now"
        self.url_air = "https://devapi.qweather.com/v7/air/now"
        self.url_hourly = "https://devapi.qweather.com/v7/weather/24h"
        """逐小时预报（未来24小时）"""

    async def load_data(self):
        """获取数据"""
        self.city_id = await self._get_city_id()
        (
            self.now,
            self.daily,
            self.air,
            self.warning,
            self.hourly,
        ) = await asyncio.gather(
            self._get_now_weather(),
            self._get_daily_weather(),
            self._get_air_quality(),
            self._get_weather_disaster_warning(),
            self._get_hourly_weather()
        )
        return self

    async def check_future24_rain(self):
        self.city_id = await self._get_city_id()
        hourly: List[Hourly] = (await self._get_hourly_weather()).hourly
        for weather in hourly:
            if "雨" in weather.text or "雪" in weather.text:
                dt = datetime.fromisoformat(weather.fxTime)
                time_str: str = dt.strftime('%H:%M')
                return time_str.split(":")[0], weather.text
        raise FutureNotRain()

    async def _get_city_id(self) -> str:
        """获取根据城市名字获取城市id"""
        res = await self._get_data(
            url=self.url_geoapi,
            params={"location": self.city, "key": self.apikey, "number": 1},
        )
        res = res.json()
        if res["code"] == "404":
            raise CityNotFoundError()
        elif res["code"] != "200":
            raise APIError("错误! 错误代码: {}".format(res["code"]))
        else:
            self.city_name = res["location"][0]["name"]
            return res["location"][0]["id"]

    async def _get_now_weather(self) -> NowWeather:
        """实时天气"""
        res = await self._get_data(
            url=self.url_weather_api + "now",
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_res(res)
        return NowWeather(**res.json())

    async def _get_daily_weather(self) -> DailyWeather:
        """每日天气预报"""
        res = await self._get_data(
            url=self.url_weather_api + str(self.forecast_days) + "d",
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_res(res)
        return DailyWeather(**res.json())

    async def _get_air_quality(self) -> AirQuality:
        """实时空气质量"""
        res = await self._get_data(
            url=self.url_air,
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_res(res)
        return AirQuality(**res.json())

    async def _get_weather_disaster_warning(self) -> Optional[WeatherDisasterWarning]:
        """天气灾害预警"""
        res = await self._get_data(
            url=self.url_weather_warning,
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_res(res)
        return None if res.json().get("code") == "204" else WeatherDisasterWarning(**res.json())

    async def _get_hourly_weather(self) -> HourlyWeather:
        """逐小时天气预报"""
        res = await self._get_data(
            url=self.url_hourly,
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_res(res)
        return HourlyWeather(**res.json())

    async def _get_data(self, url: str, params: dict) -> Response:
        """请求数据"""
        async with AsyncClient() as client:
            res = await client.get(url, params=params)
        return res

    def _check_res(self, res: Response) -> bool:
        """检查返回值是否正确"""
        if res.status_code != 200:
            logger.error(f"HTTP 状态码: {res.status_code}")
            raise APIError(f"HTTP 状态码: {res.status_code}")
        return True
