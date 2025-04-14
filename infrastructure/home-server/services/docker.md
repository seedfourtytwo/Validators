# Docker Configuration

## Overview
This document describes the Docker configuration and setup for the home server. The system uses Docker Engine Community version 28.0.4 for container management.

## System Information
- **Docker Version**: 28.0.4
- **API Version**: 1.48
- **Storage Driver**: overlay2
- **Logging Driver**: json-file
- **Cgroup Driver**: systemd
- **Cgroup Version**: 2
- **Operating System**: Ubuntu 24.04.2 LTS
- **Architecture**: x86_64
- **CPUs**: 20
- **Total Memory**: 62.57GiB

## Configuration Files

### Docker Compose Configuration
Location: `/home/chris/solana-monitoring/docker-compose.yml`
```yaml
version: "3.8"

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

  prometheus:
    image: prom/prometheus
    container_name: solana-monitoring-prometheus-1
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

volumes:
  grafana-storage:
  prometheus-storage:
```

### Service Configurations
Service-specific configurations are documented in their respective files:
- Grafana configuration: See `grafana.md`
- Prometheus configuration: See `prometheus.md`

## Container Configuration

### Running Containers

#### 1. Solana Monitoring Grafana
- **Container ID**: 5342c5b6a313
- **Image**: grafana/grafana
- **Status**: Running
- **Network Mode**: host
- **Configuration**:
  - Root URL: https://metric.seed42.co/
  - Config Path: /etc/grafana
  - Data Path: /var/lib/grafana
  - Logs Path: /var/log/grafana
  - Plugins Path: /var/lib/grafana/plugins
  - Provisioning Path: /etc/grafana/provisioning
- **Volumes**:
  - Config: /home/chris/solana-monitoring/grafana-config:/etc/grafana
  - Storage: solana-monitoring_grafana-storage:/var/lib/grafana
- **Restart Policy**: unless-stopped

#### 2. Solana Monitoring Prometheus
- **Container ID**: 69191b5197c0
- **Image**: prom/prometheus
- **Status**: Running
- **Network Mode**: host
- **Configuration**:
  - Config File: /etc/prometheus/prometheus.yml
  - Working Directory: /prometheus
- **Volumes**:
  - Config: /home/chris/solana-monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
  - Data: Local volume for Prometheus data
- **Restart Policy**: unless-stopped

## Network Configuration
- **Network Drivers Available**:
  - bridge
  - host
  - ipvlan
  - macvlan
  - null
  - overlay
- **Current Setup**: Using host network mode for monitoring stack

## Storage Configuration
- **Storage Driver**: overlay2
- **Backing Filesystem**: extfs
- **Volume Management**: Local volumes for persistent data
- **Named Volumes**:
  - grafana-storage: Grafana data persistence
  - prometheus-storage: Prometheus data persistence

## Security Configuration
- **Security Options**:
  - apparmor
  - seccomp (Profile: builtin)
  - cgroupns
- **Container Isolation**: Default Docker isolation
- **Resource Limits**: No specific limits set

## Maintenance Procedures

### Container Management
```bash
# Start containers
docker-compose -f /home/chris/solana-monitoring/docker-compose.yml up -d

# Stop containers
docker-compose -f /home/chris/solana-monitoring/docker-compose.yml down

# View logs
docker logs solana-monitoring-grafana-1
docker logs solana-monitoring-prometheus-1

# Restart containers
docker restart solana-monitoring-grafana-1
docker restart solana-monitoring-prometheus-1
```

### Backup Procedures
```bash
# Backup Grafana configuration
cp -r /home/chris/solana-monitoring/grafana-config /backup/grafana-config-$(date +%Y%m%d)

# Backup Prometheus configuration
cp /home/chris/solana-monitoring/prometheus/prometheus.yml /backup/prometheus-$(date +%Y%m%d).yml

# Backup Docker volumes
docker run --rm -v solana-monitoring_grafana-storage:/source -v /backup:/backup alpine tar czf /backup/grafana-data-$(date +%Y%m%d).tar.gz -C /source .
```

### Monitoring
```bash
# Check container status
docker ps -a

# View container resources
docker stats

# Inspect container configuration
docker inspect solana-monitoring-grafana-1
docker inspect solana-monitoring-prometheus-1
```

### Cleanup Procedures
```bash
# Remove stopped containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove unused images
docker image prune

# Clean up everything (containers, networks, images, and volumes)
docker system prune -a --volumes
```