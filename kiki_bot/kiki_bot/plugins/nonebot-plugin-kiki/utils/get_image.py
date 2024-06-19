from nonebot.adapters.onebot.v11 import Bot, Event
import re
import requests
import shutil

async def handle(bot: Bot, event: Event):
    msg = '[CQ:image,file=http://gchat.qpic.cn/gchatpic_new/3478848836/536038559-2716401382-6B98BD7054894D28C1DA2A72EEBA9412/0?term=255&amp;is_origin=0,url=http://gchat.qpic.cn/gchatpic_new/3478848836/536038559-2716401382-6B98BD7054894D28C1DA2A72EEBA9412/0?term=255&amp;is_origin=0,summary=&#91;图片&#93;]'
    
    file = re.search('^\[CQ:image,file=(.*)\]$', msg)
    file = file.groups()[0]

    response = requests.get(file, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response