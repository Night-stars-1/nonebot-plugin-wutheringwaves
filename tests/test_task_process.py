import pytest
from nonebot import logger
from nonebug import App


@pytest.mark.asyncio
async def test_task_process(app: App):
    from src.nonebot_plugin_wutheringwaves.api.task_process import TaskProcessSign
    from src.nonebot_plugin_wutheringwaves.model.config import config

    user_data = config.users.get("User")
    if user_data:
        task_obj = TaskProcessSign(token=user_data.token, user_id=user_data.id)
        task_list = await task_obj.get_task_process()
        assert all(task.gold for task in task_list)
        post_list = await task_obj.get_post_list()
        for task in task_list:
            match task.name:
                case "用户签到":
                    if await task_obj.sign("3"):
                        logger.info(f"库街区签到 - 成功")
                    else:
                        logger.info(f"库街区签到 - 失败")
                        assert False
                case "分享1次帖子":
                    if await task_obj.share():
                        logger.info(f"库街区分享 - 成功")
                    else:
                        logger.info(f"库街区分享 - 失败")
                        assert False
                case "浏览3篇帖子":
                    for n in range(task.num):
                        if await task_obj.look(post_list[n]):
                            logger.info(f"库街区浏览 - 成功")
                        else:
                            logger.info(f"库街区浏览 - 失败")
                            assert False
                case "点赞5次":
                    for n in range(task.num):
                        if await task_obj.like(post_list[n]):
                            logger.info(f"库街区点赞 - 成功")
                        else:
                            logger.info(f"库街区点赞 - 失败")
                            assert False
