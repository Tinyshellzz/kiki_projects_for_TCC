from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from .authorization import *
from ..config.config import *
from ..database.BanlistMapper import BanlistMapper, BanlistUser
import re
import datetime
from ..utils import tools

class ban:
    async def handle(bot: Bot, event: Event):
        if not await auth_qq(bot, event, auth_qq_list): return
        print('####################ban start########################')
        user_id = str(event.get_user_id())

        # 信息
        msg = str(event.get_message())
        length = len(msg)
        L = 0
        R = 0
        index = 0
        player = None
        unban_date = datetime.datetime.now()
        remarke = None
        while(True):
            while(R < length and msg[R] != ' '): R += 1

            cur_str = msg[L:R]

            if(index == 1):
                player = cur_str.lower()
            if(index == 2):
                # 计算unban_date
                if(re.search("^[0-9]+[smdMyY]$") != None):
                    number = int(msg[:-1])
                    last_char = msg[len[msg]-1]
                    if last_char == 's':
                        unban_date +=  datetime.timedelta(seconds=number)
                    elif last_char == 'm':
                        unban_date +=  datetime.timedelta(seconds=number*60)
                    elif last_char == 'd':
                        unban_date +=  datetime.timedelta(seconds=number*3600)
                    elif last_char == 'M':
                        unban_date +=  datetime.timedelta(seconds=number*3600*30)
                    elif last_char == 'y' or last_char == 'Y':
                        unban_date +=  datetime.timedelta(seconds=number*3600*365)
                else:
                    unban_date = datetime.datetime(9999, 12, 31, 23, 59, 59)
                    index += 1
            if(index == 3):
                remarke = msg[L:]
                break

            L = R
            while(L < length and msg[L] == ' '): L += 1
            R = L
            if(L >= length): break
            index += 1

        ret = tools.get_name_and_uuid_by_name(player)
        if ret == None:
            await bot.send(f"未找到玩家{player}")
            return

        BanlistMapper.insert(BanlistUser(ret[1], ret[0], ret[0].low(), unban_date, remarke))
        await bot.send(f"成功封禁玩家{player}")
        