# Node Exporter Setup Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [User Configuration](#user-configuration)
5. [Service Configuration](#service-configuration)
6. [Security Configuration](#security-configuration)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

## Introduction

Node Exporter is a Prometheus exporter for hardware and OS metrics. It collects various system metrics and exposes them in Prometheus format, making them available for monitoring and alerting. This guide provides step-by-step instructions for setting up Node Exporter on your Solana validator server.

This tutorial is based on the existing Node Exporter configuration found in the [services/monitoring/node-exporter.md](../services/monitoring/node-exporter.md) file.

## Prerequisites

Before starting, ensure you have:
- A Linux server with Ubuntu 24.04 or later
- Root or sudo access
- The `node_exporter` user created and configured as described in the Linux setup tutorial
- Basic understanding of systemd service management

## Installation

### Download Node Exporter

**Run as: root or user with sudo privileges**

```bash
# Create directory for Node Exporter
sudo mkdir -p /usr/local/bin

# Download Node Exporter (version 1.9.1)
sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz

# Extract the archive
sudo tar xvf node_exporter-1.9.1.linux-amd64.tar.gz

# Copy the binary to /usr/local/bin
sudo cp node_exporter-1.9.1.linux-amd64/node_exporter /usr/local/bin/

# Set proper permissions
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
sudo chmod +x /usr/local/bin/node_exporter

# Clean up
sudo rm -rf node_exporter-1.9.1.linux-amd64.tar.gz node_exporter-1.9.1.linux-amd64
```

## User Configuration

### Create Node Exporter User

**Run as: root or user with sudo privileges**

```bash
# Create node_exporter user if not already created
sudo useradd -r -s /bin/false node_exporter

# Create node_exporter group
sudo groupadd node_exporter

# Add node_exporter user to the group
sudo usermod -a -G node_exporter node_exporter

# Set ownership of the binary
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```

## Service Configuration

### Create Systemd Service

**Run as: root or user with sudo privileges**

```bash
# Create systemd service file
sudo cat > /etc/systemd/system/node_exporter.service << EOT
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter --web.listen-address=:9110 --collector.hwmon --path.procfs=/proc --path.sysfs=/sys

[Install]
WantedBy=multi-user.target
EOT

# Reload systemd
sudo systemctl daemon-reload
```

### Command Line Options Explained

The Node Exporter is started with the following options:

| Option | Description |
|--------|-------------|
| `--web.listen-address=:9110` | Listen address for the web interface and metrics endpoint |
| `--collector.hwmon` | Enable the hwmon collector for hardware monitoring |
| `--path.procfs=/proc` | Path to the proc filesystem |
| `--path.sysfs=/sys` | Path to the sys filesystem |

## Security Configuration

### Configure Firewall Access

**Run as: root or user with sudo privileges**

The Node Exporter should only be accessible from your home IP address for security reasons. Based on the current firewall configuration in `/etc/nftables.conf`, the following rule is already in place:

```bash
# Allow Node Exporter port (9110) only from home IP address
tcp dport 9110 ip saddr { 77.200.151.32 } accept  # Node Exporter
```

If you need to add this rule manually, use the following command:

```bash
# Allow Node Exporter port (9110) only from your home IP address
sudo nft add rule inet filter input tcp dport 9110 ip saddr { 77.200.151.32 } accept comment "Node Exporter from home IP"
```

### Verify Firewall Rules

**Run as: root or user with sudo privileges**

```bash
# Check firewall rules
sudo nft list ruleset | grep -A 5 "Node Exporter"
```

You should see the rule allowing access to port 9110 only from your home IP address.

## Verification

### Start and Enable the Service

**Run as: root or user with sudo privileges**

```bash
# Enable the service to start on boot
sudo systemctl enable node_exporter.service

# Start the service
sudo systemctl start node_exporter.service

# Check status
sudo systemctl status node_exporter.service
```

### Test Metrics Access

**Run as: root or user with sudo privileges**

```bash
# Test metrics endpoint
curl -s http://localhost:9110/metrics | head -n 10
```

### Check Key Metrics

**Run as: root or user with sudo privileges**

```bash
# Check CPU metrics
curl -s http://localhost:9110/metrics | grep -E "node_cpu_seconds_total|node_memory_MemTotal_bytes"
```

## Troubleshooting

### Common Issues

1. **Service Not Starting**
   - Check system logs: `journalctl -u node_exporter.service`
   - Verify permissions on the node_exporter binary
   - Check for port conflicts

2. **Permission Errors**
   - Ensure the node_exporter user has proper permissions:
     ```bash
     sudo chown -R node_exporter:node_exporter /usr/local/bin/node_exporter
     ```

3. **Port Already in Use**
   - Check if another service is using port 9110:
     ```bash
     sudo lsof -i :9110
     ```
   - If needed, change the port in the service file and firewall rules

### Log Analysis

To analyze the Node Exporter logs:
```bash
journalctl -u node_exporter.service -n 100
```

## Integration with Prometheus

To integrate Node Exporter with Prometheus, add the following to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'validator-node'
    static_configs:
      - targets: ['38.97.62.158:9110']
```

Replace `38.97.62.158` with your validator's IP address if different.

## Grafana Dashboards

Node Exporter metrics can be visualized using Grafana dashboards. Recommended dashboards include:

1. **Node Exporter Full**: Comprehensive dashboard for all Node Exporter metrics
2. **Node Exporter for Solana**: Custom dashboard optimized for Solana validator monitoring

## Maintenance

### Updating Node Exporter

To update Node Exporter to a new version:

1. Stop the service:
   ```bash
   sudo systemctl stop node_exporter.service
   ```

2. Download and install the new version:
   ```bash
   sudo wget https://github.com/prometheus/node_exporter/releases/download/vNEW_VERSION/node_exporter-NEW_VERSION.linux-amd64.tar.gz
   sudo tar xvf node_exporter-NEW_VERSION.linux-amd64.tar.gz
   sudo cp node_exporter-NEW_VERSION.linux-amd64/node_exporter /usr/local/bin/
   sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
   sudo chmod +x /usr/local/bin/node_exporter
   sudo rm -rf node_exporter-NEW_VERSION.linux-amd64.tar.gz node_exporter-NEW_VERSION.linux-amd64
   ```

3. Start the service:
   ```bash
   sudo systemctl start node_exporter.service
   ```

Replace `NEW_VERSION` with the version number you want to install.
