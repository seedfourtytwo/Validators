# Solana Exporter Public Service

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
   - [Comprehensive Mode Operation](#comprehensive-mode-operation)
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
9. [Grafana Dashboards](#grafana-dashboards)
10. [Maintenance](#maintenance)
    - [Updating Solana Exporter](#updating-solana-exporter)
    - [Verifying Metrics](#verifying-metrics)
11. [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Log Analysis](#log-analysis)
12. [Security Considerations](#security-considerations)
13. [Distributed Monitoring Setup](#distributed-monitoring-setup)
    - [Validator Light Mode Configuration](#validator-light-mode-configuration)
    - [Home Server Comprehensive Mode Configuration](#home-server-comprehensive-mode-configuration)
    - [Prometheus Integration](#prometheus-integration)
14. [Related Documentation](#related-documentation)

## Overview
The Solana Exporter Public service runs on the home server and collects comprehensive Solana metrics from public RPC endpoints. It provides network-wide metrics and complements the light exporter running on the validator.

## Service Information
- **Service Name**: solana-exporter.service
- **Service File**: /etc/systemd/system/solana-exporter.service
- **Binary Location**: /home/chris/solana-monitoring/solana-exporter/solana-exporter
- **Run As**: chris user
- **Status**: Active and running
- **Repository**: https://github.com/seedfourtytwo/solana-exporter (forked from asymmetric-research/solana-exporter)
- **Listen Address**: 0.0.0.0:9101
- **RPC Endpoint**: https://api.testnet.solana.com (Testnet)
- **Validator Identity**: JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF
- **Vote Account**: 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL
- **Operation Mode**: Comprehensive mode with vote account tracking

## Purpose
The Solana Exporter Public service complements the light-mode exporter running on the validator by:

1. **Network Context**: Providing broader network context for validator metrics
2. **Public Data Collection**: Collecting data available from public RPCs to reduce load on the validator
3. **Comprehensive Monitoring**: Enabling complete monitoring without impacting validator performance
4. **Vote Account Tracking**: Tracking all vote accounts to compare performance against other validators

## Directory Structure

### File Locations
The Solana Exporter Public is installed in the solana-monitoring directory:

```
/home/chris/solana-monitoring/
├── solana-exporter/
│   └── solana-exporter    # Main binary
└── prometheus/            # Prometheus configuration
```

### Permissions
- Binary owner: chris:chris
- Binary permissions: rwxr-xr-x (755)
- Parent directories require read and execute (rx) permission for the chris user

## Configuration

### Systemd Service Configuration
**File**: /etc/systemd/system/solana-exporter.service
```ini
[Unit]
Description=Solana Exporter for Prometheus
After=network.target

[Service]
User=chris
Group=chris
Type=simple
ExecStart=/home/chris/solana-monitoring/solana-exporter/solana-exporter \
  -rpc-url https://api.testnet.solana.com \
  -listen-address 0.0.0.0:9101 \
  -validator-identity JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF \
  -vote-account-pubkey 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
  -comprehensive-vote-account-tracking
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Command Line Options
The Solana Exporter Public is started with the following options:

| Option | Description | Required |
|--------|-------------|----------|
| `-rpc-url` | URL of the Solana public RPC endpoint | Yes |
| `-listen-address` | Listen address for the metrics endpoint | Yes |
| `-validator-identity` | Validator identity public key to monitor | Yes |
| `-vote-account-pubkey` | Validator vote account public key | Yes |
| `-comprehensive-vote-account-tracking` | Enable tracking of all vote accounts | No |

### Comprehensive Mode Operation
The Solana Exporter on the home server runs in comprehensive mode, which:

- Collects metrics for all validators in the network
- Tracks all vote accounts to provide performance comparisons
- Utilizes a public RPC endpoint instead of the validator's local RPC
- Creates a more complete picture of the validator's performance in the network context
- Reduces the load on the validator itself by offloading metrics collection

## Metrics

### Validator Metrics
| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_validator_active_stake` | gauge | Current active stake in SOL |
| `solana_validator_commission` | gauge | Current commission percentage |
| `solana_validator_last_vote` | gauge | Slot height of the last vote |
| `solana_validator_root_slot` | gauge | Current root slot |
| `solana_validator_delinquent` | gauge | Whether validator is delinquent (1=yes, 0=no) |
| `solana_validator_current_epoch_credits` | gauge | Credits earned in the current epoch |
| `solana_validator_total_credits` | counter | Total vote credits earned since genesis |

### Network Metrics
| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_network_slot` | gauge | Current slot height |
| `solana_network_epoch` | gauge | Current epoch number |
| `solana_network_epoch_progress` | gauge | Progress through current epoch (%) |
| `solana_network_validator_count` | gauge | Total number of validators |
| `solana_network_active_stake` | gauge | Total active stake in SOL |
| `solana_network_current_stake` | gauge | Current stake in SOL |

### Performance Metrics
| Metric Name | Type | Description |
|-------------|------|-------------|
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
# HELP solana_validator_active_stake Active stake (in SOL) per validator (represented by votekey and nodekey)
# TYPE solana_validator_active_stake gauge
solana_validator_active_stake{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF",votekey="3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL"} 34051.172718636

# HELP solana_validator_delinquent Whether the validator is delinquent (not actively voting)
# TYPE solana_validator_delinquent gauge
solana_validator_delinquent{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF",votekey="3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL"} 0
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
Since the service runs on the home server, metrics can be accessed directly:

1. **Local Access**:
   ```bash
   curl http://localhost:9101/metrics
   ```

2. **Specific Metrics**:
   ```bash
   # View validator-specific metrics
   curl http://localhost:9101/metrics | grep -i JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF
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
   - Validator comparison

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
   cd /home/chris/solana-monitoring
   git pull https://github.com/seedfourtytwo/solana-exporter.git
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
# Check validator-specific metrics
curl -s localhost:9101/metrics | grep -i JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF
```

## Troubleshooting

### Common Issues

1. **Service Not Starting**
   - Check system logs: `journalctl -u solana-exporter.service`
   - Verify permissions on the solana-exporter binary
   - Check for port conflicts
   - Ensure the public RPC endpoint is accessible
   - Verify the command line parameters are correct

2. **Missing Metrics**
   - Check that the RPC endpoint is correct (mainnet vs testnet)
   - Verify that the validator identity and vote account are correct
   - Ensure the `-comprehensive-vote-account-tracking` flag is set if needed
   - Check for network connectivity issues to the RPC endpoint

3. **RPC Endpoint Issues**
   - Public RPC endpoints may have rate limits
   - Consider using a paid RPC service for more reliable access
   - Test with different public endpoints if one is unresponsive

### Log Analysis
To analyze the Solana Exporter logs:
```bash
journalctl -u solana-exporter.service -n 100
```

## Security Considerations

1. **Access Control**
   - The metrics endpoint should only be accessible locally or from trusted networks
   - Consider using a firewall to restrict access
   - The service runs with limited user privileges (chris)

2. **Resource Limits**
   - The service may use significant memory with comprehensive vote tracking enabled
   - Monitor resource usage and adjust as needed
   - Consider setting resource limits in the systemd service file

3. **Data Privacy**
   - Only public blockchain data is processed
   - No private keys or sensitive information is exposed
   - All RPC queries are read-only

## Distributed Monitoring Setup

### Validator Light Mode Configuration
The validator server runs Solana Exporter in light mode to minimize resource usage:

```ini
# On validator server: /etc/systemd/system/solana-exporter.service
[Service]
ExecStart=/home/sol/validators/monitoring/solana-exporter/solana-exporter \
  -rpc-url http://127.0.0.1:8899 \
  -listen-address 0.0.0.0:9100 \
  -validator-identity JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF \
  -vote-account-pubkey 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
  -light-mode
```

### Home Server Comprehensive Mode Configuration
The home server runs Solana Exporter in comprehensive mode:

```ini
# On home server: /etc/systemd/system/solana-exporter.service
[Service]
ExecStart=/home/chris/solana-monitoring/solana-exporter/solana-exporter \
  -rpc-url https://api.testnet.solana.com \
  -listen-address 0.0.0.0:9101 \
  -validator-identity JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF \
  -vote-account-pubkey 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
  -comprehensive-vote-account-tracking
```

### Prometheus Integration
Prometheus is configured to scrape both instances:

```yaml
# In prometheus.yml
scrape_configs:
  # Runs on the solana validator and collects metrics that cannot be obtained from public RPCs
  - job_name: 'solana-validator-light'
    static_configs:
      - targets: ['38.97.62.158:9100']
  # Runs on the solana validator and collects all the hardware and system metrics
  - job_name: 'node-validator'
    static_configs:
      - targets: ['38.97.62.158:9110']
    scrape_interval: 15s
  # Runs on the Home server and collects Bitcoin specific metrics
  - job_name: 'bitcoin-node'
    static_configs:
      - targets: ['localhost:9332']
    scrape_interval: 15s
  # Runs on the Home server and collects Solana metrics available from public RPCs
  - job_name: 'solana-public-metrics'
    static_configs:
      - targets: ['localhost:9101']
    scrape_interval: 15s
```

This distributed setup provides complete monitoring while minimizing the impact on the validator itself.

## Related Documentation
- [Solana Exporter Setup Guide](../../../setup-tutorials/solana-exporter.md) - Step-by-step guide for setting up the home server Solana exporter
- [Validator-side Solana Exporter](../../../../solana-validator/services/monitoring/solana-exporter.md) - Documentation for the light-mode Solana exporter running on the validator 