@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Please run setup_windows.bat once before starting the app.
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"
echo Starting TalentLens. Keep this window open while using the app.
python app.py
pause
