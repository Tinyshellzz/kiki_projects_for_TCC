from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
import re
from ..database import UserMapper
from ..config.config import *
from .authorization import *
from ..utils import tools

class kick:
    async def handle(bot: Bot, event: Event):
        if not await auth_qq(bot, event, auth_qq_list): return
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        match = re.search('^/{0,1}(踢|kick)(.*$)', msg)

        userbyname = None
        if len(match.groups()) == 2:
            match = match.groups()[1].strip()
            userbyname = UserMapper.get(user_name=match)

        if userbyname != None:
            for g in auth_group_list:
                await bot.set_group_kick(group_id=int(g), user_id=int(userbyname.qq_num))
            UserMapper.update_whitelisted_by_qq(userbyname.qq_num, 'ban')
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 已成功从群聊中移除玩家 {userbyname.display_name}")))
            return

        userbyqq = None
        match = re.search('([0-9]{8,12})', msg)
        if match != None:
            match = match.groups()[0].strip()
            userbyqq = UserMapper.get(qq_num=match)

        if userbyqq != None:
            for g in auth_group_list:
                await bot.set_group_kick(group_id=int(g), user_id=int(userbyqq.qq_num))
            UserMapper.update_whitelisted_by_qq(userbyqq.qq_num, 'ban')
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 已成功从群聊中移除玩家 {userbyqq.display_name}")))
            return
        
        if match == None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 指令格式错误")))
            return
        data = await tools.get_user_info(bot, event, int(match))
        if data == None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 错误, 该玩家不存在")))
        else:
            for g in auth_group_list:
                await bot.set_group_kick(group_id=int(g), user_id=int(match))
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 已成功从群聊中移除玩家 {match}")))
            

