# kiki_projects_for_TCC
TCC 是一个国内的公益原版Minecraft服务器, 这个工程实现了群内的qq聊天机器人


## 配置conda运行环境
```bash
conda env create -f environment.yml
```

## 将 start_kiki_backend.bat 和 start_kiki_bot.bat 下面的部分，改为conda的安装位置
```bash
Set  "anaconda_dir=E:\DevInstall\Anaconda"
```

## 修改kiki_backend配置文件
serIP='127.0.0.1'  // mc服务器ip
serPort=25565    // mc服务器端口
rconPort=25575  // rcon端口
rconPw='8888'  // rcon密码

## 运行工程
双击start_all.bat即可运行

## 查看服务器 status
输入网址 http://127.0.0.1:8000/status/
