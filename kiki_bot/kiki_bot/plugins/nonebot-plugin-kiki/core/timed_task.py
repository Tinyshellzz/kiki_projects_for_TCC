from ..database.UserMapper import UserMapper
from datetime import datetime, timedelta
import sched, time

# 设置定时任务
def update_user_names(scheduler):
    def update_task():
        UserMapper.update_all_user_name()

        # 计算到第二天 1 点的秒数
        x = datetime.now()
        y = x + timedelta(days=1)
        y = y.replace(day=y.day, hour=1, minute=0, second=0, microsecond=0)
        secs = (y-x).total_seconds()
        
        scheduler.enter(secs, 1, update_user_names, (scheduler,))

# 每天, 更新一次user_name
my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(0, 1, update_user_names, (my_scheduler,))
my_scheduler.run()