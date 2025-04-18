# Node Exporter Service

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
   - [System Metrics](#system-metrics)
   - [Hardware Metrics](#hardware-metrics)
   - [Process Metrics](#process-metrics)
   - [Metrics Format](#metrics-format)
7. [Service Management](#service-management)
   - [Starting the Service](#starting-the-service)
   - [Stopping the Service](#stopping-the-service)
   - [Restarting the Service](#restarting-the-service)
   - [Checking Service Status](#checking-service-status)
   - [Enabling Service on Boot](#enabling-service-on-boot)
8. [Accessing Metrics](#accessing-metrics)
   - [Remote Access from Home Server](#remote-access-from-home-server)
9. [Maintenance](#maintenance)
   - [Updating Node Exporter](#updating-node-exporter)
   - [Verifying Metrics](#verifying-metrics)
10. [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Log Analysis](#log-analysis)
11. [Security Considerations](#security-considerations)

## Overview
Node Exporter is a Prometheus exporter for hardware and OS metrics. It collects various system metrics and exposes them in Prometheus format, making them available for monitoring and alerting. This document details the configuration and operation of the Node Exporter on my Solana validator server.

## Service Information
- **Service Name**: node_exporter.service
- **Service File**: /etc/systemd/system/node_exporter.service
- **Binary Location**: /home/sol/validators/monitoring/node-exporter/node_exporter
- **Run As**: node_exporter user (member of sol group)
- **Status**: Active and running
- **Version**: node_exporter 1.9.1
- **Repository**: https://github.com/prometheus/node_exporter
- **Listen Address**: :9110
- **Server IP**: 38.97.62.158
- **Access Restriction**: Only accessible from home IP address for security

## Purpose
Node Exporter serves several critical functions for the Solana validator:

1. **System Monitoring**: Collects metrics about CPU, memory, disk, and network usage
2. **Hardware Monitoring**: Provides information about hardware components and their status
3. **Performance Tracking**: Enables tracking of system performance over time
4. **Alerting**: Provides data for alerting on system issues

## Directory Structure

### File Locations
The Node Exporter is installed in the validators monitoring directory alongside other monitoring tools:

```
/home/sol/validators/monitoring/
├── node-exporter/
│   └── node_exporter    # Main binary
└── solana-exporter/     # Other monitoring tools
```

### Permissions
- Binary owner: node_exporter:node_exporter
- Binary permissions: rwxr-xr-x (755)
- User 'node_exporter' is member of 'sol' group for directory access
- Parent directories require at least execute (x) permission for the sol group

## Configuration

### Systemd Service Configuration
**File**: /etc/systemd/system/node_exporter.service
```ini
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/home/sol/validators/monitoring/node-exporter/node_exporter \
    --web.listen-address=:9110 \
    --collector.hwmon \
    --path.procfs=/proc \
    --path.sysfs=/sys

[Install]
WantedBy=multi-user.target
```

### Command Line Options
The Node Exporter is started with the following options:

| Option | Description |
|--------|-------------|
| `--web.listen-address=:9110` | Listen address for the web interface and metrics endpoint |
| `--collector.hwmon` | Enable the hwmon collector for hardware monitoring |
| `--path.procfs=/proc` | Path to the proc filesystem |
| `--path.sysfs=/sys` | Path to the sys filesystem |

## Metrics

### System Metrics
- **CPU Metrics**: Usage, frequency, temperature, and performance
- **Memory Metrics**: Usage, swap, and memory pressure
- **Disk Metrics**: I/O, space usage, and performance
- **Network Metrics**: Traffic, errors, and connections
- **File System Metrics**: Usage, inodes, and performance

### Hardware Metrics
- **Thermal Metrics**: CPU and system temperature
- **Power Metrics**: Power consumption and limits
- **Hardware Events**: Hardware errors and warnings

### Process Metrics
- **Process Count**: Number of processes by state
- **Context Switches**: System-wide context switching
- **System Load**: System load averages

### Metrics Format
Node Exporter metrics follow the Prometheus format. Each metric has:
- A HELP line explaining the metric
- A TYPE line specifying the metric type (counter, gauge, histogram, etc.)
- One or more lines with the actual metric values and labels

Example metrics:
```
# HELP node_cpu_seconds_total Seconds the cpus spent in each mode.
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 2334.18
node_cpu_seconds_total{cpu="0",mode="iowait"} 5.64

# HELP node_memory_MemTotal_bytes Memory information field MemTotal_bytes.
# TYPE node_memory_MemTotal_bytes gauge
node_memory_MemTotal_bytes 1.34202994688e+11
```

## Service Management

### Starting the Service
```bash
sudo systemctl start node_exporter.service
```

### Stopping the Service
```bash
sudo systemctl stop node_exporter.service
```

### Restarting the Service
```bash
sudo systemctl restart node_exporter.service
```

### Checking Service Status
```bash
sudo systemctl status node_exporter.service
```

### Enabling Service on Boot
```bash
sudo systemctl enable node_exporter.service
```

## Accessing Metrics

### Remote Access from Home Server
Since the validator server doesn't have a web browser, metrics should be accessed from the home server:

1. **Direct HTTP Access**:
   ```
   curl http://38.97.62.158:9110/metrics
   ```

2. **Using SSH Tunnel**:
   ```bash
   # On home server
   ssh -L 9110:localhost:9110 38.97.62.158
   
   # Then access metrics locally
   curl http://localhost:9110/metrics
   ```

3. **Using Prometheus**:
   Configure Prometheus on the home server to scrape the validator's Node Exporter:
   ```yaml
   scrape_configs:
     - job_name: 'validator-node'
       static_configs:
         - targets: ['38.97.62.158:9110']
   ```

## Maintenance

### Updating Node Exporter
To update Node Exporter to a new version:

1. Stop the service:
   ```bash
   sudo systemctl stop node_exporter.service
   ```

2. Download and install the new version:
   ```bash
   wget https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz
   tar xvf node_exporter-1.9.1.linux-amd64.tar.gz
   sudo cp node_exporter-1.9.1.linux-amd64/node_exporter /home/sol/validators/monitoring/node-exporter/
   sudo chown node_exporter:node_exporter /home/sol/validators/monitoring/node-exporter/node_exporter
   sudo chmod 755 /home/sol/validators/monitoring/node-exporter/node_exporter
   ```

3. Start the service:
   ```bash
   sudo systemctl start node_exporter.service
   ```

### Verifying Metrics
To verify that metrics are being collected correctly:

```bash
# From home server
curl -s 38.97.62.158:9110/metrics | grep -E "node_cpu_seconds_total|node_memory_MemTotal_bytes"
```

## Troubleshooting

### Common Issues

1. **Service Not Starting**
   - Check system logs: `journalctl -u node_exporter.service`
   - Verify permissions on the node_exporter binary
   - Check for port conflicts
   - Verify node_exporter user has access to all parent directories
   - Ensure node_exporter user is in the sol group

2. **Permission Issues**
   - Verify binary ownership: `ls -l /home/sol/validators/monitoring/node-exporter/node_exporter`
   - Check group membership: `groups node_exporter`
   - Verify parent directory permissions: `ls -la /home/sol/validators/monitoring/`

### Log Analysis
To analyze the Node Exporter logs:
```bash
journalctl -u node_exporter.service -n 100
```

## Security Considerations

1. **Access Control**
   - Node Exporter is only accessible from the home server IP address
   - Firewall rules restrict access to only the home IP address for security
   - Consider implementing authentication if exposed externally

2. **Resource Limits**
   - Node Exporter has minimal resource requirements
   - No specific resource limits are needed

3. **Data Privacy**
   - Node Exporter collects system metrics only
   - No sensitive data is exposed

4. **File Permissions**
   - Binary is owned by node_exporter user
   - Minimal required permissions are set on binary and directories
   - node_exporter user has limited system access
