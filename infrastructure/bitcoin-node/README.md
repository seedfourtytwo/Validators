# Bitcoin Core Full Node Setup

## Table of Contents 📑
- [Current Status](#current-status-)
- [System Configuration](#system-configuration-)
  - [User & Directories](#user--directories)
  - [Configuration Files](#configuration-files)
  - [Security Features](#security-features)
- [Monitoring & Management](#monitoring--management-)
  - [Check Node Status](#check-node-status)
  - [Service Management](#service-management-as-super-user)
  - [Data Directory Structure](#data-directory-structure)
- [Metrics Collection](#metrics-collection-)
- [Maintenance](#maintenance-)
  - [Upgrading Bitcoin Core](#upgrading-bitcoin-core)
- [Security Notes](#security-notes-)
- [Installation Guide](#installation-guide-)
  - [Prerequisites](#prerequisites)
  - [Step 1: Create Bitcoin User](#step-1-create-bitcoin-user)
  - [Step 2: Install Dependencies](#step-2-install-dependencies)
  - [Step 3: Install Bitcoin Core](#step-3-install-bitcoin-core)
  - [Step 4: Configure Bitcoin Core](#step-4-configure-bitcoin-core)
  - [Step 5: Create Systemd Service](#step-5-create-systemd-service)
  - [Step 6: Verify Installation](#step-6-verify-installation)
  - [Step 7: Monitor Initial Sync](#step-7-monitor-initial-sync)
  - [Important Notes](#important-notes)

## Current Status ✅

- **Version**: Bitcoin Core v28.1
- **Network**: Mainnet
- **Sync Status**: Fully synced (99.99% verified)
- **Storage**: ~741GB (Full node, not pruned) (see metrics for live info)
- **Memory Usage**: ~316MB (peak: 317.8MB) (see metrics for live info)
- **Service Status**: Active and running
- **Peers**: Multiple v1 and v2 peers connected

## System Configuration 🖥️

### User & Directories
- **User**: `bitcoin` (non-privileged)
- **Data Directory**: `/mnt/bitcoin-node`
- **Binary Location**: `/opt/bitcoin`
- **OS**: Ubuntu Server

### Configuration Files

#### Bitcoin Core Config (`/mnt/bitcoin-node/bitcoin.conf`)
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

# Index settings (required for UTXO metrics)
txindex=1
coinstatsindex=1
```

#### Systemd Service (`/etc/systemd/system/bitcoind.service`)
```ini
[Unit]
Description=Bitcoin daemon
After=network.target

[Service]
User=bitcoin
Group=bitcoin
ExecStart=/opt/bitcoin/bitcoind -datadir=/mnt/bitcoin-node
ExecStop=/opt/bitcoin/bitcoin-cli -datadir=/mnt/bitcoin-node stop
Type=simple
Restart=on-failure
PrivateTmp=true
ProtectHome=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

### Security Features
- Dedicated non-privileged user
- Dedicated disk partition
- Cookie authentication enabled
- RPC restricted to localhost
- Systemd service hardening:
  - `PrivateTmp`: Isolated /tmp directory
  - `ProtectHome`: Protected home directory
  - `NoNewPrivileges`: Prevents privilege escalation

### Check Node Status (run as bitcoin user)
```bash
# Get blockchain info
bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo

# Check process status
ps aux | grep bitcoind

# View logs
tail -f /mnt/bitcoin-node/debug.log

# Check memory usage
bitcoin-cli -datadir=/mnt/bitcoin-node getmemoryinfo

# Check Bitcoin Core version
bitcoin-cli -datadir=/mnt/bitcoin-node getnetworkinfo | grep -E "version|subversion"
```

### Service Management (as super user)
```bash
# Start node
sudo systemctl start bitcoind

# Stop node
sudo systemctl stop bitcoind

# Restart node
sudo systemctl restart bitcoind

# Enable on boot
sudo systemctl enable bitcoind

# Check service status
sudo systemctl status bitcoind
```

### Data Directory Structure
```
/mnt/bitcoin-node/
├── banlist.json
├── bitcoin.conf
├── bitcoind.pid
├── blocks/
├── chainstate/
├── debug.log
├── fee_estimates.dat
├── mempool.dat
├── peers.dat
└── settings.json
```

## Metrics Collection 📊

The node is configured with a custom metrics collector service that exposes metrics in Prometheus format.

### Required Indexes
The following indexes must be enabled in `bitcoin.conf` for full metrics collection:
- `txindex=1`: Enables transaction index for efficient transaction lookups
- `coinstatsindex=1`: Enables UTXO statistics index for efficient UTXO metrics collection

Note: These indexes require additional disk space (~30GB for txindex, ~2GB for coinstatsindex) and will take some time to build after enabling.

### Metrics Collector
- Located in `metrics-collector/` directory
- Runs as systemd user service under `bitcoin` user
- Uses cookie authentication
- Exposes metrics on port 9332

### Dashboard
- Public dashboard available at: https://metric.seed42.co/public-dashboards/4de1b04bbfd5466cbc7387071ae30786?from=now-15m&to=now&refresh=15s
- Shows real-time metrics including:
  - Bitcoin Core version (v28.1)
  - Block height
  - Network difficulty
  - Mempool size and transactions
  - Network connections
  - UTXO set statistics
  - Transaction fees (low, medium, high)
  - Blockchain size
  - Network bandwidth

### Version Tracking
The metrics collector tracks the following version information:
- Full Bitcoin Core version string
- Major, minor, and patch version numbers
- Formatted version number for display (e.g., "28.1")

This allows for easy monitoring of the node's version and helps ensure timely updates.

The complete Grafana dashboard configuration is available in `../home-server/services/grafana/bitcoin-node-dashboard.json`. You can import this file directly into your Grafana instance to set up the dashboard.

## Maintenance 🔧

### Upgrading Bitcoin Core
1. Stop the service:
```bash
sudo systemctl stop bitcoind
```

2. Backup the data directory:
```bash
sudo tar -czf bitcoin-node-backup.tar.gz /mnt/bitcoin-node
```

3. Update Bitcoin Core:
```bash
cd ~/bitcoin
git fetch --tags
git checkout v29.0  # Replace with new version
git verify-tag v29.0
make clean
./configure --without-gui --disable-tests --disable-bench --enable-wallet
make -j$(nproc)
sudo cp src/bitcoind src/bitcoin-cli /opt/bitcoin/
```

4. Restart the service:
```bash
sudo systemctl start bitcoind
```

## Security Notes 🛡️

- Node runs under dedicated `bitcoin` user
- RPC access restricted to localhost
- Cookie authentication enabled
- Systemd service includes security hardening
- Regular backups recommended
- Keep system and Bitcoin Core updated

## Installation Guide 📥

### Prerequisites
- Ubuntu Server (tested on Ubuntu 22.04 LTS)
- At least 1TB of free disk space (for full node)
- 4GB RAM minimum (8GB recommended)
- Stable internet connection
- Root or sudo access

### Step 1: Create Bitcoin User
```bash
# Create bitcoin user and group
sudo useradd -m -s /bin/bash bitcoin
sudo usermod -aG sudo bitcoin

# Create data directory
sudo mkdir -p /mnt/bitcoin-node
sudo chown bitcoin:bitcoin /mnt/bitcoin-node
```

### Step 2: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y build-essential libtool autotools-dev automake pkg-config bsdmainutils python3 libssl-dev libevent-dev libboost-system-dev libboost-filesystem-dev libboost-test-dev libboost-thread-dev libminiupnpc-dev libzmq3-dev libqt5gui5 libqt5core5a libqt5dbus5 qttools5-dev qttools5-dev-tools
```

### Step 3: Install Bitcoin Core
```bash
# Switch to bitcoin user
sudo su - bitcoin

# Install additional build dependencies
sudo apt install -y wget gnupg2 dirmngr

# Add Bitcoin Core release signing key
wget https://bitcoincore.org/bin/bitcoin-core-28.1/SHA256SUMS
wget https://bitcoincore.org/bin/bitcoin-core-28.1/SHA256SUMS.asc
gpg --keyserver hkps://keys.openpgp.org --recv-keys 152812300785C96444D3334D17565732E08E5E41
gpg --verify SHA256SUMS.asc

# Clone Bitcoin repository
cd ~
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin

# Verify the release tag
git fetch --tags
git verify-tag v28.1
git checkout v28.1

# Build Bitcoin Core
./autogen.sh

# Configure build with security-focused options:
./configure \
    --without-gui \          # Disable GUI components (headless server)
    --disable-tests \        # Skip running tests during build
    --disable-bench \        # Skip building benchmarks
    --enable-wallet \        # Enable wallet functionality
    --with-gui=no \          # Explicitly disable GUI
    --disable-zmq \          # Disable ZeroMQ interface
    --disable-shared \       # Build static libraries
    --enable-static \        # Enable static linking
    --with-pic \             # Generate position-independent code
    --enable-hardening \     # Enable security hardening features
    --with-incompatible-bdb \ # Use newer Berkeley DB version
    --disable-wallet \       # Disable wallet if not needed
    --disable-mining \       # Disable mining functionality
    --disable-upnp-default \ # Disable UPnP by default
    --disable-natpmp-default # Disable NAT-PMP by default

# Build using all available CPU cores
make -j$(nproc)

# Verify the build
make check

# Create binary directory
sudo mkdir -p /opt/bitcoin
sudo cp src/bitcoind src/bitcoin-cli /opt/bitcoin/
sudo chown bitcoin:bitcoin /opt/bitcoin/bitcoind /opt/bitcoin/bitcoin-cli

# Verify binary signatures
cd /opt/bitcoin
sha256sum bitcoind bitcoin-cli
```

### Step 4: Configure Bitcoin Core
```bash
# Create configuration file
cat > /mnt/bitcoin-node/bitcoin.conf << EOF
# Bitcoin Core configuration
datadir=/mnt/bitcoin-node    # Data directory location

# RPC settings
server=1                     # Enable JSON-RPC server
rpcallowip=127.0.0.1        # Allow RPC connections only from localhost
rpcbind=127.0.0.1           # Bind RPC server to localhost
rpcport=8332                # RPC server port

# HTTP server settings
rest=1                      # Enable REST API server

# Performance settings
dbcache=450                 # Database cache size in MB
maxmempool=300             # Maximum mempool size in MB
maxconnections=40          # Maximum number of connections
maxuploadtarget=5000       # Maximum upload target in MB/day

# Security settings
discover=1                 # Enable peer discovery
listen=1                   # Accept connections from other nodes
bind=127.0.0.1            # Bind to localhost only

# Additional security settings
disablewallet=1            # Disable wallet functionality if not needed
disablemining=1            # Disable mining functionality
upnp=0                     # Disable UPnP
natpmp=0                   # Disable NAT-PMP
EOF

# Set correct permissions
chmod 600 /mnt/bitcoin-node/bitcoin.conf
```

### Step 5: Create Systemd Service
```bash
# Create service file
sudo tee /etc/systemd/system/bitcoind.service << EOF
[Unit]
Description=Bitcoin daemon
After=network.target

[Service]
User=bitcoin
Group=bitcoin
ExecStart=/opt/bitcoin/bitcoind -datadir=/mnt/bitcoin-node
ExecStop=/opt/bitcoin/bitcoin-cli -datadir=/mnt/bitcoin-node stop
Type=simple
Restart=on-failure
PrivateTmp=true
ProtectHome=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable bitcoind
sudo systemctl start bitcoind
```

### Step 6: Verify Installation
```bash
# Check service status
sudo systemctl status bitcoind

# Check blockchain info
bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo

# Check process
ps aux | grep bitcoind
```

### Step 7: Monitor Initial Sync
```bash
# Watch sync progress
watch -n 10 'bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo | grep verificationprogress'

# Check debug log
tail -f /mnt/bitcoin-node/debug.log
```

### Important Notes
- Initial sync can take several days depending on your internet connection
- The node requires approximately 741GB of disk space when fully synced
- Cookie authentication is automatically enabled
- RPC access is restricted to localhost for security
- Regular backups of the data directory are recommended