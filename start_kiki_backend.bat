@echo off
title kiki_backend
call .\venv\Scripts\activate.bat

cd kiki_backend
python manage.py runserver 0.0.0.0:8000