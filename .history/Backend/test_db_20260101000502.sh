#!/bin/bash

# ========== Test Database Connection ==========
# Script để kiểm tra kết nối PostgreSQL

echo "🔍 Testing PostgreSQL Connection..."
echo "=================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default values
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5433}
DB_NAME=${DB_NAME:-postgres}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-123456}
DB_SCHEMA=${DB_SCHEMA:-nongsan}

echo "📊 Connection Details:"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo "  Database: $DB_NAME"
echo "  Schema: $DB_SCHEMA"
echo "  User: $DB_USER"
echo ""

# Test with Python
python3 << EOF
import sys
try:
    from sqlalchemy import create_engine, text
    
    # Create connection string
    db_url = "postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
    
    # Create engine
    engine = create_engine(db_url)
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("✅ Connection successful!")
        print(f"📦 PostgreSQL version: {version[:50]}...")
        print()
        
        # Count tables
        result = conn.execute(text(f"""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = '$DB_SCHEMA'
        """))
        count = result.fetchone()[0]
        print(f"📋 Total tables in schema '$DB_SCHEMA': {count}")
        
        # List some tables
        result = conn.execute(text(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '$DB_SCHEMA'
            ORDER BY table_name
            LIMIT 10
        """))
        tables = [row[0] for row in result]
        print(f"📑 First 10 tables: {', '.join(tables)}")
        
except ImportError:
    print("❌ SQLAlchemy not installed!")
    print("Run: pip install -r requirements-minimal.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print()
    print("💡 Troubleshooting:")
    print("  1. Check if PostgreSQL is running")
    print("  2. Verify credentials in .env file")
    print("  3. Check port number (5433 vs 5432)")
    print("  4. Test password: 123456 or 000000")
    sys.exit(1)
EOF

echo ""
echo "✅ Database connection test completed!"
