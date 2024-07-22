from datetime import timedelta
import threading
import datetime
from ..sign.SignMapper import SignMapper

# 定时清理数据库
def clean():
    SignMapper.clean_up()
    
    # 计算到第二天 0 点的秒数
    x = datetime.datetime.now()
    y = x + timedelta(days=1)
    y = y.replace(hour=0, minute=0, second=0, microsecond=0)
    secs = (y-x).total_seconds()
        
    threading.Timer(secs, clean).start()    # 每隔secs秒执行一次
