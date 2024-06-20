from .db_config import *
import json
from ..utils import tools
import datetime

try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS banlist (
        mc_uuid Char(32),
        user_name Varchar(48), 
        display_name Varchar(48), 
        unban_date Datetime,
        reason TEXT,
        PRIMARY KEY (mc_uuid),
        KEY (user_name)
    ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    db.commit()
    c.close()
    db.close()
except:
    pass

class BanlistUser:
    def __init__(self, mc_uuid, user_name, display_name, unban_date: datetime.datetime = None, reason:str = None):
        if unban_date != None:
            unban_date.strftime("%Y-%m-%d %H:%M:%S")
            unban_date = unban_date.replace(microsecond=0)

        self.mc_uuid = mc_uuid
        self.user_name = user_name
        self.display_name = display_name
        self.unban_date = unban_date
        self.reason = reason

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)
    
class BanlistMapper:
    def insert(user: BanlistUser):
        if BanlistMapper.exists_mc_uuid(user.mc_uuid): 
            BanlistMapper.update(user)

        db = connect() 
        c = db.cursor()
        c.execute("INSERT INTO banlist VALUES (%s, %s, %s, %s, %s)", (user.id, user.qq_num, user.user_name, user.display_name, user.mc_uuid, user.last_login_time, user.remark))
        db.commit()

        db.close()

    def exists_mc_uuid(mc_uuid: str):
        db = connect()
        c = db.cursor()
        db.commit()
        c.execute("SELECT * FROM banlist WHERE mc_uuid=%s", (mc_uuid,))
        res = c.fetchall()

        db.close()

        return len(res) != 0

    def update(user: BanlistUser):
        db = connect() 
        c = db.cursor()
        c.execute("UPDATE banlist SET user_name=%s, display_name=%s, unban_date=%s, reason=%s WHERE mc_uuid=%s", (user.user_name, user.display_name, user.unban_date, user.reason, user.mc_uuid))
        db.commit()

        db.close()