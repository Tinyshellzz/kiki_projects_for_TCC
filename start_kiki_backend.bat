title kiki_backend
Set  "anaconda_dir=E:\DevInstall\Anaconda"

call %anaconda_dir%/Scripts/activate.bat %anaconda_dir%
REM 切换conda虚拟环境。 如果你有自己的虚拟环境, 需要自行更改
call conda activate mc
cd kiki_backend
python manage.py runserver