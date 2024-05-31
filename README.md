# kiki_projects_for_TCC
TCC 是一个国内的公益原版Minecraft服务器, 这个工程实现了群内的qq聊天机器人


## 配置conda运行环境
```bash
conda env create -f environment.yml
```

## 将 start_kiki_backend.bat 和 start_kiki_bot.bat 中的anaconda_dir，改为conda的安装位置
```bash
Set  "anaconda_dir=E:\DevInstall\Anaconda"
```

## 修改kiki_backend配置文件
serIP='127.0.0.1'  // mc服务器ip <br />
serPort=25565    // mc服务器端口 <br />
rconPort=25575  // rcon端口 <br />
rconPw='8888'  // rcon密码

## 修改kiki_bot配置文件
位置: kiki_bot\kiki_bot\plugins\nonebot-plugin-kiki\config <br />
serIP='127.0.0.1'// mc服务器ip <br />
serPort=25565 // mc服务器端口 <br />
rconPort=25575// rcon端口 <br />
rconPw='8888' // rcon密码<br />
auth_group_list = {'536038559'}     # 部分命令允许的 qq群<br />
auth_qq_list = {'3478848836'}   # 部分命令允许的 qq号 (例如 update_whitelist)

## 运行工程
双击start_all.bat即可运行

## 登录你的QQ
第一次运行, 需要扫Lagrange.OneBot文件夹里的qr.png

## 查看服务器 status
方法1: 输入网址 http://127.0.0.1:8000/status/ <br />
方法2: QQ群内输入 status
