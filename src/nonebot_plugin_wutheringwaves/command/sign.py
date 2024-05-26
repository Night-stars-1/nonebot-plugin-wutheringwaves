"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 21:49:56
LastEditTime: 2024-05-26 19:27:44
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
    message = ""
    user_id = event.get_user_id()
    user_data = config.users.get(user_id)
    await sign.send("开始执行签到")
    if user_data:
        for class_type in AVAILABLE_GAME_SIGNS:
            message += f"开始签到{class_type.name}\n\n"
            signer = class_type(token=user_data.token, user_id=user_data.id)
            rewards = await signer.get_rewards()
            sign_result = await signer.sign()
            if sign_result:
                for today in sign_result.data.todayList:
                    name = rewards.goods_config[today.goodsId].goodsName
                    num = today.goodsNum
                    message += f"签到成功，获得{name}x{num}\n"
            elif sign_result.is_signed_in:
                message += "今日已签到\n"
            elif sign_result.login_expired:
                message += "登录过期\n"
            else:
                logger.error(sign_result.msg)
                message += f"签到失败，{sign_result.msg}\n"
        await sign.finish(message[:-1])
    else:
        logger.error("签到 - 无用户信息")
        await sign.finish("无用户信息，请先登录")
