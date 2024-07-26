import time
from datetime import datetime
from nonebot.adapters.onebot.v11 import MessageEvent, Bot, MessageSegment
from nonebot.plugin import on_command
from ping3 import ping

start_time = datetime.now()

cooldown_dict = {}
botstatus = on_command("ping")


@botstatus.handle()
async def handle_status(bot: Bot, event: MessageEvent):
    now = datetime.now()
    user_id = str(event.user_id)

    # 检查用户是否处于冷却时间内
    if user_id in cooldown_dict:
        last_call = cooldown_dict[user_id]
        time_diff = (now - last_call).total_seconds()
        if time_diff < 20:
            last_time_diff = 20 - int(time_diff)
            await bot.send(event, f"此命令处于冷却中喵，请{last_time_diff}秒后再试")
            return

    def ping_host():
        # 固定的 IP 地址
        ip_address = 'service.mc.tcc-mc.com'
        response = ping(ip_address)
        if response is not None:
            return int(response * 1000)
        else:
            return None
    delay1=ping_host()
    time.sleep(0.1)
    delay2=ping_host()
    time.sleep(0.1)
    delay3=ping_host()
    time.sleep(0.1)
    delay4=ping_host()
    messages = [
        {
            "type": "node",
            "data": {
                "name": "KiKi机器人",
                "uin": "3975252362",
                "content": [MessageSegment.text(
                    f"【Tcc服务器延迟喵!】\n-----------\n第一次测试:{delay1}ms\n第二次测试:{delay2}ms\n第三次测试:{delay3}ms\n第四次测试:{delay4}ms\n-----------\n使用/ping回复None就是Tcc炸了\n-----------")],
            },
        }
    ]
    res_id = await bot.call_api("send_forward_msg", group_id=event.group_id, messages=messages)
    await bot.send(event, MessageSegment.forward(res_id))
    # 如果用户不在冷却时间内，更新最后调用时间为当前时间
    cooldown_dict[user_id] = now
