@echo off
REM Build tasbeeh_timer.exe using PyInstaller
echo Installing PyInstaller (if not already installed)...
pip install --user pyinstaller

echo Running PyInstaller to create one-file exe (using python -m PyInstaller)...
python -m PyInstaller --onefile --noconsole tasbeeh_timer.py

if exist dist\tasbeeh_timer.exe (
  echo EXE created at dist\tasbeeh_timer.exe
) else (
  echo Build failed. Check PyInstaller output above.
)

echo Done. Press any key to close.
pause
