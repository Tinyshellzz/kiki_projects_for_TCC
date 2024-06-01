import json

class WhitelistCode:
    def __init__(self, mc_uuid, code, user_name):
        self.mc_uuid = mc_uuid
        self.code = code
        self.user_name = user_name

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)