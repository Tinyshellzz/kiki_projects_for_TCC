
import pymysql
from ..config.config import *
import pymysqlpool

config = {'host': db_host, 'port': db_port, 'user': db_user, 'password': db_passwd, 'database': db_database, 'autocommit':False}
conn_pool = pymysqlpool.ConnectionPool(size=5, maxsize=10, pre_create_num=5, name='conn_pool', **config)
def connect():
    # return mysql.connector.connect(host = db_host, port = db_port, user = db_user, passwd = db_passwd, database = db_database)
    return conn_pool.get_connection()

