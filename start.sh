#!/bin/bash

##############################################################################
# Hệ Thống Quản Lý Nông Nghiệp & Truy Xuất Nguồn Gốc
# Startup Script - One Command to Rule Them All
# 
# Usage: ./start.sh [option]
# Options:
#   dev     - Start development environment (default)
#   prod    - Start production environment
#   stop    - Stop all services
#   restart - Restart all services
#   status  - Check service status
#   logs    - Show logs
#   backup  - Backup database
#   help    - Show this help
#
# Author: Development Team
# Date: January 10, 2026
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="Agricultural Management System"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/Backend"
FRONTEND_DIR="$PROJECT_DIR/Frontend"
DATABASE_DIR="$PROJECT_DIR/Database"

BACKEND_PORT=8000
FRONTEND_PORT=5173
DB_PORT=5432

BACKEND_PID_FILE="/tmp/agri_backend.pid"
FRONTEND_PID_FILE="/tmp/agri_frontend.pid"

LOG_DIR="$PROJECT_DIR/logs"
BACKUP_DIR="$PROJECT_DIR/backups"

# Create directories if not exist
mkdir -p "$LOG_DIR"
mkdir -p "$BACKUP_DIR"

##############################################################################
# Utility Functions
##############################################################################

print_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║   🌾 Hệ Thống Quản Lý Nông Nghiệp & Truy Xuất Nguồn Gốc   ║"
    echo "║                                                            ║"
    echo "║   Version: 2.0                                             ║"
    echo "║   Date: January 10, 2026                                   ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

##############################################################################
# Check Functions
##############################################################################

check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is not installed"
        return 1
    fi
    print_success "$1 is installed"
    return 0
}

check_prerequisites() {
    print_step "Checking prerequisites..."
    
    local all_ok=true
    
    # Check Python
    if check_command python3 || check_command python; then
        PYTHON_CMD=$(command -v python3 || command -v python)
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        print_info "Python version: $PYTHON_VERSION"
    else
        all_ok=false
    fi
    
    # Check Node.js
    if check_command node; then
        NODE_VERSION=$(node --version)
        print_info "Node.js version: $NODE_VERSION"
    else
        all_ok=false
    fi
    
    # Check npm
    if check_command npm; then
        NPM_VERSION=$(npm --version)
        print_info "npm version: $NPM_VERSION"
    else
        all_ok=false
    fi
    
    # Check PostgreSQL
    if check_command psql; then
        PSQL_VERSION=$(psql --version | awk '{print $3}')
        print_info "PostgreSQL version: $PSQL_VERSION"
    else
        print_warning "PostgreSQL client not found. Database connection may fail."
    fi
    
    # Check conda (optional)
    if check_command conda; then
        print_info "Conda available: Will use conda environment"
        USE_CONDA=true
    else
        print_info "Conda not available: Using system Python"
        USE_CONDA=false
    fi
    
    if [ "$all_ok" = false ]; then
        print_error "Prerequisites check failed!"
        echo ""
        echo "Please install missing requirements:"
        echo "  - Python 3.8+: https://www.python.org/"
        echo "  - Node.js 18+: https://nodejs.org/"
        echo "  - PostgreSQL 16+: https://www.postgresql.org/"
        exit 1
    fi
    
    print_success "All prerequisites satisfied"
    echo ""
}

