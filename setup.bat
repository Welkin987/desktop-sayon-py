@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! 
echo 1. Configure your API key in config\config.ini
echo 2. Run start.bat to launch Desktop Sayon
pause
