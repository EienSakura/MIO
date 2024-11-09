#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mio.MioCore import MioBotCore

mioBotCore = MioBotCore()

if __name__ == '__main__':
    """
    启动MIO
    pip list --format=freeze> requirements.txt pip打包
    """
    mioBotCore.run()
