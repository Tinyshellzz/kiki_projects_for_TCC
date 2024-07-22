# 集中处理各种消息事件
from nonebot import on_message
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event
from .core import replies
from .core import status
from .core import group
from .core import whitelist
from .core import userService
from .core import heChuan
from datetime import datetime
from .config.config import *
from .core import server
import re
from .utils import transfer_db
from .utils import tools
from .sign import sign
from .timedtasks.regular import *
matcher=on_message()
cooldown_dicts = []

# pip install pymysql-pool pymysql mcrcon pandas mcstatus psutil cryptography pillow
# [正则, 方法, 冷却(s)]  (会默认调用status.py里面的 handle(bot, event) 方法)
match_rules = [
    ['^test$', tools.no_action, 0],
    ['^/{0,1}(help|帮助)$', replies.help, 10],                   # 帮助
    ['^/{0,1}status$', status, 10],                              # 查看服务器状态
    ['^/{0,1}ban (.*)$', server.ban, 0],                         # 封禁玩家
    ['^/{0,1}unban (.*)$', server.unban, 0],                     # 解封玩家
    ['^/{0,1}whitelist update$', whitelist.update, 0],           # 将 在数据库 且 在qq群中 的账号全部添加到白名单
    # ['^/whitelist sync$', whitelist.sync, 0],                 # 同步minecraft官方的白名单
    ['^/{0,1}whitelist load$', whitelist.load, 0],               # 从 excels 文件夹加载审核结果
    ['^/{0,1}whitelist remove .*$', whitelist.remove, 0],        # 从白名单移除玩家
    ['^/{0,1}whitelist add .*$', whitelist.add, 0],              # 添加玩家到白名单
    # ['^/{0,1}mcuser (insert|bind) .*$', whitelist.insert, 0],    # 将玩家插入数据库
    ['^/{0,1}user delete .*$', userService.delete, 0],            # 从数据库将玩家删除
    ['^/{0,1}(找人|search).*$', whitelist.get, 0],                # 万能查询
    ['^/{0,1}(备注|remarke).+$', whitelist.remarke, 0],           # 添加备注
    ['^/{0,1}(邀请|invite).+$', whitelist.invite, 0],               # 邀请自己的好友, 封禁的时候会一起封禁, 一个人只能邀请3人
    ['^/{0,1}(relation).+$', whitelist.relation, 0],               # 查看邀请关系
    ['^/{0,1}(添加关系).+$', whitelist.add_relation, 0],             # 添加邀请关系
    # ['^/{0,1}(踢|kick).+$', group.kick, 0],                       # 移出群聊
    ['^川川$', heChuan.hi, 0],                                      # 川川
    ['^/{0,1}red$', sign, 0],                                      # 签到功能
    ['^online$', replies.online, 0],                                # 查看在线晚间
    ['^.*' + code_prefix + '[0-9a-zA-Z]{6}.*$', whitelist.code, 10],   # 白名单验证码
    ['(3975252362)', replies.at_self, 10],                      # 艾特回复
    ['(怎么进服|服务器地址|怎么玩)', replies.ip, 10],
    ['(未知主机|连接超时|dns|连不上|连接失败|连不了)', replies.dns, 10], #DNS
    ['(怎么飞|飞行)', replies.fly, 10],
]


@matcher.handle()
async def _(bot: Bot, event: Event):
    # await bot.send(event, Message("received message: " + str(event.get_message())))

    for i in range(len(match_rules)):
        cooldown_dicts.append({})

    log = event.get_log_string()
    msg = re.search('\'(.+)\'', log)
    msg = msg.groups()[0]
    # print(msg)
    for i in range(len(match_rules)):
        rule = match_rules[i]
        if re.search(rule[0], msg) != None:
            if await cooldown(bot, event, rule[2], i):
                await rule[1].handle(bot, event)
            break

# 各个命令的冷却时间
async def cooldown(bot: Bot, event: Event, cooldown_time, i):
    cooldown_dict = cooldown_dicts[i]

    current_time = datetime.now()
    user_id = str(event.user_id)
    # 判断用户在不在冷却时间
    if user_id in cooldown_dict:
        last_call = cooldown_dict[user_id]
        time_diff = (current_time - last_call).total_seconds()
        if time_diff < cooldown_time:
            last_time_diff = int(cooldown_time - int(time_diff))
            await bot.send(event, Message(f"[CQ:at,qq={user_id}] 诶,我也是需要休息的,请{last_time_diff}秒后再试吧😘"))
            return False
    cooldown_dict[user_id] = current_time
    return True
