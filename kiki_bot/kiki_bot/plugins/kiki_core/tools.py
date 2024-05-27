from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

def to_node(msg: Message):
    return {"type": "node", "data": {"name": "奏酱", "uin": "3135965324", "content": msg}}

# 没有效果
async def send_group_forword_msg(bot: Bot, event: GroupMessageEvent, messages):
    await bot.call_api(
        "send_group_forward_msg", groud_id=event.group_id, messages=messages
    )