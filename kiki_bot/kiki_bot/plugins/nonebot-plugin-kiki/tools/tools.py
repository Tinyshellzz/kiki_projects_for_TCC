import requests
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11 import Bot, Event

def get_uuid_by_name(user_name):
    url = f'https://api.mojang.com/users/profiles/minecraft/{user_name}?'
    response = requests.get(url)
    data = response.json()
    # 不是合法 user_name
    if 'errorMessage' in data: 
        return None
    
    mc_uuid = data['id']
    return mc_uuid

def get_name_by_uuid(uuid):
    url = f'https://api.mojang.com/user/profile/{uuid}'
    response = requests.get(url)
    data = response.json()

    # 不是合法 uuid
    if 'errorMessage' in data: 
        return None
    
    user_name = data['name']
    return user_name

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

async def send_forward_msg(bot: Bot, event: Event, messages):
    res_id = await bot.call_api("send_forward_msg", group_id=event.group_id, messages=messages)
    print(res_id)
    await bot.send(event, MessageSegment.forward(res_id))