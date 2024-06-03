from pathlib import Path
import sqlite3

project_dir = str(Path(__file__).resolve().parents[5])
source = sqlite3.connect(project_dir + '/user_old.db')
target = sqlite3.connect(project_dir + '/user.db')

c_target = target.cursor()
# 创建users表格
try:
    c_target.execute("""CREATE TABLE users (
            qq_num text,
            user_name text,
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
target.close()


def get_all_user():
    c = source.cursor()
    c.execute("SELECT * FROM users")
    res = c.fetchall()
    c.close()
    
    return res

def run():
    res = get_all_user()

    c = target.cursor()
    for r in res:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (r[0], r[1], r[2], 'true', r[4]))
    target.commit()
    c.close()