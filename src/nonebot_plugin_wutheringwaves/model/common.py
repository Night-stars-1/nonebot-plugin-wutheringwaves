"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 22:03:51
LastEditTime: 2024-05-25 22:21:14
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Optional

from pydantic import BaseModel

__all__ = ["CommandUsage", "Award", "BaseApiStatus", "GetSmsCodeStatus"]


class CommandUsage(BaseModel):
    """
    插件命令用法信息
    """

    name: Optional[str] = None
    description: Optional[str] = None
    usage: Optional[str] = None


class Award(BaseModel):
    """
    签到奖励数据
    """

    name: str
    """签到获得的物品名称"""
    icon: str
    """物品图片链接"""
    cnt: int
    """物品数量"""


class BaseApiStatus(BaseModel):
    """
    API返回结果基类
    """

    success: bool = False
    """成功"""
    login_expired: bool = False
    """登录失效"""
    need_verify: bool = False
    """需要进行人机验证"""

    def __bool__(self):
        return self.success


class GetSmsCodeStatus(BaseApiStatus):
    """
    发送短信验证码 返回结果
    """

    incorrect_geetest: bool = False
    """人机验证结果数据无效"""
    not_registered: bool = False
    """手机号码未注册"""
    invalid_phone_number: bool = False
    """手机号码无效"""
