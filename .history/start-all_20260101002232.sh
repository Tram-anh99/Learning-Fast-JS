#!/bin/bash

###############################################################################
# START ALL SERVICES - Agriculture Management System
###############################################################################
# File: start-all.sh
# Mục đích: Khởi động đồng thời cả 3 services:
#   1. PostgreSQL Database (port 5433)
#   2. Backend FastAPI (port 8000)
#   3. Frontend Vite (port 5173)
###############################################################################

echo "🚀 Starting Agriculture Management System..."
echo "==========================================="
echo ""

###############################################################################
# FUNCTION: Check if port is in use
# Args: $1 - port number
# Returns: 0 if free, 1 if in use
###############################################################################
check_port() {
    local port=$1
    # Sử dụng lsof để kiểm tra port có đang được dùng không
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port đang được dùng
    else
        return 0  # Port trống
    fi
}

###############################################################################
# FUNCTION: Kill process on port
# Args: $1 - port number
###############################################################################
kill_port() {
    local port=$1
    echo "   Killing process on port $port..."
    # Tìm và kill tất cả process đang dùng port
    lsof -ti :$port | xargs kill -9 2>/dev/null || true
    sleep 1  # Đợi 1 giây cho process dừng hoàn toàn
}

###############################################################################
# STEP 1: Check PostgreSQL Database
###############################################################################
echo "1️⃣ Checking PostgreSQL Database..."
echo "-----------------------------------"

# Kiểm tra PostgreSQL có cài đặt không
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL chưa cài đặt!"
    echo "   Install: brew install postgresql@15"
    exit 1
fi

# Kiểm tra PostgreSQL service có đang chạy không
if ! brew services list | grep postgresql | grep started &> /dev/null; then
    echo "⚠️  PostgreSQL service chưa chạy"
    echo "   Starting PostgreSQL..."
    brew services start postgresql@15
    sleep 3  # Đợi service khởi động
fi

# Kiểm tra port 5433
if check_port 5433; then
    echo "⚠️  Port 5433 chưa có PostgreSQL"
    echo "   Checking port 5432..."
    if ! check_port 5432; then
        echo "✅ PostgreSQL đang chạy trên port 5432"
        echo "   (Update .env: DB_PORT=5432)"
    fi
else
    echo "✅ PostgreSQL running on port 5433"
fi

###############################################################################
# STEP 2: Start Backend FastAPI
###############################################################################
echo ""
echo "2️⃣ Starting Backend FastAPI..."
echo "-----------------------------------"

# Chuyển vào thư mục Backend
cd Backend || exit 1

# Kiểm tra và kill port 8000 nếu đang dùng
if ! check_port 8000; then
    echo "⚠️  Port 8000 is already in use"
    kill_port 8000
fi

# Kiểm tra virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: ./setup.sh first"
    exit 1
fi

# Activate virtual environment và start server trong background
echo "   Starting FastAPI server on port 8000..."
.venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 --reload > ../logs/backend.log 2>&1 &
BACKEND_PID=$!  # Lưu Process ID để kill sau này
echo "   Backend PID: $BACKEND_PID"

# Đợi backend khởi động
echo "   Waiting for backend to start..."
sleep 3

# Test backend health
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend API running on http://localhost:8000"
    echo "   📚 API Docs: http://localhost:8000/docs"
else
    echo "❌ Backend failed to start! Check logs/backend.log"
    exit 1
fi

# Quay về root directory
cd ..

###############################################################################
# STEP 3: Start Frontend Vite
###############################################################################
echo ""
echo "3️⃣ Starting Frontend Vite..."
echo "-----------------------------------"

# Chuyển vào thư mục Frontend
cd Frontend || exit 1

# Kiểm tra node_modules
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found!"
    echo "   Installing dependencies..."
    npm install
fi

# Kiểm tra và kill port 5173 nếu đang dùng
if ! check_port 5173; then
    echo "⚠️  Port 5173 is already in use"
    kill_port 5173
fi

# Start Vite dev server trong background
echo "   Starting Vite dev server on port 5173..."
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!  # Lưu Process ID
echo "   Frontend PID: $FRONTEND_PID"

# Đợi frontend khởi động
echo "   Waiting for frontend to start..."
sleep 5

# Test frontend
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "✅ Frontend running on http://localhost:5173"
else
    echo "❌ Frontend failed to start! Check logs/frontend.log"
    exit 1
fi

# Quay về root directory
cd ..

###############################################################################
# STEP 4: Summary & Instructions
###############################################################################
echo ""
echo "==========================================="
echo "✅ ALL SERVICES STARTED SUCCESSFULLY!"
echo "==========================================="
echo ""
echo "📊 Service Status:"
echo "   🗄️  Database:  PostgreSQL (localhost:5433)"
echo "   ⚙️  Backend:   FastAPI     (http://localhost:8000)"
echo "   🎨 Frontend:  Vite        (http://localhost:5173)"
echo ""
echo "🔗 Quick Links:"
echo "   🌐 Application:  http://localhost:5173"
echo "   📚 API Docs:     http://localhost:8000/docs"
echo "   🏥 Health Check: http://localhost:8000/api/health"
echo ""
echo "📝 Process IDs:"
echo "   Backend:  $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 To stop all services:"
echo "   ./stop-all.sh"
echo "   or press Ctrl+C"
echo ""
echo "==========================================="
echo "🎉 Ready to use! Open http://localhost:5173"
echo "==========================================="

###############################################################################
# STEP 5: Save PIDs to file for stop script
###############################################################################
# Tạo thư mục logs nếu chưa có
mkdir -p logs

# Lưu PIDs vào file để script stop-all.sh có thể dùng
echo "$BACKEND_PID" > logs/backend.pid
echo "$FRONTEND_PID" > logs/frontend.pid

###############################################################################
# STEP 6: Wait for user interrupt (Ctrl+C)
###############################################################################
# Trap Ctrl+C để cleanup khi user dừng script
trap 'echo ""; echo "🛑 Stopping all services..."; ./stop-all.sh; exit' INT

# Giữ script chạy, theo dõi logs realtime
echo "📊 Monitoring logs (press Ctrl+C to stop all services)..."
echo ""

# Tail logs từ cả 2 services
tail -f logs/backend.log logs/frontend.log
