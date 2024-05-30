"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-25 01:10:28
LastEditTime: 2024-05-30 23:58:40
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from datetime import datetime
from typing import Set, Type

import httpx
from nonebot import logger

from ..model.requests import RewardsResultHandler, SignResultHandler
from .task_process import TaskProcessSign

AVAILABLE_GAME_SIGNS: Set[Type["BaseGameSign"]] = set()
"""可用的子类"""


class BaseGameSign:
    """
    游戏签到基类
    """

    name = "未知"
    """游戏名字"""

    url_reward = "https://api.kurobbs.com/encourage/signIn/initSignInV2"
    url_sign = "https://api.kurobbs.com/encourage/signIn/v2"

    game_id = "0"
    server_id = "0"
    role_id = "0"

    def __init__(self, token: str, user_id: str) -> None:
        self.token = token
        self.user_id = user_id
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; 22081212C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.179 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '"Chromium";v="124", "Android WebView";v="124", "Not-A.Brand";v="99"',
            "source": "android",
            "sec-ch-ua-mobile": "?1",
            "devcode": "111.181.85.154, Mozilla/5.0 (Linux; Android 14; 22081212C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.179 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0",
            "token": token,
            "sec-ch-ua-platform": '"Android"',
            "origin": "https://web-static.kurobbs.com",
            "x-requested-with": "com.kurogame.kjq",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "priority": "u=1, i",
        }

    async def get_rewards(self):
        """
        说明:
            获取签到信息
        """
        data = {
            "gameId": self.game_id,
            "serverId": self.server_id,
            "roleId": self.role_id,
            "userId": self.user_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url_reward, data=data, headers=self.headers
            )

        data = response.json()
        logger.debug(data)
        return RewardsResultHandler.model_validate(data)

    async def sign(self):
        """
        游戏签到
        """
        now = datetime.now()
        req_month = now.strftime("%m")
        data = {
            "gameId": self.game_id,
            "serverId": self.server_id,
            "roleId": self.role_id,
            "userId": self.user_id,
            "reqMonth": req_month,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.url_sign, data=data, headers=self.headers)

        data = response.json()
        logger.debug(data)
        return SignResultHandler.model_validate(data)

    async def user_sign(self):
        """库街区签到"""
        task_obj = TaskProcessSign(token=self.token, user_id=self.user_id)
        return task_obj.sign(self.game_id)


class WutheringWaves(BaseGameSign):
    name = "鸣潮"
    game_id = "3"
    server_id = "76402e5b20be2c39f095a152090afddc"
    role_id = "103288838"


AVAILABLE_GAME_SIGNS.add(WutheringWaves)
