"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-25 14:57:57
LastEditTime: 2024-05-26 19:14:41
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-25 14:57:57
LastEditTime: 2024-05-25 15:44:41
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import pytest
from nonebot import logger
from nonebug import App


@pytest.mark.asyncio
async def test_sign(app: App):
    from src.nonebot_plugin_wutheringwaves.api.game_sign import AVAILABLE_GAME_SIGNS
    from src.nonebot_plugin_wutheringwaves.model.config import config

    user_data = config.users.get("User")
    if user_data:
        for class_type in AVAILABLE_GAME_SIGNS:
            signer = class_type(token=user_data.token, user_id=user_data.id)
            rewards = await signer.get_rewards()
            assert rewards.success
            sign_result = await signer.sign()
            if sign_result.success:
                for today in sign_result.data.todayList:
                    name = rewards.goods_config[today.goodsId].goodsName
                    num = today.goodsNum
                    logger.info(f"签到成功，获得{name}x{num}")
                assert True
            elif sign_result.is_signed_in:
                logger.info("今日已签到")
                assert True
            elif sign_result.login_expired:
                logger.error("登录过期")
                assert False
            else:
                logger.error(sign_result.msg)
                assert False
