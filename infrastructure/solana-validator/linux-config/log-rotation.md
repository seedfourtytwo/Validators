# 📝 Log Rotation

## Overview
Log rotation is configured to manage validator logs efficiently, preventing disk space issues while maintaining a reasonable history for debugging and monitoring.

## Current Configuration
Location: `/etc/logrotate.d/solana`

```bash
/home/sol/log/*.log {
    daily
    rotate 7
    missingok
    notifempty
    compress
    delaycompress
    su sol sol
    postrotate
        systemctl kill -s USR1 validator.service
    endscript
}
```

## Configuration Details

| Feature | Description | Value | Config File |
|---------|-------------|-------|-------------|
| Rotation Frequency | Rotate logs daily | daily | /etc/logrotate.d/solana |
| Log Retention | Keep last 7 logs | rotate 7 | /etc/logrotate.d/solana |
| Permissions | Run as user sol | su sol sol | /etc/logrotate.d/solana |
| Post-rotate Hook | Reopens validator log file | systemctl kill -s USR1 validator.service | /etc/logrotate.d/solana |

## Log Files Managed
- `/home/sol/log/validator.log`: Main validator output
- `/home/sol/log/system.log`: System-related messages
- `/home/sol/log/error.log`: Error messages and warnings

## Rotation Settings

### Basic Settings
- `daily`: Rotate logs every day
- `rotate 7`: Keep 7 rotated logs
- `missingok`: Don't error if log file is missing
- `notifempty`: Don't rotate empty logs
- `compress`: Compress old logs
- `delaycompress`: Delay compression by one rotation

### Advanced Settings
- `su sol sol`: Run as sol user/group
- `postrotate`: Execute after rotation
- `systemctl kill -s USR1`: Signal validator to reopen log file

## Maintenance

### Manual Rotation
```bash
# Force log rotation
sudo logrotate -f /etc/logrotate.d/solana

# Test rotation without applying
sudo logrotate -d /etc/logrotate.d/solana
```

### Monitoring
```bash
# Check log sizes
du -sh /home/sol/log/*

# View rotation status
ls -l /home/sol/log/*.gz

# Check last rotation
stat /home/sol/log/validator.log
```

### Log Analysis
```bash
# View recent errors
tail -n 100 /home/sol/log/error.log

# Search for specific patterns
grep "ERROR" /home/sol/log/validator.log

# Count error occurrences
grep -c "ERROR" /home/sol/log/validator.log
```