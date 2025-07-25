# -*- coding: utf-8 -*-
import random
import platform
import sys
from simplepy import logger

if platform.system() == "Windows":
    import win32api

else:
    logger.info('only windows platform', '111')
    sys.exit(1)


def set_display():
    """
    屏幕分辨率设置
    Returns:

    """
    display_size = [
        [1920, 1080],
        [1680, 1050],
        [1600, 900],
        [1440, 900],
        [1400, 1050]
    ]
    d_size = random.choice(display_size)
    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsWidth = d_size[0]
    dm.PelsHeight = d_size[1]
    dm.BitsPerPel = 32
    dm.DisplayFixedOutput = 0
    win32api.ChangeDisplaySettings(dm, 0)


def wechat_send():
    """
    调用PC微信发送消息
    Returns:

    """
