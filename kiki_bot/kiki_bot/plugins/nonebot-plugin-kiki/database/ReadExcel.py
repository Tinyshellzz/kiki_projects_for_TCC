# 读取 excels 文件夹里面的 Excel
import pandas as pd
from pathlib import Path
import os
from os import listdir
from os.path import isfile, join
from .UserMapper import User, UserMapper
from .UserMCMapper import MCUser, UserMCMapper
from ..config.config import *

project_dir = str(Path(__file__).resolve().parents[5])
excels_dir = project_dir + '/excels'

def read_excel(fpath):
    xls = pd.read_excel(fpath)
    ret = []

    for index, row in xls.iterrows():
        # 将所有通过的都插入数据库
        if row['passed'] == '☑':
            email = row['qq_num'] + "@qq.com"
            if(UserMapper.exits_email_user(email=email)):
                user = UserMapper.get_user_by_email(email)
                id = user.id
            else:
                id = UserMapper.insert(User(email=email, permission=1))
            id = UserMapper.insert(User(email=email, permission=1))
            UserMCMapper.insert(MCUser(id, email))
            ret.append(row)
    
    return ret


# 读取 excels_dir 下所有的文件, 读完后就删除
def read_excels():
    excels = []
    for f in listdir(excels_dir):
        filename, file_extension = os.path.splitext(f)
        file = join(excels_dir, f)
        if isfile(file) and (file_extension == '.xlsx' or file_extension == '.xls') and f != 'example.xlsx':
            excels.append(file)

    ret = []
    for e in excels:
        ret.extend(read_excel(e))
        # 删除读完的 excel
        os.remove(e)

    return ret







