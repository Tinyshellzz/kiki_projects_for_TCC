from ..config.db_config import *
import datetime

try:
    with connect() as db:
        with db.cursor() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS signdata (
                qq_num BigInt UNSIGNED,
                code Char(6),
                timestamp Datetime,
                KEY (qq_num),
                KEY(code)
            )
            """)
            db.commit()
except:
    pass


class SignUser:
    def __init__(self, qq_num, code, timestamp = datetime.datetime.now()):
        if timestamp != None:
            timestamp.strftime("%Y-%m-%d %H:%M:%S")
            timestamp = timestamp.replace(microsecond=0)

        self.qq_num = qq_num
        self.code = code
        self.timestamp = timestamp
    

class SignMapper:
    def insert(user: SignUser):
        with connect() as db:
            with db.cursor() as c:
                c.execute("INSERT INTO signdata VALUES (%s, %s, %s)", (user.qq_num, user.code, user.timestamp))
                db.commit()

    def get_sign_rank(qq_num):
        res = None
        now = datetime.datetime.now()
        now.strftime("%Y-%m-%d %H:%M:%S")
        now = now.replace(microsecond=0)

        today = now.replace(hour=0, minute=0, second=0)
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) FROM signdata WHERE timestamp<%s AND timestamp>%s", (now, today))
                res = c.fetchall()

        return res
    
    def is_signed(qq_num):
        res = None
        now = datetime.datetime.now()
        now.strftime("%Y-%m-%d %H:%M:%S")
        now = now.replace(microsecond=0)

        today = now.replace(hour=0, minute=0, second=0)
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM signdata WHERE qq_num=%s timestamp<%s AND timestamp>%s", (qq_num, now, today))
                res = c.fetchall()

        return len(res)!=0

