from pathlib import Path
import yaml
from shutil import copyfile


# 加载配置文件
data = None
project_dir = str(Path(__file__).resolve().parents[1])
config_file = Path(project_dir, 'config/config.yml')
if not config_file.is_file():
    copyfile(Path(project_dir, 'config/config-example.yml'),  config_file)
with open(config_file, 'r', encoding='utf8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

server_ip=data['server_ip']
server_port=data['server_port']
rcon_port=data['rcon_port']
rcon_password=data['rcon_password']