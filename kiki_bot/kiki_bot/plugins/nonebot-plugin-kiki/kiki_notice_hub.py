# 集中处理notice事件, 像是退群/加群
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
from nonebot.adapters.onebot.v11.message import Message
from .core.whitelist import *
from .tools.async_tools import *
from .database import UserMapper
from datetime import datetime
import re

matcher=on_notice()

@matcher.handle()
async def _(bot: Bot, event: Event):
    # print(event)
    await GroupIncreaseNotice.handle(bot, event)
    await GroupDecreaseNotice.handle(bot, event)

# 新成员入群处理
class GroupIncreaseNotice:
    async def handle(bot: Bot, event: Event):
        # 判断是否是新成员入群事件
        if not isinstance(event, GroupIncreaseNoticeEvent): return
        if not (str(event.group_id) in auth_group_list): return
        print("-----------------welcome start-------------------")

        current_time = datetime.now()
        current = current_time.strftime("%Y-%m-%d %H:%M:%S")
        nickname = await get_nick_name(bot, event, event.user_id)
        text_lines = [
            f"@新同学 {nickname}",
            f"\n",
            f"~欢迎新同学加入咱Tcc服务器~",
            f"~请查看群内公告填写审核表呀~",
            f"~别忘记给我们的宣传片三连噢~",
            f"~审核务必详细阅读玩家手册~",
            f"~我们的官方网页:Tcc-mc.com~",
            f"\n",
            f"生成时间:{current}",
        ]

        # 进入的群号
        group_id = event.group_id
        
        url = draw_text_lines('welcome', text_lines)
        user_id = str(event.user_id)
        await bot.send_group_msg(group_id=group_id, message=Message(f"[CQ:at,qq={user_id}] [CQ:image,file={url}]"))

        # 将玩家添加到白名单
        user_name = UserMapper.get(str(event.get_user_id()))
        whitelist_add(user_name)
        sleep(1)
        os.remove(url)



class GroupDecreaseNotice:
    async def handle(bot: Bot, event: Event):
        # 判断是否是退群事件
        if not isinstance(event, GroupDecreaseNoticeEvent): return
        if not (str(event.group_id)  in auth_group_list): return
        print("-----------------group leave start-------------------")

        group_id = event.group_id
        
        # await bot.send_group_msg(group_id=group_id, message=Message(f"qq={event.user_id}] 退出群聊"))

        # 删除白名单
        user_name = UserMapper.get(str(event.get_user_id()))
        whitelist_remove(user_name)


