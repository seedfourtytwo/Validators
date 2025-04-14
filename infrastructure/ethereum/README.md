# Ethereum & EigenLayer Validator Setup

## Overview
This repository contains the configuration and setup for running an Ethereum validator node with EigenLayer integration on the Holesky testnet. The setup is designed to support running AVS (Actively Validated Services) through EigenLayer's infrastructure.

## Current Implementation Status

### Completed Components
- ✅ Base directory structure for all components
- ✅ Geth execution client configuration for Holesky testnet
- ✅ Lighthouse consensus client setup
- ✅ Basic monitoring configuration
- ✅ JWT authentication between execution and consensus clients

### In Progress
- 🔄 Service management implementation
- 🔄 Monitoring and alerting setup
- 🔄 EigenLayer validator integration
- 🔄 Eigenda AVS node configuration

## Architecture

### Directory Structure
```
/mnt/ethereum-testnet/
├── geth-holesky/        # Geth execution client data
├── lighthouse-holesky/  # Lighthouse beacon chain data
├── prysm-holesky/      # (Alternative) Prysm beacon chain data
└── jwtsecret           # Shared JWT secret

/mnt/eigenlayer/        # EigenLayer validator data
/mnt/avss/eigenda/     # Eigenda AVS node data
```

### Component Configuration

#### 1. Execution Client (Geth)
- Network: Holesky testnet
- Ports:
  - HTTP RPC: 8545
  - WebSocket: 8546
  - P2P: 30303
  - Auth RPC: 8551
- Sync Mode: Snap
- Data Directory: `/mnt/ethereum-testnet/geth-holesky`

#### 2. Consensus Client (Lighthouse)
- Mode: Beacon Node
- Execution URL: `http://localhost:8551`
- Data Directory: `/mnt/ethereum-testnet/lighthouse-holesky`
- Checkpoint Sync: Multiple providers supported

## Prerequisites
- Sufficient storage space (recommended: 1TB+ SSD)
- Stable internet connection
- Linux-based operating system
- Root/sudo access for service management

## Getting Started

### 1. System Requirements
- CPU: 4+ cores
- RAM: 16GB+ recommended
- Storage: 1TB+ SSD
- Network: 100Mbps+ connection

### 2. Installation Steps
1. Clone this repository
2. Set up directory structure
3. Configure execution client (Geth)
4. Configure consensus client (Lighthouse)
5. Set up EigenLayer validator
6. Configure AVS node (Eigenda)

## Documentation & Resources

### Detailed Configuration
- [Detailed Setup Documentation](./ethereum-eigen.md) - Complete configuration details and current setup status

### Official Documentation
- [Ethereum Documentation](https://ethereum.org/en/developers/docs/)
- [EigenLayer Documentation](https://docs.eigenlayer.xyz/)
- [Lighthouse Documentation](https://lighthouse-book.sigmaprime.io/)
- [Geth Documentation](https://geth.ethereum.org/docs/)

### Community Resources
- [Ethereum Discord](https://discord.gg/ethereum)
- [EigenLayer Discord](https://discord.gg/eigenlayer)
- [EthStaker Community](https://ethstaker.cc)

## Monitoring & Maintenance

### Monitoring Setup
- Prometheus metrics enabled
- Grafana dashboards (in progress)
- Alert system (planned)

### Maintenance Tasks
- Regular backups of validator keys
- Log rotation
- Performance monitoring
- Network health checks

## Security Considerations
- JWT authentication between clients
- Secure key management
- Regular security updates
- Network isolation (planned)

## Roadmap

### Phase 1: Basic Infrastructure (Current)
- [x] Set up execution client
- [x] Configure consensus client
- [ ] Implement service management
- [ ] Basic monitoring

### Phase 2: EigenLayer Integration (Next)
- [ ] EigenLayer validator setup
- [ ] AVS node configuration
- [ ] Advanced monitoring
- [ ] Automated maintenance

### Phase 3: Production Readiness
- [ ] Security hardening
- [ ] Backup automation
- [ ] High availability setup
- [ ] Performance optimization