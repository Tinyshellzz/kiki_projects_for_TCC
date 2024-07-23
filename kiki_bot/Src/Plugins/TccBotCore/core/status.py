from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Event
from pathlib import Path
from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont
import requests
import json
from .authorization import *
import os
from ..config.config import *
from ..utils import tools
import uuid

plugin_dir = str(Path(__file__).resolve().parents[1])
last_url = None


# 入口函数
async def handle(bot: Bot, event: Event):
    # 进行权限验证
    if not await auth_group(bot, event): return
    print("##############status start##############")

    # 发送图片
    await send_picture(bot, event)


async def send_picture(bot: Bot, event: Event):
    global last_url
    user_id = event.get_user_id()
    current_time = datetime.now()
    _current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # 获取minecraft状态, 并计算用时
    try:
        mc = json.loads(requests.get("http://222.187.239.88:8000/mcstatus/").text)
    except:
        mc = json.loads(requests.get("http://127.0.0.1:8000/mcstatus/").text)
    print(mc)
    program_elapsed_time = round((datetime.now() - current_time).total_seconds() * 1000, 2)

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

    url = tools.draw_text_lines('status', text_lines)

    # 发送图片
    await bot.send(event, Message(f"[CQ:image,file={url}]"))
