@echo off

title Creating Sayon Desktop Shortcut
echo Creating desktop shortcut for Sayon...

rem Get project root directory (parent of scripts)
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"
for %%i in ("%CURRENT_DIR%") do set "PROJECT_DIR=%%~dpi"
set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

rem Get desktop path - try multiple methods
set "DESKTOP=%USERPROFILE%\Desktop"
if not exist "%DESKTOP%" set "DESKTOP=%USERPROFILE%\桌面"
if not exist "%DESKTOP%" (
    for /f "tokens=3*" %%i in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%i %%j"
)

rem Expand environment variables in desktop path
call set "DESKTOP=%DESKTOP%"

echo Desktop path: %DESKTOP%
echo Scripts directory: %CURRENT_DIR%
echo Project directory: %PROJECT_DIR%

rem Create VBS script to create shortcut
echo Set WshShell = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%DESKTOP%\Sayon.lnk") >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.TargetPath = "%CURRENT_DIR%\start_hidden.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.WorkingDirectory = "%PROJECT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.Description = "Desktop Sayon - AI Desktop Pet" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.IconLocation = "%PROJECT_DIR%\assets\icon.ico,0" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.WindowStyle = 1 >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.Save >> "%TEMP%\CreateShortcut.vbs"

rem Execute VBS script to create shortcut
cscript //nologo "%TEMP%\CreateShortcut.vbs"

rem Clean up temporary VBS script
del "%TEMP%\CreateShortcut.vbs" 2>nul

if exist "%DESKTOP%\Sayon.lnk" (
    echo.
    echo   [SUCCESSFUL] Shortcut "Sayon" created successfully on desktop!
    echo   Target: %CURRENT_DIR%\start_hidden.bat
    echo   Working Directory: %PROJECT_DIR%
    echo   Icon: %PROJECT_DIR%\assets\icon.ico
    echo.
    echo You can now run Sayon by double-clicking the shortcut on your desktop.
) else (
    echo.
    echo [ERROR] Failed to create shortcut.
    echo Please check if you have permission to write to the desktop.
    echo You can manually create a shortcut to %CURRENT_DIR%\start_hidden.bat
)

echo.
echo Press any key to exit...
pause >nul
