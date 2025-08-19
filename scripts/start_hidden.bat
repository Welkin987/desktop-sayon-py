@echo off
cd /d "%~dp0"
powershell -WindowStyle Hidden -Command "& {Start-Process cmd -ArgumentList '/c \"%~dp0start.bat\"' -WindowStyle Minimized}"
