# 📁 File Structure

## Overview
This document outlines the key directories and files in our Solana validator setup, organized by their purpose and location.

## Core Validator Directories

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /mnt/ledger | Directory | Solana ledger data (high-write IOPS) |
| /mnt/accounts | Directory | Solana accounts DB (runtime state) |
| /mnt/snapshots | Directory | Snapshots for fast validator startup |
| /home/sol/validators/data/ledger → /mnt/ledger | Symlink | Access to ledger from validator's data directory |
| /home/sol/validators/data/accounts → /mnt/accounts | Symlink | Access to accounts from validator's data directory |
| /home/sol/validators/data/snapshots → /mnt/snapshots | Symlink | Access to snapshots from validator's data directory |
| /home/sol/validators/data/log | Directory | Validator log output files |

## Validator Software

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /home/sol/validators/jito | Directory | JITO validator implementation |
| /home/sol/validators/jito/versions/v2.2.8-jito | Directory | JITO validator binary (specific version) |
| /home/sol/validators/jito/active → versions/v2.2.8-jito | Symlink | Active JITO release for the validator |
| /home/sol/validators/agave | Directory | Agave validator backup |
| /home/sol/validators/agave/versions/v2.2.6 | Directory | Agave validator binary (specific version) |
| /home/sol/validators/agave/active → versions/v2.2.6 | Symlink | Agave release (now for backup) |
| /home/sol/validators/secure/wallets | Directory | Keypair files: identity |
| /home/sol/validators/scripts | Directory | Startup scripts for different validator types |

## Monitoring Software

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /home/sol/validators/monitoring | Directory | Monitoring tools and exporters |
| /home/sol/validators/monitoring/solana-exporter | Directory | Solana-specific metrics exporter |
| /usr/local/bin/node_exporter | Binary | System metrics exporter |

## System Configuration

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /etc/systemd/system/validator.service | Service file | Systemd service with environment-based validator selection |
| /etc/default/validator | Environment | Environment config for validator type selection |
| /etc/systemd/system/solana-exporter.service | Service file | Solana metrics exporter service |
| /etc/systemd/system/node_exporter.service | Service file | System metrics exporter service |
| /etc/nftables.conf | Config file | Firewall rules |

## Key Scripts

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /home/sol/validators/scripts/start-jito-validator.sh | Script | JITO validator startup script |
| /home/sol/validators/scripts/start-agave-validator.sh | Script | Agave validator startup script (backup) |

## Directory Details

### Data Directories
- `/mnt/ledger`: High-performance storage for transaction history
  - Requires dedicated NVMe drive
  - High write IOPS requirements
  - Currently at 59% capacity

- `/mnt/accounts`: Runtime state storage
  - Dedicated NVMe drive
  - Currently at 4% capacity
  - Contains account database

- `/mnt/snapshots`: Validator state snapshots
  - 1.2T partition
  - Used for fast validator recovery
  - Currently at 1% capacity

### Software Directories
- `/home/sol/validators/jito/`: JITO validator implementation
  - Contains versioned JITO binaries
  - Active version symlinked for easy updates
  - Includes MEV capabilities

- `/home/sol/validators/secure/wallets`: Key management
  - Contains validator identity keypair
  - Secured with appropriate permissions
  - Referenced in validator service

### Configuration Files
- `/etc/default/validator`: Environment configuration
  - Controls which validator type to use (jito/agave)
  - Used by the systemd service

- `/etc/systemd/system/validator.service`: Systemd service configuration
  - Uses environment variable to determine validator type
  - Sets resource limits
  - Configures automatic restart

- `/etc/nftables.conf`: Network security
  - Defines allowed ports
  - Sets up rate limiting
  - Configures DDoS protection

### Monitoring
- `/home/sol/validators/monitoring`: Monitoring tools
  - Contains Solana exporter for validator metrics
  - Configured to export metrics to Prometheus
  - Performance monitoring setup for JITO
