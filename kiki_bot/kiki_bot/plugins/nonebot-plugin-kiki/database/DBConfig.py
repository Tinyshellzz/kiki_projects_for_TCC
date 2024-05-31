import sqlite3
from pathlib import Path
from threading import Lock

plugin_dir = str(Path(__file__).resolve().parents[1])
conn = sqlite3.connect(plugin_dir + '/database/user.db')
dblock = Lock()