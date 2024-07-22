from ..config.db_config import *
import json
from ..utils import tools

try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id BigInt UNSIGNED AUTO_INCREMENT,
        email Varchar(256),
        phone varchar(30),
        password CHAR(32),
        permission  Tinyint,
        PRIMARY KEY (id),
        KEY (email),
        KEY (phone),
        KEY (password),
        KEY (permission )
    ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    db.commit()
    c.close()
    db.close()
except:
    pass

class User:
    # permission 是权限等级，数字越高权限越大
    def __init__(self, id: int = None, email: str = None, phone: str = None, password: str = None, permission: int = None):
        self.id = id
        self.email = email
        self.phone = phone
        self.password = password
        self.permission  = permission 
    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)


class UserMapper:
    def insert(user: User):
        if user.email != None and UserMapper.exits_email(user.email):
            raise Exception("该QQ已被绑定")
        if user.phone != None and UserMapper.exits_phone(user.phone):
            raise Exception("该电话已被绑定")
        if user.email == None and user.phone == None:
            raise tools.exception("未提供email或phone")

        with connect() as db:
            with db.cursor() as c:
                c.execute("""INSERT INTO users
                    (email, phone, password, permission )
                    values
                    (%s, %s, MD5(%s), %s)""", (user.email, user.phone, user.password, user.permission ))
                db.commit()
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                if user.email != None:
                    c.execute("SELECT * FROM users WHERE email=%s", (user.email,))
                    res = c.fetchall()
                else:
                    c.execute("SELECT * FROM users WHERE phone=%s", (user.phone,))
                    res = c.fetchall()

        return res[0][0]
    
    def verify_password_email(email, password):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users WHERE email=%s AND password=MD5(%s)", (email,password))
                res = c.fetchall()

        if len(res) != 0:
            r = res[0]
            return r[0]
        return None
    
    def update_password_by_email(email, password):
        with connect() as db:
            with db.cursor() as c:
                c.execute("""UPDATE users
                    SET password=MD5(%s)
                    WHERE email=%s""", (password, email))
                db.commit()

        return True
    
    def get_user_by_id(id: int):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users WHERE id=%s", (id,))
                res = c.fetchall()

        if len(res) == 0: return None
        r = res[0]
        return User(int(r[0]), r[1], r[2], None, r[4])
    
    def get_user_by_email(email):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users WHERE email=%s", (email,))
                res = c.fetchall()

        if len(res) == 0: return None
        r = res[0]
        return User(int(r[0]), r[1], r[2], None, r[4])

    def get_id_by_email(email):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users WHERE email=%s", (email,))
                res = c.fetchall()

        if len(res) == 0: return None
        id = res[0][0]
        return id
    
    def exits_email(email: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users WHERE email=%s", (email,))
                res = c.fetchall()

        return len(res)!=0
    
    def exits_email_user(email: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users WHERE email=%s", (email,))
                res = c.fetchall()

        if len(res) != 0:
            r = res[0]
            return r[3] != None
        return False
    
    def exits_phone(phone: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM users WHERE phone=%s", (phone,))
                res = c.fetchall()

        return res != None and len(res) != 0
    
    def delete_by_email(email: str):
        with connect() as db:
            with db.cursor() as c:
                c.execute("DELETE FROM users WHERE email=%s", (email,))
                db.commit()

        return True
