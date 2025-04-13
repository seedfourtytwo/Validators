# Bitcoin Metrics Collector

A Prometheus metrics collector for Bitcoin Core that uses cookie authentication by default.

## Prerequisites

- Python 3.8+
- Bitcoin Core running with cookie authentication enabled
- The `bitcoin` user must have access to the Bitcoin Core cookie file

## Installation

1. Clone the repository as the bitcoin user:
```bash
cd /home/bitcoin
git clone <repository-url> bitcoin-metrics
cd bitcoin-metrics
```

2. Make the installation script executable:
```bash
chmod +x install.sh
```

3. Run the installation script as the bitcoin user:
```bash
./install.sh
```

The script will:
- Create a Python virtual environment
- Install required dependencies
- Set up a systemd user service
- Enable the service to start on boot
- Start the metrics collector

## Configuration

The collector uses cookie authentication by default. The cookie file should be located at `/mnt/bitcoin-node/.cookie` and owned by the bitcoin user.

If you need to use username/password authentication instead, create a `.env` file with:
```
BITCOIN_RPC_USER=your_rpc_user
BITCOIN_RPC_PASSWORD=your_rpc_password
```

## Service Management

The metrics collector runs as a systemd user service under the bitcoin user. To manage the service:

```bash
# Check service status
systemctl --user status bitcoin-metrics.service

# Stop the service
systemctl --user stop bitcoin-metrics.service

# Start the service
systemctl --user start bitcoin-metrics.service

# Restart the service
systemctl --user restart bitcoin-metrics.service

# View logs
journalctl --user -u bitcoin-metrics.service
```

## Metrics

The collector exposes the following metrics on port 9332:

- `bitcoin_block_height`: Current block height
- `bitcoin_verification_progress`: Blockchain verification progress
- `bitcoin_difficulty`: Current mining difficulty
- `bitcoin_mempool_size`: Number of transactions in mempool
- `bitcoin_mempool_bytes`: Size of mempool in bytes
- `bitcoin_peer_count`: Number of connected peers
- `bitcoin_memory_usage_bytes`: Memory usage in bytes

## Security Notes

- The collector runs under the bitcoin user without sudo privileges
- Cookie authentication is used by default for enhanced security
- The service is configured to restart automatically on failure
- The bitcoin user's lingering is enabled to ensure the service runs after logout

## Troubleshooting

1. If the service fails to start, check the logs:
```bash
journalctl --user -u bitcoin-metrics.service
```

2. Verify the cookie file permissions:
```bash
ls -l /mnt/bitcoin-node/.cookie
```

3. Ensure Bitcoin Core is running:
```bash
systemctl status bitcoind
```

4. Check if the metrics endpoint is accessible:
```bash
curl http://localhost:9332/metrics
``` 
=======
# Validator Projects Documentation

## Overview
After 4years+ in the Crypto industry, it is time for me to start building. This project serves as both documentation and a learning platform for blockchain infrastructure.

## Table of Contents
- [Project Structure](#project-structure)
- [Validator Projects](#validator-projects)
  - [Solana Validator](#solana-validator)
  - [Ethereum Validator (Upcoming)](#ethereum-validator)
  - [Bitcoin Node (Upcoming)](#bitcoin-node)
- [Infrastructure](#infrastructure)
- [Skills & Technologies](#skills--technologies)
- [Monitoring & Metrics](#monitoring--metrics)

## Project Structure
```
.
├── solana-validator/     # Solana validator documentation and configs
├── ethereum/            # Ethereum validator documentation (upcoming)
├── bitcoin-node/        # Bitcoin node documentation (upcoming)
├── infrastructure/      # Infrastructure setup and configuration
├── docs/               # General documentation
└── overview/           # Architecture diagrams and overviews
```

## Validator Projects

### Solana Validator
- **Status**: Active on Testnet
- **Validator Address**: [JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF](https://www.validators.app/validators/JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF?locale=en&network=testnet)
- **Documentation**: [Solana Validator Setup](solana-validator/README.md)
- **Metrics Dashboard**: [Validator Metrics](https://metric.seed42.co/public-dashboards/ceff27f0e3ba4434912481b5b93f96a1)

### Ethereum Validator
- **Status**: Planning Phase
- **Documentation**: Coming Soon

### Bitcoin Node
- **Status**: Planning Phase
- **Documentation**: Coming Soon

## Infrastructure
![Validator Architecture](overview/infra-overview.png)

### Components
- **Validator Server**: Primary Solana validator
- **Home Server**: Metrics collection / visualization and running of Ethereum and Bitcoin services as they are less demanding
- **Cold Storage**: Secure key storage solution

## Skills & Technologies

### General Skills
- **Linux**: System administration, optimization, and service management
- **SSH**: Key management, security hardening, and auditing
- **Networking**: Routing, firewall configuration, port management
- **Containerization**: Docker for service deployment

### Blockchain Technologies
- **Solana**: Validator operations, key management, monitoring
- **Ethereum**: Coming soon - Validator operations, staking
- **Bitcoin**: Coming soon - Node operations

## Monitoring & Metrics
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Alerting**: Custom alert configurations

## Other
- **nginx**: reverse proxy and ssl certificat manavement
- **Termius**: Local CLI for remot access to servers
- **Git/Github**: Used for documentation in this case
- **AI**: Cursor - Chat GPT - Claude Sonnet, for learning and isntructions along the way



>>>>>>> 816c7f661314a3b9d31560dc4a9f1ee4d63009fb
