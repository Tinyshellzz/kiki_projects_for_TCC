
import mysql.connector
from ..config.config import *

def connect():
    return mysql.connector.connect(
    host = db_host,
    user = db_user,
    passwd = db_passwd,
    database = db_database)
