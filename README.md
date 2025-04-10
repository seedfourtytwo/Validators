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



