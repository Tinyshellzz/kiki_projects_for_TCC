title start_all
cd "Lagrange.OneBot"
start /min "" "Lagrange.OneBot.exe" -i
cd ..
start /min "" cmd /k call "start_kiki_bot.bat" -i
start /min "" cmd /k call "start_kiki_backend.bat" -i