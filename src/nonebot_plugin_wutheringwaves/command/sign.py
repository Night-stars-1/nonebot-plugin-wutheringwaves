"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 21:49:56
LastEditTime: 2024-05-26 02:11:40
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from nonebot import logger, on_command
from nonebot.adapters import Event

from ..api.game_sign import AVAILABLE_GAME_SIGNS
from ..command.common import CommandRegistry
from ..model import CommandUsage
from ..model.config import config

__all__ = ["sign"]

sign = on_command("签到", priority=4, block=True)
CommandRegistry.set_usage(
    sign,
    CommandUsage(
        name="签到",
        description="签到库街区",
    ),
)


@sign.handle()
async def _(event: Event):
    user_id = event.get_user_id()
    user_data = config.users.get(user_id)
    await sign.send("开始执行签到")
    if user_data:
        for class_type in AVAILABLE_GAME_SIGNS:
            signer = class_type(token=user_data.token, user_id=user_data.id)
            await signer.get_rewards()
    else:
        logger.error("签到 - 无用户信息")
        await sign.finish("无用户信息，请先登录")
