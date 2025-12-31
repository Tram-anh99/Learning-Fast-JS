#!/bin/bash

# ========== Start FastAPI Server ==========
# Script để khởi động backend server

echo "🚀 Starting FastAPI Backend Server..."
echo "====================================="

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found (.venv)"
    echo "   Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "   Installing dependencies..."
    pip install -r requirements-minimal.txt
fi

# Check dependencies
echo "🔍 Checking dependencies..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI not installed!"
    echo "   Installing dependencies..."
    pip install -r requirements-minimal.txt
fi

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Test database connection first
echo ""
echo "🔍 Testing database connection..."
python3 -c "from database import test_connection; test_connection()" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Database connection OK"
else
    echo "⚠️  Database connection failed, but continuing..."
fi

# Start server
echo ""
echo "🌐 Starting server on http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo "📖 ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop server"
echo ""

# Run uvicorn
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
