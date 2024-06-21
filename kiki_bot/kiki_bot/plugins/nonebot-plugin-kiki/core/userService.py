from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from ..database.UserMapper import User, UserMapper
from ..database.UserMCMapper import MCUser, UserMCMapper
from ..database.BanlistMapper import BanlistMapper, BanlistUser
import re

class delete:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        print(msg)
        
        match = re.search('^/{0,1}(user) delete(.*$)', msg)
        userbyname = None
        if len(match.groups()) == 2:
            match = match.groups()[1].strip()
            userbyname = UserMCMapper.get(user_name=match)

        userbyqq = None
        match = re.search('([0-9]{8,12})', msg)
        if match != None:
            match = match.groups()[0].strip()
            userbyqq = UserMCMapper.get(qq_num=match)

        if userbyname is None and userbyqq is None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 查无此人, 请检查id或者qq是否有误")))
            return
        if userbyname != None:
            UserMCMapper.remove_whitelist(userbyname.id)
            UserMCMapper.delete_by_qq(userbyname.qq_num)
            UserMapper.delete_by_email(userbyname.qq_num + "@qq.com")
            return
        if userbyqq != None:
            UserMCMapper.remove_whitelist(userbyqq.id)
            UserMCMapper.delete_by_qq(userbyqq.qq_num)
            UserMapper.delete_by_email(userbyqq.qq_num + "@qq.com")
            return   