"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-25 01:10:28
LastEditTime: 2024-05-30 23:55:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from datetime import datetime
from typing import Set, Type

import httpx
from nonebot import logger

from ..model.requests import (
    ApiResultHandler,
    ForumListResultHandler,
    LikeResultHandler,
    TaskProcessResultHandler,
    TotalGoldResultHandler,
)


class TaskProcessSign:
    """
    每日任务签到基类
    """

    name = "未知"
    """游戏名字"""

    url_task_process = "https://api.kurobbs.com/encourage/level/getTaskProcess"
    url_gold = "https://api.kurobbs.com/encourage/gold/getTotalGold"
    url_like = "https://api.kurobbs.com/forum/like"
    url_forum_list = "https://api.kurobbs.com/forum/list"
    url_post_detail = "https://api.kurobbs.com/forum/getPostDetail"
    url_share_task = "https://api.kurobbs.com/encourage/level/shareTask"
    url_user_sign = "https://api.kurobbs.com/user/signIn"

    game_id = "3"

    def __init__(self, token: str, user_id: str) -> None:
        self.user_id = user_id
        self.headers = {
            "User-Agent": "okhttp/3.11.0",
            "Connection": "Keep-Alive",
            # 'Accept-Encoding': 'gzip',
            "Content-Type": "application/x-www-form-urlencoded",
            "devCode": "7F5A1E0991356F96E4E708CF2BEABE1AAA0468C2",
            "ip": "192.168.10.249",
            "source": "android",
            "version": "2.2.0",
            "versionCode": "2200",
            "token": token,
            "osVersion": "Android",
            "distinct_id": "80337843-6746-40e0-bd40-a5556f5441bf",
            "countryCode": "CN",
            "model": "22081212C",
            "lang": "zh-Hans",
            "channelId": "2",
        }

    async def get_task_process(self):
        """
        说明:
            获取每日任务信息
        """
        data = {
            "gameId": self.game_id,
            "userId": self.user_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url_task_process, data=data, headers=self.headers
            )

        data = response.json()
        logger.debug(data)
        api_result = TaskProcessResultHandler.model_validate(data)
        return api_result.task_list

    async def get_total_gold(self):
        """
        说明:
            获取金币总数
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url_gold, headers=self.headers)

        data = response.json()
        logger.debug(data)
        api_result = TotalGoldResultHandler.model_validate(data)
        return api_result.gold

    async def get_post_list(self):
        """
        获取文章列表
        """
        data = {
            "forumId": "9",
            "gameId": self.game_id,
            "pageIndex": "1",
            "pageSize": "20",
            "searchType": "3",
            "timeType": "0",
            "topicId": "0",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url_forum_list, data=data, headers=self.headers
            )
        data = response.json()
        logger.debug(data)
        api_result = ForumListResultHandler.model_validate(data)
        return api_result.post_list

    async def like(self, post: ForumListResultHandler.PostModel):
        logger.info(f"库街区浏览 - {post.postTitle}")
        data = {
            "forumId": post.gameForumId,
            "gameId": post.gameId,
            "likeType": "1",
            "operateType": "1",
            "postCommentId": "0",
            "postCommentReplyId": "0",
            "postId": post.postId,
            "postType": post.postType,
            "toUserId": post.userId,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url_like, data=data, headers=self.headers)
        data = response.json()
        logger.debug(data)
        api_result = LikeResultHandler.model_validate(data)
        return api_result

    async def look(self, post: ForumListResultHandler.PostModel):
        data = {
            "isOnlyPublisher": "0",
            "postId": post.postId,
            "showOrderType": "2",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url_post_detail, data=data, headers=self.headers
            )
        data = response.json()
        logger.debug(data)
        api_result = ApiResultHandler.model_validate(data)
        return api_result

    async def share(self):
        data = {
            "gameId": self.game_id,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url_share_task, data=data, headers=self.headers
            )
        data = response.json()
        logger.debug(data)
        api_result = ApiResultHandler.model_validate(data)
        return api_result

    async def sign(self, game_id=game_id):
        data = {
            "gameId": game_id,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url_user_sign, data=data, headers=self.headers
            )
        data = response.json()
        logger.debug(data)
        api_result = ApiResultHandler.model_validate(data)
        return api_result
