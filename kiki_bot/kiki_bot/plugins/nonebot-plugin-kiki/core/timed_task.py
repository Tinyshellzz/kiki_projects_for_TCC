from ..database.UserMapper import UserMapper
from datetime import datetime, timedelta
from .server import *
import sched, time

def run():
    # 设置定时任务
    def task(scheduler):
        response = excute("list")
        response = re.sub('§.', '', response)
        print(response)
        
        # 计算到第二天 1 点的秒数
        x = datetime.now()
        y = x + timedelta(days=1)
        y = y.replace(day=y.day, hour=1, minute=0, second=0, microsecond=0)
        secs = (y-x).total_seconds()
            
        scheduler.enter(10, 1, task, (scheduler,))    # 每10秒执行一次

    # 每天, 更新一次user_name
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(0, 1, task, (my_scheduler,))
    my_scheduler.run()