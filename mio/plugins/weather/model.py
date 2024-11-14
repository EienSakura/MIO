from enum import IntEnum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class Now(BaseModel):
    """
    https://dev.qweather.com/docs/api/weather/weather-now/
    code 请参考状态码
    updateTime 当前API的最近更新时间
    fxLink 当前数据的响应式页面，便于嵌入网站或应用
    now.obsTime 数据观测时间
    now.temp 温度，默认单位：摄氏度
    now.feelsLike 体感温度，默认单位：摄氏度
    now.icon 天气状况的图标代码，另请参考天气图标项目
    now.text 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
    now.wind360 风向360角度
    now.windDir 风向
    now.windScale 风力等级
    now.windSpeed 风速，公里/小时
    now.humidity 相对湿度，百分比数值
    now.precip 过去1小时降水量，默认单位：毫米
    now.pressure 大气压强，默认单位：百帕
    now.vis 能见度，默认单位：公里
    now.cloud 云量，百分比数值。可能为空
    now.dew 露点温度。可能为空
    refer.sources 原始数据来源，或数据源说明，可能为空
    refer.license 数据许可或版权声明，可能为空
    """
    model_config = ConfigDict(extra="allow")
    obsTime: str
    temp: str
    icon: str
    text: str
    windScale: str
    windDir: str
    humidity: str
    precip: str
    vis: str


class NowWeather(BaseModel):
    """实时天气"""
    code: str
    now: Now


class Daily(BaseModel):
    """
    https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
    code 请参考状态码
    updateTime 当前API的最近更新时间
    fxLink 当前数据的响应式页面，便于嵌入网站或应用
    daily.fxDate 预报日期
    daily.sunrise 日出时间，在高纬度地区可能为空
    daily.sunset 日落时间，在高纬度地区可能为空
    daily.moonrise 当天月升时间，可能为空
    daily.moonset 当天月落时间，可能为空
    daily.moonPhase 月相名称
    daily.moonPhaseIcon 月相图标代码，另请参考天气图标项目
    daily.tempMax 预报当天最高温度
    daily.tempMin 预报当天最低温度
    daily.iconDay 预报白天天气状况的图标代码，另请参考天气图标项目
    daily.textDay 预报白天天气状况文字描述，包括阴晴雨雪等天气状态的描述
    daily.iconNight 预报夜间天气状况的图标代码，另请参考天气图标项目
    daily.textNight 预报晚间天气状况文字描述，包括阴晴雨雪等天气状态的描述
    daily.wind360Day 预报白天风向360角度
    daily.windDirDay 预报白天风向
    daily.windScaleDay 预报白天风力等级
    daily.windSpeedDay 预报白天风速，公里/小时
    daily.wind360Night 预报夜间风向360角度
    daily.windDirNight 预报夜间当天风向
    daily.windScaleNight 预报夜间风力等级
    daily.windSpeedNight 预报夜间风速，公里/小时
    daily.precip 预报当天总降水量，默认单位：毫米
    daily.uvIndex 紫外线强度指数
    daily.humidity 相对湿度，百分比数值
    daily.pressure 大气压强，默认单位：百帕
    daily.vis 能见度，默认单位：公里
    daily.cloud 云量，百分比数值。可能为空
    refer.sources 原始数据来源，或数据源说明，可能为空
    refer.license 数据许可或版权声明，可能为空
    """
    model_config = ConfigDict(extra="allow")
    fxDate: str
    week: Optional[str] = None
    date: Optional[str] = None
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str
    iconDay: str
    iconNight: str


class DailyWeather(BaseModel):
    """每日天气预报"""
    code: str
    daily: List[Daily]


