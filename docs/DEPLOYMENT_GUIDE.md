# 🚀 Deployment Guide

**Hệ Thống Quản Lý Nông Nghiệp & Truy Xuất Nguồn Gốc**

**Version:** 2.0  
**Last Updated:** January 10, 2026  
**Purpose:** Complete deployment guide for production environment

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Development Deployment](#development-deployment)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [Security Hardening](#security-hardening)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Hệ thống bao gồm 3 thành phần chính:
- **Frontend:** Vue.js 3 (SPA) - Port 5173 (dev) / 80/443 (prod)
- **Backend:** FastAPI - Port 8000 (dev) / 8000 (prod behind Nginx)
- **Database:** PostgreSQL 16 - Port 5432

### Architecture

```
Internet
    ↓
Nginx (80/443) ← SSL/TLS
    ↓
Frontend (Static files) + Backend Proxy (/api → 8000)
    ↓
FastAPI Backend (8000)
    ↓
PostgreSQL (5432)
```

---

## 📦 Prerequisites

### System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4 GB
- Disk: 20 GB
- OS: Ubuntu 20.04+ / CentOS 8+ / macOS

**Recommended (Production):**
- CPU: 4+ cores
- RAM: 8+ GB
- Disk: 50+ GB SSD
- OS: Ubuntu 22.04 LTS

### Software Requirements

```bash
# Required
- Python 3.8+ (hoặc Anaconda)
- Node.js 18+ và npm
- PostgreSQL 16+
- Git

# Optional (Production)
- Docker & Docker Compose
- Nginx 1.18+
- Supervisor (process manager)
- SSL certificate (Let's Encrypt)
```

---

## 💻 Development Deployment

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Tram-anh99/Learning-Fast-JS.git
cd Learning-Fast-JS

# 2. Setup database
createdb -U postgres postgres
PGPASSWORD=123456 psql -U postgres -d postgres -f Database/nongsan_backup_20260109_215915.sql

# 3. Configure environment
cd Backend
cp .env.example .env
nano .env  # Edit DB credentials

# 4. Start system (One command!)
cd ..
./start.sh
```

**Access URLs:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Development Setup

#### Backend Setup

```bash
cd Backend

# Option 1: Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-minimal.txt

# Option 2: Conda (Recommended)
conda create -n agri python=3.11
conda activate agri
pip install -r requirements-minimal.txt

# Configure .env
cat > .env << EOF
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=123456
DB_SCHEMA=nongsan
CORS_ORIGINS=http://localhost:5173
EOF

# Run backend
uvicorn app:app --reload --port 8000
```

#### Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install

# Configure API URL (optional)
# Edit vite.config.js if needed

# Run dev server
npm run dev
```

---

## 🏭 Production Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv nginx supervisor postgresql-16 git

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installations
python3 --version
node --version
psql --version
nginx -v
```

### 2. Database Setup

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE nongsan_production;
CREATE USER agri_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE nongsan_production TO agri_user;
\q

# Import data
PGPASSWORD=strong_password_here psql -U agri_user -d nongsan_production -f /path/to/backup.sql

# Verify
PGPASSWORD=strong_password_here psql -U agri_user -d nongsan_production -c "SELECT COUNT(*) FROM nongsan.vung_trong;"
```

### 3. Backend Deployment

```bash
# Create application directory
sudo mkdir -p /var/www/agri-backend
sudo chown $USER:$USER /var/www/agri-backend
cd /var/www/agri-backend

# Clone repository
git clone https://github.com/Tram-anh99/Learning-Fast-JS.git .

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r Backend/requirements-minimal.txt

# Configure production .env
cd Backend
cat > .env << EOF
APP_ENV=production
DEBUG=False

DB_HOST=localhost
DB_PORT=5432
DB_NAME=nongsan_production
DB_USER=agri_user
DB_PASSWORD=strong_password_here
DB_SCHEMA=nongsan

CORS_ORIGINS=https://yourdomain.com
HOST=127.0.0.1
PORT=8000
EOF

# Test backend
python -c "from app import app; print('✅ Backend OK')"
```

### 4. Frontend Build

```bash
cd /var/www/agri-backend/Frontend

# Install dependencies
npm ci --production

# Build for production
npm run build

# Output will be in Frontend/dist/
ls -lh dist/
```

### 5. Nginx Configuration

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/agri-system

# Paste this configuration:
```

```nginx
# /etc/nginx/sites-available/agri-system

upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Frontend (Static files)
    root /var/www/agri-backend/Frontend/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public, must-revalidate, proxy-revalidate";
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # API docs (optional - comment out in production)
    location /docs {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }

    location /redoc {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logs
    access_log /var/log/nginx/agri-access.log;
    error_log /var/log/nginx/agri-error.log;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/agri-system /etc/nginx/sites-enabled/

# Test Nginx config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### 6. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run

# Auto-renewal is enabled by default (systemd timer)
sudo systemctl status certbot.timer
```

### 7. Process Management (Supervisor)

```bash
# Create supervisor config
sudo nano /etc/supervisor/conf.d/agri-backend.conf
```

```ini
[program:agri-backend]
command=/var/www/agri-backend/venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000 --workers 4
directory=/var/www/agri-backend/Backend
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/agri-backend.err.log
stdout_logfile=/var/log/agri-backend.out.log
environment=PATH="/var/www/agri-backend/venv/bin"
```

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Start backend
sudo supervisorctl start agri-backend

# Check status
sudo supervisorctl status

# Logs
sudo tail -f /var/log/agri-backend.out.log
```

---

## 🐳 Docker Deployment

### Docker Compose Configuration

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  database:
    image: postgres:16-alpine
    container_name: agri-database
    environment:
      POSTGRES_DB: nongsan_production
      POSTGRES_USER: agri_user
      POSTGRES_PASSWORD: strong_password_here
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./Database/nongsan_backup_20260109_215915.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - agri-network
    restart: unless-stopped

  # FastAPI Backend
  backend:
    build:
      context: ./Backend
      dockerfile: Dockerfile
    container_name: agri-backend
    environment:
      DB_HOST: database
      DB_PORT: 5432
      DB_NAME: nongsan_production
      DB_USER: agri_user
      DB_PASSWORD: strong_password_here
      DB_SCHEMA: nongsan
      CORS_ORIGINS: https://yourdomain.com
    depends_on:
      - database
    ports:
      - "8000:8000"
    networks:
      - agri-network
    restart: unless-stopped

  # Vue.js Frontend
  frontend:
    build:
      context: ./Frontend
      dockerfile: Dockerfile
    container_name: agri-frontend
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    networks:
      - agri-network
    restart: unless-stopped

volumes:
  postgres-data:

networks:
  agri-network:
    driver: bridge
```

### Backend Dockerfile

Create `Backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Frontend Dockerfile

Create `Frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Frontend Nginx Config

Create `Frontend/nginx.conf`:

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
}
```

### Deploy with Docker

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

---

## 🗄️ Database Setup

### Initial Setup

```bash
# Create database
createdb -U postgres nongsan_production

# Import backup
psql -U postgres -d nongsan_production -f Database/nongsan_backup_20260109_215915.sql

# Or use backup script
cd Database
./backup_database.sh restore nongsan_backup_20260109_215915.sql
```

### Database Schema

Schema structure:
- **Schema name:** `nongsan`
- **Tables:** 28 tables
- **Views:** 5 views
- **Total records:** ~45,000+

### Performance Optimization

```sql
-- Create indexes
CREATE INDEX idx_vung_trong_ma_vung ON nongsan.vung_trong(ma_vung);
CREATE INDEX idx_vung_trong_tinh_id ON nongsan.vung_trong(tinh_id);
CREATE INDEX idx_lich_su_vung_id ON nongsan.lich_su_canh_tac(vung_trong_id);
CREATE INDEX idx_lich_su_date ON nongsan.lich_su_canh_tac(ngay_thuc_hien);

-- Vacuum and analyze
VACUUM ANALYZE;
```

---

## 🔐 Environment Variables

### Backend .env (Production)

```env
# Application
APP_NAME="Agriculture Management API"
APP_ENV=production
DEBUG=False

# Server
HOST=127.0.0.1
PORT=8000

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nongsan_production
DB_USER=agri_user
DB_PASSWORD=your_strong_password_here
DB_SCHEMA=nongsan

# CORS (Frontend domain)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# API
API_TITLE=Agricultural Management API
API_VERSION=2.0

# Security (Optional)
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Environment

Update `Frontend/vite.config.js`:

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'https://yourdomain.com',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser'
  }
})
```

---

## 🔒 Security Hardening

### 1. Database Security

```sql
-- Revoke public access
REVOKE ALL ON SCHEMA nongsan FROM PUBLIC;

-- Grant specific permissions
GRANT USAGE ON SCHEMA nongsan TO agri_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA nongsan TO agri_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA nongsan TO agri_user;

-- Enable SSL
-- Edit postgresql.conf:
-- ssl = on
-- ssl_cert_file = '/path/to/server.crt'
-- ssl_key_file = '/path/to/server.key'
```

### 2. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Block direct database access from outside
sudo ufw deny 5432/tcp
```

### 3. Application Security

- ✅ Use strong passwords
- ✅ Enable HTTPS only
- ✅ Implement JWT authentication (planned)
- ✅ Rate limiting (planned)
- ✅ Input validation (Pydantic models)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS configuration (restrict origins)

---

## 📊 Monitoring & Logging

### Application Logs

```bash
# Backend logs
tail -f /var/log/agri-backend.out.log
tail -f /var/log/agri-backend.err.log

# Nginx logs
tail -f /var/log/nginx/agri-access.log
tail -f /var/log/nginx/agri-error.log

# PostgreSQL logs
tail -f /var/log/postgresql/postgresql-16-main.log
```

### Health Check Endpoint

Backend provides health check:

```bash
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "database": "connected",
  "tables": 28
}
```

### Monitoring Tools (Optional)

- **Prometheus + Grafana:** Metrics monitoring
- **ELK Stack:** Log aggregation
- **Uptime Kuma:** Uptime monitoring
- **pgAdmin:** Database monitoring

---

## 💾 Backup & Recovery

### Automated Backups

```bash
# Use backup script
cd /var/www/agri-backend/Database
./backup_database.sh backup

# Setup cron job (daily backup at 2 AM)
crontab -e

# Add line:
0 2 * * * cd /var/www/agri-backend/Database && ./backup_database.sh backup
```

### Manual Backup

```bash
# Full database backup
pg_dump -U agri_user -d nongsan_production | gzip > backup_$(date +%Y%m%d).sql.gz

# Schema only
pg_dump -U agri_user -d nongsan_production --schema-only > schema.sql

# Data only
pg_dump -U agri_user -d nongsan_production --data-only > data.sql
```

### Restore from Backup

```bash
# Decompress and restore
gunzip < backup_20260110.sql.gz | psql -U agri_user -d nongsan_production

# Or use backup script
./backup_database.sh restore backup_20260110.sql.gz
```

### Backup Storage

Store backups in multiple locations:
- ✅ Local server: `/var/backups/agri/`
- ✅ Cloud storage: AWS S3, Google Cloud Storage
- ✅ External drive: Regular offline backups

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** Backend won't start

```bash
# Check logs
tail -50 /var/log/agri-backend.err.log

# Test manually
cd /var/www/agri-backend/Backend
source ../venv/bin/activate
python -c "from app import app"

# Check database connection
python -c "from database import test_connection; test_connection()"
```

**Problem:** Database connection failed

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
PGPASSWORD=password psql -U agri_user -d nongsan_production -c "SELECT 1"

# Check .env file
cat Backend/.env | grep DB_
```

### Frontend Issues

**Problem:** Frontend build failed

```bash
cd Frontend
npm ci
npm run build

# Check for errors in output
```

**Problem:** API calls failing

```bash
# Check CORS settings in Backend/.env
# Check Nginx proxy configuration
# Check browser console for errors
```

### Nginx Issues

**Problem:** 502 Bad Gateway

```bash
# Check backend is running
curl http://localhost:8000/health

# Check Nginx config
sudo nginx -t

# Check Nginx logs
tail -50 /var/log/nginx/agri-error.log

# Restart services
sudo supervisorctl restart agri-backend
sudo systemctl restart nginx
```

---

## 📞 Support

### Documentation
- [README.md](../README.md) - Project overview
- [DATABASE_DESIGN.md](DATABASE_DESIGN.md) - Database schema
- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - System architecture
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File structure

### Commands Reference

```bash
# Development
./start.sh              # Start all services
./start.sh stop         # Stop all services
./start.sh status       # Check status
./start.sh logs         # View logs
./start.sh backup       # Backup database

# Production
sudo supervisorctl status           # Check backend
sudo supervisorctl restart agri-backend
sudo systemctl status nginx
sudo systemctl reload nginx
docker-compose ps                   # Docker status
```

---

## 🎯 Production Checklist

Before going live:

- [ ] Database backup created and tested
- [ ] .env configured with production values
- [ ] CORS origins set to production domain
- [ ] SSL certificate installed (HTTPS)
- [ ] Firewall rules configured
- [ ] Nginx configured and tested
- [ ] Backend running with Supervisor
- [ ] Frontend built and deployed
- [ ] Health check endpoint working
- [ ] Automated backups scheduled
- [ ] Monitoring setup (optional)
- [ ] Error logging configured
- [ ] Performance testing done
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Team trained on deployment process

---

**Document Version:** 2.0  
**Last Updated:** January 10, 2026  
**Maintained by:** Development Team

**Made with ❤️ for Production Deployment 🚀**
