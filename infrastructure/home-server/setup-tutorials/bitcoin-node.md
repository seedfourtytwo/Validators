# Bitcoin Core Full Node Setup on Linux (from Source)

## Table of Contents
- [Prerequisites](#-prerequisites)
  - [System Requirements](#system-requirements)
  - [Required Packages](#required-packages)
  - [User Setup](#user-setup)
- [Goal](#-goal)
- [Environment](#-environment)
- [Setup Steps](#setup-steps)
  - [1. Partitioning & Filesystem Prep](#1️⃣-partitioning--filesystem-prep)
  - [2. Build Bitcoin Core from Source](#2️⃣-build-bitcoin-core-from-source)
  - [3. Systemd Service](#3️⃣-systemd-service)
  - [4. Configuration](#4️⃣-configuration)
  - [5. Firewall Configuration](#5️⃣-firewall-configuration)
  - [6. Monitoring Sync Progress](#6️⃣-monitoring-sync-progress)
  - [7. Metrics Collection Setup](#7️⃣-metrics-collection-setup)
- [Maintenance & Troubleshooting](#maintenance--troubleshooting)
  - [Troubleshooting](#-troubleshooting)
  - [Log Files](#log-files)
  - [Maintenance Schedule](#-maintenance-schedule)
  - [Security Checklist](#️-security-checklist)
  - [Maintenance & Upgrade Path](#-maintenance--upgrade-path)
- [References](#-references)
- [Notes](#-notes)

## 📋 Prerequisites

### System Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 2GB minimum, 4GB+ recommended
- **Storage**: 1TB+ SSD/HDD (600GB+ for blockchain, extra for growth)
- **Network**: Stable internet connection, preferably with static IP
- **OS**: Ubuntu Server 22.04 LTS or newer

### Required Packages
```bash
# Run as root
sudo apt update

# Install build dependencies
sudo apt install -y build-essential libtool autotools-dev automake pkg-config bsdmainutils python3 libssl-dev libevent-dev libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-test-dev libboost-thread-dev libminiupnpc-dev libzmq3-dev git

# Install additional utilities
sudo apt install -y wget curl jq netcat
```

### User Setup
```bash
# Run as root
sudo addgroup bitcoin
sudo adduser --system --group bitcoin
sudo usermod -aG sudo bitcoin

# Set up bitcoin user's home directory
sudo mkdir -p /home/bitcoin
sudo chown bitcoin:bitcoin /home/bitcoin
sudo chmod 700 /home/bitcoin
```

## ✅ Goal

Deploy a production-grade, secure Bitcoin full node on a Linux server:

- Built from source with PGP verification
- Dedicated user + disk partition
- `systemd` managed
- Hardened permissions
- Syncing from Genesis block (mainnet)
- Integrated with Prometheus monitoring

### 🧰 Environment

- **User**: `bitcoin` (non-privileged)
- **Data directory**: `/mnt/bitcoin-node` (on dedicated HDD partition)
- **Binary install location**: `/opt/bitcoin`
- **OS**: Ubuntu Server (no desktop)
- **Firewall**: `nftables` (with P2P port 8333 opened)

## Setup Steps

## 1️⃣ Partitioning & Filesystem Prep

### Disk Partitioning
```bash
# Run as root
# List available disks
sudo lsblk

# Create partition (replace /dev/sdX with your disk)
sudo fdisk /dev/sdX

# Format partition
sudo mkfs.ext4 /dev/sdX1

# Create mount point
sudo mkdir -p /mnt/bitcoin-node

# Add to fstab
echo "UUID=$(sudo blkid -s UUID -o value /dev/sdX1) /mnt/bitcoin-node ext4 defaults,noatime,nodiratime 0 2" | sudo tee -a /etc/fstab

# Mount partition
sudo mount -a

# Set permissions
sudo chown bitcoin:bitcoin /mnt/bitcoin-node
sudo chmod 700 /mnt/bitcoin-node
```

## 2️⃣ Build Bitcoin Core from Source

### 📥 Download and Verify
```bash
# Run as bitcoin user
# Switch to bitcoin user
sudo -u bitcoin bash

# Clone repository
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin
git checkout v28.1
git verify-tag v28.1

# Import key if needed
gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys 152812300785C96444D3334D17565732E08E5E41
```

### ⚙️ Build
```bash
# Run as bitcoin user
# Generate build scripts
./autogen.sh

# Configure build
./configure --without-gui --disable-tests --disable-bench --enable-wallet

# Build (this may take several hours)
make -j$(nproc)
```

### 🚚 Deploy the Binaries
```bash
# Run as root
# Create directory for binaries
sudo mkdir -p /opt/bitcoin

# Copy binaries
sudo cp /home/bitcoin/bitcoin/src/bitcoind /home/bitcoin/bitcoin/src/bitcoin-cli /opt/bitcoin/

# Set permissions
sudo chown root:root /opt/bitcoin/*
sudo chmod 755 /opt/bitcoin/*
```

## 3️⃣ Systemd Service

Create `/etc/systemd/system/bitcoind.service`:
```bash
# Run as root
sudo nano /etc/systemd/system/bitcoind.service
```

Add the following content:
```ini
[Unit]
Description=Bitcoin daemon
After=network.target

[Service]
User=bitcoin
Group=bitcoin
ExecStart=/opt/bitcoin/bitcoind -datadir=/mnt/bitcoin-node -nodaemon
ExecStop=/opt/bitcoin/bitcoin-cli -datadir=/mnt/bitcoin-node stop
Type=simple
Restart=on-failure
PrivateTmp=true
ProtectHome=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Then reload and start:
```bash
# Run as root
# Reload systemd
sudo systemctl daemon-reload

# Start and enable the service
sudo systemctl start bitcoind
sudo systemctl enable bitcoind

# Check status
sudo systemctl status bitcoind
```

## 4️⃣ Configuration

### Bitcoin Configuration
Create `/mnt/bitcoin-node/bitcoin.conf`:
```bash
# Run as root
sudo nano /mnt/bitcoin-node/bitcoin.conf
```

Add the following content:
```ini
# Bitcoin Core configuration
datadir=/mnt/bitcoin-node

# RPC settings
server=1
rpcallowip=127.0.0.1
rpcbind=127.0.0.1
rpcport=8332

# HTTP server settings
rest=1

# Index Settings
txindex=1
coinstatsindex=1
```

## 5️⃣ Firewall Configuration

### nftables Rules
```bash
# Run as root
# Install nftables if not already installed
sudo apt install -y nftables

# Create a basic configuration
sudo nano /etc/nftables.conf

# Add these rules
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    
    # Allow established connections
    ct state established,related accept
    
    # Allow SSH
    tcp dport 22 accept
    
    # Allow Bitcoin P2P
    tcp dport 8333 accept
    
    # Allow Bitcoin RPC from local network
    tcp dport 8332 ip saddr 192.168.1.0/24 accept
    
    # Allow localhost
    iifname lo accept
  }
}

# Apply the configuration
sudo nft -f /etc/nftables.conf

# Enable and start nftables
sudo systemctl enable nftables
sudo systemctl start nftables
```

## 6️⃣ Monitoring Sync Progress

### Manual Check
```bash
# Run as bitcoin user
# Switch to bitcoin user
sudo -u bitcoin bash

# Check blockchain info
/opt/bitcoin/bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo
```

### Auto-refresh
```bash
# Run as bitcoin user
# Watch sync progress
watch -n 10 '/opt/bitcoin/bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo | grep -E "blocks|headers|verificationprogress"'
```

Example output:
```json
{
  "blocks": 32161,
  "headers": 891895,
  "verificationprogress": 0.000027
}
```

## 7️⃣ Metrics Collection Setup

### Overview
Our custom Bitcoin metrics collector provides detailed insights into the Bitcoin node's performance and health. It collects metrics such as:
- Block processing rate
- Memory usage
- Network connections
- Transaction throughput
- Validation statistics

### Installation
```bash
# Run as root
# Clone the repository
sudo git clone https://github.com/seedfourtytwo/Validators.git /opt/Validators
cd /opt/Validators/bitcoin-node/metrics-collector

# Create directory for the collector
sudo mkdir -p /opt/bitcoin/metrics-collector

# Copy files to proper location
sudo cp -r * /opt/bitcoin/metrics-collector/

# Set permissions
sudo chown -R bitcoin:bitcoin /opt/bitcoin/metrics-collector
```

### Configuration
Create `.env` file in the metrics-collector directory:
```bash
# Run as bitcoin user
# Switch to bitcoin user
sudo -u bitcoin bash

# Navigate to the collector directory
cd /opt/bitcoin/metrics-collector

# Create and edit the .env file
nano .env
```

Add the following content:
```
# Bitcoin RPC Configuration
BITCOIN_RPC_HOST=127.0.0.1
BITCOIN_RPC_PORT=8332

# Cookie Authentication
BITCOIN_COOKIE_PATH=/mnt/bitcoin-node/.cookie

# Metrics Configuration
METRICS_PORT=9332
METRICS_HOST=0.0.0.0
```

### Python Environment Setup
```bash
# Run as bitcoin user
# Set up Python virtual environment
cd /opt/bitcoin/metrics-collector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Systemd Service
Create `/etc/systemd/system/bitcoin-metrics.service`:
```bash
# Run as root
sudo nano /etc/systemd/system/bitcoin-metrics.service
```

Add the following content:
```ini
[Unit]
Description=Bitcoin Metrics Collector
After=bitcoind.service
Requires=bitcoind.service

[Service]
Type=simple
User=bitcoin
Group=bitcoin
WorkingDirectory=/opt/bitcoin/metrics-collector
Environment=PATH=/opt/bitcoin/metrics-collector/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/opt/bitcoin/metrics-collector/venv/bin/python src/collector.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Start the Collector
```bash
# Run as root
# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable bitcoin-metrics.service
sudo systemctl start bitcoin-metrics.service

# Check status
sudo systemctl status bitcoin-metrics.service
```

### Metrics
The collector exposes the following metrics on port 9332:
- `bitcoin_block_height`: Current block height
- `bitcoin_verification_progress`: Blockchain verification progress
- `bitcoin_difficulty`: Current mining difficulty
- `bitcoin_mempool_size`: Number of transactions in mempool
- `bitcoin_mempool_bytes`: Size of mempool in bytes
- `bitcoin_peer_count`: Number of connected peers
- `bitcoin_memory_usage_bytes`: Memory usage in bytes

### Documentation
For detailed information about the metrics collector, including:
- Available metrics
- Configuration options
- Troubleshooting
- Custom metric development

See the [Bitcoin Metrics Collector Documentation](infrastructure/home-server/services/bitcoin-metrics-collector.md) or visit the [GitHub repository](https://github.com/seedfourtytwo/Validators/tree/main/bitcoin-node/metrics-collector)

## Maintenance & Troubleshooting

## 🔧 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Run as root
   # Check ownership
   sudo ls -la /mnt/bitcoin-node
   sudo ls -la /opt/bitcoin
   
   # Fix permissions if needed
   sudo chown -R bitcoin:bitcoin /mnt/bitcoin-node
   sudo chmod 700 /mnt/bitcoin-node
   ```

2. **Sync Issues**
   ```bash
   # Run as bitcoin user
   # Switch to bitcoin user
   sudo -u bitcoin bash
   
   # Check debug log
   tail -f /mnt/bitcoin-node/debug.log
   
   # Verify network connectivity
   /opt/bitcoin/bitcoin-cli -datadir=/mnt/bitcoin-node getnetworkinfo
   ```

3. **Memory Issues**
   ```bash
   # Run as root
   # Check memory usage
   sudo free -h
   
   # Adjust dbcache if needed in bitcoin.conf
   sudo nano /mnt/bitcoin-node/bitcoin.conf
   # Add: dbcache=450
   ```

### Log Files
- Debug log: `/mnt/bitcoin-node/debug.log`
- Systemd logs: `sudo journalctl -u bitcoind -f`

## 📚 References

- [Bitcoin Core Documentation](https://bitcoin.org/en/bitcoin-core/)
- [Bitcoin Core GitHub](https://github.com/bitcoin/bitcoin)
- [Bitcoin Metrics Collector Documentation](infrastructure/home-server/services/bitcoin-metrics-collector.md)
- [Systemd Service Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)


## 📌 Notes

- Full blockchain size: ~600GB+ as of 2025
- Initial sync (IBD) takes time but ensures full validation
- Node will auto-restart on failure and boot

## 🔁 Maintenance & Upgrade Path

To upgrade:
```bash
# Run as bitcoin user
# Switch to bitcoin user
sudo -u bitcoin bash

# Navigate to bitcoin directory
cd ~/bitcoin

# Fetch latest tags
git fetch --tags

# Checkout new version
git checkout v29.0
git verify-tag v29.0

# Clean previous build
make clean

# Configure and build
./configure --without-gui --disable-tests --disable-bench --enable-wallet
make -j$(nproc)

# Run as root
# Copy new binaries
sudo cp src/bitcoind src/bitcoin-cli /opt/bitcoin/

# Restart service
sudo systemctl restart bitcoind
```
