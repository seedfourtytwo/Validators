# Bitcoin Node Metrics Collector

A Prometheus exporter for Bitcoin Core metrics.

## Prerequisites

- Python 3.8+
- Bitcoin Core running with cookie authentication enabled
- The `bitcoin` user must have access to the Bitcoin Core cookie file
- Root/sudo access for systemd service setup
- Bitcoin Core indexes enabled:
  - `txindex=1`: Required for transaction lookups
  - `coinstatsindex=1`: Required for UTXO metrics collection

## Installation

### 1. Setup Python Environment (as bitcoin user)
```bash
cd /opt/bitcoin/metrics-collector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment (as bitcoin user)
Create a `.env` file with the following configuration:
```bash
cat > .env << EOL
# Bitcoin RPC Configuration
BITCOIN_RPC_HOST=127.0.0.1
BITCOIN_RPC_PORT=8332

# Cookie Authentication
BITCOIN_COOKIE_PATH=/mnt/bitcoin-node/.cookie

# Metrics Configuration
METRICS_PORT=9332
METRICS_HOST=0.0.0.0
EOL
```

### 3. Create Systemd Service (as root/sudo user)
Create the service file:
```bash
echo '[Unit]
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
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/bitcoin-metrics.service
```

### 4. Enable and Start Service (as root/sudo user)
```bash
sudo systemctl daemon-reload
sudo systemctl enable bitcoin-metrics.service
sudo systemctl start bitcoin-metrics.service
```

## Service Management

The metrics collector runs as a systemd service under the bitcoin user. To manage the service:

```bash
# Check service status
sudo systemctl status bitcoin-metrics.service

# Stop the service
sudo systemctl stop bitcoin-metrics.service

# Start the service
sudo systemctl start bitcoin-metrics.service

# Restart the service
sudo systemctl restart bitcoin-metrics.service

# View logs
sudo journalctl -u bitcoin-metrics.service
```

## Metrics

The collector exposes the following metrics on port 9332:

### Blockchain Metrics
- `bitcoin_block_height`: Current block height
- `bitcoin_verification_progress`: Blockchain verification progress
- `bitcoin_difficulty`: Current mining difficulty

### Mempool Metrics
- `bitcoin_mempool_size`: Number of transactions in mempool
- `bitcoin_mempool_bytes`: Size of mempool in bytes

### Network Metrics
- `bitcoin_peer_count`: Number of connected peers
- `bitcoin_network_bytes_sent_total`: Total bytes sent
- `bitcoin_network_bytes_received_total`: Total bytes received
- `bitcoin_connections_inbound`: Number of inbound connections
- `bitcoin_connections_outbound`: Number of outbound connections

### UTXO Metrics (requires coinstatsindex)
- `bitcoin_utxo_count`: Total number of unspent transaction outputs
- `bitcoin_utxo_size_bytes`: Total size of UTXO set in bytes

### System Metrics
- `bitcoin_memory_usage_bytes`: Memory usage in bytes
- `bitcoin_size_on_disk_bytes`: Total blockchain size on disk in bytes

### Block Metrics
- `bitcoin_block_size_bytes_mean`: Average block size in bytes
- `bitcoin_block_transactions_mean`: Average transactions per block
- `bitcoin_block_interval_seconds`: Time between last two blocks

### Fee Metrics
- `bitcoin_fee_high`: Estimated fee rate for high priority - next block (sat/vB)
- `bitcoin_fee_medium`: Estimated fee rate for medium priority - 3 blocks (sat/vB)
- `bitcoin_fee_low`: Estimated fee rate for low priority - 6 blocks (sat/vB)

### Market Metrics
- `bitcoin_price_usd`: Current Bitcoin price in USD

## Security Notes

- The collector runs under the bitcoin user without sudo privileges
- Cookie authentication is used by default for enhanced security
- The service is configured to restart automatically on failure
- The service runs as a system service with proper user/group permissions

## Troubleshooting

1. If the service fails to start, check the logs:
```bash
sudo journalctl -u bitcoin-metrics.service
```

2. Verify the cookie file permissions:
```bash
ls -l /mnt/bitcoin-node/.cookie
```

3. Ensure Bitcoin Core is running:
```bash
sudo systemctl status bitcoind
```

4. Check if the metrics endpoint is accessible:
```bash
curl http://localhost:9332/metrics
```

5. Verify Python environment:
```bash
cd /opt/bitcoin/metrics-collector
source venv/bin/activate
python3 -c "import bitcoinrpc, prometheus_client, dotenv, aiohttp"
```

6. Test the collector directly:
```bash
cd /opt/bitcoin/metrics-collector
source venv/bin/activate
python3 src/collector.py
```

## RPC Commands Used

Currently, the collector uses these Bitcoin Core RPC endpoints:

### Blockchain Information
- `getblockchaininfo`: General blockchain state
  - Used for: block height, verification progress, difficulty, disk size
- `getbestblockhash`: Latest block hash
- `getblock`: Block details
  - Used for: block time calculations

### Mempool & Fees
- `getmempoolinfo`: Mempool statistics
  - Used for: transaction count, mempool size in bytes
- `estimatesmartfee`: Fee estimates
  - Used for: high (1 block), medium (3 blocks), low (6 blocks) priority fees

### Network
- `getnetworkinfo`: Network state
  - Used for: connection count
- `getnettotals`: Network traffic
  - Used for: bytes sent/received
- `getpeerinfo`: Peer details
  - Used for: inbound/outbound connection counts

### Block Statistics
- `getblockstats`: Detailed block metrics
  - Used for: average block size, transactions per block

### Memory & UTXO
- `getmemoryinfo`: Memory usage statistics
- `gettxoutsetinfo`: UTXO set information
  - Used with "muhash" mode for faster UTXO stats

## Available but Unused RPC Commands

These RPC commands could be useful for additional metrics:

### Mining
- `getmininginfo`: Mining statistics
- `getnetworkhashps`: Network hash rate
- `getblocktemplate`: Current block template

### Transaction Pool
- `getrawmempool`: Detailed mempool transactions
- `getmempoolancestors`: Transaction dependencies
- `getmempooldescendants`: Child transactions
- `getmempoolentry`: Single transaction details

### Network
- `getnodeaddresses`: Known network nodes
- `getnetworkinfo`: More network details
- `getpeerinfo`: Additional peer metrics

### Blockchain
- `getchaintips`: Chain reorganization info
- `getchaintxstats`: Chain transaction statistics
- `getblockstats`: Additional block metrics
  - total_weight
  - total_size
  - subsidy
  - totalfee

### Wallet & UTXO
- `getwalletinfo`: Wallet statistics
- `listunspent`: Detailed UTXO information

## Adding New Metrics

To add new metrics from these endpoints:

1. Define a new Prometheus metric in the collector
2. Add the RPC call in the `collect_metrics()` function
3. Update tests and documentation

## Configuration

[Configuration details here...]
