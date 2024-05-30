"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 22:06:22
LastEditTime: 2024-05-30 19:19:56
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from ast import alias
import json
from pathlib import Path
from typing import Dict, List, Union

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
    "RESOURCES",
    "get_role_name",
]

ROOT_PATH = Path(__file__).resolve().parent.parent
"""NoneBot2 机器人根目录"""
RESOURCES = ROOT_PATH / "resources"
"""资源目录"""

GeneralMessageEvent = Union[OneBotV11MessageEvent, ConsoleMessageEvent]
"""消息事件类型"""
GeneralPrivateMessageEvent = PrivateMessageEvent, ConsoleMessageEvent
"""私聊消息事件类型"""
GeneralGroupMessageEvent = GroupMessageEvent, ConsoleMessageEvent
"""群聊消息事件类型"""


def read_json(path: Union[str, Path]):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


ROLE_ALIAS_LIST: Dict[str, List[str]] = read_json(RESOURCES / "role_alias.json")


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
    说明:
        检查手机号是否有效（只包含数字且长度为11位）
    """
    return mobile.isdigit() and len(mobile) == 11


def mask_mobile(mobile: str):
    """
    说明:
        模糊手机号
    """
    if is_valid_mobile(mobile):
        # 将中间4位数字用星号替换
        masked_number = mobile[:3] + "****" + mobile[-4:]
        return masked_number
    else:
        return None


def get_role_name(name: str):
    """
    说明:
        通过别名获取角色名称
    参数:
        :param name 别名
    """
    for role_name, alias_name in ROLE_ALIAS_LIST.items():
        if name in alias_name:
            return role_name
    return name
