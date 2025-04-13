# Prometheus Monitoring Setup

## Container Information
- **Container Name**: solana-monitoring-prometheus-1
- **Image**: prom/prometheus:v2.45.0
- **Network**: solana-monitoring_default (172.18.0.3)

## Configuration
### Ports
- **Internal**: 9090
- **External Access**:
  - Local: http://192.168.1.210:9090
  - External: http://77.200.151.32:9090

### Volumes
- **Configuration**:
  - Host: `/home/chris/solana-monitoring/prometheus/prometheus.yml`
  - Container: `/etc/prometheus/prometheus.yml`
- **Data Storage**:
  - Named Volume: `solana-monitoring_prometheus_data`
  - Mount Point: `/prometheus`

### Entrypoint
```bash
/bin/prometheus --config.file=/etc/prometheus/prometheus.yml
```

## Monitoring Targets
### Current Configuration
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

### Monitored Services
1. **Solana Validator**
   - Target: 38.97.62.158:9100
   - Metrics: Node exporter metrics
   - Scrape Interval: 15s

2. **Node Validator** (Solana Validator hardware metrics)
   - Target: 38.97.62.158:9110
   - Metrics: Custom validator metrics
   - Scrape Interval: 15s

3. **Bitcoin Node**
   - Target: localhost:9332
   - Metrics: Bitcoin Core metrics
   - Scrape Interval: 15s

## Maintenance
### Common Commands
```bash
# Restart Prometheus
docker restart solana-monitoring-prometheus-1

# View logs
docker logs solana-monitoring-prometheus-1

# Check configuration
docker exec solana-monitoring-prometheus-1 promtool check config /etc/prometheus/prometheus.yml
```

### Backup
- Configuration file is stored at: `/home/chris/solana-monitoring/prometheus/prometheus.yml`
- Metrics data is stored in Docker volume: `solana-monitoring_prometheus_data`