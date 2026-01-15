@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo Daily Screenshot Scheduler - %date% %time%
echo ========================================
echo This will run the job daily at 8:00 AM
echo Press Ctrl+C to stop the scheduler
echo ========================================

:: Activate virtual environment if exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: Run the scheduler from src/cron
python -m src.cron.scheduler

pause