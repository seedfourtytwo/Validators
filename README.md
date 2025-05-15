# 🌐 Validators

Infrastructure and configuration for running blockchain validators.
This project serves as my first learning platform for blockchain infrastructure.

## Infrastructure Overview
![Validator Infrastructure Overview](infra-overview.png)

## Table of Contents
- [Project Structure](#project-structure)
- [Validator Projects](#validator-projects)
  - [Solana Validator](#solana-validator)
  - [Ethereum Validator (Upcoming)](#ethereum-validator)
  - [Bitcoin Node](#bitcoin-node)
- [Infrastructure](#infrastructure)
- [Monitoring Stack](#monitoring-stack)
- [Skills & Technologies used](#skills--technologies)
- [Resources & References](#resources--references)

## Project Structure
```
.
├── infrastructure/
│   ├── solana-validator/    # Solana validator documentation and configs
│   │   ├── services/        # Service configurations and documentation
│   │   │   ├── monitoring/  # Monitoring service configurations
│   │   │   └── validator/   # Validator service configurations
│   │   └── README.md        # Solana validator documentation
│   ├── ethereum/           # Ethereum & EigenLayer validator documentation
│   ├── bitcoin-node/      # Bitcoin node documentation
│   ├── home-server/       # Home server setup and services
│   │   ├── services/      # Home server services
│   │   │   └── monitoring/ # Monitoring service configurations
│   │   │       └── solana-exporter-public/ # Solana exporter using public RPC
│   │   └── setup-tutorials/ # Setup guides for home server services
│   └── home-router/       # Network and routing configuration
├── resources/            # Documentation, guides, and references
├── infra-overview.png    # Infrastructure overview diagram
└── todo.md              # List of things to improve
```

## 🔄 Current Validators

### Solana Validator
- **Status**: Active on Testnet
- **Validator**: [JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF](https://www.validators.app/validators/JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF?locale=en&network=testnet)
- **Documentation**: [Solana Validator Setup](infrastructure/solana-validator/README.md)
- **Metrics Dashboard**: [Validator Metrics](https://metric.seed42.co/public-dashboards/94ca941675e947cb877619494cf95d80)
- **Features**: 
  - JITO MEV Integration for enhanced block building
  - Custom monitoring with Prometheus & Grafana
  - Automated alerts for validator health
  - Performance optimization for MEV rewards
  - Distributed monitoring architecture (validator + home server)
- **Next Steps**: 
  - Optimize MEV performance
  - Enhance monitoring coverage
  - Implement additional alerting rules

### Ethereum Validator
- **Status**: Planning Phase
- **Documentation**: [Ethereum & EigenLayer Setup](infrastructure/ethereum/README.md)
- **Focus**: 
  - EigenLayer Integration for AVS Support

### Bitcoin Node
- **Status**: Active (Basic setup)
- **Documentation**: [Bitcoin Node Setup](infrastructure/bitcoin-node/README.md)
- **Metrics Dashboard**: [Node Metrics](https://metric.seed42.co/public-dashboards/4de1b04bbfd5466cbc7387071ae30786?from=now-15m&to=now&refresh=15s)
- **Features**:
  - Full node operation
  - Network monitoring
  - Transaction fee metrics collection
- **Planned Improvements**:
  - Enhanced fee estimation using blended approach (mempool + historical data)
  - Improved fee prediction accuracy for various confirmation targets

## Infrastructure

### Components
- **Validator Server** (Fiberstate Data Center)
  - Primary Solana validator
  - High-performance hardware
  - Light-mode monitoring tools

- **Home Server**
  - Metrics collection & visualization
  - Bitcoin node
  - Ethereum services (planned)
  - Prometheus & Grafana
  - Solana public metrics collector (via public RPC)

- **Cold Storage**: Secure key generation and storage solution

- **Cold Storage**
  - Secure key generation
  - Hardware wallet integration
  - Backup solution
  - Multi-location storage

## Monitoring Stack

### Metrics Collection
- **Prometheus**
  - High-performance time-series database
  - Custom scrape configurations
  - Long-term metric storage
  - Efficient querying capabilities

### Visualization
- **Grafana**
  - Real-time dashboards
  - Custom visualization panels
  - Historical data analysis
  - Public dashboard sharing
  - Multi-validator comparison

### Exporters
- **Node Exporter**
  - System metrics
  - Hardware monitoring
  - Resource utilization
  - Performance tracking

- **Solana Exporter (Distributed)**
  - **Validator Side (Light Mode)**
    - Validator-specific metrics
    - Reduced resource footprint
    - Local RPC access
  - **Home Server Side (Comprehensive Mode)**
    - Network-wide metrics
    - Public RPC access
    - Complete validator context

- **Bitcoin Exporter** (self made)
  - Node health
  - Network status
  - Transaction metrics
  - Memory pool stats

## Skills & Technologies used

### System Administration
- **Linux**
  - System optimization
  - Service management
  - Security hardening
  - Performance tuning

- **Networking**
  - Routing configuration
  - Firewall management
  - Port security
  - VPN setup

### Blockchain Technologies
- **Solana**: Validator operations, key management, monitoring, MEV optimization with JITO
- **Ethereum**: Coming soon - Validator operations with EigenLayer integration
- **Bitcoin**: Node operations and monitoring

### Monitoring & Metrics
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and public dashboards
- **Alerting**: Custom alert configurations for validator health

### Tools & Services
- **nginx**: Reverse proxy and SSL certificate management
- **Termius**: Local CLI for remote server access
- **Git/Github**: Documentation and configuration management
- **AI Assistance**: Cursor and vairous AI tools for development and documentation support

## Resources & References
For a comprehensive list of resources, tools, and references used in this project, please see [Resources Documentation](resources/README.md).

## Contact
contact@seed42.co

