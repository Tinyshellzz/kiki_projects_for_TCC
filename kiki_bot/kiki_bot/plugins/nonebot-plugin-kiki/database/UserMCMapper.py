from .db_config import *
import json
from ..utils import tools

try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users_mc (
        id BigInt UNSIGNED,
        qq_num BigInt UNSIGNED,
        user_name Varchar(48),
        display_name Varchar(48),
        mc_uuid Char(36),
        last_login_time Datetime,
        remark Text,
        PRIMARY KEY (id),
        UNIQUE KEY (qq_num),
        KEY (user_name),
        KEY (display_name),
        UNIQUE KEY (mc_uuid),
        KEY (last_login_time)
    ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    c.execute("""CREATE TABLE IF NOT EXISTS banlist (
        id BigInt UNSIGNED,
        reason TEXT,
        unban_date Datetime,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    c.execute("""CREATE TABLE IF NOT EXISTS whitelist (
        id BigInt UNSIGNED,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    db.commit()
    c.close()
    db.close()
except:
    pass

class MCUser:
    def __init__(self, id, qq_num, user_name: str, display_name = None, mc_uuid = None, last_login_time = None, remark:str = None):
        self.id = id
        self.qq_num = qq_num
        self.user_name = user_name.lower()
        self.display_name = display_name
        self.mc_uuid = mc_uuid
        self.last_login_time = last_login_time
        self.remark = remark.replace("\"", "").replace("//", "").replace("\'", "")
    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)
    
class UserMCMapper:
    def get_user_amount():
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT COUNT(*) FROM whitelist")
        res = c.fetchall()
        c.close()
        db.close()

        return res[0][0]
    
    def get_users(page: int, size: int = 12):
        page = round(page)
        if page <= 0:
            raise Exception({'errorCode': 'userMapper_get_page_zero'})

        db = connect() 
        c = db.cursor()
        db.commit()
        offset = (page-1)*size
        c.execute("SELECT * from users_mc, whitelist WHERE users_mc.id=whitelist.id LIMIT %s OFFSET %s", (size, offset))
        res = c.fetchall()
        c.close()
        db.close()

        users_mc = []
        for r in res:
            users_mc.append(MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        return users_mc
    
    def get_users_like(keyword: str, page: int, size: int = 12):
        user_name = keyword.lower()

        page = round(page)
        if page <= 0:
            raise Exception({'errorCode': 'userMapper_get_page_zero'})

        db = connect() 
        c = db.cursor()
        db.commit()
        offset = (page-1)*size
        c.execute("SELECT * from users_mc, whitelist WHERE users_mc.id=whitelist.id AND (user_name LIKE %s OR qq_num LIKE %s) LIMIT %s OFFSET %s", ("%"+user_name+"%", "%"+keyword+"%", size, offset))
        res = c.fetchall()
        c.close()
        db.close()

        users_mc = []
        for r in res:
            users_mc.append(MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        return users_mc
    
    def get_users_amount_like(keyword: str):
        user_name = keyword.lower()
        db = connect() 
        c = db.cursor()
        db.commit()
        c.execute("SELECT COUNT(*) from users_mc, whitelist WHERE users_mc.id=whitelist.id AND (user_name LIKE %s OR qq_num LIKE %s)", ("%"+user_name+"%", "%"+keyword+"%"))
        res = c.fetchall()
        c.close()
        db.close()

        return res[0][0]
    
    def insert(user: MCUser):
        # user_name 已被绑定 
        if UserMCMapper.exists_user_name(user.user_name): 
            tools.exception(f"user_name:{user.user_name} 已被绑定")
            return
        # qq 已被绑定
        if UserMCMapper.exists_qq_id(user.qq_num): 
            tools.exception(f"qq:{user.qq_num} 已被绑定")
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
        if UserMCMapper.exists_mc_uuid(user.mc_uuid): 
            tools.exception(f"uuid:{user.mc_uuid} 已被绑定")
            return False

        db = connect() 
        c = db.cursor()
        c.execute("INSERT INTO users_mc VALUES (?, ?, ?, ?, ?, ?, ?)", (user.id, user.qq_num, user.user_name, user.display_name, user.mc_uuid, user.last_login_time, user.remark))
        db.commit()
        c.close()
        db.close()
        
        tools.info(f"user_name:{user.user_name} 已被被添加到数据库")
        return True
    

    def exists_qq_id(qq_num: str):
        db = connect() 
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users_mc WHERE qq_num=%s", (qq_num,))
        res = c.fetchall()
        c.close()
        db.close()

        return len(res)!=0
    
    def exists_user_name(user_name: str):
        db = connect() 
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users_mc WHERE user_name=%s", (user_name,))
        res = c.fetchall()
        c.close()
        db.close()

        return len(res)!=0
    
    def exists_mc_uuid(mc_uuid: str):
        db = connect() 
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users_mc WHERE mc_uuid=%s", (mc_uuid,))
        res = c.fetchall()
        c.close()
        db.close()

        return len(res)!=0
    
    def update_whitelisted_by_qq(qq_num, whitelisted):
        db = connect() 
        c = db.cursor()
        c.execute("SELECT * FROM users_mc WHERE qq_num=%s", qq_num)
        res = c.fetchall()
        if (len(res) == 0):
            return
        id = res[0][0]
        if whitelisted:
            UserMCMapper.add_whitelist(id)
        else:
            UserMCMapper.remove_whitelist(id)

        db.commit()
        c.close()
        db.close()

    def exists_whitelist(id: int):
        db = connect() 
        c = db.cursor()
        c.execute("INSERT INTO whitelist VALUES (?)", (id,))
        res = c.fetchall()
        db.commit()
        c.close()
        db.close()

        return len(res) != 0

    def add_whitelist(id: int):
        try:
            db = connect() 
            c = db.cursor()
            c.execute("INSERT INTO whitelist VALUES (?)", (id,))
            db.commit()
            c.close()
            db.close()
        except:
            pass

    def remove_whitelist(id: int):
        db = connect() 
        c = db.cursor()
        c.execute("DELETE FROM whitelist WHERE id=%s", (id,))
        db.commit()
        c.close()
        db.close()

    def update_remark_by_qq(qq_num: str, remark: str):
        db = connect() 
        c = db.cursor()
        c.execute("UPDATE users SET remark=%s WHERE qq_num=%s", (remark, qq_num))
        db.commit()
        c.close()
        db.close()

    def get_all_user():
        db = connect() 
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users")
        res = c.fetchall()
        c.close()
        db.close()

        mc_users = []
        for r in res:
            mc_users.append(MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        
        return mc_users
    
        # 通过 qq_num 或 user_name 或 mc_uuid, 查找数据库
    def get(qq_num = None, user_name: str = None, mc_uuid = None) -> MCUser:
        if user_name != None: user_name = user_name.lower()
        db = connect() 
        c = db.cursor()
        db.commit()
        if qq_num != None:
            c.execute("SELECT * FROM users WHERE qq_num=%s", (qq_num,))
        elif user_name != None:
            c.execute("SELECT * FROM users WHERE user_name=%s", (user_name,))
        elif mc_uuid != None:
            c.execute("SELECT * FROM users WHERE mc_uuid=%s", (mc_uuid,))
        
        res = c.fetchall()
        c.close()
        db.close()

        if len(res) == 0:
            return None
        r = res[0]
        return MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6])