#!/bin/bash

###############################################################################
# STOP ALL SERVICES - Agriculture Management System
###############################################################################
# File: stop-all.sh
# Mục đích: Dừng tất cả services đang chạy
###############################################################################

echo "🛑 Stopping all services..."
echo "=========================="

###############################################################################
# FUNCTION: Kill process by PID from file
# Args: $1 - PID file path, $2 - service name
###############################################################################
kill_service() {
    local pid_file=$1
    local service_name=$2
    
    # Kiểm tra file PID có tồn tại không
    if [ -f "$pid_file" ]; then
        # Đọc PID từ file
        local pid=$(cat "$pid_file")
        
        # Kiểm tra process có đang chạy không
        if ps -p $pid > /dev/null 2>&1; then
            echo "   Stopping $service_name (PID: $pid)..."
            # Kill process
            kill -9 $pid 2>/dev/null || true
            echo "   ✅ $service_name stopped"
        else
            echo "   ⚠️  $service_name not running (PID $pid not found)"
        fi
        
        # Xóa file PID
        rm "$pid_file"
    else
        echo "   ⚠️  $service_name PID file not found"
    fi
}

###############################################################################
# FUNCTION: Kill process by port
# Args: $1 - port number, $2 - service name
###############################################################################
kill_port() {
    local port=$1
    local service_name=$2
    
    echo "   Checking port $port for $service_name..."
    
    # Tìm tất cả PIDs đang dùng port này
    local pids=$(lsof -ti :$port 2>/dev/null)
    
    if [ -n "$pids" ]; then
        echo "   Killing processes on port $port: $pids"
        echo "$pids" | xargs kill -9 2>/dev/null || true
        echo "   ✅ Port $port cleared"
    else
        echo "   ✅ Port $port already free"
    fi
}

###############################################################################
# STEP 1: Stop Backend (from PID file)
###############################################################################
echo ""
echo "1️⃣ Stopping Backend FastAPI..."
kill_service "logs/backend.pid" "Backend"

# Backup: Kill by port nếu PID không work
kill_port 8000 "Backend"

###############################################################################
# STEP 2: Stop Frontend (from PID file)
###############################################################################
echo ""
echo "2️⃣ Stopping Frontend Vite..."
kill_service "logs/frontend.pid" "Frontend"

# Backup: Kill by port
kill_port 5173 "Frontend"

# Vite thường spawn nhiều process, kill port 5174 nếu có
kill_port 5174 "Frontend (backup port)"

###############################################################################
# STEP 3: Database info (không tự động stop PostgreSQL)
###############################################################################
echo ""
echo "3️⃣ Database Status..."
echo "   ℹ️  PostgreSQL is NOT stopped (runs as system service)"
echo "   To stop manually: brew services stop postgresql@15"

###############################################################################
# STEP 4: Cleanup log files
###############################################################################
echo ""
echo "🧹 Cleaning up..."

# Hỏi user có muốn xóa logs không
read -p "   Delete log files? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f logs/*.log
    echo "   ✅ Log files deleted"
else
    echo "   ℹ️  Log files kept in logs/"
fi

###############################################################################
# STEP 5: Summary
###############################################################################
echo ""
echo "=========================="
echo "✅ All services stopped!"
echo "=========================="
echo ""
echo "📊 Current Status:"

# Check ports
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "   ⚠️  Port 8000: STILL IN USE"
else
    echo "   ✅ Port 8000: Free"
fi

if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "   ⚠️  Port 5173: STILL IN USE"
else
    echo "   ✅ Port 5173: Free"
fi

echo ""
echo "To start again: ./start-all.sh"
echo ""
