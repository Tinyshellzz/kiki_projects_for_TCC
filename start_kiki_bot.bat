@echo off
title kiki_bot
Set  "anaconda_dir=E:\DevInstall\Anaconda"

call conda init
call conda activate mc
cd kiki_bot
nb run