import mcrcon
import re
from .authorization import *
from nonebot.adapters.onebot.v11 import Bot, Event
import json

        
class hi:
    async def handle(bot: Bot, event: Event):
        await bot.send(event,Message((f"川川爱你~")))
        return  