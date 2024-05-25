from typing import Optional
from pydantic import BaseModel


class ApiResultHandler(BaseModel):
    """
    API返回的数据处理器
    """

    code: int = -1
    """返回码"""
    success: bool = False
    """成功"""
    data: Optional[dict] = None
    """返回数据"""
    need_verify: bool = False
    """需要进行人机验证"""

    def __bool__(self):
        return self.success


class GetSmsCodeResultHandler(ApiResultHandler):
    """
    获取短信验证码数据处理器
    """

    class DataModel(BaseModel):
        geeTest: bool
        """是否需要人机验证"""

    data: DataModel

    def __init__(self, **data):
        super().__init__(**data)
        if not self.data.geeTest and self.code == 200:
            self.success = True
        else:
            self.success = False
            self.need_verify = True

    def __bool__(self):
        return self.success and self.code == 200


class GeetestResultHandler(ApiResultHandler):
    """
    人机验证数据处理器
    """

    class DataModel(BaseModel):
        lot_number: str
        """验证标识"""
        result: str
        """验证结果"""
        fail_count: int
        """失败次数"""
        seccode: dict
        """验证数据"""
        score: str
        """验证分数"""
        payload: str
        """验证数据"""
        process_token: str
        """验证标识"""
        payload_protocol: int
        """验证数据"""

    status: str
    """状态"""
    data: DataModel

    def __init__(self, **data):
        super().__init__(**data)
        if self.status == "success" and self.data.result == "success":
            self.success = True
        else:
            self.success = False

    def __bool__(self):
        return self.success


class LoginResultHandler(ApiResultHandler):
    """
    登录数据处理器
    """

    class DataModel(BaseModel):
        enableChildMode: bool
        """是否启用儿童模式"""
        gender: int
        """性别"""
        signature: str
        """签名"""
        headUrl: str
        """头像链接"""
        headCode: str
        """头像编号"""
        userName: str
        """用户名"""
        userId: str
        """用户ID"""
        isRegister: int
        """是否注册"""
        isOfficial: int
        """是否官方"""
        status: int
        """状态"""
        unRegistering: bool
        """是否注销"""
        token: str
        """登录凭证"""
    msg: str
    data: Optional[DataModel] = None

    def __init__(self, **data):
        super().__init__(**data)

    def __bool__(self):
        return self.success and self.code == 200

    @property
    def code_error(self):
        """
        验证码错误
        """
        return self.code == 130
