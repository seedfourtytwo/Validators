Log Rotation:
| Feature                | Description                | Value                                      | Config File               |
| ---------------------- | -------------------------- | ------------------------------------------ | ------------------------- |
| Rotation Frequency | Rotate logs daily          | daily                                    | /etc/logrotate.d/solana |
| Log Retention      | Keep last 7 logs           | rotate 7                                 | /etc/logrotate.d/solana |
| Permissions        | Run as user sol          | su sol sol                               | /etc/logrotate.d/solana |
| Post-rotate Hook   | Reopens validator log file | systemctl kill -s USR1 validator.service | /etc/logrotate.d/solana |