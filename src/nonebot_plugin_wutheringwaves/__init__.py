"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 20:17:38
LastEditTime: 2024-05-26 01:55:39
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys

import nonebot
from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_saa")
require("nonebot_plugin_apscheduler")

_driver = nonebot.get_driver()
_command_begin = list(_driver.config.command_start)[0]

from ._version import __version__

__plugin_meta__ = PluginMetadata(
    name="库街区小助手插件\n",
    description="库街区工具-每日签到\n",
    type="application",
    homepage="",
    supported_adapters={"~onebot.v11", "~qq"},
    usage=f"\n🔐 {_command_begin}登录 ➢ 登录绑定库街区账户"
    f"\n🗓️ {_command_begin}签到 ➢ 手动进行游戏签到"
    "\n\n⚠️你的数据将经过机器人服务器，请确定你信任服务器所有者再使用。",
    extra={"version": __version__},
)

from .utils.logger import set_logger

set_logger()

# 加载命令
from .command import *
from .model.config import *
