"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 21:49:56
LastEditTime: 2024-05-26 02:18:19
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from nonebot import logger, on_command
from nonebot.adapters import Event, Message
from nonebot.adapters.onebot.v11 import MessageEvent as OneBotV11MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as OneBotV11MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg, T_State

from ..api.login import get_sms_code, login_by_code
from ..command.common import CommandRegistry
from ..model import CommandUsage
from ..model.config import UsersModel, config
from ..utils import GeneralMessageEvent, mask_mobile

__all__ = ["login"]

login = on_command("登录", priority=4, block=True)
CommandRegistry.set_usage(
    login,
    CommandUsage(
        name="登录",
        description="登录库街区",
    ),
)


@login.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("mobile", args)


@login.got("mobile", prompt="请输入手机号")
async def _(state: T_State, mobile: str = ArgPlainText()):
    if mobile == "退出":
        await login.finish("退出成功")
    is_mobile = mask_mobile(mobile)
    if is_mobile:
        sms_code_status = await get_sms_code(mobile)
        if sms_code_status:
            state["mobile"] = mobile
            await login.send("短信验证码已发送，请查收")
        else:
            await login.finish("获取短信验证码失败")
    else:
        await login.reject("请输入正确的手机号码")


code = on_command("验证码", priority=4, block=True)
CommandRegistry.set_usage(
    login,
    CommandUsage(
        name="验证码",
        description="登录库街区的验证码",
    ),
)


@code.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    logger.info(args)
    if args.extract_plain_text():
        matcher.set_arg("mobile", args)


@code.got("mobile", prompt="请输入手机号")
async def _(state: T_State, mobile: str = ArgPlainText()):
    if mobile == "退出":
        await login.finish("退出成功")
    is_mobile = mask_mobile(mobile)
    if is_mobile:
        state["mobile"] = mobile
    else:
        await login.reject("请输入正确的手机号码")


@login.got("code", prompt="请输入验证码")
@code.got("code", prompt="请输入验证码")
async def _(event: Event, state: T_State, code: str = ArgPlainText()):
    if code == "退出":
        await login.finish("退出成功")
    user_id = event.get_user_id()
    mobile = state["mobile"]
    login_result = await login_by_code(code, mobile)
    if login_result:
        logger.info("短信验证码登录 - 登录成功")
        if user_id in config.users:
            user_data = config.users[user_id]
            user_data.id = login_result.data.userId
            user_data.token = login_result.data.token
        else:
            config.users.setdefault(
                user_id,
                UsersModel(id=login_result.data.userId, token=login_result.data.token),
            )
        config.save()
        await login.finish("登录成功")
    elif login_result.code_error:
        logger.info("短信验证码登录 - 验证码错误")
        await login.finish("验证码错误")
    else:
        logger.error("短信验证码登录 - 登录失败")
        await login.finish("登录失败")
