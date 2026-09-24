@echo off
echo ==========================================
echo Conventor Build Script (PyInstaller)
echo ==========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if %errorlevel% neq 0 (
    echo PyInstaller is not installed. Installing...
    pip install -r requirements-build.txt
)

echo Cleaning previous builds...
rmdir /s /q build 2>NUL
rmdir /s /q dist 2>NUL
del /f /q Conventor.spec 2>NUL
del /f /q main.spec 2>NUL

echo.
echo Building executable with PyInstaller...
echo This might take a few moments...
echo.

python -m PyInstaller --noconfirm --onefile --windowed --icon=assets/icons/icon.ico --name=Conventor --add-data "assets;assets" --add-data "ui/qml;ui/qml" --hidden-import=PIL --hidden-import=PySide6.QtQuick --hidden-import=PySide6.QtQml --hidden-import=PySide6.QtSvg main.py

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo Build SUCCESSFUL!
    echo Executable is located in: dist\Conventor.exe
    echo You can move this file anywhere and run it.
    echo ==========================================
) else (
    echo.
    echo Build FAILED. Please check the errors above.
)
pause
