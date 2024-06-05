from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11 import Bot, Event
import os
import asyncio
from time import sleep

async def send_forward_msg(bot: Bot, event: Event, messages):
    res_id = await bot.call_api("send_forward_msg", group_id=event.group_id, messages=messages)
    print(res_id)
    await bot.send(event, MessageSegment.forward(res_id))

def to_msg_node(msg):
    ret = {
                "type": "node",
                "data": {
                    "name": "KiKi机器人",
                    "uin": "3975252362",
                    "content": [MessageSegment.text(msg)],
                },
        }
    
    return ret
    
def to_image_node(fpath):
    ret = {
                "type": "node",
                "data": {
                    "name": "KiKi机器人",
                    "uin": "3975252362",
                    "content": [MessageSegment.image(fpath)],
                },
        }
    
    return ret

async def get_user_info(bot: Bot, event: Event, user_id):
    return await bot.call_api('get_stranger_info', user_id=user_id)

async def get_nick_name(bot: Bot, event: Event, user_id):
    info = await get_user_info(bot, event, user_id)
    return info.get('nickname')