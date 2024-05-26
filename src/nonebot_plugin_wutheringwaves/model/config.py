from pathlib import Path
from typing import Dict

from nonebot import logger
from pydantic import BaseModel


ROOT_PATH = Path(__name__).parent.absolute()
"""NoneBot2 机器人根目录"""

DATA_PATH = ROOT_PATH / "data" / "nonebot-plugin-wutheringwaves"
"""插件数据保存目录"""

CONFIG_PATH = DATA_PATH / "config.json"


class GeetestModel(BaseModel):
    geetest_url: str = ""
    geetest_params: dict = {"gt": "{gt}"}


class UsersModel(BaseModel):
    id: str
    token: str
    platform: str = "qq"


class Config(BaseModel):
    geetest: GeetestModel = GeetestModel()
    users: Dict[str, UsersModel] = {}
    """所有用户数据"""

    def save(self):
        """
        保存数据到文件
        """
        try:
            str_data = self.model_dump_json(indent=4)
        except (AttributeError, TypeError, ValueError):
            logger.exception("数据对象序列化失败，可能是数据类型错误")
            return False
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(str_data)
        return True


if CONFIG_PATH.exists() and CONFIG_PATH.is_file():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = f.read()
    config = Config.model_validate_json(data)
else:
    config = Config()
    try:
        str_data = config.model_dump_json(indent=4)
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(str_data)
    except (AttributeError, TypeError, ValueError, PermissionError):
        logger.exception(
            f"创建插件配置文件失败，请检查是否有权限读取和写入 {CONFIG_PATH}"
        )
        raise
    else:
        logger.info(f"插件配置文件 {CONFIG_PATH} 不存在，已创建默认插件配置文件。")
