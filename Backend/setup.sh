#!/bin/bash

# ========== Setup Backend Environment ==========
# Script tự động setup môi trường Backend

echo "🚀 Setting Up Backend Environment..."
echo "===================================="

# Step 1: Check Python
echo "1️⃣ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"

# Step 2: Create/Activate Virtual Environment
echo ""
echo "2️⃣ Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    echo "   Creating .venv..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate venv
source .venv/bin/activate
echo "✅ Activated .venv"

# Step 3: Upgrade pip
echo ""
echo "3️⃣ Upgrading pip..."
pip install --upgrade pip -q
echo "✅ Pip upgraded"

# Step 4: Install Dependencies
echo ""
echo "4️⃣ Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements-minimal.txt -q
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Step 5: Check .env file
echo ""
echo "5️⃣ Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env from .env.example"
    fi
else
    echo "✅ .env file exists"
fi

# Step 6: Test Database Connection
echo ""
echo "6️⃣ Testing database connection..."
python3 << EOF
try:
    from database import test_connection, get_table_count
    if test_connection():
        info = get_table_count()
        print(f"✅ Database connected: {info.get('count', 0)} tables in '{info.get('schema', 'unknown')}' schema")
    else:
        print("⚠️  Database connection failed - Check your credentials in .env")
except Exception as e:
    print(f"⚠️  Could not test database: {e}")
EOF

# Step 7: Done
echo ""
echo "=================================="
echo "✅ Backend setup completed!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env if needed (database credentials)"
echo "   2. Run: ./start.sh"
echo "   3. Open: http://localhost:8000/docs"
echo ""
echo "🔧 Useful commands:"
echo "   ./test_db.sh  - Test database connection"
echo "   ./start.sh    - Start development server"
echo "   python app.py - Start server manually"
