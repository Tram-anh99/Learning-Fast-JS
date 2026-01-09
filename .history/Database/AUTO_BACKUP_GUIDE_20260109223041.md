# 🔄 Automatic Database Backup Setup

## Đã hoàn thành:
- ✅ Script backup tự động: `auto_backup.sh`
- ✅ Test thành công: Backup 13MB, ~42,902 records
- ✅ Retention: Giữ backup 7 ngày

---

## Cách setup Cron Job (chạy hàng ngày lúc 2:00 AM)

### Bước 1: Mở crontab editor
```bash
crontab -e
```

### Bước 2: Thêm dòng sau (chạy daily lúc 2:00 AM)
```bash
0 2 * * * /Users/anllen/LapTrinh/Learning-Fast-JS/Database/auto_backup.sh >> /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/backup.log 2>&1
```

### Bước 3: Save và exit (trong vi/vim: ESC → :wq → Enter)

### Bước 4: Verify cron job đã được add
```bash
crontab -l
```

---

## Cron Schedule Syntax

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, 0=Sunday)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Ví dụ schedules:

```bash
# Mỗi ngày lúc 2:00 AM
0 2 * * * /path/to/auto_backup.sh

# Mỗi ngày lúc 3:30 AM
30 3 * * * /path/to/auto_backup.sh

# Mỗi Chủ nhật lúc 1:00 AM
0 1 * * 0 /path/to/auto_backup.sh

# Mỗi 6 giờ (0h, 6h, 12h, 18h)
0 */6 * * * /path/to/auto_backup.sh

# Mỗi 30 phút
*/30 * * * * /path/to/auto_backup.sh
```

---

## Manual Backup (Test ngay)

```bash
cd /Users/anllen/LapTrinh/Learning-Fast-JS/Database
./auto_backup.sh
```

---

## Kiểm tra Backup Logs

```bash
# Xem toàn bộ log
cat /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/backup.log

# Xem log realtime
tail -f /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/backup.log

# Xem 50 dòng cuối
tail -50 /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/backup.log
```

---

## Kiểm tra Backups

```bash
# List tất cả backups
ls -lh /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/*.sql

# Count backups
ls /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/*.sql | wc -l
```

---

## Restore từ Backup

```bash
# Restore toàn bộ database
psql -h localhost -U postgres -d postgres < /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/nongsan_backup_20260109_222957.sql

# Restore vào database mới (test)
createdb -h localhost -U postgres nongsan_test
psql -h localhost -U postgres -d nongsan_test < /Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/nongsan_backup_20260109_222957.sql
```

---

## Troubleshooting

### Cron không chạy?

1. **Check cron service (Linux):**
```bash
sudo service cron status
```

2. **Check cron logs (Linux):**
```bash
grep CRON /var/log/syslog
```

3. **macOS: Check launchd logs:**
```bash
log show --predicate 'process == "cron"' --last 1h
```

4. **Verify cron có quyền truy cập Full Disk Access (macOS):**
   - System Preferences → Security & Privacy → Privacy → Full Disk Access
   - Add `/usr/sbin/cron`

### Script chạy thủ công OK nhưng cron fail?

- **Vấn đề:** Cron môi trường khác với shell môi trường
- **Giải pháp:** Thêm full path cho python3:

```bash
# Tìm python3 path
which python3

# Update script với full path
0 2 * * * /usr/local/bin/python3 /path/to/script.py
```

---

## Monitoring & Alerts (Optional)

### Email notification khi backup hoàn thành

Thêm vào cuối `auto_backup.sh`:

```bash
# Send email notification
echo "Backup completed: $BACKUP_FILE ($FILE_SIZE)" | \
mail -s "Database Backup Successful" your-email@example.com
```

### Slack notification (với webhook)

```bash
# Add to auto_backup.sh
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"✅ Database backup completed: $BACKUP_FILE ($FILE_SIZE)\"}" \
  $SLACK_WEBHOOK
```

---

## Best Practices

1. ✅ **Test restore thường xuyên** - Backup chỉ có giá trị khi restore được
2. ✅ **Monitor disk space** - Ensure đủ chỗ cho backups
3. ✅ **Offsite backup** - Copy backups ra external drive hoặc cloud
4. ✅ **Encrypt backups** - Nếu chứa dữ liệu nhạy cảm
5. ✅ **Document restore process** - Team khác biết cách restore

---

## Summary

- 📍 **Backup Location:** `/Users/anllen/LapTrinh/Learning-Fast-JS/Database/backups/`
- 🕐 **Schedule:** Daily at 2:00 AM (after setup cron)
- 📦 **Retention:** 7 days (configurable)
- 📊 **Size:** ~13 MB per backup
- 📝 **Log File:** `backups/backup.log`
- ✅ **Status:** Ready to deploy!

**Next Step:** Run `crontab -e` and add the cron job line above! 🚀
