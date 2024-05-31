import logging
from pathlib import Path
import mcrcon

# create logger with 'kiki_bot'
logger = logging.getLogger('kiki_bot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
plugin_dir = str(Path(__file__).resolve().parents[1])
fh = logging.FileHandler(plugin_dir + '/logs/kiki.log')     # 最好每天生成一个新的 log
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


serIP='127.0.0.1'
serPort=25565
rconPort=25575
rconPw='8888'
auth_group_list = {'536038559'}     # 部分命令允许的 qq群
auth_qq_list = {'3478848836'}   # 部分命令允许的 qq号 (例如 update_whitelist)