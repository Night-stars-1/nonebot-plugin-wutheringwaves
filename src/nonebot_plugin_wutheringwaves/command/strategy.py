from typing import Annotated, Any
from nonebot import logger, on_regex
from nonebot.params import RegexGroup
from nonebot.adapters import Event
from nonebot.adapters.console import Event as ConsoleEvent
from nonebot_plugin_saa import Image

from ..command.common import CommandRegistry
from ..model import CommandUsage
from ..utils import RESOURCES, get_role_name

__all__ = ["strategy"]


strategy = on_regex(r"/一图流(.*)|/(.*)一图流")
CommandRegistry.set_usage(
    strategy,
    CommandUsage(
        name="一图流",
        description="获取角色一图流攻略",
    ),
)


@strategy.handle()
async def _(event: Event, role_name_list: Annotated[tuple[Any, ...], RegexGroup()]):
    role_name: str = get_role_name(role_name_list[0] or role_name_list[1])
    role_strategy_path = RESOURCES / "一图流" / f"{role_name}.jpg"
    if role_strategy_path.exists():
        if isinstance(event, ConsoleEvent):
            await strategy.finish(str(role_strategy_path))
        else:
            await Image(role_strategy_path).finish()
    else:
        await strategy.finish("角色不存在")
