"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-26 01:51:10
LastEditTime: 2024-05-26 01:51:20
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path

from nonebot import logger

ROOT_PATH = Path(__name__).parent.absolute()
"""NoneBot2 机器人根目录"""

DATA_PATH = ROOT_PATH / "data" / "nonebot-plugin-wutheringwaves"
"""插件数据保存目录"""

LOGGER_PATH = DATA_PATH / "debug.log"


def set_logger():
    logger.add(
        LOGGER_PATH,
        format="{time:HH:mm:ss} - "
        "{level}\t| "
        "{module}.{function}:{line} - "
        " {message}",
        level="DEBUG",
        rotation="1 days",
        enqueue=True,
        serialize=False,
        encoding="utf-8",
        retention="10 days",
    )
