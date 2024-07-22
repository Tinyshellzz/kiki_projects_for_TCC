from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from .authorization import *
from ..config.config import *
from ..database.BanlistMapper import BanlistMapper, BanlistUser
import re
import datetime
from ..utils import tools

server_banlist = ""
class sync():
    async def handle(bot: Bot, event: Event):
        users = BanlistMapper.get_all()

        # if os.path.exists(server_whitelist):
        #     whitelist = "["
            
        #     for user in users:
        #         whitelist = whitelist + json.dumps({"uuid": user.mc_uuid, "name": user.user_name}) + ','
            
        #     l = len(whitelist)
        #     if whitelist[l-1] ==',':
        #         whitelist = whitelist[:-1] + ']'
        #     else:
        #         whitelist = whitelist + ']'

        #     # 直接将白名单写入 whitelist.json
        #     with open(server_whitelist, "w") as text_file:
        #         text_file.write(whitelist)
            