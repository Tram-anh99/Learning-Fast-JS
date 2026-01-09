#!/bin/bash

################################################################################
# Automatic Database Backup Script
# Purpose: Create daily backup of nongsan database
# Schedule: Run daily at 2:00 AM via cron
# Retention: Keep backups for 7 days
################################################################################

# Configuration
BACKUP_DIR="/Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups"
LOG_FILE="$BACKUP_DIR/backup.log"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="nongsan_backup_$TIMESTAMP.sql"

# Colors for output
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to log colored messages (terminal only)
log_colored() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%H:%M:%S')] ${message}${NC}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" >> "$LOG_FILE"
}

################################################################################
# Main Backup Process
################################################################################

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

log "================================"
log_colored "$GREEN" "🔄 Starting automatic database backup"
log "================================"

# Change to backup directory
cd "$BACKUP_DIR" || exit 1

# Run Python export script
log "Running Python backup script..."
if python3 "../export_sql_backup.py" > /dev/null 2>&1; then
    # Find the most recent backup file (created in last 2 minutes)
    LATEST_BACKUP=$(find . -name "nongsan_backup_*.sql" -mmin -2 -type f | head -1)
    
    if [ -n "$LATEST_BACKUP" ]; then
        # Get file size
        FILE_SIZE=$(ls -lh "$LATEST_BACKUP" | awk '{print $5}')
        RECORD_COUNT=$(grep -c "INSERT INTO" "$LATEST_BACKUP" || echo "0")
        
        log_colored "$GREEN" "✅ Backup completed successfully"
        log "   File: $LATEST_BACKUP"
        log "   Size: $FILE_SIZE"
        log "   Records: ~$RECORD_COUNT"
    else
        log_colored "$RED" "❌ Backup file not found"
        exit 1
    fi
else
    log_colored "$RED" "❌ Backup script failed"
    exit 1
fi

################################################################################
# Cleanup Old Backups
################################################################################

log ""
log_colored "$YELLOW" "🗑️  Cleaning up old backups (older than $RETENTION_DAYS days)..."

# Find and delete old backups
OLD_COUNT=$(find . -name "nongsan_backup_*.sql" -mtime +$RETENTION_DAYS -type f | wc -l | tr -d ' ')

if [ "$OLD_COUNT" -gt 0 ]; then
    find . -name "nongsan_backup_*.sql" -mtime +$RETENTION_DAYS -type f -delete
    log_colored "$YELLOW" "   Deleted $OLD_COUNT old backup(s)"
else
    log "   No old backups to delete"
fi

# List current backups
CURRENT_COUNT=$(find . -name "nongsan_backup_*.sql" -type f | wc -l | tr -d ' ')
log ""
log "📦 Current backups: $CURRENT_COUNT files"

# Show backup list
log "Latest 5 backups:"
find . -name "nongsan_backup_*.sql" -type f -exec ls -lh {} \; | \
    sort -k6,7r | head -5 | \
    awk '{printf "   - %s %s %s (%s)\n", $9, $6, $7, $5}' | \
    tee -a "$LOG_FILE"

log ""
log "================================"
log_colored "$GREEN" "✅ Backup process completed"
log "================================"

exit 0
