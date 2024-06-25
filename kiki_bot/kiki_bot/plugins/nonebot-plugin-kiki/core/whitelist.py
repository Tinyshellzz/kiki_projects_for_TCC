import mcrcon
import re
from ..config.config import *
from nonebot.adapters.onebot.v11 import Bot
from ..database.CodeMCMapper import CodeMCMapper
from nonebot.adapters.onebot.v11 import Bot, Event
from .authorization import *
from ..database.UserMapper import User, UserMapper
from ..database.UserMCMapper import MCUser, UserMCMapper
from ..database.BanlistMapper import BanlistMapper, BanlistUser
from ..database.InvitationMapper import InvitationMapper
from ..database.ReadExcel import *
from ..utils import tools
import json
from ..utils.MyException import MyException
import datetime


# 展示user
async def dispaly_user(bot: Bot, event: Event, user: MCUser):
    user_id = str(event.get_user_id())
    ban_user: BanlistUser = BanlistMapper.get_user_by_mc_uuid(user.mc_uuid)
    if ban_user != None and ban_user.unban_date > datetime.datetime.now():
        messages = [tools.to_msg_node(f"qq: {user.qq_num}\n游戏昵称: {user.display_name}\n上次登录: {user.last_login_time}\n封禁理由: {ban_user.reason}\n解封时间: {ban_user.unban_date}")]
        await tools.send_forward_msg(bot, event, messages)
    else:
        messages = [tools.to_msg_node(f"qq: {user.qq_num}\n游戏昵称: {user.display_name}\n上次登录: {user.last_login_time}\n备注: {user.remark}")]
        await tools.send_forward_msg(bot, event, messages)


# 检查列表里所有的QQ号, 已经数据库中的记录, 据此更改 whitelist
def whitelist_update(qq_nums):
    w = set()
    for n in qq_nums:
        user = UserMCMapper.get(n)
        if user != None: 
            UserMCMapper.add_whitelist(user.id, True)


# class sync():
#     async def handle(bot: Bot, event: Event):
#         users = UserMCMapper.get_all_user()

#         if os.path.exists(server_whitelist):
#             whitelist = "["
            
#             for user in users:
#                 whitelist = whitelist + json.dumps({"uuid": user.mc_uuid, "name": user.user_name}) + ','
            
#             l = len(whitelist)
#             if whitelist[l-1] ==',':
#                 whitelist = whitelist[:-1] + ']'
#             else:
#                 whitelist = whitelist + ']'

#             # 直接将白名单写入 whitelist.json
#             with open(server_whitelist, "w") as text_file:
#                 text_file.write(whitelist)
            
#             # reload 使白名单生效
#             rcon = mcrcon.MCRcon(server_ip, rcon_password, rcon_port, timeout=2)
#             try:
#                 rcon.connect()
#                 response = rcon.command('whitelist reload')
#                 logger.info(response)
#             except Exception as e:
#                 logger.warning(e)
#             finally:
#                 rcon.disconnect()


