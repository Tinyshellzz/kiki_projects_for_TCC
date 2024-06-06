# 负责处理简答的回复
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from pathlib import Path
from ..config.config import *
from ..tools.async_tools import *
import requests
import json
from random import randrange

plugin_dir = str(Path(__file__).resolve().parents[1])

# 入口函数
class ip:
    async def handle(bot: Bot, event: Event):
        # 判断是否是群组事件, 不是就返回
        if not isinstance(event, GroupMessageEvent): return

        user_id = str(event.user_id)
        group_id = str(event.group_id)
        self_id = str(event.self_id)
        
        msg = (f"【服务器信息-地址】\n" + 
            "-----------\n" + 
            "首选IP:Tcc-mc.com\n" + 
            "备用IP:Mc.tcc-mc.com\n" + 
            "爱坤专用IP:i-kun.love\n" + 
            "-----------\n" + 
            "进不去的可以看群公告更改dns\n" + 
            "-----------\n" + 
            "更多请查阅【TCC玩家手册】\n" + 
            "https://docs.qq.com/aio/DZGZrVFVqTERCTmNn&#34")

        messages = []
        messages.append(to_msg_node(msg))
        await send_forward_msg(bot, event, messages)


class fly:
    async def handle(bot: Bot, event: Event):
        messages = []
        messages.append(to_msg_node("【服务器指令-飞行】\n-----------\n在游戏对话框输入/fly开/关飞行\n提示:只在节假日和周五晚上开放\n-----------\n更多请查阅【TCC玩家手册】\nhttps://docs.qq.com/aio/DZGZrVFVqTERCTmNn&#34"))
        await send_forward_msg(bot, event, messages)

class dns:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())

        msg = (f"[CQ:at,qq={user_id}]\n"+
            "下面是Win10的教程\n" +
            f"[CQ:image,file={plugin_dir}/resources/dns_win11.png]"+
            "下面是Win11的教程\n" +
            f"[CQ:image,file={plugin_dir}/resources/dns_win11.png]"
            )
        await bot.send(event, Message(msg))

class help:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())

        msg = (f"[CQ:at,qq={user_id}] \n" +
                            "status: 查看服务器状态\n" +
                            "online: 查看在线玩家\n" + 
                            "search 昵称: 找人\n" +
                            "找人 昵称: 找人"
                    )
        if user_id  in auth_qq_list:
            msg = msg + ("\n")
        await bot.send(event, Message(msg))

class online:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        
        response = json.loads(requests.get("http://127.0.0.1:8000/mcstatus/online/").text)
        print(response)
        msg = response['online']

        messages = []
        messages.append(to_msg_node(msg))
        await send_forward_msg(bot, event, messages)

at_self_replies = [
    "找我干嘛！",
    "牡蛎哒哟",
    "亚美蝶",
    "爱你的猫帕瓦",
    "我只是个bot，不要为难人家",
    "装逼我让你飞起来",
    "要不要让你看看什么叫黑手",
    "哈利路大旋风",
    "哈比下",
    "一得阁拉米啊米诺斯",
    "牡蛎莫牡蛎",
    "TD",
    "他宝贝的金刚钻又坏了"
]
class at_self:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())
        print('-------------replies at_self---------------')
        
        msg = at_self_replies[randrange(len(at_self_replies))]
        await bot.send(event, Message(f"[CQ:at,qq={user_id}] {msg}"))




