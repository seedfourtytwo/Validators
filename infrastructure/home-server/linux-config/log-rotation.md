# Log Rotation Configuration

## Overview
This document describes the log rotation configuration for various services running on the home server. Log rotation helps manage disk space by automatically archiving and removing old log files.

## Configuration Locations
All logrotate configurations are stored in `/etc/logrotate.d/`. Each service has its own configuration file:

- Main logrotate configuration: `/etc/logrotate.conf`
- Service-specific configurations: `/etc/logrotate.d/`
  - Nginx: `/etc/logrotate.d/nginx`
  - System logs: `/etc/logrotate.d/rsyslog`
  - Fail2ban: `/etc/logrotate.d/fail2ban`
  - Validator service: `/etc/logrotate.d/solana`

To modify any configuration:
1. Edit the appropriate file in `/etc/logrotate.d/`
2. Test the configuration: `sudo logrotate -d /etc/logrotate.d/<service>`
3. Apply changes: `sudo logrotate -f /etc/logrotate.d/<service>`

## Service-Specific Configurations

### Nginx Logs
Location: `/etc/logrotate.d/nginx`
```bash
/var/log/nginx/*.log {
    daily                  # Rotate logs daily
    missingok             # Don't error if log file is missing
    rotate 14             # Keep 14 days of logs
    compress              # Compress old logs
    delaycompress         # Delay compression by one rotation
    notifempty            # Don't rotate empty logs
    create 0640 www-data adm  # Set permissions on new log files
    sharedscripts         # Run scripts only once for all matching files
    prerotate
        if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
            run-parts /etc/logrotate.d/httpd-prerotate; \
        fi \
    endscript
    postrotate
        invoke-rc.d nginx rotate >/dev/null 2>&1
    endscript
}
```

### Validator Service Logs
Location: `/etc/logrotate.d/solana`
```bash
/home/chris/log/validator.log {
    su chris chris        # Run as chris user
    daily                 # Rotate logs daily
    rotate 7             # Keep 7 days of logs
    missingok            # Don't error if log file is missing
    postrotate
        systemctl kill -s USR1 validator.service
    endscript
}
```

### System Logs (rsyslog)
Location: `/etc/logrotate.d/rsyslog`
```bash
/var/log/syslog
/var/log/mail.log
/var/log/kern.log
/var/log/auth.log
/var/log/user.log
/var/log/cron.log
{
    rotate 4             # Keep 4 weeks of logs
    weekly               # Rotate logs weekly
    missingok            # Don't error if log file is missing
    notifempty           # Don't rotate empty logs
    compress             # Compress old logs
    delaycompress        # Delay compression by one rotation
    sharedscripts        # Run scripts only once for all matching files
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```

### Fail2ban Logs
Location: `/etc/logrotate.d/fail2ban`
```bash
/var/log/fail2ban.log {
    weekly               # Rotate logs weekly
    rotate 4             # Keep 4 weeks of logs
    compress             # Compress old logs
    notifempty           # Don't rotate empty logs
    delaycompress        # Delay compression by one rotation
    missingok            # Don't error if log file is missing
    postrotate
        fail2ban-client flushlogs 1>/dev/null
    endscript
    create 640 root adm  # Set permissions on new log files
}
```

## Common Options Explained
- `daily/weekly`: Frequency of rotation
- `rotate N`: Number of old log files to keep
- `compress`: Compress old logs using gzip
- `delaycompress`: Delay compression by one rotation
- `missingok`: Don't error if log file is missing
- `notifempty`: Don't rotate empty logs
- `create`: Set permissions on new log files
- `sharedscripts`: Run scripts only once for all matching files
- `postrotate`: Commands to run after rotation
- `prerotate`: Commands to run before rotation

## Maintenance
- Monitor disk space usage regularly
- Check log rotation is working properly
- Adjust rotation frequency and retention period as needed
- Review compressed log files periodically

## Last Updated
- Date: [Current Date]
- Version: 1.0