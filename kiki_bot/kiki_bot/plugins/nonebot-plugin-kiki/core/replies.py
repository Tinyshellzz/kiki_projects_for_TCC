# 负责处理简答的回复
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from pathlib import Path
from ..config.config import *
from ..tools.tools import *
import json

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
            "下面是教程\n" +
            f"[CQ:image,file={plugin_dir}/resources/status.png]")
        await bot.send(event, Message(msg))

class help:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())

        msg = (f"[CQ:at,qq={user_id}] \n" +
                            "status: 查看服务器状态\n"
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





