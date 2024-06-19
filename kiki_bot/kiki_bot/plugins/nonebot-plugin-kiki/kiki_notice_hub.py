# 集中处理notice事件, 像是退群/加群
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
from nonebot.adapters.onebot.v11.message import Message
from .core.whitelist import *
from .utils import tools
from .database.UserMCMapper import UserMCMapper
from datetime import datetime
import re

matcher=on_notice()

@matcher.handle()
async def _(bot: Bot, event: Event):
    # print(event)
    await GroupIncreaseNotice.handle(bot, event)
    await GroupDecreaseNotice.handle(bot, event)

last_url = None
# 新成员入群处理
class GroupIncreaseNotice:
    async def handle(bot: Bot, event: Event):
        global last_url
        # 判断是否是新成员入群事件
        if not isinstance(event, GroupIncreaseNoticeEvent): return
        if not (str(event.group_id) in auth_group_list): return
        print("-----------------welcome start-------------------")

        current_time = datetime.now()
        current = current_time.strftime("%Y-%m-%d %H:%M:%S")
        nickname = await tools.get_nick_name(bot, event, event.user_id)
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
        
        url = tools.draw_text_lines('welcome', text_lines)
        user_id = str(event.user_id)
        await bot.send_group_msg(group_id=group_id, message=Message(f"[CQ:at,qq={user_id}] [CQ:image,file={url}]"))

        # 将玩家添加到白名单
        mc_user = UserMCMapper.get(str(event.get_user_id()))
        UserMCMapper.add_whitelist(mc_user.id)


class GroupDecreaseNotice:
    async def handle(bot: Bot, event: Event):
        # 判断是否是退群事件
        if not isinstance(event, GroupDecreaseNoticeEvent): return
        if not (str(event.group_id)  in auth_group_list): return
        print("-----------------group leave start-------------------")

        group_id = event.group_id
        
        # await bot.send_group_msg(group_id=group_id, message=Message(f"qq={event.user_id}] 退出群聊"))

        # 删除白名单
        mc_user = UserMCMapper.get(str(event.get_user_id()))
        mc_user = UserMCMapper.get(str(event.get_user_id()))
        UserMCMapper.remove_whitelist(mc_user.id)