# mc的白名单验证码
class code:
    async def handle(bot: Bot, event: Event):
        if not await auth_group(bot, event): return
        print('####################whitelist code start########################')
        user_id = str(event.get_user_id())

        # 获取验证码
        msg = str(event.get_message())
        # code = msg[-6:]
        code = re.search('^.*' + code_prefix + '([0-9a-zA-Z]{6}).*$', msg)
        code = code.groups()[0].lower()

        # 从验证码数据库获取验证码数据
        data = CodeMCMapper.get(code)

                
        if data != None:
            if UserMCMapper.exists_qq_num(user_id):
                user = UserMCMapper.get(qq_num=user_id)
                if user.mc_uuid != data.mc_uuid:
                    await bot.send(event, Message(f'[CQ:at,qq={user_id}] 老东西，你已经绑定了账号『{user.display_name}』无法重复绑定'))
                    return
                else:
                    UserMCMapper.add_whitelist(user.id)
                    await bot.send(event, Message(f'[CQ:at,qq={user_id}]『{data.display_name}』是吧，我在服务器等你嗷！来了服务器指定没你好果汁吃！'))
                    return
            if UserMCMapper.exists_mc_uuid(data.mc_uuid):
                user = UserMCMapper.get(mc_uuid=data.mc_uuid)
                if user.qq_num != user_id:
                    await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败:『{data.user_name}』已被『{user.qq_num}』绑定\n如有问题请联系管理员'))
                    return
                else:
                    UserMCMapper.add_whitelist(user.id)
                    await bot.send(event, Message(f'[CQ:at,qq={user_id}]『{data.display_name}』是吧，我在服务器等你嗷！来了服务器指定没你好果汁吃！'))
                    return
            # 不存在数据库记录, 则将将玩家添加到数据库
            id = None
            email = user_id + "@qq.com"
            if(UserMapper.exits_email(email=email)):
                user = UserMapper.get_user_by_email(email)
                id = user.id
            else:
                id = UserMapper.insert(User(email=email, permission=2))
            mc_user = MCUser(id, user_id, data.user_name, data.display_name, data.mc_uuid, datetime.datetime.now())
            UserMCMapper.insert(mc_user)
            UserMCMapper.add_whitelist(mc_user.id)
            await bot.send(event, Message(f'[CQ:at,qq={user_id}]『{data.display_name}』是吧，我在服务器等你嗷！来了服务器指定没你好果汁吃！'))
        else:
            if UserMCMapper.exists_qq_num(user_id):
                user = UserMCMapper.get(qq_num=user_id)
                await bot.send(event, Message(f'[CQ:at,qq={user_id}] 老东西，你已经绑定了账号『{user.display_name}』无法重复绑定'))
            else:
                await bot.send(event, Message(f'[CQ:at,qq={user_id}] 验证码有误，请返回服务器检查'))

# 更新服务器的白名单
class update:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_qq(bot, event): return

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
        if not await auth_qq(bot, event): return
        
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
        if not await auth_qq(bot, event): return

        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        mc_user = UserMCMapper.get(user_name=user_name)
        if mc_user == None:
            await bot.send(event, Message(f"{user_name} 玩家不存在"))
        UserMCMapper.remove_whitelist(mc_user.id)
        await bot.send(event, Message(f"{user_name} 已被移除白名单"))

class add:
    async def handle(bot: Bot, event: Event):
        # 设置使用权限
        if not await auth_qq(bot, event): return

        msg = str(event.get_message())
        user_name = msg.split(' ')[2]

        mc_user = UserMCMapper.get(user_name=user_name)
        if mc_user:
            await bot.send(event, Message(f"{user_name} 玩家不存在"))
        UserMCMapper.add_whitelist(mc_user.id)
        await bot.send(event, Message(f"{user_name} 已被添加白名单"))

class get:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        print(msg)
        
        match = re.search('^/{0,1}(找人|search)(.+$)', msg)
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
            await dispaly_user(bot, event, userbyname)
            return
        if userbyqq != None:
            await dispaly_user(bot, event, userbyqq)
            return      

