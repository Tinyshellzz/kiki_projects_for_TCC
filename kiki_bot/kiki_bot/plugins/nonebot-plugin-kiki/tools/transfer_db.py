from pathlib import Path
import sqlite3
from ..config.config import *
from ..core.authorization import *
from ..tools.tools import *
from nonebot.adapters.onebot.v11 import Bot, Event

async def handle(bot: Bot, event: Event):
    print('转移开始')
    if not await auth_user(bot, event, auth_qq_list): return

    project_dir = str(Path(__file__).resolve().parents[5])
    source = sqlite3.connect(project_dir + '/user_old.db')
    target = sqlite3.connect(project_dir + '/user.db')

    c_target = target.cursor()
    # 创建users表格
    try:
        c_target.execute("""CREATE TABLE users (
                qq_num text,
                user_name text,
                display_name text,
                mc_uuid text,
                whitelisted text,
                user_info text
        )""")

        # 创建索引
        c_target.execute("""CREATE UNIQUE INDEX qq_num_index
                on users (qq_num);""")
        c_target.execute("""CREATE INDEX user_name_index
                on users (user_name);""")
        c_target.execute("""CREATE UNIQUE INDEX mc_uuid_index
                on users (mc_uuid);""")

        # 提交修改
        target.commit()
    except Exception as e:
        pass
    c_target.close()

    c_source = source.cursor()
    c_source.execute("SELECT * FROM users")
    res = c_source.fetchall()

    c_target = target.cursor()
    for r in res:
        try:
            name = get_name_by_uuid(r[2])
        except:
            print(f'###############转移{r[1].lower()}失败#############')
        print(f'转移{name}成功')
        c_target.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (r[0], r[1].lower(), name, r[2], 'true', r[4]))
    target.commit()
    c_target.close()
    c_source.close()
    
    print('--------------------------------------------')
