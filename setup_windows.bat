@echo off
cd /d "%~dp0"
echo ============================================
echo TalentLens - One-time setup for Windows 11
echo ============================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Install Python 3.11 or 3.12 first.
  echo During installation, select the option to add Python to PATH.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  if errorlevel 1 goto fail
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto fail
pip install -r requirements.txt
if errorlevel 1 goto fail
echo.
echo Setup complete. Double-click run_windows.bat to start TalentLens.
pause
exit /b 0
:fail
echo.
echo Setup failed. Check the error above and confirm that your internet connection is working.
pause
exit /b 1
