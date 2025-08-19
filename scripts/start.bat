@echo off
cd /d "%~dp0\.."
title Sayon
chcp 65001 > nul
if not "%1"=="min" start /min cmd /c "%~0" min & exit
echo Starting Desktop Sayon...
call venv\Scripts\activate
echo Virtual environment activated
echo Starting Desktop Sayon application...
python src\main.py
if %errorlevel% neq 0 (
    echo.
    echo Program ended with error code: %errorlevel%
    pause
)
