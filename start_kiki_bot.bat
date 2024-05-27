@echo off
Set  "anaconda_dir=E:\DevInstall\Anaconda"

cd "Lagrange.OneBot"
start /min "" "Lagrange.OneBot.exe" -i
cd ..
call %anaconda_dir%/Scripts/activate.bat %anaconda_dir%
REM "切换conda虚拟环境。 如果你有自己的虚拟环境, 需要自行更改"
call conda activate mc
cd kiki_bot
nb run