# Ethereum & EigenLayer Validator Setup Tutorial

## Table of Contents
- [Prerequisites](#prerequisites)
- [Directory Structure Setup](#directory-structure-setup)
- [Execution Client Setup (Geth)](#execution-client-setup-geth)
- [Consensus Client Setup](#consensus-client-setup)
- [EigenLayer Integration](#eigenlayer-integration)
- [Eigenda Node Setup](#eigenda-node-setup)
- [Service Management](#service-management)
- [Monitoring Setup](#monitoring-setup)
- [Maintenance & Management](#maintenance--management)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## Prerequisites

### System Requirements
- Ubuntu 24.04.2 LTS or newer
- x86_64 architecture
- At least 16GB RAM
- At least 2TB SSD storage
- Stable internet connection
- Static IP recommended

### Required Packages
```bash
# Update package lists
sudo apt update

# Install prerequisites
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    jq \
    make \
    gcc \
    g++ \
    pkg-config \
    libssl-dev \
    python3 \
    python3-pip \
    nodejs \
    npm
```

## Directory Structure Setup

### 1. Create Base Directories
```bash
# Create main directories
sudo mkdir -p /mnt/ethereum-testnet
sudo mkdir -p /mnt/eigenlayer
sudo mkdir -p /mnt/avss/eigenda

# Create client-specific directories
sudo mkdir -p /mnt/ethereum-testnet/geth-holesky
sudo mkdir -p /mnt/ethereum-testnet/lighthouse-holesky
sudo mkdir -p /mnt/ethereum-testnet/prysm-holesky

# Set permissions
sudo chown -R $USER:$USER /mnt/ethereum-testnet
sudo chown -R $USER:$USER /mnt/eigenlayer
sudo chown -R $USER:$USER /mnt/avss
```

### 2. Create Symlinks
```bash
# Create symlinks in home directory
ln -s /mnt/eigenlayer ~/eigenlayer
ln -s /mnt/avss/eigenda ~/eigenda
```

## Execution Client Setup (Geth)

### 1. Install Geth
```bash
# Clone Geth repository
git clone https://github.com/ethereum/go-ethereum.git
cd go-ethereum

# Build Geth
make geth

# Install Geth
sudo cp build/bin/geth /usr/local/bin/
```

### 2. Configure Geth
```bash
# Create Geth configuration directory
mkdir -p /mnt/ethereum-testnet/geth-holesky/geth

# Create JWT secret
openssl rand -hex 32 | sudo tee /mnt/ethereum-testnet/geth-holesky/geth/jwtsecret
```

<details>
<summary>Geth startup command</summary>

```bash
geth \
  --datadir /mnt/ethereum-testnet/geth-holesky \
  --networkid 17000 \
  --http \
  --http.api eth,net,web3,debug,engine,admin \
  --http.addr 0.0.0.0 \
  --http.port 8545 \
  --http.corsdomain "*" \
  --ws \
  --ws.api eth,net,web3,debug,engine,admin \
  --ws.addr 0.0.0.0 \
  --ws.port 8546 \
  --authrpc.addr 0.0.0.0 \
  --authrpc.port 8551 \
  --authrpc.vhosts "*" \
  --authrpc.jwtsecret /mnt/ethereum-testnet/geth-holesky/geth/jwtsecret \
  --syncmode snap \
  --metrics \
  --pprof \
  --verbosity 3 \
  --allow-insecure-unlock
```
</details>

## Consensus Client Setup

### 1. Lighthouse Setup
```bash
# Install Rust (if not installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone Lighthouse repository
git clone https://github.com/sigp/lighthouse.git
cd lighthouse

# Build Lighthouse
make

# Install Lighthouse
sudo cp target/release/lighthouse /usr/local/bin/
```

<details>
<summary>Lighthouse startup command</summary>

```bash
lighthouse bn \
  --datadir /mnt/ethereum-testnet/lighthouse-holesky \
  --execution-endpoint http://localhost:8551 \
  --execution-jwt /mnt/ethereum-testnet/geth-holesky/geth/jwtsecret \
  --checkpoint-sync-url https://holesky.beaconstate.info \
  --http \
  --http.address 0.0.0.0 \
  --http.port 5052 \
  --metrics \
  --validator-monitor-auto \
  --debug-level info
```
</details>

### 2. Prysm Setup (Alternative)
```bash
# Install Prysm
curl https://raw.githubusercontent.com/prysmaticlabs/prysm/master/prysm.sh --output prysm.sh
chmod +x prysm.sh
sudo mv prysm.sh /usr/local/bin/prysm
```

<details>
<summary>Prysm startup command</summary>

```bash
prysm.sh beacon-chain \
  --datadir=/mnt/ethereum-testnet/prysm-holesky \
  --execution-endpoint=http://localhost:8551 \
  --jwt-secret=/mnt/ethereum-testnet/geth-holesky/geth/jwtsecret \
  --checkpoint-sync-url=https://holesky.beaconstate.info \
  --accept-terms-of-use \
  --holesky \
  --monitoring-host=0.0.0.0
```
</details>

## EigenLayer Integration

### 1. Directory Setup
```bash
# Create EigenLayer directories
mkdir -p /mnt/eigenlayer/validator
mkdir -p /mnt/eigenlayer/keys
mkdir -p /mnt/eigenlayer/config
```

### 2. Configuration
```bash
# Create EigenLayer configuration
nano /mnt/eigenlayer/config/config.yaml
```

<details>
<summary>EigenLayer configuration</summary>

```yaml
network:
  holesky:
    rpc_url: "http://localhost:8545"
    ws_url: "ws://localhost:8546"
    chain_id: 17000

validator:
  data_dir: "/mnt/eigenlayer/validator"
  keys_dir: "/mnt/eigenlayer/keys"
  monitoring:
    enabled: true
    prometheus_port: 9090
    metrics_path: "/metrics"

eigenda:
  enabled: true
  node_type: "validator"
  data_dir: "/mnt/avss/eigenda"
```
</details>

## Eigenda Node Setup

### 1. Directory Setup
```bash
# Create Eigenda directories
mkdir -p /mnt/avss/eigenda/data
mkdir -p /mnt/avss/eigenda/config
mkdir -p /mnt/avss/eigenda/logs
```

### 2. Configuration
```bash
# Create Eigenda configuration
nano /mnt/avss/eigenda/config/config.yaml
```

<details>
<summary>Eigenda configuration</summary>

```yaml
node:
  type: "validator"
  data_dir: "/mnt/avss/eigenda/data"
  log_dir: "/mnt/avss/eigenda/logs"
  monitoring:
    enabled: true
    prometheus_port: 9091
    metrics_path: "/metrics"

network:
  holesky:
    rpc_url: "http://localhost:8545"
    ws_url: "ws://localhost:8546"
    chain_id: 17000

eigenlayer:
  enabled: true
  config_path: "/mnt/eigenlayer/config/config.yaml"
```
</details>

## Service Management

### 1. Create Systemd Services
```bash
# Create Geth service
sudo nano /etc/systemd/system/geth-holesky.service
```

<details>
<summary>Geth service file</summary>

```ini
[Unit]
Description=Geth Holesky Execution Client
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
Group=$USER
ExecStart=/usr/local/bin/geth \
  --datadir /mnt/ethereum-testnet/geth-holesky \
  --networkid 17000 \
  --http \
  --http.api eth,net,web3,debug,engine,admin \
  --http.addr 0.0.0.0 \
  --http.port 8545 \
  --http.corsdomain "*" \
  --ws \
  --ws.api eth,net,web3,debug,engine,admin \
  --ws.addr 0.0.0.0 \
  --ws.port 8546 \
  --authrpc.addr 0.0.0.0 \
  --authrpc.port 8551 \
  --authrpc.vhosts "*" \
  --authrpc.jwtsecret /mnt/ethereum-testnet/geth-holesky/geth/jwtsecret \
  --syncmode snap \
  --metrics \
  --pprof \
  --verbosity 3 \
  --allow-insecure-unlock
Restart=always
RestartSec=5
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
```
</details>

```bash
# Create Lighthouse service
sudo nano /etc/systemd/system/lighthouse-holesky.service
```

<details>
<summary>Lighthouse service file</summary>

```ini
[Unit]
Description=Lighthouse Holesky Beacon Node
After=network.target geth-holesky.service
Wants=network-online.target geth-holesky.service

[Service]
Type=simple
User=$USER
Group=$USER
ExecStart=/usr/local/bin/lighthouse bn \
  --datadir /mnt/ethereum-testnet/lighthouse-holesky \
  --execution-endpoint http://localhost:8551 \
  --execution-jwt /mnt/ethereum-testnet/geth-holesky/geth/jwtsecret \
  --checkpoint-sync-url https://holesky.beaconstate.info \
  --http \
  --http.address 0.0.0.0 \
  --http.port 5052 \
  --metrics \
  --validator-monitor-auto \
  --debug-level info
Restart=always
RestartSec=5
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
```
</details>

### 2. Enable and Start Services
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable geth-holesky
sudo systemctl enable lighthouse-holesky

# Start services
sudo systemctl start geth-holesky
sudo systemctl start lighthouse-holesky

# Check status
sudo systemctl status geth-holesky
sudo systemctl status lighthouse-holesky
```

## Monitoring Setup

### 1. Configure Prometheus
Add to your existing Prometheus configuration:

<details>
<summary>Prometheus configuration for Ethereum and EigenLayer</summary>

```yaml
scrape_configs:
  # ... existing configs ...

  - job_name: 'geth'
    static_configs:
      - targets: ['localhost:6060']
    scrape_interval: 15s
    scrape_timeout: 10s

  - job_name: 'lighthouse'
    static_configs:
      - targets: ['localhost:5054']
    scrape_interval: 15s
    scrape_timeout: 10s

  - job_name: 'eigenlayer'
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 15s
    scrape_timeout: 10s

  - job_name: 'eigenda'
    static_configs:
      - targets: ['localhost:9091']
    scrape_interval: 15s
    scrape_timeout: 10s
```
</details>

### 2. Create Grafana Dashboards
Import the following dashboards into Grafana:
- Ethereum Execution Client (Geth)
- Ethereum Consensus Client (Lighthouse)
- EigenLayer Validator
- Eigenda Node

## Maintenance & Management

### Backup Procedures
```bash
# Create backup directory
mkdir -p ~/ethereum-backups

# Backup Geth data
tar -czf ~/ethereum-backups/geth-holesky-$(date +%Y%m%d).tar.gz -C /mnt/ethereum-testnet/geth-holesky .

# Backup Lighthouse data
tar -czf ~/ethereum-backups/lighthouse-holesky-$(date +%Y%m%d).tar.gz -C /mnt/ethereum-testnet/lighthouse-holesky .

# Backup EigenLayer data
tar -czf ~/ethereum-backups/eigenlayer-$(date +%Y%m%d).tar.gz -C /mnt/eigenlayer .

# Backup Eigenda data
tar -czf ~/ethereum-backups/eigenda-$(date +%Y%m%d).tar.gz -C /mnt/avss/eigenda .
```

### Log Management
```bash
# View Geth logs
sudo journalctl -fu geth-holesky

# View Lighthouse logs
sudo journalctl -fu lighthouse-holesky

# View EigenLayer logs
tail -f /mnt/eigenlayer/validator/logs/validator.log

# View Eigenda logs
tail -f /mnt/avss/eigenda/logs/node.log
```

## Troubleshooting

### Common Issues

1. **Geth Sync Issues**
```bash
# Check Geth logs
sudo journalctl -fu geth-holesky

# Check disk space
df -h /mnt/ethereum-testnet

# Check network connectivity
curl -X POST --data '{"jsonrpc":"2.0","method":"net_version","params":[],"id":67}' -H "Content-Type: application/json" http://localhost:8545
```

2. **Lighthouse Sync Issues**
```bash
# Check Lighthouse logs
sudo journalctl -fu lighthouse-holesky

# Check JWT secret
cat /mnt/ethereum-testnet/geth-holesky/geth/jwtsecret

# Verify execution client connection
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' -H "Content-Type: application/json" http://localhost:8551
```

3. **EigenLayer Issues**
```bash
# Check EigenLayer logs
tail -f /mnt/eigenlayer/validator/logs/validator.log

# Verify configuration
cat /mnt/eigenlayer/config/config.yaml

# Check permissions
ls -la /mnt/eigenlayer
```

## Security Considerations

### Best Practices
1. Keep all clients updated regularly
2. Use secure passwords and keys
3. Implement proper firewall rules with nftables
4. Regular security audits
5. Monitor system resources
6. Backup configurations and data
7. Use secure RPC endpoints
8. Implement rate limiting
9. Regular cleanup of old data
10. Monitor for suspicious activity

### Firewall Configuration
```bash
# Install nftables if not already installed
sudo apt install -y nftables

# Create nftables configuration
sudo nano /etc/nftables.conf
```

<details>
<summary>nftables configuration</summary>

```nft
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    
    # Allow established connections
    ct state established,related accept
    
    # Allow SSH
    tcp dport 22 accept
    
    # Allow Geth ports
    tcp dport 8545 accept  # HTTP RPC
    tcp dport 8546 accept  # WebSocket
    tcp dport 8551 accept  # Auth RPC
    tcp dport 30303 accept # P2P
    
    # Allow Lighthouse ports
    tcp dport 5052 accept  # HTTP
    tcp dport 13000 accept # P2P
    
    # Allow metrics ports
    tcp dport 9090 accept  # EigenLayer metrics
    tcp dport 9091 accept  # Eigenda metrics
    
    # Allow localhost
    iifname lo accept
  }
  
  chain output {
    type filter hook output priority 0; policy accept;
  }
  
  chain forward {
    type filter hook forward priority 0; policy drop;
  }
}
```
</details>

```bash
# Apply the configuration
sudo nft -f /etc/nftables.conf

# Enable and start nftables
sudo systemctl enable nftables
sudo systemctl start nftables

# Verify configuration
sudo nft list ruleset
```

### Rate Limiting
```bash
# Add rate limiting rules to nftables
sudo nano /etc/nftables.conf
```

<details>
<summary>Rate limiting configuration</summary>

```nft
table inet filter {
  # ... existing chains ...

  chain input {
    # ... existing rules ...

    # Rate limit RPC endpoints
    tcp dport 8545 limit rate 100/minute accept  # HTTP RPC
    tcp dport 8551 limit rate 100/minute accept  # Auth RPC
    
    # Rate limit metrics endpoints
    tcp dport 9090 limit rate 60/minute accept  # EigenLayer metrics
    tcp dport 9091 limit rate 60/minute accept  # Eigenda metrics
  }
}
```
</details>

```bash
# Apply updated configuration
sudo nft -f /etc/nftables.conf
```

### Security Monitoring
```bash
# Monitor nftables logs
sudo journalctl -fu nftables

# Check active connections
sudo nft list ruleset

# Monitor rate limits
sudo nft list ruleset | grep limit
```