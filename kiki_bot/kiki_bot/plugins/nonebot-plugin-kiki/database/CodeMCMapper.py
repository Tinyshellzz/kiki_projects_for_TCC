from .db_config import *
import json
import datetime
import re

# codes_mc:
# user_name, code, mc_uuid, display_name, time
try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS codes_mc (
        code Char(6),
        user_name Varchar(48),
        display_name Varchar(48),
        mc_uuid Char(36),
        PRIMARY KEY (code),
        KEY (display_name),
        UNIQUE (mc_uuid)
    ) ENGINE=InnoDB CHARACTER SET=utf8;
    """)
    db.commit()
    c.close()
    db.close()
except:
    pass

class mc_code:
    def __init__(self, code, user_name, display_name, mc_uuid):
        self.code = code
        self.user_name = user_name
        self.display_name = display_name
        self.mc_uuid = mc_uuid

class CodeMCMapper:
    def get(code):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM codes_mc WHERE code=%s", (code,))
                res = c.fetchall()

        # 没找到
        if len(res) == 0:
            return None
        
        if res == None or len(res) == 0: return None
        r = res[0]
        return mc_code(r[0], r[1], r[2], r[3])