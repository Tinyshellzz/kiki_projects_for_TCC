from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
from nonebot.adapters.onebot.v11.message import Message
from .core.whitelist import *
from .database.UserMapper import UserMapper
import re

matcher=on_notice()

@matcher.handle()
async def _(bot: Bot, event: Event):
    # print(event)
    await GroupIncreaseNotice.handle(bot, event)

# 新成员入群处理
class GroupIncreaseNotice:
    async def handle(bot: Bot, event: Event):
        # 判断是否是新成员入群事件
        if not isinstance(event, GroupIncreaseNoticeEvent): return

        # 进入的群号
        group_id = event.group_id
        
        await bot.send_group_msg(group_id=group_id, message=Message(f"[CQ:at,qq={event.user_id}] 欢迎入群"))

        # 将玩家添加到白名单
        user_name = UserMapper.get(str(event.get_user_id()))
        whitelist_add(user_name)


class GroupDecreaseNotice:
    async def handle(bot: Bot, event: Event):
        # 判断是否是退群事件
        if not isinstance(event, GroupDecreaseNoticeEvent): return

        group_id = event.group_id
        
        await bot.send_group_msg(group_id=group_id, message=Message(f"qq={event.user_id}] 退出群聊"))

        # 删除白名单
        user_name = UserMapper.get(str(event.get_user_id()))
        whitelist_remove(user_name)
