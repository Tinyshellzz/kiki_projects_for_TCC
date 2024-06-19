from .db_config import *
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

        db = connect()
        c = db.cursor()
        c.execute("""INSERT INTO users
            (email, phone, password, permission )
            values
            (%s, %s, MD5(%s), %s)""", (user.email, user.phone, user.password, user.permission ))
        db.commit()
        res = None
        if user.email != None:
            res = c.execute("SELECT * FROM users WHERE email=%s", (user.email,))
        else:
            res = c.execute("SELECT * FROM users WHERE phone=%s", (user.phone,))
        c.close()
        db.close()

        return res[0][0]
    
    def verify_password_email(email, password):
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users WHERE email=%s AND password=MD5(%s)", (email,password))
        res = c.fetchall()
        c.close()
        db.close()

        if len(res) != 0:
            r = res[0]
            return r[0]
        return None
    
    def update_password_by_email(email, password):
        db = connect()
        c = db.cursor()
        c.execute("""UPDATE users
            SET password=MD5(%s)
            WHERE email=%s""", (password, email))
        db.commit()
        c.close()
        db.close()

        return True
    
    def get_user_by_id(id):
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users WHERE id=%s", (id,))
        res = c.fetchall()
        c.close()
        db.close()

        r = res[0]
        return User(int(r[0]), r[1], r[2], None, r[4])
    
    def get_id_by_email(email):
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users WHERE email=%s", (email,))
        res = c.fetchall()
        c.close()
        db.close()

        id = res[0][0]
        return id
    
    def exits_email(email: str):
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users WHERE email=%s", (email,))
        res = c.fetchall()
        c.close()
        db.close()

        if len(res) != 0:
            return True
        return False
    
    def exits_email_user(email: str):
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users WHERE email=%s", (email,))
        res = c.fetchall()
        c.close()
        db.close()

        if len(res) != 0:
            r = res[0]
            return r[3] != None
        return False
    
    def exits_phone(phone: str):
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM users WHERE phone=%s", (phone,))
        res = c.fetchall()
        c.close()
        db.close()

        if len(res) != 0:
            return True
        return False
    
