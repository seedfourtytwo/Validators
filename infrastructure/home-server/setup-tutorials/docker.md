# Docker Setup Tutorial

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Initial Configuration](#initial-configuration)
- [Setting Up Monitoring Stack](#setting-up-monitoring-stack)
- [Maintenance & Management](#maintenance--management)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## Prerequisites

### Required Packages
```bash
# Update package lists
sudo apt update

# Install prerequisites
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common
```

## Installation

### 1. Add Docker's Official GPG Key
```bash
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### 2. Set Up Docker Repository
```bash
# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 3. Install Docker Engine
```bash
# Update package lists again
sudo apt update

# Install Docker Engine
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 4. Verify Installation
```bash
# Check Docker version
docker --version

# Verify Docker is running
sudo systemctl status docker

# Run test container
sudo docker run hello-world
```

### 5. Configure Docker to Start on Boot
```bash
# Enable Docker service
sudo systemctl enable docker

# Start Docker service
sudo systemctl start docker
```

### 6. Add Current User to Docker Group
```bash
# Add current user to docker group
sudo usermod -aG docker $USER

# Apply group changes (requires logout/login)
newgrp docker
```

## Initial Configuration

### 1. Create Docker Configuration Directory
```bash
# Create directory for Docker configurations
mkdir -p /home/chris/solana-monitoring
cd /home/chris/solana-monitoring
```

### 2. Create Docker Compose File
```bash
# Create docker-compose.yml
nano /home/chris/solana-monitoring/docker-compose.yml
```

<details>
<summary>Full docker-compose.yml content</summary>

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
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G

  prometheus:
    image: prom/prometheus
    container_name: solana-monitoring-prometheus-1
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

volumes:
  grafana-storage:
  prometheus-storage:
```
</details>

### 3. Create Required Directories
```bash
# Create directories for configurations
mkdir -p /home/chris/solana-monitoring/grafana-config
mkdir -p /home/chris/solana-monitoring/prometheus
```

## Setting Up Monitoring Stack

### 1. Configure Grafana
```bash
# Create Grafana configuration
nano /home/chris/solana-monitoring/grafana-config/grafana.ini
```

<details>
<summary>Full grafana.ini content</summary>

```ini
[server]
root_url = https://metric.seed42.co/
serve_from_sub_path = true
protocol = http
http_port = 3000
domain = metric.seed42.co
enforce_domain = true
socket = /var/run/grafana/grafana.sock

[security]
admin_user = admin
admin_password = your_secure_password
secret_key = your_secret_key_here
disable_gravatar = true
cookie_secure = true
cookie_samesite = strict
allow_embedding = false

[auth.anonymous]
enabled = false

[auth.basic]
enabled = true

[users]
allow_sign_up = false
auto_assign_org = true
auto_assign_org_role = Viewer

[dashboards]
min_refresh_interval = 5s

[paths]
data = /var/lib/grafana
logs = /var/log/grafana
plugins = /var/lib/grafana/plugins
provisioning = /etc/grafana/provisioning

[log]
mode = file
level = info
```
</details>

### 2. Configure Prometheus
```bash
# Create Prometheus configuration
nano /home/chris/solana-monitoring/prometheus/prometheus.yml
```

<details>
<summary>Full prometheus.yml content</summary>

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  scrape_timeout: 10s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'bitcoin-node'
    static_configs:
      - targets: ['localhost:9332']
    scrape_interval: 30s
    scrape_timeout: 10s

  - job_name: 'solana-validator'
    static_configs:
      - targets: ['localhost:9100']
    scrape_interval: 15s
    scrape_timeout: 10s
```
</details>

### 3. Start the Monitoring Stack
```bash
# Navigate to the configuration directory
cd /home/chris/solana-monitoring

# Start containers
docker compose up -d

# Verify containers are running
docker ps

# Check logs
docker logs solana-monitoring-grafana-1
docker logs solana-monitoring-prometheus-1
```

## Maintenance & Management

### Container Management
```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Stop containers
cd /home/chris/solana-monitoring
docker compose down

# Start containers
cd /home/chris/solana-monitoring
docker compose up -d

# Restart containers
cd /home/chris/solana-monitoring
docker compose restart

# View container logs
docker logs -f solana-monitoring-grafana-1
docker logs -f solana-monitoring-prometheus-1
```

### Backup Procedures
```bash
# Create backup directory
mkdir -p /home/chris/docker-backups

# Backup Grafana configuration
cp -r /home/chris/solana-monitoring/grafana-config /home/chris/docker-backups/grafana-config-$(date +%Y%m%d)

# Backup Prometheus configuration
cp /home/chris/solana-monitoring/prometheus/prometheus.yml /home/chris/docker-backups/prometheus-$(date +%Y%m%d).yml

# Backup Docker volumes
docker run --rm \
    -v solana-monitoring_grafana-storage:/source \
    -v /home/chris/docker-backups:/backup \
    alpine tar czf /backup/grafana-data-$(date +%Y%m%d).tar.gz -C /source .
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

# Clean up everything (use with caution)
docker system prune -a --volumes
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
```bash
# Check Docker group membership
groups

# Re-add user to Docker group if needed
sudo usermod -aG docker $USER
newgrp docker

# Fix directory permissions if needed
sudo chown -R $USER:$USER /home/chris/solana-monitoring
```

2. **Container Won't Start**
```bash
# Check container logs
docker logs solana-monitoring-grafana-1

# Check Docker daemon logs
sudo journalctl -fu docker

# Verify port availability
sudo netstat -tulpn | grep LISTEN
```

3. **Volume Mount Issues**
```bash
# Check volume permissions
ls -la /home/chris/solana-monitoring/grafana-config
ls -la /home/chris/solana-monitoring/prometheus

# Fix permissions if needed
sudo chown -R $USER:$USER /home/chris/solana-monitoring
```

4. **Network Issues**
```bash
# Check network configuration
docker network ls

# Inspect network
docker network inspect bridge

# Test network connectivity
docker run --rm alpine ping -c 3 google.com
```

## Security Considerations

### Regular Maintenance
```bash
# Update Docker
sudo apt update
sudo apt upgrade docker-ce docker-ce-cli containerd.io

# Update containers
cd /home/chris/solana-monitoring
docker compose pull
docker compose up -d

# Check for security updates
docker scan solana-monitoring-grafana-1
docker scan solana-monitoring-prometheus-1
```

### Resource Limits
The resource limits are already included in the docker-compose.yml file:

<details>
<summary>Resource limits configuration</summary>

```yaml
services:
  grafana:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    # ... rest of grafana config

  prometheus:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    # ... rest of prometheus config
```
</details>

## Notes
- Keep Docker and containers updated regularly
- Monitor system resources
- Regular backups are essential
- Document any custom configurations
- Test backups periodically
- Monitor security advisories
- Keep track of container logs
- Document any changes to configurations