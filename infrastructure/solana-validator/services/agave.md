# ⚠️ DEPRECATED - Agave Validator Service ⚠️

> **WARNING**: This validator setup is now deprecated as we have moved to using JITO. 
> This documentation is kept for backup purposes only.
> For the current validator setup, please see [JITO Validator Setup](./jito.md)

---

[Original documentation below]

# Agave Validator Service

## Overview
Agave is a Solana validator implementation forked from the official Solana validator. It's designed to provide enhanced performance and reliability for running Solana validators. This document details the configuration and operation of the Agave validator on our Solana validator server.

## Service Information
- **Service Name**: validator.service
- **Service File**: /etc/systemd/system/validator.service
- **Run As**: sol user
- **Status**: Active and running
- **Version**: agave-validator 2.2.6 (src:00000000; feat:4066693973, client:Agave)
- **Repository**: https://github.com/anza-xyz/agave

## Configuration Files

### CLI Configuration
**File**: /home/sol/.config/solana/cli/config.yml
```
---
json_rpc_url: https://api.testnet.solana.com
websocket_url: ''
keypair_path: /home/sol/wallets/validator-identity.json
address_labels:
  '11111111111111111111111111111111': System Program
commitment: confirmed
```

### Systemd Service Configuration
**File**: /etc/systemd/system/validator.service
```
[Unit]
Description=Solana Validator
After=network.target network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
LimitNOFILE=2000000
LogRateLimitIntervalSec=0
User=sol
Environment=SOLANA_METRICS_CONFIG=host=https://metrics.solana.com:8086,db=testnet,u=testnet_write,p=password
Environment=PATH=/home/sol/.local/share/solana/install/active_release/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/sol/start-validator.sh

[Install]
WantedBy=multi-user.target
```

### Startup Script
**File**: /home/sol/start-validator.sh
```bash
#!/bin/bash

exec agave-validator \
  --identity ~/wallets/validator-identity.json \
  --vote-account 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
  --entrypoint entrypoint.testnet.solana.com:8001 \
  --entrypoint entrypoint2.testnet.solana.com:8001 \
  --entrypoint entrypoint3.testnet.solana.com:8001 \
  --known-validator 5D1fNXzvv5NjV1ysLjirC4WY92RNsVH18vjmcszZd8on \
  --known-validator dDzy5SR3AXdYWVqbDEkVFdvSPCtS9ihF5kJkHCtXoFs \
  --known-validator Ft5fbkqNa76vnsjYNwjDZUXoTWpP7VYm3mtsaQckQADN \
  --known-validator eoKpUABi59aT4rR9HGS3LcMecfut9x7zJyodWWP43YQ \
  --known-validator 9QxCLckBiJc783jnMvXZubK4wH86Eqqvashtrwvcsgkv \
  --expected-genesis-hash 4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY \
  --only-known-rpc \
  --rpc-port 8899 \
  --private-rpc \
  --dynamic-port-range 8000-8020 \
  --wal-recovery-mode skip_any_corrupted_record \
  --ledger ~/ledger \
  --accounts ~/accounts \
  --snapshots ~/snapshots \
  --log ~/log/validator.log \
  --limit-ledger-size \
  --full-rpc-api
```

## Data Storage
The validator uses the following storage locations:

| Directory | Mount Point | Filesystem | Size | Used | Available | Use% |
|-----------|-------------|------------|------|------|-----------|------|
| /home/sol/ledger | /mnt/ledger | /dev/nvme1n1p1 | 916G | 508G | 362G | 59% |
| /home/sol/accounts | /mnt/accounts | /dev/nvme0n1p1 | 916G | 30G | 840G | 4% |
| /home/sol/snapshots | /mnt/snapshots | /dev/nvme2n1p4 | 1.2T | 11G | 1.1T | 1% |

## Logging
- **Log File**: /home/sol/log/validator.log
- **Log Rotation**: Daily rotation with 7 days retention
- **Current Log Size**: ~1.8GB
- **Log Location**: Stored on the local filesystem

## Service Management

### Starting the Service
```bash
sudo systemctl start validator.service
```

### Stopping the Service
```bash
sudo systemctl stop validator.service
```

