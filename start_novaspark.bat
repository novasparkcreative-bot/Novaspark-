@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py run_novaspark.py
) else (
  python run_novaspark.py
)
pause
