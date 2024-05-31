import sqlite3
from pathlib import Path
from .User import User

plugin_dir = str(Path(__file__).resolve().parents[1])
conn = sqlite3.connect(plugin_dir + '/database/user.db')
c = conn.cursor()

# 创建users表格
try:
    c.execute("""CREATE TABLE users (
            qq_user_id text,
            mc_user_name text,
            mc_user_id text,
            is_in_qq_group integer,
            banned_date text
    )""")

    # 创建索引
    c.execute("""CREATE UNIQUE INDEX qq_user_id_index
            on users (qq_user_id);""")
    c.execute("""CREATE INDEX mc_user_name_index
            on users (mc_user_name);""")
    c.execute("""CREATE INDEX mc_user_id_index
            on users (mc_user_id);""")

    # 提交修改
    conn.commit()
except Exception as e:
    pass

class UserMapper:
    def insert(user: User):
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user.qq_user_id, user.mc_user_name, user.mc_user_id, user.is_in_qq_group, user.banned_date))
        conn.commit()

    def get(qq_user_id = None, mc_user_name = None, mc_user_id = None) -> list:
        if qq_user_id != None:
            c.execute("SELECT * FROM users WHERE qq_user_id=:qq_user_id", {'qq_user_id': qq_user_id})
        elif mc_user_name != None:
            c.execute("SELECT * FROM users WHERE mc_user_name=:mc_user_name", {'mc_user_name': mc_user_name})
        elif mc_user_id != None:
            c.execute("SELECT * FROM users WHERE mc_user_id=:mc_user_id", {'mc_user_id': mc_user_id})
        
        res = c.fetchall()
        return User.create_users_from_db(res)
    
    def update(user: User):
        c.execute("""UPDATE users 
                  SET mc_user_name=?, mc_user_id=?, mc_user_id=?, is_in_qq_group=?, banned_date=?
                  WHERE qq_user_id=?""", (user.mc_user_name, user.mc_user_id, user.is_in_qq_group, user.banned_date, user.qq_user_id))
