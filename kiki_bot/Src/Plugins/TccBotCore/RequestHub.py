# 集中处理加群请求
from nonebot import on_request
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import GroupRequestEvent
import re
from .database.UserMCMapper import UserMCMapper
from .database.BanlistMapper import BanlistMapper
from .database.InvitationMapper import InvitationMapper
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
        if not (str(group_id) in auth_group_list): return
        
        # 入群验证的答案
        answer = re.search(".*答案：(.*)", event.comment)
        answer = answer.groups()[0]

        # 申请者的QQ号
        user_id = str(event.get_user_id())
        # QQ号再数据库中
        if UserMCMapper.exists_qq_id(user_id):
            user = UserMCMapper.get(user_id)
            # 拒绝, 被封禁的玩家
            if BanlistMapper.exists_mc_uuid(user.mc_uuid):
                await bot.set_group_add_request(flag = event.flag, approve=False, reason='你已被封禁, 不允许加入该群')
                return
            # 同意, 被邀请的玩家
            if InvitationMapper.exists_id(user.id):
                await bot.set_group_add_request(flag = event.flag, approve=True)
        else:
            # False拒绝申请, True就是同意
            pass
            # await bot.set_group_add_request(flag = event.flag, approve=False, reason='答案错误')
        