"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-25 16:17:25
LastEditTime: 2024-05-25 22:39:56
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import httpx
from nonebot import logger

from ..model import GetSmsCodeStatus
from ..model.requests import GetSmsCodeResultHandler, LoginResultHandler
from ..utils.common import get_validate_v4

GET_SMS_CODE_URL = "https://api.kurobbs.com/user/getSmsCode"
LOGIN_URL = "https://api.kurobbs.com/user/sdkLogin"
LOGIN_HEADERS = {
    "User-Agent": "okhttp/3.11.0",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "osVersion": "Android",
    "devCode": "7F5A1E0991356F96E4E708CF2BEABE1AAA0468C2",
    "distinct_id": "80337843-6746-40e0-bd40-a5556f5441bf",
    "countryCode": "CN",
    "ip": "192.168.10.249",
    "model": "22081212C",
    "source": "android",
    "lang": "zh-Hans",
    "version": "2.2.0",
    "versionCode": "2200",
    "channelId": "2",
}


async def get_sms_code(mobile: str):
    data = {
        "mobile": mobile,
        "geeTestData": {},
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GET_SMS_CODE_URL, data=data, headers=LOGIN_HEADERS)

    data = response.json()
    logger.debug(data)
    api_result = GetSmsCodeResultHandler.model_validate(data)
    if api_result:
        logger.info("获取短信验证码 - 获取短信验证码成功")
        return GetSmsCodeStatus(success=True)
    elif api_result.need_verify:
        logger.error("获取短信验证码 - 需要进行人机验证")
        return await get_sms_code_by_captcha(mobile)
    else:
        logger.error("获取短信验证码 - 获取短信验证码失败")
        return GetSmsCodeStatus()


async def get_sms_code_by_captcha(mobile: str):
    geetest_status, geetest_data = await get_validate_v4()
    if geetest_status:
        data = {
            "mobile": mobile,
            "geeTestData": geetest_data,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GET_SMS_CODE_URL, data=data, headers=LOGIN_HEADERS
            )

        data = response.json()
        logger.debug(data)
        api_result = GetSmsCodeResultHandler.model_validate(data)
        if api_result:
            logger.info("通过验证获取短信验证码 - 获取短信验证码成功")
            return GetSmsCodeStatus(success=True)
        elif api_result.need_verify:
            logger.error("通过验证获取短信验证码 - 需要进行人机验证")
            return GetSmsCodeStatus(need_verify=True)
        else:
            logger.error("通过验证获取短信验证码 - 获取短信验证码失败")
            return GetSmsCodeStatus()
    else:
        logger.error("通过验证获取短信验证码 - 获取人机验证数据失败")
        return GetSmsCodeStatus(incorrect_geetest=True)


async def login_by_code(code: str, mobile: str):
    """
    说明:
        通过短信验证码登录
    """
    data = {
        "code": code,
        "devCode": LOGIN_HEADERS["devCode"],
        "gameList": "",
        "mobile": mobile,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            LOGIN_URL,
            headers=LOGIN_HEADERS,
            data=data,
        )
    data = response.json()
    logger.debug(data)
    api_result = LoginResultHandler.model_validate(data)
    return api_result
