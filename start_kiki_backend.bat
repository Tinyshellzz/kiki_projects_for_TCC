@echo off
title kiki_backend
Set  "anaconda_dir=E:\DevInstall\Anaconda"

call conda init
call conda activate mc
cd kiki_backend
python manage.py runserver