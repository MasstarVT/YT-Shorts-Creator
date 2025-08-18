@echo off
echo ================================
echo    Story Video Creator
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

REM Check if required packages are installed
echo Checking dependencies...
python -c "import moviepy" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Dependencies OK!
echo.

REM Check for required arguments
if "%~3"=="" (
    echo Usage: run_story_creator.bat ^<story_file^> ^<video_folder^> ^<output_file^>
    echo.
    echo Example:
    echo run_story_creator.bat sample_story.txt backgrounds\ my_video.mp4
    echo.
    pause
    exit /b 1
)

REM Run the main program
echo Running Story Video Creator...
echo Story: %1
echo Videos: %2
echo Output: %3
echo.

python story_video_creator.py "%~1" "%~2" "%~3"

if errorlevel 1 (
    echo.
    echo Error: Program failed to complete
) else (
    echo.
    echo Success! Video created: %3
)

echo.
pause
