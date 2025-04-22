# Grafana Monitoring Setup

## Overview
This document describes the Grafana monitoring setup running in Docker, integrated with Prometheus for data collection and visualization.

## Current Status
| Component | Status | Notes |
|-----------|---------|-------|
| Grafana | Running | Container: solana-monitoring-grafana-1 |
| Prometheus | Running | Container: solana-monitoring-prometheus-1 |
| Data Sources | Active | Prometheus, Node Exporter |

## Directory Structure
```
/home/chris/solana-monitoring/
├── docker-compose.yml
├── grafana-config/
│   ├── grafana.ini
│   └── dashboards/
│       ├── system-metrics.json
│       ├── validator-performance.json
│       └── network-health.json
└── prometheus/
    └── prometheus.yml
```

## Docker Configuration

### Container Details
| Setting | Value | Notes |
|---------|-------|-------|
| Container Name | solana-monitoring-grafana-1 | Unique identifier |
| Image | grafana/grafana | Latest stable version |
| Network Mode | host | Direct host network access |
| Restart Policy | unless-stopped | Automatic restart |
| Data Volume | grafana-storage | Persistent storage |
| Config Volume | ./grafana-config | Custom configuration |

### Docker Compose Configuration
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

## Grafana Configuration

### Server Settings
File: `/home/chris/solana-monitoring/grafana-config/grafana.ini`
```ini
[server]
root_url = https://metric.seed42.co/
serve_from_sub_path = false

[auth.anonymous]
enabled = false
```

### Security Settings
- Anonymous access disabled
- HTTPS enabled
- Authentication required for all access
- Session timeout: 24 hours (default)

### Data Sources
1. **Prometheus**
   - URL: http://localhost:9090
   - Access: Server (default)
   - Scrape interval: 15s

2. **Node Exporter**
   - URL: http://localhost:9100
   - Access: Server (default)
   - Scrape interval: 15s

## Dashboards and Alerts
Dashboard configurations and alert rules are stored in JSON format. See the dashboard JSON files in the `grafana-config/dashboards/` directory for detailed configurations.


### Alert Rules
Alert configurations will be added to the dashboard JSON files as they are developed.

## Monitoring Configuration

### Updates
```bash
# Update Grafana container
docker-compose pull
docker-compose up -d

# Verify configuration
docker exec solana-monitoring-grafana-1 grafana-cli admin reset-admin-password
```

### Monitoring
```bash
# Check container status
docker ps | grep grafana

# View logs
docker logs solana-monitoring-grafana-1

# Check resource usage
docker stats solana-monitoring-grafana-1
```

## Troubleshooting

### Log Analysis
```bash
# View recent logs
docker logs --tail 100 solana-monitoring-grafana-1

# Search for errors
docker logs solana-monitoring-grafana-1 | grep -i error

# Check configuration
docker exec solana-monitoring-grafana-1 cat /etc/grafana/grafana.ini
```
