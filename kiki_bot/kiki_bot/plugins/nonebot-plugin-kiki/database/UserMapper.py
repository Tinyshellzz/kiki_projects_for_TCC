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
            mc_uuid text,
            is_banned text,
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

class UserMapper:
    def insert(user: User):
        # user_name 已被绑定 
        if UserMapper.exists_qq_id(user.user_name): 
            logger.error(f"user_name:{user.user_name} 已被绑定")
            return

        # qq 已被绑定
        if UserMapper.exists_qq_id(user.qq_num): 
            logger.error(f"qq:{user.qq_num} 已被绑定")
            return

        # 验证 uuid
        if user.mc_uuid == None:
            user.mc_uuid = tools.get_uuid_by_name(user.user_name)
            if user.mc_uuid == None: return     # 名称不合法

        # uuid 已被绑定 
        if UserMapper.exists_mc_uuid(user.mc_uuid): 
            logger.error(f"uuid:{user.mc_uuid} 已被绑定")
            return

        # 锁住数据库, 插入操作
        with dblock:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user.qq_num, user.user_name, str(user.mc_uuid), user.is_banned, user.user_info))
            conn.commit()
        
        logger.info(f"user_name:{user.user_name} 已被被添加到数据库")

    # 通过 qq_num 或 user_name 或 mc_uuid, 查找数据库
    def get(qq_num = None, user_name = None, mc_uuid = None) -> User:
        if qq_num != None:
            c.execute("SELECT * FROM users WHERE qq_num=:qq_num", {'qq_num': qq_num})
        elif user_name != None:
            c.execute("SELECT * FROM users WHERE user_name=:user_name", {'user_name': user_name})
        elif mc_uuid != None:
            c.execute("SELECT * FROM users WHERE mc_uuid=:mc_uuid", {'mc_uuid': mc_uuid})
        
        res = c.fetchall()

        # 没找到
        if len(res) == 0:
            return None

        res = res[0]
        return User(res[0], res[1], res[2], res[3], res[4])
    
    def is_banned(qq_num):
        pass
    
    # 检查是否有重复的 qq_id
    def exists_qq_id(qq_num, user_name = None, mc_uuid = None) -> bool:
        c.execute("SELECT * FROM users WHERE qq_num=:qq_num", {'qq_num': qq_num})
        res = c.fetchall()
        if len(res) != 0: 
            return True

        return False

    def exists_user_name(user_name) -> bool:
        c.execute("SELECT * FROM users WHERE user_name=:user_name", {'user_name': user_name})
        res = c.fetchall()
        if len(res) != 0: 
            return True
        
        return False
    
    def exists_mc_uuid(mc_uuid) -> bool:
        c.execute("SELECT * FROM users WHERE mc_uuid=:mc_uuid", {'mc_uuid': mc_uuid})
        res = c.fetchall()
        if len(res) != 0: 
            return True
        
        return False

    # 更新 is_banned 和 user_info
    def update_banned_by_qq(qq_num, is_banned, user_info = None):
        # 锁住数据库
        with dblock:
            c.execute("""UPDATE users 
                    SET is_banned=?, user_info=?
                    WHERE qq_num=?""", (is_banned, user_info, qq_num))
            conn.commit()

    # 将 user_name 更改的与 uuid 一致, 因为有人可能会改名
    def update_all_user_name():
        c.execute('SELECT * FROM users')
        for row in c:
            user_name = tools.get_name_by_uuid(row[2])
            if not (row[1] == user_name):
                with dblock:
                    logger.info(f"user_name:{row[1]} 被更新为 {user_name}")
                    c.execute("UPDATE users SET user_name=? WHERE qq_num=?", (user_name, row[0]))
                    conn.commit()

    # 删除
    def delete_by_qq(qq_num):
        with dblock:
            c.execute("DELETE FROM users WHERE qq_num=:qq_num", {'qq_num': qq_num})
            conn.commit()
