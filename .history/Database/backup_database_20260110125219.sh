#!/bin/bash

##############################################################################
# Database Backup & Restore Script
# 
# Usage:
#   ./backup_database.sh backup   - Create backup
#   ./backup_database.sh restore <file>  - Restore from backup
#   ./backup_database.sh list     - List all backups
#
# Author: Development Team
# Date: January 10, 2026
##############################################################################

set -e

# Configuration
DB_NAME="nongsan_db"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"

BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/backups"
mkdir -p "$BACKUP_DIR"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

backup_database() {
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql"
    
    print_info "Creating backup..."
    print_info "Database: $DB_NAME"
    print_info "User: $DB_USER"
    print_info "Host: $DB_HOST:$DB_PORT"
    
    # Backup with pg_dump
    if pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > "$BACKUP_FILE"; then
        print_success "Backup created: $BACKUP_FILE"
        
        # Compress
        gzip "$BACKUP_FILE"
        COMPRESSED="${BACKUP_FILE}.gz"
        
        BACKUP_SIZE=$(du -h "$COMPRESSED" | cut -f1)
        print_success "Compressed: $COMPRESSED ($BACKUP_SIZE)"
        
        # Get stats
        TABLE_COUNT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'nongsan'" | tr -d ' ')
        print_info "Tables backed up: $TABLE_COUNT"
        
        echo ""
        print_success "Backup completed successfully!"
    else
        print_error "Backup failed!"
        exit 1
    fi
}

restore_database() {
    BACKUP_FILE="$1"
    
    if [ -z "$BACKUP_FILE" ]; then
        print_error "Please specify backup file"
        echo "Usage: ./backup_database.sh restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    print_info "Restoring from backup..."
    print_info "File: $BACKUP_FILE"
    
    # Check if compressed
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        print_info "Decompressing..."
        gunzip -c "$BACKUP_FILE" | psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME
    else
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME < "$BACKUP_FILE"
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Database restored successfully!"
    else
        print_error "Restore failed!"
        exit 1
    fi
}

list_backups() {
    print_info "Available backups in: $BACKUP_DIR"
    echo ""
    
    if [ -z "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
        print_info "No backups found"
    else
        ls -lh "$BACKUP_DIR"/*.sql.gz 2>/dev/null || true
    fi
}

# Main
case "${1:-backup}" in
    backup)
        backup_database
        ;;
    restore)
        restore_database "$2"
        ;;
    list)
        list_backups
        ;;
    *)
        echo "Usage: ./backup_database.sh {backup|restore|list}"
        exit 1
        ;;
esac
