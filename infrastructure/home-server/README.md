# Home Server Documentation

## 🖥️ System Overview
This server serves as the primary infrastructure for running the Monitoring stack monitoring, a Bitcoin nodes, and Ethereum - Eigenlayer validation services.

## 🧱 Hardware Specifications

| Component       | Details                                   |
|----------------|--------------------------------------------|
| **IP Address**  | 192.168.1.210                             |
| **OS**          | Ubuntu 24.04                              |
| **CPU**         | 13th Gen Intel(R) Core(TM) i5-13500       |
| **RAM**         | 64 GB DDR4                                |
| **Storage**     | 2 x 12TB SATA - 2 x 1TB NVMe               |
| **Network**     | [See Home Router Configuration](../home-router/README.md) |

## 🚀 Services

### Currently Running
- Monitoring Stack
  - [Grafana](./services/monitoring/grafana/README.md)
  - [Prometheus](./services/monitoring/prometheus/prometheus.md)
  - [Docker Infrastructure](./services/docker.md)
  - [Solana Exporter Public](./services/monitoring/solana-exporter-public/solana-exporter-public.md)
  - [Delegator Tracker](./services/monitoring/delegator-tracker/README.md) - Near real-time tracking of validator delegations
- Bitcoin Infrastructure
  - [Bitcoin Node](../bitcoin-node/README.md)
  - [Bitcoin Node Collector](../bitcoin-node/metrics-collector/README.md)
- Ethereum Infrastructure
  - [Ethereum-Eigen Validator](./services/ethereum-eigen/ethereum-eigen.md)

## 📁 Directory Structure
- `/setup-tutorials/` - Installation and setup guides
  - [Solana Exporter Setup](./setup-tutorials/solana-exporter.md)
  - [Prometheus Setup](./setup-tutorials/prometheus.md)
  - [Grafana Setup](./setup-tutorials/grafana.md)
  - [Docker Setup](./setup-tutorials/docker.md)
- `/services/` - Service configurations and documentation
  - `/monitoring/` - Monitoring service configurations
    - `/solana-exporter-public/` - Solana exporter (public RPC) documentation
    - `/delegator-tracker/` - Validator delegation monitoring service (1h updates)
- `/linux-config/` - System-level configurations
- `/monitoring/` - Monitoring stack configurations

## 🔄 Service Dependencies
The following services require specific dependencies:

### Delegator Tracker
- Python 3.x with `requests` library
- Grafana with Infinity plugin
- Systemd for service management
- Port 8080 for HTTP server


