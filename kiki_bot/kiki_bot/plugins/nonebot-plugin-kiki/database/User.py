import json
from ..tools.tools import *

class User:
    def __init__(self, qq_num, user_name, mc_uuid = None, whitelisted = None, user_info = None):
        self.qq_num = qq_num
        self.user_name = user_name.lower()
        self.mc_uuid = mc_uuid
        self.whitelisted = whitelisted
        self.user_info = user_info      # 封禁理由, 封禁时间 之类的

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)
    
    def get_display_name(self):
        (name, uuid) = get_name_and_uuid_by_name(self.name)
        return name