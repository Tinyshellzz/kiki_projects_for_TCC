from nonebot import on_keyword, on_message
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event
from .kiki_core import replies
from .kiki_core import status
from datetime import datetime
import re

matcher=on_message()
cooldown_dicts = []

match_rules = [
    ['^/{0,1}status$', status, 60],     # [正则, 方法, 冷却(s)]  (会默认调用status.py里面的 handle(bot, event) 方法)
    ['(ip|怎么进服|服务器地址|怎么玩)', replies.ip, 10],
    ['(未知主机|连接超时|dns|连不上|连接失败|连不了)', replies.dns, 10],
    ['(怎么飞|飞行|飞)', replies.fly, 10],
    ['^test$', replies.test, 10],
]


@matcher.handle()
async def _(bot: Bot, event: Event):
    # 这句只是用于测试
    await bot.send(event, "recieve message: " + event.get_message())

    for i in range(len(match_rules)):
        cooldown_dicts.append({})

    msg = str(event.get_message())
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
