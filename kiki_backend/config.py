from pathlib import Path
import yaml


# 加载配置文件
data = None
project_dir = str(Path(__file__).resolve().parents[1])
with open(project_dir + '/config.yml', 'r', encoding='utf8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

server_ip=data['server_ip']
server_port=data['server_port']
rcon_port=data['rcon_port']
rcon_password=data['rcon_password']