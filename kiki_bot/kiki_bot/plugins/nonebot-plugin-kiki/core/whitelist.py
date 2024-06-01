import mcrcon
import re
from ..config.config import *
from nonebot.adapters.onebot.v11 import Bot
from ..database.UserMapper import UserMapper
from ..database.WhitelistCodeMapper import WhitelistCodeMapper
from nonebot.adapters.onebot.v11 import Bot, Event
from .authorization import *
from ..database.User import User
from ..database.ReadExcel import *

def whitelist_get_players():
    players = None
    rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
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
    rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
    try:
        rcon.connect()
        response = rcon.command(f'whitelist add {user_name}')
        logger.info(response)
        rcon.command(f'whitelist reload')
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()

def whitelist_remove(user_name):
    if user_name == None: return
    rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
    try:
        rcon.connect()
        response = rcon.command(f'whitelist remove {user_name}')
        logger.info(response)
        rcon.command(f'whitelist reload')
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()


# 检查列表里所有的QQ号, 已经数据库中的记录, 据此更改 whitelist
def whitelist_update(qq_nums):
    rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
    try:
        rcon.connect()
        # 新的 whitelist
        new_whitelist = set()
        
        for n in qq_nums:
            user = UserMapper.get(n)
            if user != None and user.is_banned == None: new_whitelist.add(user.user_name)
        
        whitelist = whitelist_get_players()

        for p in whitelist:
            if not (p in new_whitelist):
                whitelist_remove(p)

        # 将不在服务器白名单的QQ号, 加入白名单
        for p in new_whitelist: 
            if not (p in whitelist):
                response = rcon.command(f'whitelist remove {p}')
                logger.info(response)
        
        rcon.command(f'whitelist reload')

    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()

# mc的白名单验证码
class code:
    async def handle(bot: Bot, event: Event):
        if not await auth_group(bot, event, auth_group_list): return
        user_id = str(event.get_user_id())

        # 获取验证码
        msg = str(event.get_message())
        code = msg[-6:]

        # 从验证码数据库获取数据
        data = WhitelistCodeMapper.get(code)
        print(data)
        if data != None:
            if UserMapper.exists_mc_uuid(data.mc_uuid):
                await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败: {data.user_name} 的mc账号已被绑定'))
                return
            if UserMapper.exists_qq_id(user_id):
                await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败: 你的qq已被绑定'))
                return

            # 将玩家添加到数据库, 并添加白名单
            UserMapper.insert(User(user_id, data.user_name, data.mc_uuid))
            whitelist_add(data.user_name)
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] {data.user_name}绑定成功'))
        else:
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 验证码错误'))
            

# 更新服务器的白名单
class update:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return

        qq_nums = set()
        for group_id in auth_group_list:
            l = await bot.get_group_member_list(group_id=group_id)
            for q in l:
                qq_nums.add(str(q['user_id']))
        
        whitelist_update(qq_nums)
        await bot.send(event, Message(f"白名单更新成功"))

class load:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return
        
        # 向所有通过审核的人发送通知
        players = read_excels()
        for p in players:
            await bot.send_private_msg(user_id=p['qq_num'], message="你已通过TCC审核")

        await bot.send(event, Message(f"excel 读取成功"))


class remove:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return

        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        whitelist_remove(user_name)

        await bot.send(event, Message(f"{user_name} 已被移除白名单"))
