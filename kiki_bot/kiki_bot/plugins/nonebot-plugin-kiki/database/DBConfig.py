import sqlite3
from pathlib import Path
from threading import Lock
from ..config.config import *

plugin_dir = str(Path(__file__).resolve().parents[5])
conn = sqlite3.connect(plugin_dir + '/user.db')
dblock = Lock()

conn_codes = sqlite3.connect(kiki_whitelist_db)