### Restarting the Service
```bash
sudo systemctl restart validator.service
```

### Checking Service Status
```bash
sudo systemctl status validator.service
```

### Enabling Service on Boot
```bash
sudo systemctl enable validator.service
```

## Command Line Options
The Agave validator is started with the following options:

| Option | Description |
|--------|-------------|
| `--identity` | Path to the validator identity keypair |
| `--vote-account` | Vote account public key |
| `--entrypoint` | Entrypoint nodes for network connection (multiple) |
| `--known-validator` | Known validator public keys (multiple) |
| `--expected-genesis-hash` | Expected genesis hash for the network |
| `--only-known-rpc` | Only connect to known RPC endpoints |
| `--rpc-port` | Port for RPC server (8899) |
| `--private-rpc` | Restrict RPC access to localhost |
| `--dynamic-port-range` | Port range for dynamic connections (8000-8020) |
| `--wal-recovery-mode` | WAL recovery mode (skip_any_corrupted_record) |
| `--ledger` | Directory for ledger storage |
| `--accounts` | Directory for accounts storage |
| `--snapshots` | Directory for snapshots storage |
| `--log` | Log file path |
| `--limit-ledger-size` | Limit ledger size to save disk space |
| `--full-rpc-api` | Enable full RPC API |

## Monitoring
The validator is configured to send metrics to Solana's metrics server:
```
SOLANA_METRICS_CONFIG=host=https://metrics.solana.com:8086,db=testnet,u=testnet_write,p=password
```

## Maintenance

### Updating Agave
To update the Agave validator to a new version:

1. Stop the validator service:
   ```bash
   sudo systemctl stop validator.service
   ```

2. Update the Agave binary:
   ```bash
   solana-install update
   ```

3. Restart the validator service:
   ```bash
   sudo systemctl start validator.service
   ```

### Updating via Symlink Active Release
The validator uses a symlink-based approach for managing releases, which allows for quick rollbacks if needed:

1. Check the current active release:
   ```bash
   ls -la /home/sol/.local/share/solana/install/active_release
   ```

2. Download a new release without activating it:
   ```bash
   solana-install init v2.2.7 --data-dir /home/sol/.local/share/solana/install
   ```

3. Verify the new release:
   ```bash
   /home/sol/.local/share/solana/install/v2.2.7/bin/agave-validator --version
   ```

4. Stop the validator service:
   ```bash
   sudo systemctl stop validator.service
   ```

5. Update the symlink to point to the new release:
   ```bash
   rm /home/sol/.local/share/solana/install/active_release
   ln -s /home/sol/.local/share/solana/install/v2.2.7 /home/sol/.local/share/solana/install/active_release
   ```

6. Start the validator service:
   ```bash
   sudo systemctl start validator.service
   ```

7. If issues occur, quickly roll back to the previous version:
   ```bash
   sudo systemctl stop validator.service
   rm /home/sol/.local/share/solana/install/active_release
   ln -s /home/sol/.local/share/solana/install/v2.2.6 /home/sol/.local/share/solana/install/active_release
   sudo systemctl start validator.service
   ```

### Backup Procedures
Regular backups of the following components are recommended:

1. **Identity Keypair**: /home/sol/wallets/validator-identity.json
2. **Vote Account Keypair**: Stored securely off-site
3. **Configuration Files**: All configuration files should be backed up

### Disk Space Management
- The ledger directory is limited in size using the `--limit-ledger-size` option
- Regular monitoring of disk usage is recommended
- Consider implementing a cleanup script for old snapshots if needed

## Troubleshooting

### Common Issues

1. **Validator Not Syncing**
   - Check network connectivity
   - Verify entrypoint nodes are accessible
   - Check for disk space issues

2. **High Memory Usage**
   - The validator is configured with a high file descriptor limit (2000000)
   - Monitor memory usage and consider adjusting system parameters if needed

3. **Service Crashes**
   - Check the log file for errors
   - The service is configured to restart automatically

### Log Analysis
To analyze the validator log:
```bash
tail -f /home/sol/log/validator.log
```

To search for specific errors:
```bash
grep -i error /home/sol/log/validator.log
```