class Air(BaseModel):
    """
    https://dev.qweather.com/docs/api/air/air-now/
    code 请参考状态码
    updateTime 当前API的最近更新时间
    fxLink 当前数据的响应式页面，便于嵌入网站或应用
    now.pubTime 空气质量数据发布时间
    now.aqi 空气质量指数
    now.level 空气质量指数等级
    now.category 空气质量指数级别
    now.primary 空气质量的主要污染物，空气质量为优时，返回值为NA
    now.pm10 PM10
    now.pm2p5 PM2.5
    now.no2 二氧化氮
    now.so2 二氧化硫
    now.co 一氧化碳
    now.o3 臭氧
    station.name 监测站名称
    station.id 监测站ID
    station.pubTime 空气质量数据发布时间
    station.aqi 空气质量指数
    station.level 空气质量指数等级
    station.category 空气质量指数级别
    station.primary 空气质量的主要污染物，空气质量为优时，返回值为NA
    station.pm10 PM10
    station.pm2p5 PM2.5
    station.no2 二氧化氮
    station.so2 二氧化硫
    station.co 一氧化碳
    station.o3 臭氧
    refer.sources 原始数据来源，或数据源说明，可能为空
    refer.license 数据许可或版权声明，可能为空
    """
    model_config = ConfigDict(extra="allow")
    category: str
    aqi: str
    pm2p5: str
    pm10: str
    o3: str
    co: str
    no2: str
    so2: str
    tag_color: Optional[str] = None


class AirQuality(BaseModel):
    """实时空气质量"""
    model_config = ConfigDict(extra="allow")
    code: str
    now: Optional[Air] = None


class Warning(BaseModel):
    """
    https://dev.qweather.com/docs/api/warning/weather-warning/
    code 请参考状态码
    updateTime 当前API的最近更新时间
    fxLink 当前数据的响应式页面，便于嵌入网站或应用
    warning.id 本条预警的唯一标识，可判断本条预警是否已经存在
    warning.sender 预警发布单位，可能为空
    warning.pubTime 预警发布时间
    warning.title 预警信息标题
    warning.startTime 预警开始时间，可能为空
    warning.endTime 预警结束时间，可能为空
    warning.status 预警信息的发布状态
    warning.level 预警等级（已弃用），不要再使用这个字段，该字段已弃用，目前返回为空或未更新的值。请使用severity和severityColor代替
    warning.severity 预警严重等级
    warning.severityColor 预警严重等级颜色，可能为空
    warning.type 预警类型ID
    warning.typeName 预警类型名称
    warning.urgency 预警信息的紧迫程度，可能为空
    warning.certainty 预警信息的确定性，可能为空
    warning.text 预警详细文字描述
    warning.related 与本条预警相关联的预警ID，当预警状态为cancel或update时返回。可能为空
    refer.sources 原始数据来源，或数据源说明，可能为空
    refer.license 数据许可或版权声明，可能为空
    """
    model_config = ConfigDict(extra="allow")
    title: str
    type: str
    pubTime: str
    text: str


class WeatherDisasterWarning(BaseModel):
    """天气灾害预警"""
    model_config = ConfigDict(extra="allow")
    code: str
    warning: Optional[List[Warning]] = None


class Hourly(BaseModel):
    """
    https://dev.qweather.com/docs/api/weather/weather-hourly-forecast/
    code 请参考状态码
    updateTime 当前API的最近更新时间
    fxLink 当前数据的响应式页面，便于嵌入网站或应用
    hourly.fxTime 预报时间
    hourly.temp 温度，默认单位：摄氏度
    hourly.icon 天气状况的图标代码，另请参考天气图标项目
    hourly.text 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
    hourly.wind360 风向360角度
    hourly.windDir 风向
    hourly.windScale 风力等级
    hourly.windSpeed 风速，公里/小时
    hourly.humidity 相对湿度，百分比数值
    hourly.precip 当前小时累计降水量，默认单位：毫米
    hourly.pop 逐小时预报降水概率，百分比数值，可能为空
    hourly.pressure 大气压强，默认单位：百帕
    hourly.cloud 云量，百分比数值。可能为空
    hourly.dew 露点温度。可能为空
    refer.sources 原始数据来源，或数据源说明，可能为空
    refer.license 数据许可或版权声明，可能为空
    """
    model_config = ConfigDict(extra="allow")
    fxTime: str
    hour: Optional[str] = None
    temp: str
    icon: str
    text: str
    temp_percent: Optional[str] = None


class HourlyWeather(BaseModel):
    """逐小时天气预报"""
    model_config = ConfigDict(extra="allow")
    code: str
    hourly: List[Hourly]


class HourlyType(IntEnum):
    """逐小时天气预报显示12小时或24小时"""
    current_12h = 1
    current_24h = 2
