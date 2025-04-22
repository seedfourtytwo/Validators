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
   - [Light Mode Operation](#light-mode-operation)
6. [Metrics](#metrics)
   - [Validator Metrics](#validator-metrics)
   - [Network Metrics](#network-metrics)
   - [Performance Metrics](#performance-metrics)
   - [Metrics Format](#metrics-format)
   - [Metrics Availability by Mode](#metrics-availability-by-mode)
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
13. [Distributed Monitoring Setup](#distributed-monitoring-setup)
    - [Validator Light Mode Configuration](#validator-light-mode-configuration)
    - [Home Server Comprehensive Mode Configuration](#home-server-comprehensive-mode-configuration)
    - [Prometheus Integration](#prometheus-integration)

## Overview
Solana Exporter is a Prometheus exporter for Solana blockchain metrics. It collects various Solana-specific metrics and exposes them in Prometheus format, making them available for monitoring and alerting. This document details the configuration and operation of the Solana Exporter on my Solana validator server.

## Service Information
- **Service Name**: solana-exporter.service
- **Service File**: /etc/systemd/system/solana-exporter.service
- **Binary Location**: /home/sol/validators/monitoring/solana-exporter/solana-exporter
- **Run As**: sol user
- **Status**: Active and running
- **Repository**: https://github.com/seedfourtytwo/solana-exporter (forked from asymmetric-research/solana-exporter)
- **Listen Address**: 0.0.0.0:9100
- **Server IP**: 38.97.62.158
- **Access Restriction**: Only accessible from home IP address for security
- **RPC Endpoint**: http://127.0.0.1:8899
- **Validator Identity**: JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF
- **Vote Account**: 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL
- **Operation Mode**: Light mode (validator-specific metrics only)

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
  -validator-identity JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF \
  -vote-account-pubkey 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
  -light-mode
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
| `-validator-identity` | Validator identity public key to monitor | Yes |
| `-vote-account-pubkey` | Validator vote account public key | Yes |
| `-light-mode` | Enable light mode (validator-specific metrics only) | No |

### Light Mode Operation
The Solana Exporter supports a "light mode" that reduces the load on the validator by only collecting metrics that are unique to the validator node being queried. In light mode:

- Only validator-specific metrics that require local node access are collected
- Network-wide metrics (`solana_network_*`) are completely excluded
- Cluster metrics (`solana_cluster_*`) are excluded to avoid duplication with the home server exporter
- Performance metrics that can be obtained from public RPCs are excluded
- The validator experiences reduced CPU, memory, and network load
- The exporter's memory footprint is significantly smaller

This optimized light mode implementation ensures no metric duplication between the validator's exporter and the home server's comprehensive exporter. Each exporter has a clearly defined role:

- **Validator Light Exporter**: Collects only metrics that require local access to the validator
- **Home Server Comprehensive Exporter**: Collects all network-wide metrics and metrics available through public RPCs

Light mode is ideal for the validator server, while a separate instance in full mode can run on a monitoring server using public RPCs to collect the remaining metrics.

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

### Metrics Availability by Mode

| Metric Category | Full Mode | Light Mode | Source in Light Mode |
|-----------------|-----------|------------|----------------------|
| `solana_node_*` metrics | ✅ | ✅ | Validator RPC |
| Validator status | ✅ | ✅ | Validator RPC |
| Validator version | ✅ | ✅ | Validator RPC |
| Validator health | ✅ | ✅ | Validator RPC |
| `solana_validator_*` credits | ✅ | ✅ | Validator RPC |
| `solana_network_*` metrics | ✅ | ❌ | N/A (collected by home server) |
| `solana_cluster_*` metrics | ✅ | ❌ | N/A (collected by home server) |
| Public validator stats | ✅ | ❌ | N/A (collected by home server) |
| Performance metrics | ✅ | ❌ | N/A (collected by home server) |

When running in light mode, the metrics output is significantly reduced to only include validator-specific metrics:
```
# Before light mode: ~10,742 bytes of metrics data
# After optimized light mode: ~150 lines of metrics data
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

## Distributed Monitoring Setup

The monitoring setup is distributed between the validator and home server to optimize resource usage while still providing complete metrics:

### Validator Light Mode Configuration
The validator server runs Solana Exporter in light mode to minimize resource usage while still collecting essential validator-specific metrics that can only be obtained from the validator itself:

1. **Light Mode Service Configuration**:
   ```ini
   # /etc/systemd/system/solana-exporter.service
   [Service]
   ExecStart=/home/sol/validators/monitoring/solana-exporter/solana-exporter \
     -rpc-url http://127.0.0.1:8899 \
     -listen-address 0.0.0.0:9100 \
     -validator-identity JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF \
     -vote-account-pubkey 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
     -light-mode
   ```

2. **Metrics Available**:
   - `solana_node_*` metrics (health, slots, epochs, identity)
   - `solana_validator_current_epoch_credits`
   - `solana_validator_total_credits`
   - Validator-specific internal metrics

3. **Metrics Excluded**:
   - `solana_network_*` metrics
   - `solana_cluster_*` metrics
   - Performance metrics that can be obtained from public RPCs
   - Public validator statistics

### Home Server Comprehensive Mode Configuration
The home server runs a separate instance of Solana Exporter in comprehensive mode, collecting all network-wide and public metrics from public RPC endpoints (testnet):

1. **Full Mode Service Configuration**:
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

2. **Metrics Available**:
   - Network-wide metrics (slots, epochs, total stake)
   - Public validator statistics
   - Performance metrics
   - Comparison with other validators

3. **Home Server Documentation**:
   - Full documentation: [Solana Exporter Public](../../../home-server/services/monitoring/solana-exporter-public/solana-exporter-public.md)
   - Setup guide: [Solana Exporter Setup Guide](../../../home-server/setup-tutorials/solana-exporter.md)

### Prometheus Integration
Prometheus is configured to scrape both instances, using job names to distinguish the sources:

```yaml
# In prometheus.yml on the home server
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

This setup allows for complete monitoring of the validator with minimal impact on the validator's performance. The validator-side exporter (light mode) focuses on metrics that can only be obtained locally, while the home server exporter (comprehensive mode) collects all public metrics using testnet RPC endpoints.