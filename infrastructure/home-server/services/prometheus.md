Prometheus
Running in Docker:

### Prometheus

Container: solana-monitoring-prometheus-1

Image: prom/prometheus:v2.45.0

Ports: 9090

Volumes:

  - /home/chris/solana-monitoring/prometheus/prometheus.yml → /etc/prometheus/prometheus.yml

Named Volume: solana-monitoring_prometheus_data → /prometheus

Network: solana-monitoring_default / 172.18.0.3

Entrypoint: /bin/prometheus --config.file=/etc/prometheus/prometheus.yml

Access:

  - Local: http://192.168.1.210:9090

  - External: http://77.200.151.32:9090

Settings:

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