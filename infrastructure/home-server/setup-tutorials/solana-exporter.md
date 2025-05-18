# Solana Exporter Setup Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
   - [Install Go](#install-go)
   - [Directory Structure](#directory-structure)
   - [Download and Build](#download-and-build)
4. [Configuration](#configuration)
   - [Test the Exporter](#test-the-exporter)
   - [Service Configuration](#service-configuration)
5. [Prometheus Integration](#prometheus-integration)
6. [Validation and Testing](#validation-and-testing)
7. [Troubleshooting](#troubleshooting)
8. [Related Documentation](#related-documentation)

## Introduction

Solana Exporter is a Prometheus exporter for Solana blockchain metrics. It collects Solana metrics via public RPC endpoints (either mainnet or testnet) and exposes them in Prometheus format, providing a complete view of the validator's performance in the broader network context.

This guide describes how to set up the Solana Exporter on your home server to collect metrics for a Solana validator using public RPC endpoints. This setup complements a light-mode Solana Exporter running on the validator itself by collecting network-wide metrics without adding extra load to the validator.

## Prerequisites

Before starting, ensure you have:
- Ubuntu server 22.04 or later
- Root or sudo access
- Your validator's identity public key
- Your validator's vote account public key
- Internet connectivity to access public Solana RPC endpoints

## Installation

### Install Go

The Solana Exporter is written in Go, so you'll need to install the Go programming language first.

**Run as: root or user with sudo privileges**

```bash
# Check if Go is already installed
go version

# If not installed, install it
sudo apt update
sudo apt install golang-go -y

# Verify installation
go version
```

You should see an output with the Go version, for example: `go version go1.18.1 linux/amd64`

### Directory Structure

Create the necessary directory structure for the Solana Exporter:

**Run as: your regular user (e.g., chris)**

```bash
# Create directory for monitoring tools
mkdir -p ~/solana-monitoring/solana-exporter
cd ~/solana-monitoring
```

### Download and Build

Clone the repository and build the exporter:

```bash
# Clone the repository
git clone https://github.com/asymmetric-research/solana-exporter.git solana-exporter

# Navigate to the exporter directory
cd solana-exporter

# Build the exporter
go build

# Verify the binary works
./solana-exporter --help
```

You should see the help output showing all available command line options.

## Configuration

### Test the Exporter

Before creating a service, test that the exporter works correctly:

```bash
# Replace the identity and vote account with your own values
./solana-exporter \
  -rpc-url https://api.testnet.solana.com \
  -listen-address 0.0.0.0:9101 \
  -validator-identity JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF \
  -vote-account-pubkey 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
  -comprehensive-vote-account-tracking
```

In a separate terminal, check if metrics are being exposed:

```bash
curl http://localhost:9101/metrics | grep solana
```

Press Ctrl+C to stop the test when finished.

### Service Configuration

Create a systemd service to run the exporter:

**Run as: root or user with sudo privileges**

```bash
sudo nano /etc/systemd/system/solana-exporter.service
```

Add the following content to the file:

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

Replace:
- `chris` with your username
- `/home/chris/...` with your actual home directory path
- The validator identity and vote account with your own values
- If you're running a mainnet validator, change the RPC URL to `https://api.mainnet-beta.solana.com`

Start and enable the service:

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Start the service
sudo systemctl start solana-exporter.service

# Enable the service to start on boot
sudo systemctl enable solana-exporter.service

# Check the status
sudo systemctl status solana-exporter.service
```

The status should show that the service is active (running).

## Prometheus Integration

Add the Solana exporter to your Prometheus configuration:

```bash
sudo nano ~/solana-monitoring/prometheus/prometheus.yml
```

Add a new job for the Solana public metrics:

```yaml
scrape_configs:
  # ... existing jobs ...
  
  # Runs on the Home server and collects Solana metrics available from public RPCs
  - job_name: 'solana-public-metrics'
    static_configs:
      - targets: ['localhost:9101']
    scrape_interval: 15s
```

Restart Prometheus to apply the changes:

```bash
# If using Docker
docker restart solana-monitoring-prometheus-1

# If using systemd
sudo systemctl restart prometheus.service
```

## Validation and Testing

### Check Service Status

Verify that the service is running correctly:

```bash
sudo systemctl status solana-exporter.service
```

### Check Metrics Availability

Verify that metrics are being correctly exposed:

```bash
# Check all metrics
curl http://localhost:9101/metrics | head -20

# Check validator-specific metrics
curl http://localhost:9101/metrics | grep -i YOUR_VALIDATOR_IDENTITY
```

Replace `YOUR_VALIDATOR_IDENTITY` with your validator's identity public key.

### Verify in Prometheus

Access the Prometheus web interface (typically at http://localhost:9090) and verify that the metrics are being scraped successfully:

1. Go to Status -> Targets to see if the `solana-public-metrics` target is UP
2. Try querying some metrics:
   - `solana_validator_active_stake`
   - `solana_validator_delinquent`
   - `solana_network_slot`

## Troubleshooting

### Common Issues

#### Service Won't Start

If the service won't start:

```bash
# Check the logs
journalctl -u solana-exporter.service -n 100

# Verify the binary path
ls -la ~/solana-monitoring/solana-exporter/solana-exporter

# Check file permissions
sudo chmod +x ~/solana-monitoring/solana-exporter/solana-exporter
```

#### No Metrics Available

If you're not seeing metrics:

```bash
# Check connectivity to the RPC endpoint
curl https://api.testnet.solana.com -I

# Verify the identity and vote account are correct
# Try running the exporter manually with verbose logging
```

#### High Memory Usage

The `-comprehensive-vote-account-tracking` flag causes the exporter to track all validators, which increases memory usage. If this is a concern, you can remove this flag, but you'll lose comparison metrics with other validators.

## Related Documentation

- [Solana Exporter Documentation](../services/monitoring/solana-exporter-public/solana-exporter-public.md) - Full documentation for the home server Solana exporter
- [Validator-side Solana Exporter](../../solana-validator/services/monitoring/solana-exporter.md) - Documentation for the light-mode Solana exporter on the validator
- [Prometheus Setup Guide](prometheus.md) - Guide for setting up Prometheus monitoring
- [Grafana Setup Guide](grafana.md) - Guide for setting up Grafana dashboards 