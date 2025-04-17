# JITO Validator Setup Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Building JITO from Source](#building-jito-from-source)
4. [Keypair Management](#keypair-management)
5. [Validator Configuration](#validator-configuration)
6. [Storage Setup](#storage-setup)
7. [Service Configuration](#service-configuration)
8. [Starting the Validator](#starting-the-validator)
9. [MEV Configuration](#mev-configuration)
10. [Monitoring and Maintenance](#monitoring-and-maintenance)
11. [Troubleshooting](#troubleshooting)
12. [Switching Between Validators](#switching-between-validators)

## Introduction

This guide provides step-by-step instructions for setting up a JITO validator on a Linux server. JITO is a Solana validator implementation that adds MEV (Maximal Extractable Value) capabilities to the standard Solana validator, allowing you to participate in additional revenue streams through block building and MEV extraction.

This tutorial is based on the following resources:
- [JITO Documentation](https://jito-labs.gitbook.io/mev/validators/getting-started)
- [JITO GitHub](https://github.com/jito-foundation/jito-solana)

## Prerequisites

Before starting, ensure you have:
- A Linux server with Ubuntu 24.04 or later
- Root or sudo access
- At least 2TB of NVMe storage (preferably 3 separate drives)
- A stable internet connection
- The `sol` user created and configured as described in the Linux setup tutorial
- An existing Solana validator identity and vote account (optional, can be created during setup)

## Building JITO from Source

### Install Dependencies

**Run as: root or user with sudo privileges**

```bash
sudo apt update && sudo apt install -y \
  git libssl-dev libudev-dev pkg-config zlib1g-dev llvm clang cmake make libprotobuf-dev protobuf-compiler
```

### Install Rust

**Run as: sol user**

```bash
# Switch to sol user if not already
su - sol

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Load Rust environment
source $HOME/.cargo/env
```

### Build JITO

**Run as: sol user**

```bash
# Create validators directory structure
mkdir -p ~/validators/jito/versions
mkdir -p ~/validators/scripts
mkdir -p ~/validators/data/log
mkdir -p ~/validators/secure/wallets

# Define version (use specific JITO version)
export TAG=v2.2.8-jito

# Clone the source code
git clone https://github.com/jito-foundation/jito-solana.git ~/jito-src-$TAG

# Checkout the specific version
cd ~/jito-src-$TAG
git checkout tags/$TAG

# Build JITO
# For validator-only build (faster):
bash ~/jito-src-$TAG/scripts/cargo-install-all.sh --validator-only ~/validators/jito/versions/$TAG

# Create symbolic link for active release
cd ~/validators/jito
ln -sf versions/$TAG active

# Verify installation
~/validators/jito/active --version
```

> **Note**: When checking the version, you'll notice that the binary still reports itself as `agave-validator` but with `client:JitoLabs` in the version string. This is normal as JITO is based on Agave's codebase.

### All-in-One Build Command

**Run as: sol user**

For faster builds, you can use this all-in-one command:

```bash
export TAG=v2.2.8-jito && \
export CARGO_BUILD_JOBS=8 && \
export RUSTFLAGS="-C target-cpu=native" && \
mkdir -p ~/validators/jito/versions && \
git clone https://github.com/jito-foundation/jito-solana.git ~/jito-src-"${TAG}" && \
cd ~/jito-src-"${TAG}" && \
git checkout tags/"${TAG}" && \
bash ~/jito-src-"${TAG}"/scripts/cargo-install-all.sh --validator-only ~/validators/jito/versions/"${TAG}" && \
cd ~/validators/jito && \
ln -sf versions/"${TAG}" active && \
~/validators/jito/active --version
```

Adjust `CARGO_BUILD_JOBS` based on your system's capabilities. If the validator is running, use a lower value (e.g., 8).

## Keypair Management

### Generate Keypairs

For secure key generation, follow the procedures outlined in our comprehensive [Cold Key Management Guide](../cold-key-management.md). This guide provides detailed instructions on generating validator keys in a secure air-gapped environment to ensure maximum security for your validator.

> **IMPORTANT**: Never generate production validator keys on internet-connected machines. The cold key generation process is essential for securing your validator and protecting staked funds.

### Validator Key Security Strategy

To follow best practices and reduce risk, only **essential keypairs** are kept on the validator. Others are stored safely in cold storage (e.g., hardware wallet or secure offline storage):

| Keypair | Location | Purpose |
|---------|----------|---------|
| `identity-keypair` | On the validator | Signs blocks, votes, and communicates with the cluster. Required to run the validator. |
| `vote-account-keypair` | Cold storage | Manages the vote account. Only needed to create the account or change its authority. Not needed for validator runtime. |
| `withdrawer-keypair` | Cold storage | Used to withdraw staking rewards. Only needed when collecting rewards, not for running the validator. |

### Configure Validator Identity

**Run as: sol user**

```bash
# Set the validator identity
solana config set --keypair ~/validators/secure/wallets/validator-identity.json

# Set the network (testnet or mainnet-beta)
solana config set --url https://api.testnet.solana.com
```

## Validator Configuration

### Create CLI Configuration

**Run as: sol user**

```bash
# Create config directory
mkdir -p ~/.config/solana/cli

# Create config file
cat > ~/.config/solana/cli/config.yml << EOT
---
json_rpc_url: https://api.testnet.solana.com
websocket_url: ''
keypair_path: /home/sol/validators/secure/wallets/validator-identity.json
address_labels:
  '11111111111111111111111111111111': System Program
commitment: confirmed
EOT
```

### Create Startup Script

**Run as: sol user**

```bash
# Create startup script
cat > ~/validators/scripts/start-jito-validator.sh << EOT
#!/bin/bash

exec /home/sol/validators/jito/active \\
  --identity /home/sol/validators/secure/wallets/validator-identity.json \\
  --vote-account YOUR_VOTE_ACCOUNT_PUBKEY \\
  --entrypoint entrypoint.testnet.solana.com:8001 \\
  --entrypoint entrypoint2.testnet.solana.com:8001 \\
  --entrypoint entrypoint3.testnet.solana.com:8001 \\
  --known-validator 5D1fNXzvv5NjV1ysLjirC4WY92RNsVH18vjmcszZd8on \\
  --known-validator dDzy5SR3AXdYWVqbDEkVFdvSPCtS9ihF5kJkHCtXoFs \\
  --known-validator Ft5fbkqNa76vnsjYNwjDZUXoTWpP7VYm3mtsaQckQADN \\
  --known-validator eoKpUABi59aT4rR9HGS3LcMecfut9x7zJyodWWP43YQ \\
  --known-validator 9QxCLckBiJc783jnMvXZubK4wH86Eqqvashtrwvcsgkv \\
  --expected-genesis-hash 4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY \\
  --only-known-rpc \\
  --rpc-port 8899 \\
  --private-rpc \\
  --dynamic-port-range 8000-8020 \\
  --wal-recovery-mode skip_any_corrupted_record \\
  --ledger /home/sol/validators/data/ledger \\
  --accounts /home/sol/validators/data/accounts \\
  --snapshots /home/sol/validators/data/snapshots \\
  --log /home/sol/validators/data/log/validator.log \\
  --limit-ledger-size \\
  --full-rpc-api \\
  --tip-payment-program-pubkey GJHtFqM9agxPmkeKjHny6qiRKrXZALvvFGiKf11QE7hy \\
  --tip-distribution-program-pubkey F2Zu7QZiTYUhPd7u9ukRVwxh7B71oA3NMJcHuCHc29P2 \\
  --merkle-root-upload-authority GZctHpWXmsZC1YHACTGGcHhYxjdRqQvTpYkb9LMvxDib \\
  --commission-bps 800 \\
  --block-engine-url https://ny.testnet.block-engine.jito.wtf \\
  --relayer-url http://ny.testnet.relayer.jito.wtf:8100 \\
  --shred-receiver-address 141.98.216.132:1002
EOT

# Make the script executable
chmod +x ~/validators/scripts/start-jito-validator.sh
```

Replace `YOUR_VOTE_ACCOUNT_PUBKEY` with your actual vote account public key.

## Storage Setup

### Create Storage Directories

**Run as: root or user with sudo privileges**

```bash
# Create mount points if not already created
sudo mkdir -p /mnt/ledger
sudo mkdir -p /mnt/accounts
sudo mkdir -p /mnt/snapshots

# Set ownership to sol user
sudo chown -R sol:sol /mnt/ledger
sudo chown -R sol:sol /mnt/accounts
sudo chown -R sol:sol /mnt/snapshots
```

### Create Symbolic Links

**Run as: sol user**

```bash
# Create symbolic links in validators data directory
ln -s /mnt/ledger ~/validators/data/ledger
ln -s /mnt/accounts ~/validators/data/accounts
ln -s /mnt/snapshots ~/validators/data/snapshots
```

### Configure Log Rotation

**Run as: root or user with sudo privileges**

```bash
# Create log rotation configuration
sudo cat > /etc/logrotate.d/solana-validator << EOT
/home/sol/validators/data/log/*.log {
  su sol sol
  daily
  rotate 7
  missingok
  postrotate
    systemctl kill -s USR1 validator.service
  endscript
}
EOT

# Restart logrotate service
sudo systemctl restart logrotate
```

## Service Configuration

### Create Environment Configuration

**Run as: root or user with sudo privileges**

> **Note**: This environment-based configuration is only necessary if you plan to switch between different validator clients (e.g., Agave and JITO). If you're only running JITO, you can simplify by using a direct path to the JITO binary in your service file instead of using environment variables.

```bash
# Create environment file for validator type
sudo cat > /etc/default/validator << EOT
# Valid values: agave, jito
VALIDATOR_TYPE=jito
EOT
```

### Create Systemd Service

**Run as: root or user with sudo privileges**

> **Note**: This service configuration uses environment variables to allow switching between validator clients. If you only intend to run JITO, you can simplify by directly referencing the JITO startup script.

```bash
# Create systemd service file
sudo cat > /etc/systemd/system/validator.service << EOT
[Unit]
Description=Solana Validator
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=sol
EnvironmentFile=/etc/default/validator
ExecStart=/bin/bash -c '/home/sol/validators/scripts/start-\${VALIDATOR_TYPE}-validator.sh'
LimitNOFILE=1000000

[Install]
WantedBy=multi-user.target
EOT

# Reload systemd
sudo systemctl daemon-reload
```

### Simplified Service Configuration (JITO Only)

If you only plan to run JITO and don't need the ability to switch between validator clients, you can use this simpler service configuration:

```bash
# Create simplified systemd service file for JITO only
sudo cat > /etc/systemd/system/validator.service << EOT
[Unit]
Description=JITO Solana Validator
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=sol
ExecStart=/home/sol/validators/scripts/start-jito-validator.sh
LimitNOFILE=1000000

[Install]
WantedBy=multi-user.target
EOT

# Reload systemd
sudo systemctl daemon-reload
```

## MEV Configuration

### JITO-Specific Parameters

JITO validators require additional parameters to participate in MEV extraction. The following parameters are already included in the startup script:

1. **Tip Payment & Distribution Programs**:
   - `--tip-payment-program-pubkey`: Program address for processing tips (`GJHtFqM9agxPmkeKjHny6qiRKrXZALvvFGiKf11QE7hy` for testnet)
   - `--tip-distribution-program-pubkey`: Program address for distributing rewards (`F2Zu7QZiTYUhPd7u9ukRVwxh7B71oA3NMJcHuCHc29P2` for testnet)

2. **Merkle Root Upload Authority**:
   - `--merkle-root-upload-authority`: Set to `GZctHpWXmsZC1YHACTGGcHhYxjdRqQvTpYkb9LMvxDib` for JITO to handle airdrops and claims

3. **MEV Commission**:
   - `--commission-bps`: Sets commission for MEV tips in basis points (800 = 8%)

4. **Connection Endpoints**:
   - `--block-engine-url`: Endpoint for JITO's block engine 
   - `--relayer-url`: Endpoint for JITO's transaction relayer
   - `--shred-receiver-address`: Address where validator shreds are sent

> **Note**: For mainnet, you will need to use different addresses for the parameters above. Consult the [JITO Documentation](https://jito-labs.gitbook.io/mev/validators/getting-started) for mainnet values.

## Starting the Validator

### Enable and Start the Service

**Run as: root or user with sudo privileges**

```bash
# Enable the service to start on boot
sudo systemctl enable validator.service

# Start the service
sudo systemctl start validator.service

# Check status
sudo systemctl status validator.service
```

### Monitor the Validator

**Run as: sol user**

```bash
# Monitor validator startup (add monitor parameter to the validator binary)
/home/sol/validators/jito/active --ledger /home/sol/validators/data/ledger monitor
```

The validator startup process includes:
1. Finding an available RPC node
2. Downloading snapshot
3. Loading ledger state from snapshot
4. Catching up to the cluster

This can take 30+ minutes on mainnet.

### Check Catch-up Status

**Run as: sol user**

```bash
# Check if validator has caught up to the cluster
solana catchup --url https://api.testnet.solana.com JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF
```

Replace `JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF` with your validator's identity public key.

## Monitoring and Maintenance

### Log Analysis

**Run as: sol user**

```bash
# View recent logs
tail -f ~/validators/data/log/validator.log

# Search for errors
grep --extended-regexp 'ERROR|WARN' ~/validators/data/log/validator.log

# Search for MEV-related activity
grep -a "tip" ~/validators/data/log/validator.log | grep "payment"
```

### Checking MEV Rewards

To check if your validator is receiving MEV rewards:

```bash
# Check your vote account transaction history for MEV payments
solana vote-account --with-rewards ~/validators/secure/wallets/vote-account.json
```

### Verifying JITO Binary

The JITO binary is based on Agave but includes additional MEV functionality. When checking the version, it will show "agave-validator" in the name but with "client:JitoLabs" to indicate it's the JITO fork:

```bash
/home/sol/validators/jito/active --version
# Example output: agave-validator 2.2.8 (src:00000000; feat:1522022101, client:JitoLabs)
```

### Updating JITO

To update to a new version:

```bash
# Define new version
export TAG=v2.2.9-jito

# Clone and build new version
git clone https://github.com/jito-foundation/jito-solana.git ~/jito-src-$TAG
cd ~/jito-src-$TAG
git checkout tags/$TAG
bash ~/jito-src-$TAG/scripts/cargo-install-all.sh --validator-only ~/validators/jito/versions/$TAG

# Update symbolic link
cd ~/validators/jito
ln -sf versions/$TAG active

# Verify installation
~/validators/jito/active --version

# Clean up
rm -rf ~/jito-src-$TAG
```

**Run as: root or user with sudo privileges**

```bash
# Restart the validator service
sudo systemctl restart validator.service
```

## Troubleshooting

### Common Issues

1. **Missing Required Parameters**
   - Ensure all JITO-specific parameters are included in your startup script
   - Check logs for errors related to MEV parameters

2. **Connectivity Issues**
   - Verify connectivity to JITO's infrastructure endpoints
   - Check network connectivity for block engine and relayer URLs

3. **Validator Not Syncing**
   - Check network connectivity
   - Verify entrypoint nodes are accessible
   - Check for disk space issues

4. **MEV Rewards Not Showing**
   - Verify validator is properly voting
   - Check that all JITO-specific parameters are correct
   - Ensure your validator has sufficient stake to be selected for block production

### Log Analysis

To analyze the validator log for MEV-related information:

```bash
# Search for tip-related activities
grep -a "tip" ~/validators/data/log/validator.log | grep "payment"

# Check for MEV-related errors
grep -a -i "mev\|tip\|block-engine\|relayer" ~/validators/data/log/validator.log | grep -i "error\|warn"
```

## Switching Between Validators

### Switch to Agave (Standard Validator)

If you need to temporarily switch back to the standard Agave validator:

```bash
# Change the validator type to agave
sudo sed -i 's/VALIDATOR_TYPE=jito/VALIDATOR_TYPE=agave/' /etc/default/validator

# Restart the validator service
sudo systemctl restart validator.service
```

### Switch to JITO (MEV Validator)

To switch back to JITO:

```bash
# Change the validator type to jito
sudo sed -i 's/VALIDATOR_TYPE=agave/VALIDATOR_TYPE=jito/' /etc/default/validator

# Restart the validator service
sudo systemctl restart validator.service
```

> **Note**: Switching between validators will cause your validator to restart. This will temporarily affect your validator's uptime and performance metrics. 