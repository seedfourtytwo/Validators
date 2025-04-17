# JITO Validator Service

## Table of Contents
- [Overview](#overview)
- [Service Information](#service-information)
- [Directory Structure](#directory-structure)
- [Configuration Files](#configuration-files)
  - [CLI Configuration](#cli-configuration)
  - [Systemd Service Configuration](#systemd-service-configuration)
  - [Startup Script](#startup-script)
- [Data Storage](#data-storage)
- [Logging](#logging)
- [Service Management](#service-management)
- [Command Line Options](#command-line-options)
- [Switching Between Validators](#switching-between-validators)
  - [Environment Configuration](#environment-configuration)
  - [Switching Process](#switching-process)
- [Updating JITO](#updating-jito)
  - [Current Version Management](#current-version-management)
  - [Update Process](#update-process)
  - [Rollback Procedure](#rollback-procedure)
- [Verification Steps](#verification-steps)
- [Monitoring](#monitoring)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

## Overview
JITO is our current Solana validator implementation, replacing the previous Agave setup. This document details the configuration and operation of the JITO validator on our Solana validator server.

## Service Information
- **Service Name**: validator.service
- **Service File**: /etc/systemd/system/validator.service
- **Run As**: sol user
- **Status**: Active and running
- **Version**: agave-validator 2.2.8-jito (src:00000000; feat:1522022101, client:JitoLabs)
- **Repository**: https://github.com/jito-foundation/jito-solana

## Directory Structure
```bash
/home/sol/validators/
├── agave/                    # Backup of original Agave setup
│   ├── active -> versions/v2.2.6
│   └── versions/
│       └── v2.2.6
├── jito/
│   ├── active -> versions/v2.2.8-jito
│   └── versions/
│       └── v2.2.8-jito
├── data/
│   ├── ledger -> /mnt/ledger
│   ├── accounts -> /mnt/accounts
│   ├── snapshots -> /mnt/snapshots
│   └── log/
├── secure/
│   └── wallets/
└── scripts/
    ├── start-agave-validator.sh
    └── start-jito-validator.sh
```

## Configuration Files

### CLI Configuration
**File**: /home/sol/.config/solana/cli/config.yml
```yaml
---
json_rpc_url: https://api.testnet.solana.com
websocket_url: ''
keypair_path: /home/sol/validators/secure/wallets/validator-identity.json
address_labels:
  '11111111111111111111111111111111': System Program
commitment: confirmed
```

### Startup Script
**File**: /home/sol/validators/scripts/start-jito-validator.sh
```bash
#!/bin/bash

exec /home/sol/validators/jito/active \
  --identity /home/sol/validators/secure/wallets/validator-identity.json \
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
  --ledger /home/sol/validators/data/ledger \
  --accounts /home/sol/validators/data/accounts \
  --snapshots /home/sol/validators/data/snapshots \
  --log /home/sol/validators/data/log/validator.log \
  --limit-ledger-size \
  --full-rpc-api \
  --tip-payment-program-pubkey GJHtFqM9agxPmkeKjHny6qiRKrXZALvvFGiKf11QE7hy \
  --tip-distribution-program-pubkey F2Zu7QZiTYUhPd7u9ukRVwxh7B71oA3NMJcHuCHc29P2 \
  --merkle-root-upload-authority GZctHpWXmsZC1YHACTGGcHhYxjdRqQvTpYkb9LMvxDib \
  --commission-bps 800 \
  --block-engine-url https://ny.testnet.block-engine.jito.wtf \
  --relayer-url http://ny.testnet.relayer.jito.wtf:8100 \
  --shred-receiver-address 141.98.216.132:1002
```

## Data Storage
The validator uses the following storage locations:

| Directory | Mount Point | Filesystem | Size | Used | Available | Use% |
|-----------|-------------|------------|------|------|-----------|------|
| /home/sol/validators/data/ledger | /mnt/ledger | /dev/nvme1n1p1 | 916G | 508G | 362G | 59% |
| /home/sol/validators/data/accounts | /mnt/accounts | /dev/nvme0n1p1 | 916G | 30G | 840G | 4% |
| /home/sol/validators/data/snapshots | /mnt/snapshots | /dev/nvme2n1p4 | 1.2T | 11G | 1.1T | 1% |

## Logging
- **Log File**: /home/sol/validators/data/log/validator.log
- **Log Rotation**: Daily rotation with 7 days retention
- **Current Log Size**: ~1.8GB
- **Log Location**: Stored on the local filesystem

## Command Line Options
The JITO validator is started with the following options:

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
| `--tip-payment-program-pubkey` | Address of JITO's tip payment program for testnet |
| `--tip-distribution-program-pubkey` | Address of JITO's tip distribution program for testnet |
| `--merkle-root-upload-authority` | Authority that uploads MEV airdrop merkle roots |
| `--commission-bps` | MEV commission in basis points (800 = 8%) |
| `--block-engine-url` | URL of JITO's block engine |
| `--relayer-url` | URL of JITO's relayer |
| `--shred-receiver-address` | Address where shreds are sent |

## JITO-Specific Configuration

### MEV Parameters
JITO requires specific parameters to function properly on the Solana network. These parameters connect your validator to JITO's MEV infrastructure:

1. **Tip Payment & Distribution Programs**: JITO uses on-chain programs to handle MEV tips and distribute rewards:
   - `--tip-payment-program-pubkey`: Program address for processing tips (`GJHtFqM9agxPmkeKjHny6qiRKrXZALvvFGiKf11QE7hy` for testnet)
   - `--tip-distribution-program-pubkey`: Program address for distributing rewards (`F2Zu7QZiTYUhPd7u9ukRVwxh7B71oA3NMJcHuCHc29P2` for testnet)

2. **Merkle Root Upload Authority**: Controls who can upload MEV airdrop merkle roots to the validator:
   - `--merkle-root-upload-authority`: Set to `GZctHpWXmsZC1YHACTGGcHhYxjdRqQvTpYkb9LMvxDib` for JITO to handle airdrops and claims

3. **MEV Commission**: Sets what percentage of MEV rewards the validator keeps:
   - `--commission-bps`: Commission in basis points (800 = 8%)

4. **Connection Endpoints**: Connects your validator to JITO's infrastructure:
   - `--block-engine-url`: Endpoint for JITO's block engine
   - `--relayer-url`: Endpoint for JITO's transaction relayer
   - `--shred-receiver-address`: Address where validator shreds are sent

### JITO vs Agave Binary
The JITO binary at `/home/sol/validators/jito/versions/v2.2.8-jito` is based on the Agave validator but includes additional MEV functionality. When checking the version, it will still show "agave-validator" in the name, but with "client:JitoLabs" to indicate it's the JITO fork:

```
agave-validator 2.2.8 (src:00000000; feat:1522022101, client:JitoLabs)
```

### Troubleshooting JITO MEV
If you're having issues with JITO MEV functionality:

1. Ensure all required MEV parameters are included in your start script
2. Verify connectivity to JITO's block engine and relayer endpoints
3. Check your validator logs for any MEV-related errors or warnings
4. Make sure your validator is properly voting on the network

## Monitoring
The validator is configured to send metrics to Solana's metrics server:
```
SOLANA_METRICS_CONFIG=host=https://metrics.solana.com:8086,db=testnet,u=testnet_write,p=password
```

For detailed information about monitoring your JITO validator, refer to:
- [Node Exporter](monitoring/node-exporter.md) - System-level metrics
- [Solana Exporter](monitoring/solana-exporter.md) - Solana-specific metrics
- [Metrics Reference](monitoring/metrics-reference.md) - Comprehensive list of available metrics

These monitoring tools provide valuable insights into validator performance, system health, and JITO MEV-related metrics.

## Switching Between Validators
The system is set up to easily switch between JITO and Agave validators using an environment file and systemd service.

### Environment Configuration
**File**: /etc/default/validator
```bash
# Valid values: agave, jito
VALIDATOR_TYPE=jito
```

### Systemd Service Configuration
**File**: /etc/systemd/system/validator.service
```ini
[Unit]
Description=Solana Validator
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=sol
EnvironmentFile=/etc/default/validator
ExecStart=/bin/bash -c '/home/sol/validators/scripts/start-${VALIDATOR_TYPE}-validator.sh'
LimitNOFILE=1000000

[Install]
WantedBy=multi-user.target
```

### Switching Process
To switch between validators:

1. Stop the current validator:
```bash
sudo systemctl stop validator
```

2. Change the validator type in the environment file:
```bash
# To switch to JITO
sudo sed -i 's/VALIDATOR_TYPE=agave/VALIDATOR_TYPE=jito/' /etc/default/validator

# To switch to Agave
sudo sed -i 's/VALIDATOR_TYPE=jito/VALIDATOR_TYPE=agave/' /etc/default/validator
```

3. Start the new validator:
```bash
sudo systemctl start validator
```

4. Monitor the transition:
```bash
tail -f /home/sol/validators/data/log/validator.log
```

## Updating JITO

### Current Version Management
JITO releases are managed using a version-based directory structure and symlinks:
```bash
/home/sol/validators/jito/
├── active -> versions/v2.2.8-jito
└── versions/
    └── v2.2.8-jito
```

### Update Process

1. Check current version:
```bash
/home/sol/validators/jito/active --version
```

2. Clone and build new version:
```bash
cd ~/jito
git clone https://github.com/jito-foundation/jito-solana.git
cd jito-solana
git fetch --all --tags
git checkout v2.x.x-jito  # Replace with target version
cargo clean
./cargo build --release
```

3. Copy new binary to versions directory:
```bash
cp target/release/agave-validator /home/sol/validators/jito/versions/v2.x.x-jito
chmod +x /home/sol/validators/jito/versions/v2.x.x-jito
```

4. Stop the validator:
```bash
sudo systemctl stop validator
```

5. Update the symlink:
```bash
cd /home/sol/validators/jito
rm active
ln -s versions/v2.x.x-jito active
```

6. Start the validator:
```bash
sudo systemctl start validator
```

### Rollback Procedure
If issues occur with the new version:

1. Stop the validator:
```bash
sudo systemctl stop validator
```

2. Switch back to previous version:
```bash
cd /home/sol/validators/jito
rm active
ln -s versions/v2.2.8-jito active  # Or whichever version was working
```

3. Restart the validator:
```bash
sudo systemctl start validator
```

4. Monitor logs:
```bash
tail -f /home/sol/validators/data/log/validator.log
```

## Verification Steps

### After Updates or Switches
1. Check the correct binary is running:
```bash
ps aux | grep validator
```

2. Verify version:
```bash
/home/sol/validators/jito/active --version
```

3. Monitor logs for errors:
```bash
tail -f /home/sol/validators/data/log/validator.log
```

4. Check validator status:
```bash
sudo systemctl status validator
```

## Troubleshooting

### Common Issues

1. **Validator Not Syncing**
   - Check network connectivity
   - Verify entrypoint nodes are accessible
   - Check for disk space issues

2. **High Memory Usage**
   - The validator is configured with a high file descriptor limit (1000000)
   - Monitor memory usage and consider adjusting system parameters if needed

3. **Service Crashes**
   - Check the log file for errors
   - The service is configured to restart automatically

### Log Analysis
To analyze the validator log:
```bash
tail -f /home/sol/validators/data/log/validator.log
```

To search for specific errors:
```bash
grep -i error /home/sol/validators/data/log/validator.log
```
