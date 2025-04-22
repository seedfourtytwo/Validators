# Prometheus Monitoring Setup

## Overview
This document describes the Prometheus monitoring setup used to collect and store metrics from various services including Solana validator, Bitcoin node, and system metrics. Prometheus is deployed as a Docker container and integrated with Grafana for visualization.

## Current Status
| Component | Status | Notes |
|-----------|---------|-------|
| Prometheus | Running | Container: solana-monitoring-prometheus-1 |
| Data Retention | Active | Stored in Docker volume |
| Integration | Active | Connected to Grafana |
| Targets | Active | Monitoring 4 services |

## Container Information
- **Container Name**: solana-monitoring-prometheus-1
- **Image**: prom/prometheus:v2.45.0
- **Network**: solana-monitoring_default (172.18.0.3)
- **Restart Policy**: unless-stopped

## Configuration

### Ports
- **Internal**: 9090
- **External Access**:
  - Local: http://192.168.1.210:9090
  - Note: External access is restricted to Grafana only for security

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

## Monitoring Configuration

### Prometheus Configuration
File: `/home/chris/solana-monitoring/prometheus/prometheus.yml`
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  # Runs on the solana validator and collects metrics that cannot be obtained from public RPCs
  - job_name: 'solana-validator-light'
    static_configs:
      - targets: ['38.97.62.158:9100']
  # Runs on the solana validator and collects all the hardware and system metrics
  - job_name: 'node-validator'
    static_configs:
      - targets: ['38.97.62.158:9110']
    scrape_interval: 15s
  # Runs on the Home server and collects Bitcoin specific metrics
  - job_name: 'bitcoin-node'
    static_configs:
      - targets: ['localhost:9332']
    scrape_interval: 15s
  # Runs on the Home server and collects Solana metrics available from public RPCs
  - job_name: 'solana-public-metrics'
    static_configs:
      - targets: ['localhost:9101']
    scrape_interval: 15s
```

### Monitored Services
1. **Solana Validator Light**
   - Target: 38.97.62.158:9100
   - Metrics: Validator-specific metrics that can only be obtained locally
   - Scrape Interval: 15s
   - Purpose: Validator-specific metrics from validator server

2. **Node Validator** (Solana Validator hardware metrics)
   - Target: 38.97.62.158:9110
   - Metrics: System and hardware metrics
   - Scrape Interval: 15s
   - Purpose: System-level metrics from validator server

3. **Bitcoin Node**
   - Target: localhost:9332
   - Metrics: Bitcoin Core metrics
   - Scrape Interval: 15s
   - Purpose: Bitcoin node performance metrics

4. **Solana Public Metrics**
   - Target: localhost:9101
   - Metrics: Comprehensive Solana metrics via public RPC
   - Scrape Interval: 15s
   - Purpose: Network-wide metrics and validator comparison

## Data Management

### Retention Policy
- Default retention period: 15 days
- Storage location: Docker volume `solana-monitoring_prometheus_data`
- Estimated storage requirements: ~10GB per month

### Backup Procedures
1. **Configuration Backup**
   ```bash
   # Backup configuration file
   cp /home/chris/solana-monitoring/prometheus/prometheus.yml /home/chris/solana-monitoring/prometheus/prometheus.yml.backup
   ```

2. **Data Backup**
   ```bash
   # Create a backup of the Prometheus data volume
   docker run --rm -v solana-monitoring_prometheus_data:/source -v /backup/prometheus:/backup alpine tar czf /backup/prometheus_data_$(date +%Y%m%d).tar.gz -C /source .
   ```

## Maintenance Procedures

### Verification Procedures
1. **Basic Health Check**
   ```bash
   # Check if Prometheus is healthy and responding
   curl http://localhost:9090/-/healthy
   ```
   Expected output: `Prometheus is Healthy.`

2. **Target Status Verification**
   ```bash
   # Check status of all configured targets
   curl http://localhost:9090/api/v1/targets | jq .
   ```
   This will show:
   - Current state of each target (up/down)
   - Last scrape time
   - Any errors encountered
   - Labels and metadata

3. **Data Storage Verification**
   ```bash
   # List all time series databases
   docker exec solana-monitoring-prometheus-1 promtool tsdb list
   ```
   Shows:
   - Available time series
   - Data retention status
   - Storage blocks

4. **Log Analysis**
   ```bash
   # Check Prometheus logs for errors or warnings
   docker logs solana-monitoring-prometheus-1
   ```
   Look for:
   - Scrape failures
   - Configuration errors
   - Storage issues
   - Target connection problems

5. **Network Connectivity Check**
   ```bash
   # Check Solana validator connectivity
   nc -zv 38.97.62.158 9100
   nc -zv 38.97.62.158 9110

   # Check Bitcoin node connectivity
   nc -zv localhost 9332
   
   # Check Solana exporter public connectivity
   nc -zv localhost 9101
   ```
   These commands verify:
   - Port accessibility
   - Network connectivity
   - Firewall rules
   - Service availability

### Common Commands
```bash
# Restart Prometheus
docker restart solana-monitoring-prometheus-1

# View logs
docker logs solana-monitoring-prometheus-1

# Check configuration
docker exec solana-monitoring-prometheus-1 promtool check config /etc/prometheus/prometheus.yml

# Check targets
curl http://localhost:9090/api/v1/targets

# Check self-monitoring
curl http://localhost:9090/-/healthy
```

### Health Checks
1. **Service Health**
   ```bash
   # Check if Prometheus is running
   docker ps | grep prometheus
   
   # Check container health
   docker inspect solana-monitoring-prometheus-1 | grep Health
   ```

2. **Target Health**
   ```bash
   # Check target status
   curl http://localhost:9090/api/v1/targets | jq .
   ```

### Troubleshooting
1. **High Memory Usage**
   - Check container stats: `docker stats solana-monitoring-prometheus-1`
   - Review retention settings
   - Consider increasing container memory limits

2. **Scrape Failures**
   - Check target accessibility
   - Verify network connectivity
   - Review target configuration

3. **Storage Issues**
   - Monitor volume usage
   - Check for disk space
   - Review retention policies

## Related Documentation
- [Solana Exporter Public](../solana-exporter-public/solana-exporter-public.md) - Documentation for the Solana exporter using public RPC
- [Solana Exporter Setup Guide](../../../setup-tutorials/solana-exporter.md) - Setup instructions for the Solana exporter
- [Prometheus Setup Guide](../../../setup-tutorials/prometheus.md) - Setup instructions for Prometheus