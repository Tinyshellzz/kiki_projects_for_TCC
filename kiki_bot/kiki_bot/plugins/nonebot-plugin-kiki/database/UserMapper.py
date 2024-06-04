# 负责与玩家数据库交互
from pathlib import Path
from .User import User
from .DBConfig import *
from ..tools import tools
from ..config.config import *


c = conn.cursor()
# 创建users表格
try:
    c.execute("""CREATE TABLE users (
            qq_num text,
            user_name text,
            display_name text,
            mc_uuid text,
            whitelisted text,
            last_login_time text,
            user_info text
    )""")

    # 创建索引
    c.execute("""CREATE UNIQUE INDEX qq_num_index
            on users (qq_num);""")
    c.execute("""CREATE INDEX user_name_index
            on users (user_name);""")
    c.execute("""CREATE UNIQUE INDEX mc_uuid_index
            on users (mc_uuid);""")

    # 提交修改
    conn.commit()
except Exception as e:
    pass
c.close()


def insert(user: User):
    # user_name 已被绑定 
    if exists_qq_id(user.user_name): 
        logger.error(f"user_name:{user.user_name} 已被绑定")
        return
    # qq 已被绑定
    if exists_qq_id(user.qq_num): 
        logger.error(f"qq:{user.qq_num} 已被绑定")
        return
    # 验证 uuid
    if user.mc_uuid == None:
        uuid = None
        try:
            (display_name, uuid) = tools.get_name_and_uuid_by_name(user.user_name)
        except:
            pass
        if uuid == None: return False
        user.display_name = display_name
        user.mc_uuid = uuid
    # uuid 已被绑定 
    if exists_mc_uuid(user.mc_uuid): 
        logger.error(f"uuid:{user.mc_uuid} 已被绑定")
        return False

    c = conn.cursor()
    # 锁住数据库, 插入操作
    with dblock:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (user.qq_num, user.user_name, user.display_name, user.mc_uuid, user.whitelisted, user.last_login_time, user.user_info))
        conn.commit()
    c.close()
    
    logger.info(f"user_name:{user.user_name} 已被被添加到数据库")
    return True
# 通过 qq_num 或 user_name 或 mc_uuid, 查找数据库
def get(qq_num = None, user_name = None, mc_uuid = None) -> User:
    if user_name != None: user_name = user_name.lower()
    c = conn.cursor()
    if qq_num != None:
        c.execute("SELECT * FROM users WHERE qq_num=:qq_num", {'qq_num': qq_num})
    elif user_name != None:
        c.execute("SELECT * FROM users WHERE user_name=:user_name", {'user_name': user_name})
    elif mc_uuid != None:
        c.execute("SELECT * FROM users WHERE mc_uuid=:mc_uuid", {'mc_uuid': mc_uuid})
    
    res = c.fetchall()
    c.close()
    # 没找到
    if len(res) == 0:
        return None
    res = res[0]
    return User(res[0], res[1], res[2], res[3], res[4], res[5], res[6])

def whitelisted(qq_num):
    pass

# 检查是否有重复的 qq_id
def exists_qq_id(qq_num, user_name = None, mc_uuid = None) -> bool:
    if user_name != None: user_name = user_name.lower()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE qq_num=:qq_num", {'qq_num': qq_num})
    res = c.fetchall()
    c.close()
    if len(res) != 0: 
        return True
    return False
def exists_user_name(user_name) -> bool:
    user_name = user_name.lower()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_name=:user_name", {'user_name': user_name})
    res = c.fetchall()
    c.close()
    if len(res) != 0: 
        return True
    
    return False

def exists_mc_uuid(mc_uuid) -> bool:
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE mc_uuid=:mc_uuid", {'mc_uuid': mc_uuid})
    res = c.fetchall()
    c.close()
    if len(res) != 0: 
        return True
    
    return False
# 更新 whitelisted
def update_whitelisted_by_uuid(mc_uuid, user_name, whitelisted):
    user_name = user_name.lower()
    c = conn.cursor()
    # 锁住数据库
    with dblock:
        c.execute("""UPDATE users 
                SET user_name=?, whitelisted=?
                WHERE mc_uuid=?""", (user_name, whitelisted, mc_uuid))
        conn.commit()
    c.close()
    # 更新 whitelisted
def update_whitelisted_by_name(user_name, whitelisted):
    if user_name != None: user_name = user_name.lower()
    c = conn.cursor()
    # 锁住数据库
    with dblock:
        c.execute("""UPDATE users 
                SET whitelisted=?
                WHERE user_name=?""", (whitelisted, user_name))
        conn.commit()
    c.close()
# 更新 user_info
def update_user_info_by_uuid(mc_uuid, user_name, user_info):
    if user_name != None: user_name = user_name.lower()
    
    c = conn.cursor()
    # 锁住数据库
    with dblock:
        c.execute("""UPDATE users 
                SET user_name=?, user_info=?
                WHERE mc_uuid=?""", (user_name, user_info, mc_uuid))
        conn.commit()
    c.close()
# 更新 user_info
def update_name_by_uuid(mc_uuid, user_name, display_name):
    if user_name != None: user_name = user_name.lower()
    
    c = conn.cursor()
    # 锁住数据库
    with dblock:
        c.execute("""UPDATE users 
                SET user_name=?, display_name=?
                WHERE mc_uuid=?""", (user_name, display_name, mc_uuid))
        conn.commit()
    c.close()
def update_whitelisted_by_qq(qq_num, whitelisted):
    c = conn.cursor()
    # 锁住数据库
    with dblock:
        c.execute("""UPDATE users 
                SET whitelisted=?
                WHERE qq_num=?""", (whitelisted, qq_num))
        conn.commit()
    c.close()
    
# 删除
def delete_by_qq(qq_num):
    c = conn.cursor()
    with dblock:
        c.execute("DELETE FROM users WHERE qq_num=:qq_num", {'qq_num': qq_num})
        conn.commit()
    c.close()

# 删除
def delete_by_uuid(mc_uuid):
    c = conn.cursor()
    with dblock:
        c.execute("DELETE FROM users WHERE mc_uuid=:mc_uuid", {'mc_uuid': mc_uuid})
        conn.commit()
    c.close()

# 删除
def delete_by_name(user_name):
    if user_name != None: user_name = user_name.lower()
    
    c = conn.cursor()
    with dblock:
        c.execute("DELETE FROM users WHERE user_name=:user_name", {'user_name': user_name})
        conn.commit()
    c.close()

def get_all_user():
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    res = c.fetchall()
    c.close()
    users = []
    for r in res:
        users.append(User(res[0], res[1], res[2], res[3], res[4], res[5], res[6]))
    
    return users