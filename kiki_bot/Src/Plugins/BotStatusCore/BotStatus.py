from datetime import datetime
from nonebot.adapters.onebot.v11 import MessageEvent, Bot, MessageSegment
from nonebot.plugin import on_command
import psutil

start_time = datetime.now()

cooldown_dict = {}
botstatus = on_command("bot")


@botstatus.handle()
async def handle_status(bot: Bot, event: MessageEvent):
    now = datetime.now()
    user_id = str(event.user_id)

    # 检查用户是否处于冷却时间内
    if user_id in cooldown_dict:
        last_call = cooldown_dict[user_id]
        time_diff = (now - last_call).total_seconds()
        if time_diff < 20:
            last_time_diff = 20 - int(time_diff)
            await bot.send(event, f"此命令处于冷却中喵，请{last_time_diff}秒后再试")
            return

    def get_cpu_cores():
        return psutil.cpu_count(logical=False)

    def get_cpu_usage():
        cpu_usage = psutil.cpu_percent(interval=1)
        return f"{cpu_usage}%"

    def get_memory_usage():
        memory_status = psutil.virtual_memory()
        memory_usage = memory_status.percent
        memory_used = memory_status.used / (1024 ** 3)
        return f"{memory_used:.1f}GB | {memory_usage}%"

    def get_total_run_time():
        global start_time
        end_time = datetime.now()
        total_run_time = end_time - start_time
        return total_run_time.total_seconds()

    cpu_cores = get_cpu_cores()
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    total_run_time = get_total_run_time()

    message = (
        f"【KiKi运行状态喵(/≧▽≦)/】\n"
        f"-----------\n"
        f"KiKi-Bot总运行时间:{total_run_time:.1f}秒\n"
        f"CPU核心数量:{cpu_cores}\n"
        f"CPU使用率:{cpu_usage}\n"
        f"内存使用率:{memory_usage}\n"
        f"-----------\n"
        f"如果本Ki还活着,此消息一定会出来的，使用/bot命令没有回复就是炸力\n"
        f"-----------"
    )

    await bot.send(event, MessageSegment.text(message))

    # 如果用户不在冷却时间内，更新最后调用时间为当前时间
    cooldown_dict[user_id] = now
