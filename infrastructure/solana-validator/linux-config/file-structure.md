# 📁 File Structure

## Overview
This document outlines the key directories and files in our Solana validator setup, organized by their purpose and location.

## Core Validator Directories

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /mnt/ledger → ~/ledger | Directory | Solana ledger data (high-write IOPS) |
| /mnt/accounts → ~/accounts | Directory | Solana accounts DB (runtime state) |
| /mnt/snapshots → ~/snapshots | Directory | Snapshots for fast validator startup |
| /home/sol | Directory | Main validator user home directory |

## Solana Software

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /home/sol/.local/share/solana/install/releases/2.2.6 | Directory | Built Agave binaries from source |
| /home/sol/.local/share/solana/install/active_release → ~/agave | Symlink | Active Agave release for CLI/systemd use |
| /home/sol/wallets | Directory | Keypair files: identity |
| /home/sol/log | Directory | Validator log output file |

## System Configuration

| Path / Symlink | Type | Purpose / Contents |
|----------------|------|-------------------|
| /etc/systemd/system/validator.service | Service file | Tells Linux how to start the validator service |
| /etc/nftables.conf | Config file | Firewall rules |
| /etc/sol/solana-exporter | Directory | Solana exporter binaries |

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
- `/home/sol/.local/share/solana/install/`: Solana software installation
  - Contains multiple release versions
  - Active release symlinked for easy updates
  - Built from source for security

- `/home/sol/wallets`: Key management
  - Contains validator identity keypair
  - Secured with appropriate permissions
  - Referenced in validator service

### Configuration Files
- `/etc/systemd/system/validator.service`: Systemd service configuration
  - Defines validator startup parameters
  - Sets resource limits
  - Configures automatic restart

- `/etc/nftables.conf`: Network security
  - Defines allowed ports
  - Sets up rate limiting
  - Configures DDoS protection

- `/etc/sol/solana-exporter`: Monitoring
  - Contains Prometheus exporter
  - Metrics collection configuration
  - Performance monitoring setup
