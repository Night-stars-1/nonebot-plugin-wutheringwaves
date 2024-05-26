"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 22:06:22
LastEditTime: 2024-05-25 22:14:23
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Union

import httpx
from loguru import logger
from nonebot.adapters.console import MessageEvent as ConsoleMessageEvent
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as OneBotV11MessageEvent
from nonebot.adapters.onebot.v11 import PrivateMessageEvent

from ..model import BaseApiStatus
from ..model.config import config
from ..model.requests import GeetestResultHandler

__all__ = [
    "GeneralMessageEvent",
    "GeneralPrivateMessageEvent",
    "GeneralGroupMessageEvent",
    "is_valid_mobile",
    "mask_mobile",
]

GeneralMessageEvent = Union[OneBotV11MessageEvent, ConsoleMessageEvent]
"""消息事件类型"""
GeneralPrivateMessageEvent = PrivateMessageEvent, ConsoleMessageEvent
"""私聊消息事件类型"""
GeneralGroupMessageEvent = GroupMessageEvent, ConsoleMessageEvent
"""群聊消息事件类型"""


async def get_validate_v4():
    try:
        content = config.geetest.geetest_params
        for key, value in content.items():
            if isinstance(value, str):
                content[key] = value.format(gt="3f7e2d848ce0cb7e7d019d621e556ce2")
        async with httpx.AsyncClient() as client:
            response = await client.post(config.geetest.geetest_url, json=content)
        data = response.json()
        api_result = GeetestResultHandler.model_validate(data)
        if api_result:
            logger.info("获取人机验证数据成功")
            return BaseApiStatus(success=True), api_result.data.seccode
        else:
            logger.error("获取人机验证数据失败")
            return BaseApiStatus(), None
    except Exception as e:
        logger.exception(f"获取人机验证数据失败: {e}")
        return BaseApiStatus(), None


def is_valid_mobile(mobile: str):
    """
    检查手机号是否有效（只包含数字且长度为11位）
    """
    return mobile.isdigit() and len(mobile) == 11


def mask_mobile(mobile: str):
    """
    模糊手机号
    """
    if is_valid_mobile(mobile):
        # 将中间4位数字用星号替换
        masked_number = mobile[:3] + "****" + mobile[-4:]
        return masked_number
    else:
        return None
