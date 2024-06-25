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
        source Varchar(100),
        unban_date Datetime,
        reason TEXT,
        PRIMARY KEY (mc_uuid),
        KEY (user_name),
        KEY (source)
    ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    db.commit()
    c.close()
    db.close()
except:
    pass

class BanlistUser:
    def __init__(self, mc_uuid, user_name, display_name, source: str, unban_date: datetime.datetime = None, reason:str = None):
        if unban_date != None:
            unban_date.strftime("%Y-%m-%d %H:%M:%S")
            unban_date = unban_date.replace(microsecond=0)

        self.mc_uuid = mc_uuid
        self.user_name = user_name
        self.display_name = display_name
        self.source = source
        self.unban_date = unban_date
        self.reason = reason

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)
    
class BanlistMapper:
    def insert(user: BanlistUser):
        if BanlistMapper.exists_mc_uuid(user.mc_uuid): 
            BanlistMapper.update(user)

        with connect() as db:
            with db.cursor() as c:
                c.execute("INSERT INTO banlist VALUES (%s, %s, %s, %s, %s, %s)", (user.mc_uuid, user.user_name, user.display_name, user.source, user.unban_date, user.reason))
                db.commit()

    def exists_mc_uuid(mc_uuid: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM banlist WHERE mc_uuid=%s", (mc_uuid,))
                res = c.fetchall()

        return len(res) != 0
    
    def get_user_by_mc_uuid(mc_uuid: str) -> BanlistUser:
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM banlist WHERE mc_uuid=%s", (mc_uuid,))
                res = c.fetchall()

        if len(res) == 0:
            return None
        r = res[0]
        return BanlistUser(r[0], r[1], r[2], r[3], r[4], r[5])

    def update(user: BanlistUser):
        with connect() as db:
            with db.cursor() as c:
                c.execute("UPDATE banlist SET user_name=%s, display_name=%s, source=%s, unban_date=%s, reason=%s WHERE mc_uuid=%s", (user.user_name, user.display_name, user.source, user.unban_date, user.reason, user.mc_uuid))
                db.commit()