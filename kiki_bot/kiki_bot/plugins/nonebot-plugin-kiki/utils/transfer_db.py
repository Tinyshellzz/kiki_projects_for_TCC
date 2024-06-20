import datetime
from pathlib import Path
import sqlite3
from ..config.config import *
from ..core.authorization import *
from . import tools
from nonebot.adapters.onebot.v11 import Bot, Event
from ..database.UserMapper import UserMapper, User
from ..database.UserMCMapper import UserMCMapper, MCUser

async def handle(bot: Bot, event: Event):
    print('转移开始')
    if not await auth_user(bot, event, auth_qq_list): return

    project_dir = str(Path(__file__).resolve().parents[5])
    source = sqlite3.connect(project_dir + '/user.db')
    c_source = source.cursor()
    c_source.execute("SELECT * FROM users")
    res = c_source.fetchall()

    for r in res:
        try:
            email = r[0] + "@qq.com"
            id = None
            if(UserMapper.exits_email(email=email)):
                user = UserMapper.get_user_by_email(email)
                id = user.id
            else:
                id = UserMapper.insert(User(email=email, permission=1))
            last_login_time = None
            if r[5] != None:
                last_login_time = datetime.datetime.strptime(r[5], "%Y-%m-%dT%H:%M:%S")
            UserMCMapper.insert(MCUser(id, r[0], r[1], r[2], r[3].replace("-", ""), last_login_time, r[6]))
            if r[4]=='true': UserMCMapper.add_whitelist(id)
            print(f'转移{r[2]}成功')
        except Exception as e:
            print(e)
            print(f'-----------------转移{r[2]}失败-----------------')
    c_source.close()
    source.close()
    
    print('--------------------------------------------')
