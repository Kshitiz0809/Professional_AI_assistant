#!/bin/bash
# Professional AI Assistant Startup Script

echo "🚀 Starting Professional AI Assistant..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv .venv"
    echo "Then: source .venv/bin/activate (or .venv\\Scripts\\activate on Windows)"
    echo "Then: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    source .venv/Scripts/activate
else
    # macOS/Linux
    source .venv/bin/activate
fi

# Check if required packages are installed
python -c "import fastapi, uvicorn, google.generativeai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required packages not installed!"
    echo "Please run: pip install -r requirements.txt"
    echo ""
    echo "💡 Note: If PyAudio fails to install, voice features will be disabled"
    echo "   but the app will still work for text-based conversations."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Create .env file with your API keys for full functionality"
fi

echo "✅ Starting backend server..."
# Start backend in background
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo "✅ Starting GUI..."
# Start GUI
python modern_gui.py

# Cleanup: Kill backend when GUI closes
echo "🔄 Shutting down backend server..."
kill $BACKEND_PID 2>/dev/null
echo "👋 Professional AI Assistant stopped."