check_database() {
    print_step "Checking database connection..."
    
    # Try to connect to database
    if psql -U postgres -d nongsan_db -c "SELECT 1" &> /dev/null; then
        print_success "Database connection OK"
        
        # Get table count
        TABLE_COUNT=$(psql -U postgres -d nongsan_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'nongsan'" 2>/dev/null | tr -d ' ')
        print_info "Found $TABLE_COUNT tables in schema 'nongsan'"
        return 0
    else
        print_warning "Cannot connect to database 'nongsan_db'"
        print_info "Make sure PostgreSQL is running and database exists"
        print_info "Create database: createdb -U postgres nongsan_db"
        return 1
    fi
}

##############################################################################
# Service Management Functions
##############################################################################

start_backend() {
    print_step "Starting Backend (FastAPI)..."
    
    cd "$BACKEND_DIR"
    
    # Check if already running
    if [ -f "$BACKEND_PID_FILE" ] && kill -0 $(cat "$BACKEND_PID_FILE") 2>/dev/null; then
        print_warning "Backend is already running (PID: $(cat $BACKEND_PID_FILE))"
        return 0
    fi
    
    # Install dependencies if needed
    if [ ! -d "venv" ] && [ "$USE_CONDA" = false ]; then
        print_step "Creating Python virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        print_step "Installing Python dependencies..."
        pip install -r requirements-minimal.txt
    fi
    
    # Activate environment
    if [ "$USE_CONDA" = true ]; then
        print_info "Using conda environment"
        source /opt/anaconda3/bin/activate
        PYTHON_CMD="/opt/anaconda3/bin/python"
    elif [ -d "venv" ]; then
        source venv/bin/activate
        PYTHON_CMD="python"
    else
        PYTHON_CMD="python3"
    fi
    
    # Start server
    print_info "Starting Uvicorn server on port $BACKEND_PORT..."
    nohup $PYTHON_CMD -m uvicorn app:app --host 0.0.0.0 --port $BACKEND_PORT --reload \
        > "$LOG_DIR/backend.log" 2>&1 &
    
    BACKEND_PID=$!
    echo $BACKEND_PID > "$BACKEND_PID_FILE"
    
    # Wait for server to start
    sleep 3
    
    # Check if server is running
    if kill -0 $BACKEND_PID 2>/dev/null; then
        print_success "Backend started successfully (PID: $BACKEND_PID)"
        print_info "API URL: http://localhost:$BACKEND_PORT"
        print_info "API Docs: http://localhost:$BACKEND_PORT/docs"
        print_info "Logs: $LOG_DIR/backend.log"
    else
        print_error "Failed to start backend"
        print_info "Check logs: tail -f $LOG_DIR/backend.log"
        return 1
    fi
}

start_frontend() {
    print_step "Starting Frontend (Vue.js + Vite)..."
    
    cd "$FRONTEND_DIR"
    
    # Check if already running
    if [ -f "$FRONTEND_PID_FILE" ] && kill -0 $(cat "$FRONTEND_PID_FILE") 2>/dev/null; then
        print_warning "Frontend is already running (PID: $(cat $FRONTEND_PID_FILE))"
        return 0
    fi
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_step "Installing npm dependencies..."
        npm install
    fi
    
    # Start dev server
    print_info "Starting Vite dev server on port $FRONTEND_PORT..."
    nohup npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
    
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$FRONTEND_PID_FILE"
    
    # Wait for server to start
    sleep 5
    
    # Check if server is running
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        print_success "Frontend started successfully (PID: $FRONTEND_PID)"
        print_info "App URL: http://localhost:$FRONTEND_PORT"
        print_info "Logs: $LOG_DIR/frontend.log"
    else
        print_error "Failed to start frontend"
        print_info "Check logs: tail -f $LOG_DIR/frontend.log"
        return 1
    fi
}

stop_backend() {
    print_step "Stopping Backend..."
    
    if [ -f "$BACKEND_PID_FILE" ]; then
        PID=$(cat "$BACKEND_PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            rm "$BACKEND_PID_FILE"
            print_success "Backend stopped"
        else
            print_warning "Backend not running"
            rm "$BACKEND_PID_FILE"
        fi
    else
        print_warning "Backend PID file not found"
    fi
    
    # Force kill uvicorn if still running
    pkill -f "uvicorn app:app" 2>/dev/null || true
}

stop_frontend() {
    print_step "Stopping Frontend..."
    
    if [ -f "$FRONTEND_PID_FILE" ]; then
        PID=$(cat "$FRONTEND_PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            rm "$FRONTEND_PID_FILE"
            print_success "Frontend stopped"
        else
            print_warning "Frontend not running"
            rm "$FRONTEND_PID_FILE"
        fi
    else
        print_warning "Frontend PID file not found"
    fi
    
    # Force kill vite if still running
    pkill -f "vite" 2>/dev/null || true
}

check_service_status() {
    echo ""
    print_step "Service Status:"
    echo ""
    
    # Backend status
    if [ -f "$BACKEND_PID_FILE" ] && kill -0 $(cat "$BACKEND_PID_FILE") 2>/dev/null; then
        print_success "Backend: Running (PID: $(cat $BACKEND_PID_FILE))"
        echo "         URL: http://localhost:$BACKEND_PORT"
        echo "         Docs: http://localhost:$BACKEND_PORT/docs"
    else
        print_error "Backend: Not running"
    fi
    
    # Frontend status
    if [ -f "$FRONTEND_PID_FILE" ] && kill -0 $(cat "$FRONTEND_PID_FILE") 2>/dev/null; then
        print_success "Frontend: Running (PID: $(cat $FRONTEND_PID_FILE))"
        echo "          URL: http://localhost:$FRONTEND_PORT"
    else
        print_error "Frontend: Not running"
    fi
    
    # Database status
    if psql -U postgres -d nongsan_db -c "SELECT 1" &> /dev/null; then
        print_success "Database: Connected"
    else
        print_error "Database: Not connected"
    fi
    
    echo ""
}

show_logs() {
    echo ""
    print_step "Recent Logs:"
    echo ""
    
    if [ -f "$LOG_DIR/backend.log" ]; then
        echo -e "${BLUE}=== Backend Logs (last 20 lines) ===${NC}"
        tail -n 20 "$LOG_DIR/backend.log"
        echo ""
    fi
    
    if [ -f "$LOG_DIR/frontend.log" ]; then
        echo -e "${BLUE}=== Frontend Logs (last 20 lines) ===${NC}"
        tail -n 20 "$LOG_DIR/frontend.log"
        echo ""
    fi
    
    print_info "To tail logs continuously:"
    echo "  Backend:  tail -f $LOG_DIR/backend.log"
    echo "  Frontend: tail -f $LOG_DIR/frontend.log"
    echo ""
}

backup_database() {
    print_step "Backing up database..."
    
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/nongsan_db_$TIMESTAMP.sql"
    
    if pg_dump -U postgres -d nongsan_db > "$BACKUP_FILE"; then
        print_success "Database backup created: $BACKUP_FILE"
        
        # Compress backup
        gzip "$BACKUP_FILE"
        print_success "Backup compressed: ${BACKUP_FILE}.gz"
        
        # Show backup size
        BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
        print_info "Backup size: $BACKUP_SIZE"
    else
        print_error "Database backup failed"
        return 1
    fi
}

##############################################################################
# Main Commands
##############################################################################

cmd_dev() {
    print_header
    print_info "Starting development environment..."
    echo ""
    
    check_prerequisites
    check_database
    
    echo ""
    start_backend
    
    echo ""
    start_frontend
    
    echo ""
    print_success "🎉 System started successfully!"
    echo ""
    print_info "Access points:"
    echo "  📱 Frontend: http://localhost:$FRONTEND_PORT"
    echo "  🔧 Backend API: http://localhost:$BACKEND_PORT"
    echo "  📚 API Docs: http://localhost:$BACKEND_PORT/docs"
    echo ""
    print_info "To stop all services: ./start.sh stop"
    print_info "To check status: ./start.sh status"
    print_info "To view logs: ./start.sh logs"
    echo ""
}

cmd_stop() {
    print_header
    print_info "Stopping all services..."
    echo ""
    
    stop_backend
    stop_frontend
    
    echo ""
    print_success "All services stopped"
    echo ""
}

cmd_restart() {
    print_header
    print_info "Restarting all services..."
    echo ""
    
    cmd_stop
    sleep 2
    cmd_dev
}

cmd_status() {
    print_header
    check_service_status
}

cmd_logs() {
    print_header
    show_logs
}

cmd_backup() {
    print_header
    backup_database
    echo ""
}

cmd_help() {
    print_header
    echo "Usage: ./start.sh [option]"
    echo ""
    echo "Options:"
    echo "  dev      Start development environment (default)"
    echo "  stop     Stop all services"
    echo "  restart  Restart all services"
    echo "  status   Check service status"
    echo "  logs     Show recent logs"
    echo "  backup   Backup database"
    echo "  help     Show this help"
    echo ""
    echo "Examples:"
    echo "  ./start.sh              # Start dev environment"
    echo "  ./start.sh dev          # Same as above"
    echo "  ./start.sh stop         # Stop all services"
    echo "  ./start.sh status       # Check what's running"
    echo ""
    echo "Access Points:"
    echo "  Frontend:  http://localhost:$FRONTEND_PORT"
    echo "  Backend:   http://localhost:$BACKEND_PORT"
    echo "  API Docs:  http://localhost:$BACKEND_PORT/docs"
    echo ""
    echo "Logs:"
    echo "  Backend:   $LOG_DIR/backend.log"
    echo "  Frontend:  $LOG_DIR/frontend.log"
    echo ""
    echo "Backups:"
    echo "  Directory: $BACKUP_DIR"
    echo ""
}

##############################################################################
# Main Entry Point
##############################################################################

main() {
    COMMAND=${1:-dev}
    
    case $COMMAND in
        dev)
            cmd_dev
            ;;
        prod)
            print_error "Production mode not implemented yet"
            exit 1
            ;;
        stop)
            cmd_stop
            ;;
        restart)
            cmd_restart
            ;;
        status)
            cmd_status
            ;;
        logs)
            cmd_logs
            ;;
        backup)
            cmd_backup
            ;;
        help|-h|--help)
            cmd_help
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            echo ""
            cmd_help
            exit 1
            ;;
    esac
}

# Run main with all arguments
main "$@"
