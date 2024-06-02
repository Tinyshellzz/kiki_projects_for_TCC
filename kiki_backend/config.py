from pathlib import Path
import yaml


# 加载配置文件
data = None
project_dir = str(Path(__file__).resolve().parents[1])
with open(project_dir + '/config.yml', 'r', encoding='utf8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

serIP=data['server_ip']
serPort=data['server_port']
rconPort=data['rcon_port']
rconPw=data['rcon_password']