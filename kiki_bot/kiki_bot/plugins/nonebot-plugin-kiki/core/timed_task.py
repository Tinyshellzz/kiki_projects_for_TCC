import threading
from ..database.UserMapper import UserMapper
from datetime import datetime, timedelta
from .server import *
import sched, time

def run():
    response = excute("list")
    response = re.sub('§.', '', response)
    matches = re.findall('[离开](.*?),', response, re.DOTALL)
    for m in matches:
        logger.debug(m)
        r = excute(f"matrix reset {m}")
        logger.debug(r)
    
    # 计算到第二天 1 点的秒数
    x = datetime.now()
    y = x + timedelta(days=1)
    y = y.replace(day=y.day, hour=1, minute=0, second=0, microsecond=0)
    secs = (y-x).total_seconds()
        
    threading.Timer(10, run).start()    # 每隔10秒执行一次