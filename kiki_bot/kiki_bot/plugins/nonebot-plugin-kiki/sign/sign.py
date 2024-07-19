from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from .SignMapper import SignMapper
import uuid

# 插件命令
sign_cmd = on_command("sign", priority=5)


@sign_cmd.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()

    
    if SignMapper.is_signed(user_id):
        await sign_cmd.finish(f"您今天已经签到过了喵\n请明天中午12.00后再次签到")
    else:
        code = uuid.uuid4().hex[:6]
        SignMapper.insert(SignMapper(user_id, code))
        sign_rank = SignMapper.get_sign_rank(user_id)
        messages = [
            {
                "type": "node",
                "data": {
                    "name": "KiKi机器人",
                    "uin": "3975252362",
                    "content": [MessageSegment.text(f"【提嘻嘻每日签到喵!】\n-----------\n你是今日内第{sign_rank}个签到的\n您的兑换码是{code}!\n在游戏内输入下列指令兑换\n【 /sign {code} 】\n-----------\n本次由用户【{user_id}】唤起!\n注意:兑换码与你的游戏ID绑定,他人无法使用\n快来玩Tcc谢谢喵!!!\n-----------")],
                },
            }
        ]
        res_id = await bot.call_api("send_forward_msg", group_id=event.group_id, messages=messages)
        await bot.send(event, MessageSegment.forward(res_id))