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
from ..tools.tools import *
import json

def whitelist_insert(qq_num, _user_name):
    name = None
    mc_uuid = None
    try:
        name, mc_uuid = get_name_and_uuid_by_name(_user_name)
    except:
        return False
    if name == None or mc_uuid == None: return False 
    
    UserMapper.insert(User(qq_num, name, mc_uuid, 'true'))

def whitelist_add(user_name):
    UserMapper.update_whitelisted_by_name(user_name, 'true')

def whitelist_remove(user_name):
    UserMapper.update_whitelisted_by_uuid(user_name, None)

def whitelist_delete(user_name):
    UserMapper.delete_by_name(user_name)


# 检查列表里所有的QQ号, 已经数据库中的记录, 据此更改 whitelist
def whitelist_update(qq_nums):
    w = set()
    for n in qq_nums:
        user = UserMapper.get(n)
        if user != None and user.whitelisted == None: 
            UserMapper.update_whitelisted_by_qq(n, 'true')


class sync():
    async def handle(bot: Bot, event: Event):
        users = UserMapper.get_all_user()

        if os.path.exists(server_whitelist):
            whitelist = "["
            
            for user in users:
                whitelist = whitelist + json.dumps({"uuid": user.mc_uuid, "name": user.user_name}) + ','
            
            l = len(whitelist)
            if whitelist[l-1] ==',':
                whitelist = whitelist[:-1] + ']'
            else:
                whitelist = whitelist + ']'

            # 直接将白名单写入 whitelist.json
            with open(server_whitelist, "w") as text_file:
                text_file.write(whitelist)
            
            # reload 使白名单生效
            rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
            try:
                rcon.connect()
                response = rcon.command('whitelist reload')
                logger.info(response)
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
        if UserMapper.exists_qq_id(user_id):
            user = UserMapper.get(qq_num=user_id)
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 老东西，你已经绑定了账号『{user.user_name}』无法重复绑定'))
            return
        if UserMapper.exists_mc_uuid(data.mc_uuid):
            user = UserMapper.get(mc_uuid=data.mc_uuid)
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败:『{data.user_name}』已被『{user.qq_num}』绑定\n如有问题请联系管理员'))
            return
        if data != None:
            # 将玩家添加到数据库, 并添加白名单
            UserMapper.insert(User(user_id, data.user_name, data.mc_uuid))
            whitelist_add(data.user_name)
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] {data.user_name}是吧，我在服务器等你嗷！来了服务器指定没你好果汁吃！'))
        else:
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 验证码有误，请返回服务器检查'))

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

        state = whitelist_remove(user_name)
        if state == False:
            await bot.send(event, Message(f"错误"))
        else:
            await bot.send(event, Message(f"{user_name} 已被移除白名单"))

class add:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return

        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        state = whitelist_add(user_name)
        if state == False:
            await bot.send(event, Message(f"错误"))
        else:
            await bot.send(event, Message(f"{user_name} 已被添加白名单"))

class getbyqq:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        qq_num = msg.split(' ')[2]

        user = UserMapper.get(qq_num)
        if user == None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 该qq没有绑定玩家")))
            return
        await bot.send(event, Message(f"[CQ:at,qq={user_id}]\nqq: {user.qq_num}\n游戏昵称: {user.user_name}\nuuid: {user.mc_uuid}\n备注: {user.user_info}"))


class getbyname:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        user = UserMapper.get(user_name=user_name)
        if user == None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 未找到该玩家qq，请检查id拼写")))
            return
        await bot.send(event, Message(f"[CQ:at,qq={user_id}]\nqq: {user.qq_num}\n游戏昵称: {user.user_name}\nuuid: {user.mc_uuid}\n备注: {user.user_info}"))

class get:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        user_name = msg.split(' ')[1]
        qq_num = msg.split(' ')[1]

        userbyname = UserMapper.get(user_name=user_name)
        userbyqq = UserMapper.get(qq_num)

        if userbyname is None and userbyqq is None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 查无此人，请检查id或者qq是否有误")))
            return
        if userbyname != None:
            await bot.send(event, Message(f"[CQ:at,qq={user_id}]\nqq: {userbyname.qq_num}\n游戏昵称: {userbyname.user_name}\nuuid: {userbyname.mc_uuid}\n备注: {userbyname.user_info}"))
            return
        if userbyqq != None:
            await bot.send(event, Message(f"[CQ:at,qq={user_id}]\nqq: {userbyqq.qq_num}\n游戏昵称: {userbyqq.user_name}\nuuid: {userbyqq.mc_uuid}\n备注: {userbyqq.user_info}"))
            return

# 与remove不同, 删除该玩家的数据库记录
class delete:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return

        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        state = whitelist_delete(user_name)
        if state == False:
            await bot.send(event, Message(f"错误"))
        else:
            await bot.send(event, Message(f"{user_name} 已被删除该玩家"))

# 将玩家插入数据库
class insert:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_user(bot, event, auth_qq_list): return

        msg = str(event.get_message())
        sp = msg.split(' ')
        if len(sp) < 4: 
            bot.send(event, Message(f"参数不足, /whiteliste insert QQ号 游戏昵称"))
        
        qq_num = sp[2]
        user_name = sp[3]

        state = whitelist_insert(qq_num, user_name)
        if state == False:
            await bot.send(event, Message(f"错误"))
        else:
            await bot.send(event, Message(f"{user_name} 已被删除该玩家"))