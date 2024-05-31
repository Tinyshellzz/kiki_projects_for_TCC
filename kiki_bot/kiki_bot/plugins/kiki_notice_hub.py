from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent
from nonebot.adapters.onebot.v11.message import Message
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