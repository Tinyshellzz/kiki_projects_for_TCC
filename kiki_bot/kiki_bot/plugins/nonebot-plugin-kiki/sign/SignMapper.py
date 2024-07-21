from ..config.db_config import *
import datetime
import uuid
from datetime import timedelta
import threading

try:
    with connect() as db:
        with db.cursor() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS signdata (
                qq_num BigInt UNSIGNED,
                code Char(6),
                timestamp Datetime,
                redeemed Tinyint,
                KEY (qq_num),
                KEY(code)
            )
            """)
            db.commit()
except:
    pass

class SignUser:
    def __init__(self, qq_num, code, timestamp = datetime.datetime.now(), redeemed = 0):
        self.qq_num = qq_num
        self.code = code
        self.timestamp = timestamp.__str__()[:19]
        self.redeemed = redeemed

class SignMapper:
    def insert(user: SignUser):
        with connect() as db:
            with db.cursor() as c:
                c.execute("INSERT INTO signdata VALUES (%s, %s, %s, %s)", (user.qq_num, user.code, user.timestamp, user.redeemed))
                db.commit()

    def get_sign_rank(qq_num):
        res = None
        now = datetime.datetime.now()

        today = now.replace(hour=0, minute=0, second=0)
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) FROM signdata WHERE timestamp>=%s", (today))
                res = c.fetchall()

        return res[0][0]
    
    def is_signed(qq_num):
        res = None
        now = datetime.datetime.now()

        today = now.replace(hour=0, minute=0, second=0)
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM signdata WHERE qq_num=%s AND timestamp>=%s", (qq_num, today))
                res = c.fetchall()

        return len(res)!=0
    
    def get_sign_day(qq_num):
        res = None
        now = datetime.datetime.now()

        today = now.replace(hour=0, minute=0, second=0)
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) FROM signdata WHERE timestamp<=%s AND qq_num=%s", (today, qq_num))
                res = c.fetchall()

        return res[0][0]

    def generate_code(qq_num):
        code = uuid.uuid4().hex[:6]
        while SignMapper.exists_code(qq_num, code):
            code = uuid.uuid4().hex[:6]
        return code

    def exists_code(qq_num, code):
        res = None
        with connect() as db:
            with db.cursor() as c:
                c.execute("DELETE FROM signdata WHERE qq_num=%s AND code=%s", (qq_num, code))
                db.commit()
                res = c.fetchall()

        return len(res)!=0
    
    def clean_up():
        now = datetime.datetime.now()

        now_month = now.replace(day=1, hour=0, minute=0, second=0)
        now_day = now.replace(hour=0, minute=0, second=0)
        with connect() as db:
            with db.cursor() as c:
                c.execute("DELETE FROM signdata WHERE timestamp<%s", (now_month))
                db.commit()

# 定时清理数据库
def clean():
    SignMapper.clean_up()
    
    # 计算到第二天 0 点的秒数
    x = datetime.datetime.now()
    y = x + timedelta(days=1)
    y = y.replace(hour=0, minute=0, second=0, microsecond=0)
    secs = (y-x).total_seconds()
        
    threading.Timer(secs, clean).start()    # 每隔secs秒执行一次
clean()