# Prometheus Setup Tutorial

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Image Setup](#docker-image-setup)
3. [Directory Structure Setup](#directory-structure-setup)
4. [Configuration Files](#configuration-files)
5. [Firewall Configuration](#firewall-configuration)
6. [Docker Setup](#docker-setup)
7. [Monitoring Configuration](#monitoring-configuration)
8. [Data Management](#data-management)
9. [Maintenance & Management](#maintenance--management)
10. [Troubleshooting](#troubleshooting)

## Prerequisites
- Docker and Docker Compose installed
- Access to ports 9090 (Prometheus) and target ports (9100, 9110, 9332)
- Basic understanding of YAML
- Root or sudo access
- Network access to monitored services

## Docker Image Setup

### 1. Pull Prometheus Image
```bash
# Pull the official Prometheus image
docker pull prom/prometheus:v2.45.0

# Verify the image
docker images | grep prometheus
```

### 2. Image Details
- **Official Image**: `prom/prometheus`
- **Version**: v2.45.0 (stable)
- **Size**: ~200MB
- **Base OS**: Alpine Linux
- **Architecture**: Supports multiple architectures (amd64, arm64, arm/v7)

### 3. Version Control
```bash
# List available tags
docker search prom/prometheus

# Tag the image for your project
docker tag prom/prometheus:v2.45.0 solana-monitoring-prometheus:v2.45.0
```

## Directory Structure Setup
```bash
# Create base directory
mkdir -p /home/chris/solana-monitoring/prometheus

# Set proper permissions
chown -R chris:chris /home/chris/solana-monitoring/prometheus
chmod -R 755 /home/chris/solana-monitoring/prometheus
```

## Configuration Files

### 1. Prometheus Configuration
File: `/home/chris/solana-monitoring/prometheus/prometheus.yml`
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'solana-validator'
    static_configs:
      - targets: ['38.97.62.158:9100']
  - job_name: 'node_validator'
    static_configs:
      - targets: ['38.97.62.158:9110']
    scrape_interval: 15s
  - job_name: 'bitcoin-node'
    static_configs:
      - targets: ['localhost:9332']
    scrape_interval: 15s
```

### 2. Docker Compose Configuration
Add to your existing `docker-compose.yml`:
```yaml
services:
  prometheus:
    image: prom/prometheus:v2.45.0
    container_name: solana-monitoring-prometheus-1
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'

volumes:
  prometheus_data:
```

## Firewall Configuration

### 1. Required Ports
| Port | Service | Direction | Purpose |
|------|---------|-----------|----------|
| 9090 | Prometheus | Inbound | Web interface and API |
| 9100 | Solana Validator | Outbound | Node exporter metrics |
| 9110 | Node Validator | Outbound | Custom validator metrics |
| 9332 | Bitcoin Node | Local | Bitcoin metrics |

### 2. NFTables Configuration
File: `/etc/nftables.conf`
```bash
# Add to your existing nftables configuration
table inet filter {
    chain input {
        # Allow Prometheus web interface
        tcp dport 9090 accept
    }
    
    chain output {
        # Allow outbound connections to validators
        tcp dport 9100 accept
        tcp dport 9110 accept
    }
}
```

### 3. Apply NFTables Rules
```bash
# Test the configuration
sudo nft -f /etc/nftables.conf

# If test is successful, apply the rules
sudo nft -f /etc/nftables.conf

# Verify rules
sudo nft list ruleset
```

### 4. Firewall Rules Verification
```bash
# Test Prometheus web interface
curl http://localhost:9090/-/healthy

# Test validator connections
nc -zv 38.97.62.158 9100
nc -zv 38.97.62.158 9110

# Test Bitcoin node connection
nc -zv localhost 9332
```

## Docker Setup

### 1. Start Prometheus Container
```bash
# Navigate to the monitoring directory
cd /home/chris/solana-monitoring

# Start the container
docker-compose up -d prometheus

# Verify the container is running
docker ps | grep prometheus
```

### 2. Initial Verification
```bash
# Check if Prometheus is healthy
curl http://localhost:9090/-/healthy

# Check target status
curl http://localhost:9090/api/v1/targets | jq .
```

## Monitoring Configuration

### 1. Monitored Services
1. **Solana Validator**
   - Target: 38.97.62.158:9100
   - Metrics: Node exporter metrics
   - Scrape Interval: 15s
   - Purpose: System metrics from validator server

2. **Node Validator**
   - Target: 38.97.62.158:9110
   - Metrics: Custom validator metrics
   - Scrape Interval: 15s
   - Purpose: Solana-specific validator metrics

3. **Bitcoin Node**
   - Target: localhost:9332
   - Metrics: Bitcoin Core metrics
   - Scrape Interval: 15s
   - Purpose: Bitcoin node performance metrics

### 2. Security Configuration
- External access restricted to Grafana only
- Internal access via localhost:9090
- No authentication (handled by reverse proxy)

## Data Management

### 1. Retention Policy
- Default retention period: 15 days
- Storage location: Docker volume `prometheus_data`
- Estimated storage requirements: ~10GB per month

### 2. Backup Procedures
```bash
# Backup configuration
cp /home/chris/solana-monitoring/prometheus/prometheus.yml /home/chris/solana-monitoring/prometheus/prometheus.yml.backup

# Backup data volume
docker run --rm -v prometheus_data:/source -v $(pwd):/backup alpine tar czf /backup/prometheus_data_$(date +%Y%m%d).tar.gz -C /source .
```

## Maintenance & Management

### 1. Updates
```bash
# Update Prometheus container
cd /home/chris/solana-monitoring
docker-compose pull prometheus
docker-compose up -d prometheus
```

### 2. Monitoring
```bash
# Check container status
docker ps | grep prometheus

# View logs
docker logs solana-monitoring-prometheus-1

# Check resource usage
docker stats solana-monitoring-prometheus-1
```

### 3. Health Checks
```bash
# Service health
docker ps | grep prometheus
docker inspect solana-monitoring-prometheus-1 | grep Health

# Target health
curl http://localhost:9090/api/v1/targets | jq .

# Configuration check
docker exec solana-monitoring-prometheus-1 promtool check config /etc/prometheus/prometheus.yml
```

## Troubleshooting

### 1. Common Issues

#### High Memory Usage
```bash
# Check container stats
docker stats solana-monitoring-prometheus-1

# Review retention settings
docker exec solana-monitoring-prometheus-1 promtool tsdb list
```

#### Scrape Failures
```bash
# Check target accessibility
nc -zv 38.97.62.158 9100
nc -zv 38.97.62.158 9110
nc -zv localhost 9332

# Check target status
curl http://localhost:9090/api/v1/targets | jq .
```

#### Storage Issues
```bash
# Check volume usage
docker system df -v | grep prometheus_data

# List time series
docker exec solana-monitoring-prometheus-1 promtool tsdb list
```

### 2. Log Analysis
```bash
# View recent logs
docker logs --tail 100 solana-monitoring-prometheus-1

# Search for errors
docker logs solana-monitoring-prometheus-1 | grep -i error

# Check configuration
docker exec solana-monitoring-prometheus-1 cat /etc/prometheus/prometheus.yml
```

### 3. Reset Procedures
```bash
# Stop container
docker-compose stop prometheus

# Remove volume (WARNING: This will delete all data)
docker volume rm prometheus_data

# Restore from backup
tar -xzf prometheus_data_backup.tar.gz -C /var/lib/docker/volumes/prometheus_data/_data/

# Restart container
docker-compose up -d prometheus
```
