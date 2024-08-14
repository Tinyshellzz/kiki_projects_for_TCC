import logging
from pathlib import Path
import yaml
from shutil import copyfile

# create logger with 'kiki_bot'
logger = logging.getLogger('kiki_bot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
plugin_dir = str(Path(__file__).resolve().parents[1])
print(plugin_dir)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler(plugin_dir + '/test.log', encoding='utf-8', mode="a")     # 最好每天生成一个新的 log
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

# 加载配置文件
data = None
project_dir = str(Path(__file__).resolve().parents[5])
config_file = Path(project_dir, 'config/config.yml')
if not config_file.is_file():
    copyfile(Path(project_dir, 'config/config-example.yml'),  config_file)
with open(config_file, 'r', encoding='utf8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

db_host=data['db_host']
db_port=int(data['db_port'])
db_user=data['db_user']
db_passwd=data['db_passwd']
db_database=data['db_database']
server_ip=data['server_ip']
rcon_port=data['rcon_port']
self_qq=data['self_qq']
rcon_password=data['rcon_password']
auth_group_list = data['auth_group_list']       # bot工作qq群, 这些群里的人必须都是服务器玩家
auth_qq_list = data['auth_qq_list']             # 部分命令允许的 qq号 (例如 /whitelist update)
code_prefix =  data['code_prefix']              # 白名单验证码前缀