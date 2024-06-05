import mcrcon
from mcstatus import JavaServer
from time import sleep
import config
import re
import logging
import psutil
import sys
import time

logger = logging.getLogger(__name__)
# 获取服务器 tps
def get_tps():
    tps_value = None
    rcon = mcrcon.MCRcon(config.serIP, config.rconPw, config.rconPort, timeout=2)
    try:
        rcon.connect()
        response = rcon.command('tps')
        match = re.search("Median Region TPS:.*?([0-9]{1,2}\.[0-9]+)", response)
        tps_value = match.groups()[0]
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()
    return tps_value

def get_system_status():
    # 获取 CPU 状态
    cpu_usage = psutil.cpu_percent()
    time.sleep(0.1)
    cpu_usage = psutil.cpu_percent()
    cpu_usage = '{0}%'.format(cpu_usage)
    # 获取 内存 状态
    memory_status = psutil.virtual_memory()
    memory_usage = memory_status.percent
    memory_used = memory_status.used / (1024 ** 3)
    memory_status = '{0:.2f}GB | {1}%'.format(memory_used, memory_usage)
    # 获取 网络 状态
    last_received = psutil.net_io_counters().bytes_recv
    last_sent = psutil.net_io_counters().bytes_sent
    sleep(1)
    now_received = psutil.net_io_counters().bytes_recv - last_received
    now_sent = psutil.net_io_counters().bytes_sent - last_sent
    net_IO = "{0:.2f} | {1:.2f}/Mbps".format(now_received/1024/128, now_sent/1024/128)
    return {'cpu_usage': cpu_usage, "memory_status": memory_status, "net_IO": net_IO}


# 获取 (在线人数, 查询延迟, 服务器版本)
def get_mc_status():
    try:
        server = JavaServer.lookup('{0}:{1}'.format(config.serIP, config.serPort), 200)
        serstatus = server.status()
        onlinePlayers = serstatus.players.online
        queryLatency = round(serstatus.latency, 3)  # 保留三位小数
        version = serstatus.version.name.replace(' ', '-')
        return {'onlinePlayers': onlinePlayers, 'queryLatency': queryLatency, 'version': version}
    except Exception as e:
        logger.warning(e)
    
    return {'onlinePlayers': None, 'queryLatency': None, 'version': None}

def get_online_players():
    online = None
    rcon = mcrcon.MCRcon(config.serIP, config.rconPw, config.rconPort, timeout=2)
    try:
        rcon.connect()
        response = rcon.command('tps')
        match = re.search("(.*)", response)
        online = match.groups()[0]
    except Exception as e:
        logger.warning(e)
    finally:
        rcon.disconnect()
    return {"online": online}