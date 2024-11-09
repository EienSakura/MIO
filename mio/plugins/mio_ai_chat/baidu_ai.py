"""
yi_34b_chat
"""
import base64
import logging
import os

import qianfan
import requests
from qianfan import Image2Text

from mio.plugins.mio_ai_chat import config


def _image_to_base64(url):
    url = url.replace("https://", "http://")
    logging.captureWarnings(True)
    # 使用requests获取图片内容
    response = requests.get(url, verify=False)
    # 确保请求成功
    if response.status_code == 200:
        # 转换图片到Base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        # print(image_base64)
        return image_base64
    else:
        print("Failed to download image")
        return None


class BaiduAi:

    def __init__(self):
        baidu_config = config.baidu_config
        # 获取配置文件中 百度ai access_key和secret_key
        os.environ["QIANFAN_ACCESS_KEY"] = baidu_config.baidu_access_key
        os.environ["QIANFAN_SECRET_KEY"] = baidu_config.baidu_secret_key
        self.chat_comp = qianfan.ChatCompletion()

    def get_ai_response(self, question: str):
        """
        百度ai 对话模型
        :param question:
        :return:
        """
        # 指定特定模型
        resp = self.chat_comp.do(model="Yi-34B-Chat", messages=[{
            "role": "user",
            "content": question
        }])
        return resp["body"]

    @staticmethod
    def get_ai_image_recognition(image_path: str):
        """
        百度ai 图片识别
        :param image_path:
        :return:
        """
        encoded_string = _image_to_base64(image_path)
        # 使用model参数
        i2t = Image2Text(model="Fuyu-8B")
        resp = i2t.do(prompt="分析图片", image=encoded_string)
        # resp = i2t.do(prompt="分析一下图片画了什么", image=encoded_string)
        return resp["result"]

    def en_to_ch(self, text: str):
        """
            百度ai 文本翻译
            :param text:
            :return:
        """
        # 翻译到中文
        return self.get_ai_response("英译中 " + text)['result']
