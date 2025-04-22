# Ethereum & EigenLayer Validator Setup

## Overview
This document describes the setup and configuration for running an Ethereum validator with EigenLayer integration on the Holesky testnet. The setup is currently in progress and components are being tested individually before full integration.

## Current Status
| Component | Status | Notes |
|-----------|---------|-------|
| Geth (Execution) | Manual startup | Using Holesky testnet; multiple runs via CLI |
| Lighthouse | Manual startup | Tested with various checkpoint sync URLs |
| Prysm | Manual startup | Alternative to Lighthouse, tested for comparison |
| EigenLayer | Directory prep | Symlinks and data directories set, no service yet |
| Eigenda | Directory prep | Placeholder created, pending implementation |

## Directory Structure
| Path | Purpose | Status |
|------|---------|--------|
| `/mnt/ethereum-testnet` | Base directory for Ethereum Holesky data | Active |
| `/mnt/ethereum-testnet/geth-holesky` | Geth execution client data | Active |
| `/mnt/ethereum-testnet/lighthouse-holesky` | Lighthouse beacon chain data | Active |
| `/mnt/ethereum-testnet/prysm-holesky` | Prysm beacon chain data | Tested |
| `/mnt/eigenlayer` | EigenLayer validator data | Prepared |
| `/mnt/avss/eigenda` | Eigenda node data | Prepared |

### Symlinks
- `~/eigenlayer → /mnt/eigenlayer`
- `~/eigenda → /mnt/avss/eigenda`

## Component Configuration

### 1. Geth (Execution Client)
| Setting | Value | Notes |
|---------|-------|-------|
| Binary | `geth` | Latest stable version |
| Data Directory | `/mnt/ethereum-testnet/geth-holesky` | Persistent storage |
| Network | Holesky | `--networkid 17000` or `--holesky` |
| Ports | - RPC: 8545 (HTTP)<br>- WS: 8546<br>- P2P: 30303<br>- Auth RPC: 8551 | Auth RPC used by consensus clients |
| JWT Secret | `/secrets/jwtsecret` | Shared with consensus clients |
| Sync Mode | `snap` | Fast sync with snapshots |
| Additional Flags | `--metrics`<br>`--pprof`<br>`--verbosity 3`<br>`--allow-insecure-unlock` | For monitoring and debugging |

### 2. Consensus Clients

#### Lighthouse
| Setting | Value | Notes |
|---------|-------|-------|
| Binary | `lighthouse` | Latest stable version |
| Mode | `lighthouse bn` | Beacon node operation |
| Data Directory | `/mnt/ethereum-testnet/lighthouse-holesky` | Persistent storage |
| Execution URL | `http://localhost:8551` | Geth connection |
| JWT Secret | `/mnt/ethereum-testnet/geth-holesky/geth/jwtsecret` | Shared with Geth |
| Checkpoint URLs | Multiple tested:<br>- ethstaker.cc<br>- chainsafe.io<br>- stakely.io | For fast sync |

#### Prysm (Alternative)
| Setting | Value | Notes |
|---------|-------|-------|
| Binary | `beacon-chain` | Latest stable version |
| Data Directory | `/mnt/ethereum-testnet/prysm-holesky` | Persistent storage |
| Execution URL | `http://localhost:8551` | Geth connection |
| JWT Secret | `/secrets/jwtsecret` | Shared with Geth |
| Checkpoint URL | `https://holesky.beaconstate.info` | For fast sync |
| Additional Flags | `--accept-terms-of-use`<br>`--holesky`<br>`--monitoring-host` | Basic configuration |

## Work in Progress

### Current Tasks
1. **Execution Client Stability**
   - [ ] Optimize Geth configuration for Holesky
   - [ ] Implement proper service management
   - [ ] Set up monitoring and alerts

2. **Consensus Client Selection**
   - [ ] Compare Lighthouse vs Prysm performance
   - [ ] Document pros and cons of each
   - [ ] Finalize client choice

3. **EigenLayer Integration**
   - [ ] Complete directory structure setup
   - [ ] Implement validator service
   - [ ] Test EigenLayer functionality

4. **Eigenda Node**
   - [ ] Set up base infrastructure
   - [ ] Implement node service
   - [ ] Configure monitoring

### Next Steps
1. **Service Management**
   - [ ] Create systemd service files
   - [ ] Implement proper startup/shutdown procedures
   - [ ] Set up automatic recovery

2. **Monitoring**
   - [ ] Integrate with Prometheus
   - [ ] Create Grafana dashboards
   - [ ] Set up alerts

3. **Security**
   - [ ] Review and harden configurations
   - [ ] Implement proper key management
   - [ ] Set up backup procedures

## Notes
- All components are currently running in manual mode for testing
- Directory structure is prepared for future service implementation
- Monitoring and automation are planned but not yet implemented
- Regular backups of validator keys and data are essential (procedure to be documented)
