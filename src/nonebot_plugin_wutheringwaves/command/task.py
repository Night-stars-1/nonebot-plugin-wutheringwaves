"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 21:49:56
LastEditTime: 2024-05-31 00:12:04
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from nonebot import logger, on_command
from nonebot.adapters import Event

from ..api.task_process import TaskProcessSign
from ..command.common import CommandRegistry
from ..model import CommandUsage
from ..model.config import config

__all__ = ["task_sign"]

task_sign = on_command("库街区签到", priority=4, block=True)
CommandRegistry.set_usage(
    task_sign,
    CommandUsage(
        name="库街区签到",
        description="库街区签到",
    ),
)


@task_sign.handle()
async def _(event: Event):
    await task_sign.send("开始库街区签到")
    message = "库街区\n"
    user_id = event.get_user_id()
    user_data = config.users.get(user_id)
    if user_data:
        task_obj = TaskProcessSign(token=user_data.token, user_id=user_data.id)
        task_list = await task_obj.get_task_process()
        post_list = await task_obj.get_post_list()
        for task in task_list:
            match task.name:
                case "用户签到":
                    for _ in range(task.num):
                        if await task_obj.sign("3"):
                            logger.info("库街区签到 - 成功")
                            message += "库街区签到 - 成功\n"
                        else:
                            logger.info("库街区签到 - 失败")
                            message += "库街区签到 - 失败\n"
                case "分享1次帖子":
                    for _ in range(task.num):
                        if await task_obj.share():
                            logger.info("库街区分享 - 成功")
                            message += "库街区分享 - 成功\n"
                        else:
                            logger.info("库街区分享 - 失败")
                            message += "库街区分享 - 失败\n"
                case "浏览3篇帖子":
                    for n in range(task.num):
                        if await task_obj.look(post_list[n]):
                            logger.info("库街区浏览 - 成功")
                            message += "库街区浏览 - 成功\n"
                        else:
                            logger.info("库街区浏览 - 失败")
                            message += "库街区浏览 - 失败\n"
                case "点赞5次":
                    for n in range(task.num):
                        if await task_obj.like(post_list[n]):
                            logger.info("库街区点赞 - 成功")
                            message += "库街区点赞 - 成功\n"
                        else:
                            logger.info("库街区点赞 - 失败")
                            message += "库街区点赞 - 失败\n"
        gold = await task_obj.get_total_gold()
        message += f"当前库币: {gold}"
        await task_sign.finish(message[:-1])
    else:
        logger.error("签到 - 无用户信息")
        await task_sign.finish("无用户信息，请先登录")
