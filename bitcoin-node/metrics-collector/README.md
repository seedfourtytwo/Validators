# Bitcoin Metrics Collector

A Prometheus metrics collector for Bitcoin Core that uses cookie authentication by default.

## Prerequisites

- Python 3.8+
- Bitcoin Core running with cookie authentication enabled
- The `bitcoin` user must have access to the Bitcoin Core cookie file
- Root/sudo access for systemd service setup

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

- `bitcoin_block_height`: Current block height
- `bitcoin_verification_progress`: Blockchain verification progress
- `bitcoin_difficulty`: Current mining difficulty
- `bitcoin_mempool_size`: Number of transactions in mempool
- `bitcoin_mempool_bytes`: Size of mempool in bytes
- `bitcoin_peer_count`: Number of connected peers
- `bitcoin_memory_usage_bytes`: Memory usage in bytes

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
