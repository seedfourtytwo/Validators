# Grafana Setup Tutorial

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Image Setup](#docker-image-setup)
3. [Directory Structure Setup](#directory-structure-setup)
4. [Configuration Files](#configuration-files)
5. [Docker Setup](#docker-setup)
6. [Initial Configuration](#initial-configuration)
7. [Data Sources Setup](#data-sources-setup)
8. [Dashboard Import](#dashboard-import)
9. [Security Configuration](#security-configuration)
10. [Maintenance & Management](#maintenance--management)
11. [Troubleshooting](#troubleshooting)

## Prerequisites
- Docker and Docker Compose installed
- Access to port 3000 (default Grafana port)
- Basic understanding of YAML and JSON
- Root or sudo access

## Docker Image Setup

### 1. Pull Grafana Image
```bash
# Pull the official Grafana image
docker pull grafana/grafana:latest

# Verify the image
docker images | grep grafana
```

### 2. Image Details
- **Official Image**: `grafana/grafana`
- **Latest Version**: Available on [Docker Hub](https://hub.docker.com/r/grafana/grafana)
- **Size**: ~150MB
- **Base OS**: Alpine Linux
- **Architecture**: Supports multiple architectures (amd64, arm64, arm/v7)

### 3. Version Control
```bash
# List available tags
docker search grafana/grafana

# Pull specific version (recommended for production)
docker pull grafana/grafana:9.5.2  # Replace with desired version

# Tag the image for your project
docker tag grafana/grafana:latest solana-monitoring-grafana:latest
```

### 4. Image Verification
```bash
# Inspect the image
docker inspect grafana/grafana:latest

# Test run the container
docker run --rm -p 3000:3000 grafana/grafana:latest
```

## Directory Structure Setup
```bash
# Create base directory
mkdir -p /home/chris/solana-monitoring

# Create Grafana configuration directory
mkdir -p /home/chris/solana-monitoring/grafana-config/dashboards

# Set proper permissions
chown -R chris:chris /home/chris/solana-monitoring
chmod -R 755 /home/chris/solana-monitoring
```

## Configuration Files

### 1. Docker Compose Configuration
File: `/home/chris/solana-monitoring/docker-compose.yml`
```yaml
services:
  grafana:
    image: grafana/grafana
    container_name: solana-monitoring-grafana-1
    restart: unless-stopped
    network_mode: host
    environment:
      - GF_SERVER_ROOT_URL=https://metric.seed42.co/
      - GF_SERVER_SERVE_FROM_SUB_PATH=true
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./grafana-config:/etc/grafana

volumes:
  grafana-storage:
```

### 2. Grafana Configuration
File: `/home/chris/solana-monitoring/grafana-config/grafana.ini`
```ini
[server]
root_url = https://metric.seed42.co/
serve_from_sub_path = false

[auth.anonymous]
enabled = false
```

## Docker Setup

### 1. Start Grafana Container
```bash
# Navigate to the monitoring directory
cd /home/chris/solana-monitoring

# Start the container
docker-compose up -d

# Verify the container is running
docker ps | grep grafana
```

### 2. Initial Access
1. Open your browser and navigate to `https://metric.seed42.co`
2. Default login credentials:
   - Username: admin
   - Password: admin
3. You will be prompted to change the password on first login

## Data Sources Setup

### 1. Prometheus Data Source
1. Navigate to Configuration > Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Configure with these settings:
   ```
   Name: Prometheus
   URL: http://localhost:9090
   Access: Server (default)
   Scrape interval: 15s
   ```
5. Click "Save & Test"

### 2. Node Exporter Data Source
1. Navigate to Configuration > Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Configure with these settings:
   ```
   Name: Node Exporter
   URL: http://localhost:9100
   Access: Server (default)
   Scrape interval: 15s
   ```
5. Click "Save & Test"

## Dashboard Import

### 1. System Metrics Dashboard
File: `/home/chris/solana-monitoring/grafana-config/dashboards/system-metrics.json`
```json
{
  "annotations": {
    "list": []
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "links": [],
  "liveNow": false,
  "panels": [],
  "refresh": "15s",
  "schemaVersion": 38,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "UTC",
  "title": "System Metrics",
  "version": 0,
  "weekStart": ""
}
```

### 2. Import Procedure
1. Navigate to Dashboards > Import
2. Click "Upload JSON file"
3. Select the dashboard JSON file
4. Configure the data source mapping
5. Click "Import"

## Security Configuration

### 1. HTTPS Setup
1. Navigate to Configuration > Server
2. Verify these settings:
   ```
   Root URL: https://metric.seed42.co/
   Serve from sub path: false
   ```

### 2. Authentication
1. Navigate to Configuration > Security
2. Verify these settings:
   ```
   Anonymous access: Disabled
   Session timeout: 24h
   ```

## Maintenance & Management

### 1. Updates
```bash
# Update Grafana container
cd /home/chris/solana-monitoring
docker-compose pull
docker-compose up -d

# Verify configuration
docker exec solana-monitoring-grafana-1 grafana-cli admin reset-admin-password
```

### 2. Monitoring
```bash
# Check container status
docker ps | grep grafana

# View logs
docker logs solana-monitoring-grafana-1

# Check resource usage
docker stats solana-monitoring-grafana-1
```

### 3. Backup
```bash
# Backup Grafana configuration
tar -czf grafana-config-backup.tar.gz /home/chris/solana-monitoring/grafana-config

# Backup Grafana data
docker run --rm -v grafana-storage:/source -v $(pwd):/backup alpine tar czf /backup/grafana-data-backup.tar.gz -C /source .
```

## Troubleshooting

### 1. Log Analysis
```bash
# View recent logs
docker logs --tail 100 solana-monitoring-grafana-1

# Search for errors
docker logs solana-monitoring-grafana-1 | grep -i error

# Check configuration
docker exec solana-monitoring-grafana-1 cat /etc/grafana/grafana.ini
```

### 2. Common Issues

#### Container Won't Start
```bash
# Check container logs
docker logs solana-monitoring-grafana-1

# Verify port availability
netstat -tulpn | grep 3000

# Check permissions
ls -la /home/chris/solana-monitoring/grafana-config
```

#### Data Source Connection Issues
1. Verify Prometheus is running:
   ```bash
   docker ps | grep prometheus
   ```
2. Check Prometheus logs:
   ```bash
   docker logs solana-monitoring-prometheus-1
   ```
3. Test Prometheus endpoint:
   ```bash
   curl http://localhost:9090/-/healthy
   ```

#### Dashboard Import Failures
1. Verify JSON file format:
   ```bash
   cat /home/chris/solana-monitoring/grafana-config/dashboards/system-metrics.json | jq '.'
   ```
2. Check file permissions:
   ```bash
   ls -la /home/chris/solana-monitoring/grafana-config/dashboards/
   ```

### 3. Reset Procedures

#### Reset Admin Password
```bash
docker exec solana-monitoring-grafana-1 grafana-cli admin reset-admin-password
```

#### Reset Configuration
```bash
# Stop container
docker-compose down

# Remove volumes
docker volume rm solana-monitoring_grafana-storage

# Restore from backup
tar -xzf grafana-config-backup.tar.gz -C /

# Restart container
docker-compose up -d
```
