# Solana Exporter Service

## Table of Contents
1. [Overview](#overview)
2. [Service Information](#service-information)
3. [Purpose](#purpose)
4. [Directory Structure](#directory-structure)
   - [File Locations](#file-locations)
   - [Permissions](#permissions)
5. [Configuration](#configuration)
   - [Systemd Service Configuration](#systemd-service-configuration)
   - [Command Line Options](#command-line-options)
6. [Metrics](#metrics)
   - [Validator Metrics](#validator-metrics)
   - [Network Metrics](#network-metrics)
   - [Performance Metrics](#performance-metrics)
   - [Metrics Format](#metrics-format)
7. [Service Management](#service-management)
   - [Starting the Service](#starting-the-service)
   - [Stopping the Service](#stopping-the-service)
   - [Restarting the Service](#restarting-the-service)
   - [Checking Service Status](#checking-service-status)
   - [Enabling Service on Boot](#enabling-service-on-boot)
8. [Accessing Metrics](#accessing-metrics)
   - [Remote Access from Home Server](#remote-access-from-home-server)
9. [Grafana Dashboards](#grafana-dashboards)
10. [Maintenance](#maintenance)
    - [Updating Solana Exporter](#updating-solana-exporter)
    - [Verifying Metrics](#verifying-metrics)
11. [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Log Analysis](#log-analysis)
12. [Security Considerations](#security-considerations)

## Overview
Solana Exporter is a Prometheus exporter for Solana blockchain metrics. It collects various Solana-specific metrics and exposes them in Prometheus format, making them available for monitoring and alerting. This document details the configuration and operation of the Solana Exporter on my Solana validator server.

## Service Information
- **Service Name**: solana-exporter.service
- **Service File**: /etc/systemd/system/solana-exporter.service
- **Binary Location**: /home/sol/validators/monitoring/solana-exporter/solana-exporter
- **Run As**: sol user
- **Status**: Active and running
- **Repository**: https://github.com/asymmetric-research/solana-exporter
- **Listen Address**: 0.0.0.0:9100
- **Server IP**: 38.97.62.158
- **Access Restriction**: Only accessible from home IP address for security
- **RPC Endpoint**: http://127.0.0.1:8899
- **Validator Identity**: JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF

## Purpose
Solana Exporter serves several critical functions for the Solana validator:

1. **Validator Monitoring**: Collects metrics about validator performance and health
2. **Network Monitoring**: Provides information about the Solana network status
3. **Performance Tracking**: Enables tracking of validator performance over time
4. **Alerting**: Provides data for alerting on validator issues

## Directory Structure

### File Locations
The Solana Exporter is installed in the validators monitoring directory alongside other monitoring tools:

```
/home/sol/validators/monitoring/
├── solana-exporter/
│   └── solana-exporter    # Main binary
└── node-exporter/         # Other monitoring tools
```

### Permissions
- Binary owner: sol:sol
- Binary permissions: rwxr-xr-x (755)
- Parent directories require read and execute (rx) permission for the sol user

## Configuration

### Systemd Service Configuration
**File**: /etc/systemd/system/solana-exporter.service
```ini
[Unit]
Description=Solana Exporter for Prometheus
After=network.target

[Service]
User=sol
WorkingDirectory=/home/sol
ExecStart=/home/sol/validators/monitoring/solana-exporter/solana-exporter \
  -rpc-url http://127.0.0.1:8899 \
  -listen-address 0.0.0.0:9100 \
  -nodekey JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Command Line Options
The Solana Exporter is started with the following options:

| Option | Description | Required |
|--------|-------------|----------|
| `-rpc-url` | URL of the Solana RPC endpoint | Yes |
| `-listen-address` | Listen address for the metrics endpoint | Yes |
| `-nodekey` | Validator identity public key to monitor | Yes |

## Metrics

### Validator Metrics
| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_validator_activated_stake` | gauge | Current activated stake in SOL |
| `solana_validator_commission` | gauge | Current commission percentage |
| `solana_validator_last_vote` | gauge | Slot height of the last vote |
| `solana_validator_root_slot` | gauge | Current root slot |
| `solana_validator_delinquent` | gauge | Whether validator is delinquent (1=yes, 0=no) |
| `solana_validator_version` | gauge | Solana software version |
| `solana_validator_credits` | counter | Total vote credits earned |
| `solana_validator_skip_rate` | gauge | Vote skip rate as percentage |

### Network Metrics
| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_network_slot` | gauge | Current slot height |
| `solana_network_epoch` | gauge | Current epoch number |
| `solana_network_epoch_progress` | gauge | Progress through current epoch (%) |
| `solana_network_validator_count` | gauge | Total number of validators |
| `solana_network_active_stake` | gauge | Total active stake in SOL |
| `solana_network_current_stake` | gauge | Current stake in SOL |
| `solana_network_total_supply` | gauge | Total SOL supply |

### Performance Metrics
| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_performance_tower_distance` | gauge | Tower vote distance |
| `solana_performance_block_time` | gauge | Average block time (ms) |
| `solana_performance_slot_time` | gauge | Average slot time (ms) |
| `solana_performance_skip_rate` | gauge | Network skip rate (%) |
| `solana_performance_transaction_count` | counter | Total transaction count |
| `solana_performance_block_height` | gauge | Current block height |

### Metrics Format
Solana Exporter metrics follow the Prometheus format. Each metric has:
- A HELP line explaining the metric
- A TYPE line specifying the metric type (counter, gauge, histogram)
- One or more lines with the actual metric values and labels

Example metrics:
```
# HELP solana_validator_activated_stake Current activated stake in SOL
# TYPE solana_validator_activated_stake gauge
solana_validator_activated_stake{pubkey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"} 1234567.89

# HELP solana_validator_skip_rate Vote skip rate as percentage
# TYPE solana_validator_skip_rate gauge
solana_validator_skip_rate{pubkey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"} 1.23

# HELP solana_network_epoch Current epoch number
# TYPE solana_network_epoch gauge
solana_network_epoch 123
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

### Available Dashboards
1. **Solana Validator Dashboard**
   - Validator performance metrics
   - Skip rate comparison
   - Vote statistics
   - Stake and commission tracking

2. **Solana Network Dashboard**
   - Network-wide metrics
   - Epoch progress
   - Transaction statistics
   - Supply and stake distribution

### Dashboard Features
- Real-time updates
- Historical data views
- Customizable time ranges
- Alert thresholds
- Multi-validator comparison

## Maintenance

### Updating Solana Exporter
To update Solana Exporter to a new version:

1. Stop the service:
   ```bash
   sudo systemctl stop solana-exporter.service
   ```

2. Update the code:
   ```bash
   cd /home/sol/validators/monitoring
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
   - Verify the `-nodekey` parameter is correct (not `-identity`)

2. **Missing Metrics**
   - Verify that the Solana RPC endpoint is responding
   - Check that the sol user has access to the required files
   - Ensure the Solana validator is running

### Log Analysis
To analyze the Solana Exporter logs:
```bash
journalctl -u solana-exporter.service -n 100
```

## Security Considerations

1. **Access Control**
   - Solana Exporter is only accessible from the home server IP address
   - Firewall rules restrict access to port 9100
   - RPC endpoint is only accessible locally

2. **Resource Limits**
   - Service runs with regular user privileges (sol)
   - No special resource limits needed
   - Minimal system impact

3. **Data Privacy**
   - Only public validator data is exposed
   - No private keys or sensitive information collected
   - RPC queries are read-only

4. **Network Security**
   - Local RPC endpoint reduces attack surface
   - Metrics endpoint is firewalled
   - Regular security updates applied