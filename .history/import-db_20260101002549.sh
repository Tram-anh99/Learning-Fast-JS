#!/bin/bash

###############################################################################
# IMPORT DATABASE SCHEMA - Quick Setup
###############################################################################
# Import schema_complete.sql vào PostgreSQL database
###############################################################################

echo "📊 Importing Database Schema..."
echo "==============================="

# Database connection info (from Backend/.env)
DB_HOST="localhost"
DB_PORT="5432"
DB_USER="postgres"
DB_NAME="postgres"

# Đọc password từ user
echo "Enter PostgreSQL password (default: 123456):"
read -s DB_PASSWORD
DB_PASSWORD=${DB_PASSWORD:-123456}

echo ""
echo "Connecting to: $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
echo ""

# Set PGPASSWORD environment variable để không phải nhập password
export PGPASSWORD=$DB_PASSWORD

# Import schema
echo "Importing schema_complete.sql..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f Database/schema_complete.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Schema imported successfully!"
    echo ""
    
    # Count tables
    echo "Checking tables..."
    TABLE_COUNT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='nongsan';")
    echo "✅ Total tables in 'nongsan' schema: $TABLE_COUNT"
else
    echo ""
    echo "❌ Failed to import schema!"
    exit 1
fi

# Unset password
unset PGPASSWORD
