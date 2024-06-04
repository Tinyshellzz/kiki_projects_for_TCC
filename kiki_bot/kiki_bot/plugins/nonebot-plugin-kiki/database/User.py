import json
from ..tools.tools import *
from .UserMapper import *

class User:
    def __init__(self, qq_num, user_name, display_name = None, mc_uuid = None, whitelisted = None, user_info = None):
        self.qq_num = qq_num
        self.user_name = user_name.lower()
        self.display_name = display_name
        self.mc_uuid = mc_uuid
        self.whitelisted = whitelisted
        self.user_info = user_info      # 封禁理由, 封禁时间 之类的

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)
    
    def get_display_name(self):
        if self.display_name == None:
            user = get(user_name=self.user_name)
            if user.display_name != None: 
                self.display_name = user.display_name
                return self.display_name
            else:
                name = None
                try:
                    name = get_name_by_uuid(self.mc_uuid)
                    update_name_by_uuid(self.mc_uuid, name, name)
                except:
                    pass
                self.user_name = name.lower()
                self.display_name = name
        return self.display_name