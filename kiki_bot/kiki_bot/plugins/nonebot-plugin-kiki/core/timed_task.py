import threading
from ..database.UserMapper import UserMapper
from datetime import datetime, timedelta
from .server import *
import sched, time

def run():
    rcon = mcrcon.MCRcon(server_ip, rcon_password, rcon_port, timeout=2)
    response  = None
    try:
        rcon.connect()
        response = rcon.command("list")
        response = re.sub('§.', '', response)
        matches = re.findall('\[离开\](.*?),', response, re.DOTALL)
        for m in matches:
            rcon.command("matrix reset {m}")
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()
    
    # 计算到第二天 1 点的秒数
    x = datetime.now()
    y = x + timedelta(days=1)
    y = y.replace(day=y.day, hour=1, minute=0, second=0, microsecond=0)
    secs = (y-x).total_seconds()
        
    threading.Timer(10, run).start()    # 每隔10秒执行一次