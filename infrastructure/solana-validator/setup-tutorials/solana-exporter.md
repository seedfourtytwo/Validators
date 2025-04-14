# Solana Exporter Setup Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Security Configuration](#security-configuration)
6. [Service Setup](#service-setup)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

## Introduction

Solana Exporter is a Prometheus exporter for Solana blockchain metrics. It collects various Solana-specific metrics and exposes them in Prometheus format, making them available for monitoring and alerting. This guide provides step-by-step instructions for setting up Solana Exporter on your Solana validator server.

This tutorial is based on the existing Solana Exporter configuration found in the [services/solana-exporter.md](../services/solana-exporter.md) file.

## Prerequisites

Before starting, ensure you have:
- A Linux server with Ubuntu 24.04 or later
- Root or sudo access
- The `sol` user created and configured as described in the Linux setup tutorial
- Go programming language installed (version 1.16 or later)
- Basic understanding of systemd service management
- A running Solana validator with RPC access

## Installation

### Install Go (if not already installed)

**Run as: root or user with sudo privileges**

```bash
# Update package list
sudo apt update

# Install Go
sudo apt install golang-go -y

# Verify installation
go version
```

### Clone the Exporter Repository

**Run as: sol user**

```bash
# Switch to sol user if not already
su - sol

# Create directory for the exporter
mkdir -p ~/solana-exporter

# Clone the repository
git clone https://github.com/asymmetric-research/solana-exporter.git ~/solana-exporter
```

### Build the Exporter Binary

**Run as: sol user**

```bash
# Navigate to the exporter directory
cd ~/solana-exporter

# Build the exporter
go build -o ~/solana-exporter/solana-exporter

# Verify it built correctly
~/solana-exporter/solana-exporter --help
```

## Configuration

### Test the Exporter

**Run as: sol user**

```bash
# Run the exporter for testing
~/solana-exporter/solana-exporter \
  -rpc-url http://127.0.0.1:8899 \
  -listen-address 0.0.0.0:9100
```

You should see output similar to:
```
Starting Solana exporter on 0.0.0.0:9100
```

### Test Metrics Access

**Run as: sol user**

In a separate terminal:
```bash
# Test metrics endpoint
curl http://localhost:9100/metrics
```

You should see a list of Solana metrics in Prometheus format.

## Security Configuration

### Configure Firewall Access

**Run as: root or user with sudo privileges**

The Solana Exporter should only be accessible from your home IP address for security reasons. Based on the current firewall configuration in `/etc/nftables.conf`, the following rule is already in place:

```bash
# Allow Solana Exporter port (9100) only from home IP address
tcp dport 9100 ip saddr { 77.200.151.32 } accept  # Solana Exporter
```

If you need to add this rule manually, use the following command:

```bash
# Allow Solana Exporter port (9100) only from your home IP address
sudo nft add rule inet filter input tcp dport 9100 ip saddr { 77.200.151.32 } accept comment "Solana Exporter from home IP"
```

### Verify Firewall Rules

**Run as: root or user with sudo privileges**

```bash
# Check firewall rules
sudo nft list ruleset | grep -A 5 "Solana Exporter"
```

You should see the rule allowing access to port 9100 only from your home IP address.

## Service Setup

### Create Systemd Service

**Run as: root or user with sudo privileges**

```bash
# Create systemd service file
sudo cat > /etc/systemd/system/solana-exporter.service << EOT
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
EOT

# Reload systemd
sudo systemctl daemon-reload
```

### Command Line Options Explained

The Solana Exporter is started with the following options:

| Option | Description |
|--------|-------------|
| `-rpc-url http://127.0.0.1:8899` | URL of the Solana RPC endpoint |
| `-listen-address 0.0.0.0:9100` | Listen address for the metrics endpoint |

## Verification

### Start and Enable the Service

**Run as: root or user with sudo privileges**

```bash
# Enable the service to start on boot
sudo systemctl enable solana-exporter.service

# Start the service
sudo systemctl start solana-exporter.service

# Check status
sudo systemctl status solana-exporter.service
```

### Test Metrics Access

**Run as: sol user**

```bash
# Test metrics endpoint
curl -s http://localhost:9100/metrics | head -n 20
```

### Check Key Metrics

**Run as: sol user**

```bash
# Check Solana metrics
curl -s http://localhost:9100/metrics | grep -E "solana_block_height|solana_epoch|solana_slot"
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

3. **Permission Errors**
   - Ensure the sol user has proper permissions:
     ```bash
     sudo chown -R sol:sol ~/solana-exporter
     ```

4. **Port Already in Use**
   - Check if another service is using port 9100:
     ```bash
     sudo lsof -i :9100
     ```
   - If needed, change the port in the service file and firewall rules

### Log Analysis

To analyze the Solana Exporter logs:
```bash
journalctl -u solana-exporter.service -n 100
```

## Integration with Prometheus

To integrate Solana Exporter with Prometheus, add the following to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'validator-solana'
    static_configs:
      - targets: ['38.97.62.158:9100']
```

Replace `38.97.62.158` with your validator's IP address if different.

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
   cd ~/solana-exporter
   git pull https://github.com/asymmetric-research/solana-exporter.git
   go build -o ~/solana-exporter/solana-exporter
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

Replace `38.97.62.158` with your validator's IP address if different.