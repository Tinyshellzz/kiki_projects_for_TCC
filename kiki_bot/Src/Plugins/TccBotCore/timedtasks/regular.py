from nonebot import require, get_bots
from nonebot.adapters.onebot.v11 import MessageSegment
from ..config.config import *

mess1 = require("nonebot_plugin_apscheduler").scheduler

print("-------------regular----------------")


@mess1.scheduled_job("cron", hour='00', minute='00', id="messages")
async def messages():
    bot, = get_bots().values()
    for group in auth_group_list:
        await bot.send_msg(
            message_type="group",
            group_id=int(group),
            message='/sign功能已刷新喵!\n快在群内使用/sign来签到获取物品!'
        )
