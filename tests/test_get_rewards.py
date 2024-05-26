"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-25 14:57:57
LastEditTime: 2024-05-26 02:21:56
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-25 14:57:57
LastEditTime: 2024-05-25 15:44:41
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import pytest
from nonebug import App

from .utils import make_event

@pytest.mark.asyncio
async def test_login(app: App):
    from src.nonebot_plugin_wutheringwaves.command.login import login

    async with app.test_matcher(login) as ctx:
        bot = ctx.create_bot()
        event = make_event("/登录")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "请输入手机号")
        ctx.should_rejected(login)

        event = make_event("12345678975")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "短信验证码已发送，请查收")
        ctx.should_call_send(event, "请输入验证码")

        event = make_event("123")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "123")
        ctx.should_finished(login)

@pytest.mark.asyncio
async def test_code(app: App):
    from src.nonebot_plugin_wutheringwaves.command.login import code

    async with app.test_matcher(code) as ctx:
        bot = ctx.create_bot()
        event = make_event("/验证码")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "请输入手机号")
        ctx.should_rejected(code)

        event = make_event("12345678975")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "短信验证码已发送，请查收")
        ctx.should_call_send(event, "请输入验证码")

        event = make_event("123")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "123")
        ctx.should_finished(code)