# 邀请好友
class invite:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())

        msg = str(event.get_message())
        sp = msg.split(' ')
        if len(sp) < 3: 
            bot.send(event, Message(f"参数不足, /invite QQ号 游戏昵称"))
        
        qq_num = sp[1]
        user_name = sp[2].lower()

        inviter = UserMapper.get_user_by_email(user_id + "@qq.com")
        if inviter == None or inviter.permission < 2:
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 你没有邀请权限'))
            return
        if InvitationMapper.get_times(user_id) >= 3:
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 你的邀请次数已用完'))
            return
        if not UserMCMapper.exists_id(inviter.id):
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 你还未加入游戏'))
            return
        if UserMCMapper.exists_qq_num(qq_num):
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败: QQ『qq_num』已被绑定'))
            return
        if UserMCMapper.exists_mc_uuid(user_name):
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败: 用户『user_name』已被绑定'))
            return
        
        ret = tools.get_name_and_uuid_by_name(user_name)
        if ret == None:
            await bot.send(event, Message(f'[CQ:at,qq={user_id}] 绑定失败: 用户名『user_name』不存在'))
            return
        (display_name, mc_uuid) = ret

        # 不存在数据库记录, 则将将玩家添加到数据库
        id = None
        email = qq_num + "@qq.com"
        if(UserMapper.exits_email(email=email)):
            user = UserMapper.get_user_by_email(email)
            id = user.id
        else:
            id = UserMapper.insert(User(email=email, permission=1))
        mc_user = MCUser(id, qq_num, user_name, display_name, mc_uuid, datetime.datetime.now())
        UserMCMapper.insert(mc_user)
        InvitationMapper.insert(mc_user.id, inviter.id)
        await bot.send(event, Message(f'[CQ:at,qq={user_id}]『{display_name}』已被邀请成功'))


class relation:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        msg = str(event.get_message())
        print(msg)
        
        match = re.search('^/{0,1}(relation|关系)(.+$)', msg)
        user = None
        if len(match.groups()) == 2:
            match = match.groups()[1].strip()
            print(match)
            user = UserMCMapper.get(user_name=match)

        if user == None:
            match = re.search('([0-9]{8,12})', msg)
            if match != None:
                match = match.groups()[0].strip()
                user = UserMCMapper.get(qq_num=match)

        if user is None:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 查无此人, 请检查id或者qq是否有误")))
            return
        
        res = InvitationMapper.get_relations(user.id)
        if res == None or len(res) < 2:
            await bot.send(event, Message((f"[CQ:at,qq={user_id}] 该用户不存在邀请信息")))
            return
        
        msg = f"[CQ:at,qq={user_id}] 『{res[0].display_name}』邀请了："
        for i in range(1, len(res)):
            msg += f"『{res[i].display_name}』"
            msg += ","
        if msg[len(msg) - 1] == ',': 
            msg = msg[:-1]

        await bot.send(event, Message(msg))



class remarke:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        print('-------------replies remarke---------------')

        msg = str(event.get_message())
        splite = msg.split(' ')
        if len(splite) == 2:
            user = UserMCMapper.get(user_id)
            if user != None:
                # if user.user_info != None and user.user_info != '无':
                #     if user_id in auth_qq_list:
                #         UserMCMapper.update_remark_by_qq(user_id, splite[1])
                #         await bot.send(event, Message((f"[CQ:at,qq={user_id}] {user.display_name} 的备注已设置为 {splite[1]}")))
                #     else:
                #         await bot.send(event, Message((f"[CQ:at,qq={user_id}] 错误, 你只有已经设置过备注")))
                # else:
                    remake = ""
                    for i in range(1, len(splite)): 
                        remake += splite[i]
                    if len(splite[1].encode('utf-8')) > 100:
                        await bot.send(event, Message((f"[CQ:at,qq={user_id}] 备注过长, 30字以内")))
                        return
                    UserMCMapper.update_remark_by_qq(user_id, remake)
                    await bot.send(event, Message((f"[CQ:at,qq={user_id}] {user.display_name} 的备注已设置为 {splite[1]}")))
            else:
                await bot.send(event, Message((f"[CQ:at,qq={user_id}] 你还没有绑定白名单")))
        else:
            if user_id in auth_qq_list:
                user = UserMCMapper.get(user_name=splite[1])
                if user == None:
                    user = UserMCMapper.get(qq_num=splite[1])
                if user == None:
                    await bot.send(event, Message((f"[CQ:at,qq={user_id}] 错误, 未找到此人")))
                    return
                
                user.remark = ""
                for i in range(2, len(splite)):
                    user.remark += splite[i]
                UserMCMapper.update_remark_by_qq(user.qq_num, user.remark)
                await bot.send(event, Message((f"[CQ:at,qq={user_id}] {user.display_name} 的备注已设置为 {splite[2]}")))