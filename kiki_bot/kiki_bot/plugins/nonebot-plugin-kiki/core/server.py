from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import mcrcon
import re
from ..config.config import *
from .authorization import *
from ..database import UserMapper

def excute(command):
    rcon = mcrcon.MCRcon(serIP, rconPw, rconPort, timeout=2)
    response  = None
    try:
        rcon.connect()
        response = rcon.command(command)
        logger.info(response)
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()

    return response

class ban:
    async def handle(bot: Bot, event: Event):
        if not await auth_user(bot, event): return
        print('------------server ban-------------')
        msg = str(event.get_message())
        
        match = re.search('^/ban (.*)$', msg)
        command = match.groups()[0]
        name = command.split(' ')[0]

        response = excute(f'ban {command}')
        UserMapper.update_whitelisted_by_name(name, "ban")

        await bot.send(event, Message(f'{response}--完成'))

class unban:
    async def handle(bot: Bot, event: Event):
        if not await auth_user(bot, event): return
        msg = str(event.get_message())
        
        user_name = re.search('^/unban (.*)$', msg)
        user_name = user_name.groups()[0]

        response = excute(f'pardon {user_name}')
        UserMapper.update_whitelisted_by_name(user_name, None)

        await bot.send(event, Message(f'{response}--完成'))

class ban_syn:
    async def handle(bot: Bot, event: Event):
        pass