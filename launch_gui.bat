@echo off
echo ================================
echo    Story Video Creator GUI
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist ".venv\Scripts\Activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\Activate.bat
)

REM Check if required packages are installed
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo Error: tkinter is not available
    echo Please install Python with tkinter support
    pause
    exit /b 1
)

echo Starting Story Video Creator GUI...
echo Close this window to exit the application.
echo.

REM Launch the GUI
python story_video_gui.py

echo.
echo GUI application closed.
pause
