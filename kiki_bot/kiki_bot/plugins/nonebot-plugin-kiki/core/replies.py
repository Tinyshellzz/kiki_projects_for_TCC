from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from pathlib import Path
from ..config.config import *

plugin_dir = str(Path(__file__).resolve().parents[1])

# 入口函数
class ip:
    async def handle(bot: Bot, event: Event):
        # 判断是否是群组事件, 不是就返回
        if not isinstance(event, GroupMessageEvent): return

        user_id = str(event.user_id)
        group_id = str(event.group_id)
        self_id = str(event.self_id)
        
        msg = (f"[CQ:at,qq={user_id}]\n"+
            "【服务器信息-地址】\n" + 
            "-----------\n" + 
            "首选IP:Tcc-mc.com\n" + 
            "备用IP:Mc.tcc-mc.com\n" + 
            "爱坤专用IP:i-kun.love\n" + 
            "-----------\n" + 
            "进不去的可以看群公告更改dns\n" + 
            "-----------\n" + 
            "更多请查阅【TCC玩家手册】\n" + 
            "https://docs.qq.com/aio/DZGZrVFVqTERCTmNn&#34")

        await bot.send_group_msg(group_id=group_id, message=Message(msg))


class fly:
    async def handle(bot: Bot, event: Event):
        user_id = str(event.get_user_id())

        msg = (f"[CQ:at,qq={user_id}]\n"+
            "节假日开启飞行, 命令是/fly")
        await bot.send(event, Message(msg))

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

        if user_id in auth_qq_list:
            msg = (f"[CQ:at,qq={user_id}] \n" +
                    "status\n查看服务器状态\n\n"+
                    "/whitelist update\n将 在数据库 且 在qq群中 的账号全部添加到白名单 (不在的则全部移除白名单)\n\n" +
                    "/whitelist load\n从 excels 文件夹加载审核结果, 并把审核通过的消息发送给候选人\n\n"
            )
        else:
            msg = (f"[CQ:at,qq={user_id}] \n" +
                    "status\n查看服务器状态\n\n"
            )
        await bot.send(event, Message(msg))





