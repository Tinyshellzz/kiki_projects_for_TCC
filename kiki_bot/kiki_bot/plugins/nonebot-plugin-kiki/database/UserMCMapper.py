from .db_config import *
import json
from ..utils import tools
import datetime

try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users_mc (
        id BigInt UNSIGNED,
        qq_num BigInt UNSIGNED,
        user_name Varchar(48),
        display_name Varchar(48),
        mc_uuid Char(32),
        last_login_time Datetime,
        remark Text,
        PRIMARY KEY (id),
        UNIQUE KEY (qq_num),
        KEY (user_name),
        KEY (display_name),
        UNIQUE KEY (mc_uuid),
        KEY (last_login_time)
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
    def __init__(self, id, qq_num, user_name: str, display_name = None, mc_uuid = None, last_login_time: datetime.datetime = None, remark:str = None):
        if last_login_time != None:
            last_login_time.strftime("%Y-%m-%d %H:%M:%S")
            last_login_time = last_login_time.replace(microsecond=0)

        self.id = id
        self.qq_num = qq_num
        self.user_name = None if user_name == None else user_name.lower()
        self.display_name = display_name
        self.mc_uuid = mc_uuid
        self.last_login_time = last_login_time
        self.remark = None if remark == None else remark.replace("\"", "").replace("//", "").replace("\'", "")
    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)
    
class UserMCMapper:
    def get_user_amount():
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) FROM whitelist")
                res = c.fetchall()

        return res[0][0]
    
    def get_users(page: int, size: int = 12):
        page = round(page)
        if page <= 0:
            raise Exception({'errorCode': 'userMapper_get_page_zero'})

        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                offset = (page-1)*size
                c.execute("SELECT * from users_mc, whitelist WHERE users_mc.id=whitelist.id LIMIT %s OFFSET %s", (size, offset))
                res = c.fetchall()

        users_mc = []
        for r in res:
            users_mc.append(MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        return users_mc
    
    def get_users_like(keyword: str, page: int, size: int = 12):
        user_name = keyword.lower()

        page = round(page)
        if page <= 0:
            raise Exception({'errorCode': 'userMapper_get_page_zero'})

        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                offset = (page-1)*size
                c.execute("SELECT * from users_mc, whitelist WHERE users_mc.id=whitelist.id AND (user_name LIKE %s OR qq_num LIKE %s) LIMIT %s OFFSET %s", ("%"+user_name+"%", "%"+keyword+"%", size, offset))
                res = c.fetchall()

        users_mc = []
        for r in res:
            users_mc.append(MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        return users_mc
    
    def get_users_amount_like(keyword: str):
        user_name = keyword.lower()
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) from users_mc, whitelist WHERE users_mc.id=whitelist.id AND (user_name LIKE %s OR qq_num LIKE %s)", ("%"+user_name+"%", "%"+keyword+"%"))
                res = c.fetchall()

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

        res = None
        with connect() as db:
            with db.cursor() as c:
                c.execute("INSERT INTO users_mc VALUES (%s, %s, %s, %s, %s, %s, %s)", (user.id, user.qq_num, user.user_name, user.display_name, user.mc_uuid, user.last_login_time, user.remark))
                db.commit()
        
        tools.info(f"user_name:{user.user_name} 已被被添加到数据库")
        return True
    

    def exists_qq_id(qq_num: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users_mc WHERE qq_num=%s", (qq_num,))
                res = c.fetchall()

        return len(res)!=0
    
    def exists_user_name(user_name: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users_mc WHERE user_name=%s", (user_name,))
                res = c.fetchall()

        return len(res)!=0
    
    def exists_mc_uuid(mc_uuid: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users_mc WHERE mc_uuid=%s", (mc_uuid,))
                res = c.fetchall()

        return len(res)!=0
    
    def update_whitelisted_by_qq(qq_num, whitelisted):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
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
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM whitelist WHERE id=%s", (id,))
                res = c.fetchall()

        return len(res) != 0

    def add_whitelist(id: int):
        if UserMCMapper.exists_whitelist(id):
            return

        with connect() as db:
            with db.cursor() as c:
                c.execute("INSERT INTO whitelist VALUES (%s)", (id,))
                db.commit()


    def remove_whitelist(id: int):
        with connect() as db:
            with db.cursor() as c:
                c.execute("DELETE FROM whitelist WHERE id=%s", (id,))
                db.commit()

    def update_remark_by_qq(qq_num: str, remark: str):
        with connect() as db:
            with db.cursor() as c:
                c.execute("UPDATE users_mc SET remark=%s WHERE qq_num=%s", (remark, qq_num))
                db.commit()

    def get_all_user():
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users_mc")
                res = c.fetchall()

        mc_users = []
        for r in res:
            mc_users.append(MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        
        return mc_users
    
        # 通过 qq_num 或 user_name 或 mc_uuid, 查找数据库
    def get(qq_num = None, user_name: str = None, mc_uuid = None) -> MCUser:
        if user_name != None: user_name = user_name.lower()

        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                if qq_num != None:
                    c.execute("SELECT * FROM users_mc WHERE qq_num=%s", (qq_num,))
                elif user_name != None:
                    c.execute("SELECT * FROM users_mc WHERE user_name=%s", (user_name,))
                elif mc_uuid != None:
                    c.execute("SELECT * FROM users_mc WHERE mc_uuid=%s", (mc_uuid,))
                
                res = c.fetchall()

        if len(res) == 0:
            return None
        r = res[0]
        return MCUser(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
    
    def delete_by_qq(qq_num):
        with connect() as db:
            with db.cursor() as c:
                c.execute("DELETE FROM users_mc WHERE qq_num=%s", (qq_num,))
                db.commit()

        return True