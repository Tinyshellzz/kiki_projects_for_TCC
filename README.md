# kiki_projects_for_TCC
TCC 是一个国内的公益原版Minecraft服务器, 这个工程实现了群内的qq聊天机器人


## 1.配置conda运行环境
```bash
conda env create -f environment.yml
```

## 2.将 start_kiki_backend.bat 和 start_kiki_bot.bat 中的anaconda_dir，改为conda的安装位置
```bash
Set  "anaconda_dir=E:\DevInstall\Anaconda"
```

## 3.修改配置文件 config.yml

## 4.安装bukkit插件, 以使用白名单验证码功能
https://github.com/TinyShellzz/KikiWhitelist

## 5.运行工程
双击start_all.bat即可运行

## 6.登录你的QQ
第一次运行, 需要扫Lagrange.OneBot文件夹里的r-0.png.png

## 7.查看服务器 status
方法1: 输入网址 http://127.0.0.1:8000/mcstatus/ <br />
方法2: QQ群内输入 status

## 8.bot的其他使用方法
帮助文档：在qq中发送消息 help 
