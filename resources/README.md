# Project Resources & References

## Table of Contents
- [Monitoring Stack](#monitoring-stack)
- [Blockchain Infrastructure](#blockchain-infrastructure)
- [System Administration](#system-administration)
- [Security](#security)
- [Community Resources](#community-resources)

## Monitoring Stack

### Core Components
| Tool | Description | Documentation | Source |
|------|-------------|---------------|--------|
| Prometheus | Time series database and monitoring system | [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/) | [prometheus/GitHub](https://github.com/prometheus/prometheus) |
| Grafana | Data visualization and alerting | [Grafana Documentation](https://grafana.com/docs/) | [grafana/GitHub](https://github.com/grafana/grafana) |
| Node Exporter | System metrics collector | [Node Exporter Documentation](https://prometheus.io/docs/guides/node-exporter/) | [prometheus/node_exporter](https://github.com/prometheus/node_exporter) |

### Blockchain-Specific Exporters
| Tool | Purpose | Link |
|------|---------|------|
| Solana Exporter | Solana metrics collector | [Solana Exporter Documentation](https://github.com/asymmetric-research/solana-exporter) |
| Bitcoin Exporter | Bitcoin metrics collector | [jvstein/bitcoin-prometheus-exporter](https://github.com/jvstein/bitcoin-prometheus-exporter) |
| Ethereum Exporter | Ethereum metrics collector | [31z4/ethereum-prometheus-exporter](https://github.com/31z4/ethereum-prometheus-exporter) |

## Blockchain Infrastructure

### Solana Resources
| Resource | Description | Link |
|----------|-------------|------|
| Agave Requirements | Agave validator requirements | [docs.anza.xyz](https://docs.anza.xyz/operations/requirements) |
| Hardware Compatibility | Solana Hardware Compatibility List | [solanahcl.org](https://solanahcl.org/) |
| RPC API Documentation | Solana RPC HTTP API reference | [solana.com/docs/rpc/http](https://solana.com/docs/rpc/http) |
| Validator Performance | Track validator statistics and performance | [validators.app](https://www.validators.app/) |
| Testnet Faucet | SOL faucet (requires KYC) | [testnetfaucet.org](https://www.testnetfaucet.org/) |

### Solana Tutorials & Guides
| Guide | Description | Link |
|-------|-------------|------|
| Building from Source | Build Solana from source code | [Building from Source](https://github.com/agjell/sol-tutorials/blob/master/building-solana-from-source.md) |
| Agave Guide | Agave validator setup guide | [Agave Guide](https://github.com/agjell/sol-tutorials/blob/master/agave-beginners-guide.md) |

### Example Dashboards
| Dashboard | Description | Link |
|-----------|-------------|------|
| Nordstar Dashboard | Reference Grafana dashboard setup | [Nordstar Dashboard](https://nordstar.one/) |

## System Administration

### Linux Configuration
| Resource | Description | Link |
|----------|-------------|------|
| Performance Tuning | Linux performance tuning | [Red Hat Tuning Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/monitoring_and_managing_system_status_and_performance/getting-started-with-tuned_monitoring-and-managing-system-status-and-performance#ch-Tuned-overview) |

### Infrastructure Tools
| Tool | Description | Link |
|------|-------------|------|
| nginx | Web server & reverse proxy | [nginx.org/en/docs/](https://nginx.org/en/docs/) |
| Certbot | SSL certificate management | [certbot.eff.org/docs](https://certbot.eff.org/docs) |

### Hosting & Domain Services
| Service | Description | Link |
|---------|-------------|------|
| OVH | Domain registration and management | [ovh.com](https://www.ovh.com/) |
| Fiberstate | Bare metal server hosting | [fiberstate.com](https://www.fiberstate.com/) |

## Security

### Security Tools
| Tool | Description | Source |
|------|-------------|--------|
| SSH Audit | SSH configuration analyzer | [jtesta/ssh-audit](https://github.com/jtesta/ssh-audit) |
| Lynis | Security auditing tool | [CISOfy/lynis](https://github.com/CISOfy/lynis) |
| RKHunter | Rootkit detection | [rkhunter docs](https://rkhunter.sourceforge.net/) |
| Mozilla SSL Config | SSL configuration generator | [ssl-config.mozilla.org](https://ssl-config.mozilla.org/) |

### Security Guides
| Resource | Description | Link |
|----------|-------------|------|
| Linux Server Security | Comprehensive guide | [Security Guide](https://github.com/imthenachoman/How-To-Secure-A-Linux-Server) |
| SSH Hardening | OpenSSH security guide | [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh) |

## Community Resources

### Forums & Communities
| Platform | Purpose | Link |
|----------|----------|------|
| Solana Tech Discord | Validator support & updates | [discord.gg/solana](https://discord.gg/solana) |
| Ethereum R&D Discord | ETH2 staking discussion | [discord.gg/ethereum](https://discord.gg/ethereum) |
| Bitcoin Core GitHub | Development & issues | [github.com/bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) |
| Nordstar Guide | Solana validator guide | [nordstar.one](https://nordstar.one/) |

### Monitoring Dashboards
| Dashboard | Purpose | Link |
|-----------|----------|------|
| Solana Beach | Network statistics | [solanabeach.io](https://solanabeach.io/) |
| Validators App | Validator performance | [validators.app](https://www.validators.app/) |
| EtherScan | Ethereum network explorer | [etherscan.io](https://etherscan.io/) |
| Mempool Space | Bitcoin mempool visualization | [mempool.space](https://mempool.space/) |

## 📊 Metrics Reference
- [Solana Validator Metrics](https://docs.solana.com/developing/network/validating/validator-monitoring#metrics)
- [Prometheus Metrics Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/best-practices/)

