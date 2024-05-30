"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-30 21:19:58
LastEditTime: 2024-05-30 22:56:36
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import pytest
from nonebug import App

from .utils import make_event


@pytest.mark.asyncio
async def test_strategy(app: App):
    from src.nonebot_plugin_wutheringwaves.command import strategy
    from src.nonebot_plugin_wutheringwaves.utils import RESOURCES

    async with app.test_matcher(strategy) as ctx:
        bot = ctx.create_bot()
        event = make_event("/湮灭主一图流")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, str(RESOURCES / "一图流" / "漂泊者-湮灭.jpg"))
        ctx.should_finished(strategy)
