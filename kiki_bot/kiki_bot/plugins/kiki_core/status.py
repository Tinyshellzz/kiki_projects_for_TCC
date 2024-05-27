from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Event
from pathlib import Path
from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont
import requests
import json
from .authorization import *

plugin_dir = str(Path(__file__).resolve().parents[1])
background = Image.open(plugin_dir+"/resources/status.png")
font = ImageFont.truetype(plugin_dir+"/resources/YeZiGongChangAoYeHei-2.ttf", 36)
# 授权群组
auth_group_list = {'536038559'}

# 入口函数
async def handle(bot: Bot, event: Event):
    # 进行权限验证
    if not await auth(bot, event, group_list=auth_group_list): return
    # 发送图片
    await send_picture(bot, event)

async def send_picture(bot: Bot, event: Event):
    user_id = event.get_user_id()
    current_time = datetime.now()
    _current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # 文件存储位置
    timestr = time.strftime("%Y%m%d-%H%M%S")
    url = plugin_dir + f"/Output/Output_Serverstatus_{timestr}--{user_id}.png"

    # 获取minecraft状态, 并计算用时
    mc = json.loads(requests.get("http://127.0.0.1:8000/mcstatus/").text)
    program_elapsed_time = round((datetime.now()-current_time).total_seconds()*1000, 2)

    # 要画的文本
    text_lines = [
        f"查询使用的IP: Tcc-mc.com",
        f"在线玩家: {mc['onlinePlayers']}名玩家",
        f"Mc服务器版本: {mc['version']}",
        f"Mc服务器TPS: {mc['tps']}",
        f"Cpu-使用率: {mc['cpu_usage']}",
        f"内存-使用率: {mc['memory_status']}",
        f"带宽-D/U流量: {mc['net_IO']}",
        f"查询使用时间: {mc['queryLatency']}ms",
        f"程序使用时间: {program_elapsed_time}ms",
        "\n",
        f"本次指令由“{user_id}”唤起",
        f"唤起时间: {_current_time}",
    ]
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

    # 发送图片
    await bot.send(event, MessageSegment.image(url))