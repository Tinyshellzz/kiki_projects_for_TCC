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
from threading import Lock
import json

lock = Lock()

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
    with lock:
        if user_name == None: return
        print(rconPw)
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
    with lock:
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

def whitelist_reload():
    rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
    try:
        rcon.connect()
        rcon.command(f'whitelist reload')
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()


# 检查列表里所有的QQ号, 已经数据库中的记录, 据此更改 whitelist
def whitelist_update(qq_nums):
    w = set()
    for n in qq_nums:
        user = UserMapper.get(n)
        if user != None and user.is_banned == None: w.add(user)

    with lock:
        if os.path.exists(server_whitelist):
            whitelist = "["
            
            for user in w:
                whitelist = whitelist + json.dumps({"uuid": user.mc_uuid, "name": user.user_name}) + ','
            
            l = len(whitelist)
            if whitelist[l-1] ==',':
                whitelist = whitelist[:-1] + ']'
            else:
                whitelist = whitelist + ']'

            # 直接将白名单写入 whitelist.json
            with open(server_whitelist, "w") as text_file:
                text_file.write(whitelist)
            
            whitelist_reload()
        else:
            # 新的 whitelist
            new_whitelist = set()
            
            for user in w:
                new_whitelist.add(user.user_name)
            rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
            try:
                rcon.connect()
                
                whitelist = whitelist_get_players()

                # 将不在服务器白名单的QQ号, 加入白名单
                for p in new_whitelist: 
                    if not (p in whitelist):
                        response = rcon.command(f'whitelist add {p}')
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
        # code = msg[-6:]
        code = re.search(code_prefix + '([0-9a-zA-Z]{6})', msg)
        code = code.groups()[0].lower()

        # 从验证码数据库获取数据
        data = WhitelistCodeMapper.get(code)
        print(data)
        if data != None:
            if UserMapper.exists_mc_uuid(data.mc_uuid):
                user = UserMapper.get(mc_uuid=data.mc_uuid)
                await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败: \n{data.user_name} 的mc账号已被 {user.qq_num} 绑定\n如有问题请联系管理员'))
                return
            if UserMapper.exists_qq_id(user_id):
                user = UserMapper.get(qq_num=user_id)
                await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败: \n你的qq已被 {user.user_name} 绑定\n如有问题请联系管理员'))
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

        await bot.send(event, Message(f"白名单更新中...(耗时可能较长)"))
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
        
        await bot.send(event, Message(f"excel 读取中... (耗时较长)"))
        # 向所有通过审核的人发送通知
        players = read_excels()
        for p in players:
            # await bot.send_private_msg(user_id=p['qq_num'], message="你已通过TCC审核")
            pass

        await bot.send(event, Message(f"excel 读取成功"))


class remove:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return

        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        whitelist_remove(user_name)

        await bot.send(event, Message(f"{user_name} 已被移除白名单"))

class add:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return

        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        whitelist_add(user_name)

        await bot.send(event, Message(f"{user_name} 已被添加白名单"))

class getqq:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        qq_num = msg.split(' ')[2]

        user = UserMapper.get(qq_num)
        if user == None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 未找到找到该qq")))
            return
        await bot.send(event, Message(f"[CQ:at,qq={user_id}]\nqq: {user.qq_num}\n游戏昵称: {user.user_name}\nuuid: {user.mc_uuid}\n备注: {user.user_info}"))

class getname:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        user = UserMapper.get(user_name=user_name)
        if user == None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 未找到找到该玩家")))
            return
        await bot.send(event, Message(f"[CQ:at,qq={user_id}]\nqq: {user.qq_num}\n游戏昵称: {user.user_name}\nuuid: {user.mc_uuid}\n备注: {user.user_info}"))
