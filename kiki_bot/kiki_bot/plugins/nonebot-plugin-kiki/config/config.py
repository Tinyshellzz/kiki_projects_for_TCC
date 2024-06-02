import logging
from pathlib import Path
import yaml

# create logger with 'kiki_bot'
logger = logging.getLogger('kiki_bot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
plugin_dir = str(Path(__file__).resolve().parents[1])
fh = logging.FileHandler(plugin_dir + '/logs/kiki.log', encoding='utf-8', mode="a")     # 最好每天生成一个新的 log
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# 加载配置文件
data = None
project_dir = str(Path(__file__).resolve().parents[5])
with open(project_dir + '/config.yml', 'r', encoding='utf8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

serIP=data['server_ip']
serPort=data['server_port']
rconPort=data['rcon_port']
rconPw=data['rcon_password']
server_whitelist=data['server_whitelist']     # 服务器白名单位置
auth_group_list = data['auth_group_list']       # bot工作qq群, 这些群里的人必须都是服务器玩家
auth_qq_list = data['auth_qq_list']             # 部分命令允许的 qq号 (例如 /whitelist update)
code_prefix =  data['code_prefix']              # 白名单验证码前缀
kiki_whitelist_db = data['kiki_whitelist_db']   # mc白名单数据库的位置