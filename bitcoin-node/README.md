# Bitcoin Core Full Node Setup

## Current Status ✅

- **Version**: Bitcoin Core v28.1
- **Network**: Mainnet
- **Sync Status**: Fully synced (99.99% verified)
- **Block Height**: 892,246
- **Storage**: ~741GB (Full node, not pruned)
- **Memory Usage**: ~316MB (peak: 317.8MB)
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

## Monitoring & Management 🔍

### Check Node Status
```bash
# Get blockchain info
bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo

# Check process status
ps aux | grep bitcoind

# View logs
tail -f /mnt/bitcoin-node/debug.log

# Check memory usage
bitcoin-cli -datadir=/mnt/bitcoin-node getmemoryinfo
```

### Service Management
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

### Metrics Collector
- Located in `metrics-collector/` directory
- Runs as systemd user service under `bitcoin` user
- Uses cookie authentication
- Exposes metrics on port 9332

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