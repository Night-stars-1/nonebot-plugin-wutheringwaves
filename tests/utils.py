from datetime import datetime

from nonebot.adapters.console import Message, MessageEvent
from nonechat.info import User


def make_event(message: str = "") -> MessageEvent:
    return MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message(message),
        user=User(id=123456789),
    )
