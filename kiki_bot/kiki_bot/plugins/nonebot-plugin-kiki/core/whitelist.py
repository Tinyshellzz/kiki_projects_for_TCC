import mcrcon
import re
from ..config.config import *
from nonebot.adapters.onebot.v11 import Bot
from ..database.UserMapper import UserMapper
from nonebot.adapters.onebot.v11 import Bot, Event
from .authorization import *

def whitelist_get_players():
    players = None
    try:
        rcon.connect()
        response = rcon.command('whitelist list')
        match = re.search('.*: (.*)', response)
        if match == None: return
        match = match.groups()[0]
        res = match.split(', ')
        players = set(res)
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()

    return players

def whitelist_add(user_name):
    if user_name == None: return

    try:
        rcon.connect()
        response = rcon.command(f'whitelist add {user_name}')
        logger.info(response)
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()

def whitelist_remove(user_name):
    if user_name == None: return

    try:
        rcon.connect()
        response = rcon.command(f'whitelist remove {user_name}')
        logger.info(response)
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()

def whitelist_reload():
    try:
        rcon.connect()
        rcon.command(f'whitelist reload')
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()

# 检查列表里所有的QQ号, 已经数据库中的记录, 据此更改 whitelist
def whitelist_update(qq_nums):
    # 新的 whitelist
    new_whitelist = set()
    
    for n in qq_nums:
        user = UserMapper.get(n)
        if user != None: new_whitelist.add(user.user_name)
    
    whitelist = whitelist_get_players()
    # 移除不在数据库中的 QQ 号, 谨慎处理
    # for p in whitelist:
    #     if not (p in new_whitelist):
    #         whitelist_remove(p)

    for p in new_whitelist: 
        if not (p in whitelist):
            whitelist_add(p)
    
    whitelist_reload()

# 添加白名单
class add:
    async def handle(bot: Bot, event: Event):
        pass

# 跟新服务器的白名单
class update:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        auth_user(bot, event, auth_qq_list)

        qq_nums = set()
        for group_id in auth_group_list:
            l = await bot.get_group_member_list(group_id=group_id)
            for q in l:
                qq_nums.add(str(q['user_id']))
        
        print(qq_nums)
        whitelist_update(qq_nums)