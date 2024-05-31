import pandas as pd
from pathlib import Path
import os
from os import listdir
from os.path import isfile, join
from .UserMapper import UserMapper
from .User import User
from datetime import datetime, timedelta
from threading import Timer
import sched, time

plugin_dir = str(Path(__file__).resolve().parents[1])
excels_dir = plugin_dir + '/resources/excels/'

def read_excel(fpath):
    xls = pd.read_excel(fpath)

    for index, row in xls.iterrows():
        # 将所有通过的都插入数据库
        if row['passed'] == '☑':
            UserMapper.insert(User(row['qq_num'], row['user_name']))


# 读取 excels_dir 下所有的文件, 读完后就删除
def read_excels():
    excels = []
    for f in listdir(excels_dir):
        filename, file_extension = os.path.splitext(f)
        file = join(excels_dir, f)
        if isfile(file) and (file_extension == '.xlsx' or file_extension == '.xls'):
            excels.append(file)

    for e in excels:
        read_excel(e)
        # 删除读完的 excel
        os.remove(e)

# 设置定时任务
def update_user_names(scheduler):
    def update_task():
        UserMapper.update_all_user_name()
        x = datetime.now()
        y = x + timedelta(days=1)
        y = y.replace(day=y.day, hour=1, minute=0, second=0, microsecond=0)
        secs = (y-x).total_seconds()
        scheduler.enter(secs, 1, update_user_names, (scheduler,))

# 每天, 更新一次user_name
my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(0, 1, update_user_names, (my_scheduler,))

def _read_excels(scheduler): 
    # 开始读取 excels
    read_excels()
    scheduler.enter(60, 1, _read_excels, (scheduler,))
# 每隔10s, 读取 excels
my_scheduler.enter(10, 1, _read_excels, (my_scheduler,))
# my_scheduler.run()



