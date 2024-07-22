from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from .SignMapper import SignMapper, SignUser



async def handle(bot: Bot, event: Event):
    print("----------sign start------------")
    user_id = event.get_user_id()
    
    if SignMapper.is_signed(user_id):
        await bot.send(event, f"您今天已经签到过了喵\n请明天凌晨00.00后再次签到")
    else:
        code = SignMapper.generate_code(user_id)
        SignMapper.insert(SignUser(user_id, code))
        sign_rank = SignMapper.get_sign_rank(user_id)
        sign_day = SignMapper.get_sign_day(user_id)
        messages = [
            {
                "type": "node",
                "data": {
                    "name": "KiKi机器人",
                    "uin": "3975252362",
                    "content": [MessageSegment.text(f"【提嘻嘻每日签到喵!】\n-----------\n你是今日内第{sign_rank}个签到的\n这个月共签到了{sign_day+1}次\n您的兑换码是{code}!\n在游戏内输入下列指令兑换\n【 /redeem {code} 】\n-----------\n本次由用户【{user_id}】唤起!\n注意:兑换码与你的游戏ID绑定,他人无法使用\n每天给Bot的主页点10个赞可以增加中奖概率!\n快来玩Tcc谢谢喵!!!\n-----------")],
                },
            }
        ]
        res_id = await bot.call_api("send_forward_msg", group_id=event.group_id, messages=messages)
        await bot.send(event, MessageSegment.forward(res_id))