@echo off
echo 🚀 Starting Professional AI Assistant...
echo ======================================

REM Check if virtual environment exists
if not exist ".venv" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then: .venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Check if required packages are installed
python -c "import fastapi, uvicorn, google.generativeai" >nul 2>&1
if errorlevel 1 (
    echo ❌ Required packages not installed!
    echo Please run: pip install -r requirements.txt
    echo.
    echo 💡 Note: If PyAudio fails to install, voice features will be disabled
    echo    but the app will still work for text-based conversations.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo Create .env file with your API keys for full functionality
)

echo ✅ Starting backend server...
REM Start backend in background
start "AI Assistant Backend" python main.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo ✅ Starting GUI...
REM Start GUI
python modern_gui.py

echo 👋 Professional AI Assistant stopped.
pause
