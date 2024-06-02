# 负责与验证码数据库交互
from pathlib import Path
from .User import User
from .DBConfig import *
from ..tools import tools
from ..config.config import *
from .WhitelistCode import WhitelistCode


# 获取 mc 服务器的 验证码
class WhitelistCodeMapper:
    def get(code):
        c = conn_codes.cursor()
        c.execute("SELECT * FROM codes WHERE code=:code", {'code': code})

        res = c.fetchall()
        c.close()

        # 没找到
        if len(res) == 0:
            return None
        
        res = res[0]
        return WhitelistCode(res[0], res[1], res[2])