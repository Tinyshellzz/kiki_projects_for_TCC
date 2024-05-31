from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message

# 验证权限
async def auth(bot: Bot, event: Event, user_list=None, group_list=None):
    if not await auth_user(bot, event, user_list): return False
    if not await auth_group(bot, event, group_list): return False
    return True

async def auth_user(bot: Bot, event: Event, user_list):
    if user_list == None: return True

    user_id = str(event.get_user_id())
    if not user_id in user_list: 
        await bot.send(event, Message(f"[CQ:at,qq={user_id}] 喵喵喵,此命令您没有权限使用😭"))
        return False
    return True
    
async def auth_group(bot: Bot, event: Event, group_list):
    if group_list == None: return True
    if not isinstance(event, GroupMessageEvent): return True

    group_id = str(event.group_id)
    user_id = str(event.user_id)
    if not group_id in group_list: 
        await bot.send(event, Message(f"[CQ:at,qq={user_id}] 喵喵喵,此命令在当前聊天中不可用😭"))
        return False
    return True