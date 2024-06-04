# 集中处理加群请求
from nonebot import on_request
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import GroupRequestEvent
import re
from .database import UserMapper
from .config.config import *

matcher=on_request()

@matcher.handle()
async def _(bot: Bot, event: Event):
    # print(event)
    await GroupRequest.handle(bot, event)

# 入群申请处理
class GroupRequest:
    async def handle(bot: Bot, event: Event):
        # 判断是否是加群事件
        if not isinstance(event, GroupRequestEvent): return
        # 不在目标群
        group_id = event.group_id
        if not (group_id in auth_group_list): return
        
        # 入群验证的答案
        answer = re.search(".*答案：(.*)", event.comment)
        answer = answer.groups()[0]

        # 申请者的QQ号
        user_id = event.get_user_id()
        # QQ号再数据库中, 就同意入群
        if UserMapper.exists_qq_id(user_id):
            await bot.set_group_add_request(flag = event.flag, approve=True)
        else:
            # False拒绝申请, True就是同意
            await bot.set_group_add_request(flag = event.flag, approve=True, reason='答案错误')
        