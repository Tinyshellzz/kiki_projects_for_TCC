import requests
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11 import Bot, Event
from ..config.config import *
from PIL import Image, ImageDraw, ImageFont
import os
import time
import threading

background = Image.open(plugin_dir+"/resources/status.png")
font = ImageFont.truetype(plugin_dir+"/resources/YeZiGongChangAoYeHei-2.ttf", 36)
num = 0

def get_uuid_by_name(user_name):
    url = f'https://api.mojang.com/users/profiles/minecraft/{user_name}?'
    response = requests.get(url)
    data = response.json()
    # 不是合法 user_name
    if 'errorMessage' in data: 
        return None
    
    mc_uuid = data['id']
    ret = mc_uuid[0:8] + '-' + mc_uuid[8:12] + '-' + mc_uuid[12:16] + '-' + mc_uuid[16:20] + '-' + mc_uuid[20:]
    return ret

def get_name_and_uuid_by_name(user_name):
    url = f'https://api.mojang.com/users/profiles/minecraft/{user_name}?'
    response = requests.get(url)
    data = response.json()
    # 不是合法 user_name
    if 'errorMessage' in data: 
        return None
    
    mc_uuid = data['id']
    ret = mc_uuid[0:8] + '-' + mc_uuid[8:12] + '-' + mc_uuid[12:16] + '-' + mc_uuid[16:20] + '-' + mc_uuid[20:]
    return (data['name'], ret)

def get_name_by_uuid(uuid):
    uuid = uuid.replace('-', '')
    url = f'https://api.mojang.com/user/profile/{uuid}'
    response = requests.get(url)
    data = response.json()

    # 不是合法 uuid
    if 'errorMessage' in data: 
        return None
    
    user_name = data['name']
    return user_name

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

class no_action:
    async def handle(bot: Bot, event: Event):
        pass

def draw_text_lines(name, text_lines):
    global num

    num = num + 1
    url = plugin_dir + f"/{name}_{num}.png"

    text_start_x = 170
    text_start_y = 390
    text_color = (255, 255, 255)
    line_spacing = 20

    width, height = background.size
    image = Image.new('RGBA', (width, height))
    image.paste(background, (0, 0))
    draw = ImageDraw.Draw(image)

    # 计算字体高度
    text_box = draw.textbbox((0, 0), text_lines[0], font)
    text_height = text_box[3] - text_box[1] 

    # 开始画文本
    for line in text_lines:
        draw.text((text_start_x, text_start_y), line, font=font, fill=text_color)
        text_start_y += text_height + line_spacing
        if text_start_y > height:
            break
    # 保存图片
    image.save(url, 'PNG')
    time.sleep(0.1)

    return url
