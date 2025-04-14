# Solana Exporter Service

## Overview
Solana Exporter is a Prometheus exporter for Solana blockchain metrics. It collects various Solana-specific metrics and exposes them in Prometheus format, making them available for monitoring and alerting. This document details the configuration and operation of the Solana Exporter on my Solana validator server.

## Service Information
- **Service Name**: solana-exporter.service
- **Service File**: /etc/systemd/system/solana-exporter.service
- **Run As**: sol user
- **Status**: Active and running
- **Repository**: https://github.com/asymmetric-research/solana-exporter
- **Listen Address**: 0.0.0.0:9100
- **Server IP**: 38.97.62.158
- **Access Restriction**: Only accessible from home IP address for security

## Purpose
Solana Exporter serves several critical functions for the Solana validator:

1. **Validator Monitoring**: Collects metrics about validator performance and health
2. **Network Monitoring**: Provides information about the Solana network status
3. **Performance Tracking**: Enables tracking of validator performance over time
4. **Alerting**: Provides data for alerting on validator issues

## Configuration

### Systemd Service Configuration
**File**: /etc/systemd/system/solana-exporter.service
```
[Unit]
Description=Solana Exporter for Prometheus
After=network.target

[Service]
User=sol
WorkingDirectory=/home/sol
ExecStart=/home/sol/solana-exporter/solana-exporter \
  -rpc-url http://127.0.0.1:8899 \
  -listen-address 0.0.0.0:9100
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Command Line Options
The Solana Exporter is started with the following options:

| Option | Description |
|--------|-------------|
| `-rpc-url http://127.0.0.1:8899` | URL of the Solana RPC endpoint |
| `-listen-address 0.0.0.0:9100` | Listen address for the metrics endpoint |

## Metrics

Solana Exporter collects a wide range of Solana-specific metrics. Here are some of the key metric categories:

### Validator Metrics
- **Vote Account**: Information about the validator's vote account
- **Commission**: Validator commission rate
- **Credits**: Credits earned by the validator
- **Delinquent Status**: Whether the validator is delinquent
- **Epoch Progress**: Progress through the current epoch
- **Identity**: Validator identity information
- **Last Vote**: Information about the last vote cast
- **Root Slot**: Current root slot
- **Slot**: Current slot
- **Version**: Solana software version

### Network Metrics
- **Block Height**: Current block height
- **Epoch**: Current epoch
- **Slot**: Current slot
- **Transaction Count**: Number of transactions processed
- **Vote Account**: Information about vote accounts

### Performance Metrics
- **CPU Usage**: CPU usage by the Solana process
- **Memory Usage**: Memory usage by the Solana process
- **Disk I/O**: Disk I/O operations by the Solana process
- **Network I/O**: Network I/O operations by the Solana process

### Metrics Format
Solana Exporter metrics follow the Prometheus format. Each metric has:
- A HELP line explaining the metric
- A TYPE line specifying the metric type (counter, gauge, histogram, etc.)
- One or more lines with the actual metric values and labels

Example metrics:
```
# HELP solana_block_height Current block height
# TYPE solana_block_height gauge
solana_block_height 123456789

# HELP solana_epoch Current epoch
# TYPE solana_epoch gauge
solana_epoch 123

# HELP solana_slot Current slot
# TYPE solana_slot gauge
solana_slot 123456789

# HELP solana_transaction_count Total number of transactions processed
# TYPE solana_transaction_count counter
solana_transaction_count 987654321
```

## Service Management

### Starting the Service
```bash
sudo systemctl start solana-exporter.service
```

### Stopping the Service
```bash
sudo systemctl stop solana-exporter.service
```

### Restarting the Service
```bash
sudo systemctl restart solana-exporter.service
```

### Checking Service Status
```bash
sudo systemctl status solana-exporter.service
```

### Enabling Service on Boot
```bash
sudo systemctl enable solana-exporter.service
```

## Accessing Metrics

### Remote Access from Home Server
Since the validator server doesn't have a web browser, metrics should be accessed from the home server:

1. **Direct HTTP Access**:
   ```
   curl http://38.97.62.158:9100/metrics
   ```

2. **Using SSH Tunnel**:
   ```bash
   # On home server
   ssh -L 9100:localhost:9100 38.97.62.158
   
   # Then access metrics locally
   curl http://localhost:9100/metrics
   ```

3. **Using Prometheus**:
   Configure Prometheus on the home server to scrape the validator's Solana Exporter:
   ```yaml
   scrape_configs:
     - job_name: 'validator-solana'
       static_configs:
         - targets: ['38.97.62.158:9100']
   ```


## Grafana Dashboards

Solana Exporter metrics can be visualized using Grafana dashboards. Recommended dashboards include:

1. **Solana Validator Dashboard**: Comprehensive dashboard for Solana validator metrics
2. **Solana Network Dashboard**: Dashboard for Solana network metrics

## Maintenance

### Updating Solana Exporter
To update Solana Exporter to a new version:

1. Stop the service:
   ```bash
   sudo systemctl stop solana-exporter.service
   ```

2. Update the code:
   ```bash
   cd /home/sol
   git pull https://github.com/asymmetric-research/solana-exporter.git
   cd solana-exporter
   go build
   ```

3. Start the service:
   ```bash
   sudo systemctl start solana-exporter.service
   ```

### Verifying Metrics
To verify that metrics are being collected correctly:

```bash
# From home server
curl -s 38.97.62.158:9100/metrics | grep -E "solana_block_height|solana_epoch|solana_slot"
```

## Troubleshooting

### Common Issues

1. **Service Not Starting**
   - Check system logs: `journalctl -u solana-exporter.service`
   - Verify permissions on the solana-exporter binary
   - Check for port conflicts
   - Ensure the Solana RPC endpoint is accessible

2. **Missing Metrics**
   - Verify that the Solana RPC endpoint is responding
   - Check that the sol user has access to the required files
   - Ensure the Solana validator is running

### Log Analysis
To analyze the Solana Exporter logs:
```bash
journalctl -u solana-exporter.service -n 100
```