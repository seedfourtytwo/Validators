# ⚠️ DEPRECATED - Agave Validator Setup Guide ⚠️

> **WARNING**: This setup guide is now deprecated as we have moved to using JITO for our validator implementation.
> For the current validator setup, please see [JITO Validator Setup Guide](./jito.md).
> This documentation is kept for reference purposes only.

---

# Agave Validator Setup Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Building Agave from Source](#building-agave-from-source)
4. [Keypair Management](#keypair-management)
5. [Validator Configuration](#validator-configuration)
6. [Storage Setup](#storage-setup)
7. [Service Configuration](#service-configuration)
8. [Starting the Validator](#starting-the-validator)
9. [Monitoring and Maintenance](#monitoring-and-maintenance)
10. [Troubleshooting](#troubleshooting)
11. [Testnet Setup and Vote Account Registration](#testnet-setup-and-vote-account-registration)

## Introduction

This guide provides step-by-step instructions for setting up an Agave validator on your Linux server. Agave is a Solana validator implementation forked from the official Solana validator, designed to provide enhanced performance and reliability.

This tutorial is based on the following resources:
- [Building Solana from Source](https://github.com/agjell/sol-tutorials/blob/master/building-solana-from-source.md)
- [Agave Beginners Guide](https://github.com/agjell/sol-tutorials/blob/master/agave-beginners-guide.md)

## Prerequisites

Before starting, ensure you have:
- A Linux server with Ubuntu 24.04 or later
- Root or sudo access
- At least 2TB of NVMe storage (preferably 3 separate drives)
- A stable internet connection
- The `sol` user created and configured as described in the Linux setup tutorial

## Building Agave from Source

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

### Build Agave

**Run as: sol user**

```bash
# Define version (replace with the latest mainnet version)
export TAG=v2.2.6

# Clone the source code
git clone https://github.com/anza-xyz/agave.git --depth 1 --branch $TAG ~/agave-src-$TAG

# Build and install Agave
# For validator-only build (faster):
bash ~/agave-src-$TAG/scripts/cargo-install-all.sh --validator-only ~/.local/share/solana/install/releases/$TAG

# Create symbolic link for active release
ln --symbolic ~/.local/share/solana/install/releases/$TAG ~/.local/share/solana/install/active_release

# Add to PATH
echo 'export PATH=~/.local/share/solana/install/active_release/bin:$PATH' >> ~/.profile
source ~/.profile

# Verify installation
solana --version

# Clean up source files
rm -rf ~/agave-src-$TAG
```

### All-in-One Build Command

**Run as: sol user**

For faster builds, you can use this all-in-one command:

```bash
export TAG=v2.2.6 && \
export CARGO_BUILD_JOBS=8 && \
export RUSTFLAGS="-C target-cpu=native" && \
git clone https://github.com/anza-xyz/agave.git --depth 1 --branch "${TAG}" ~/agave-src-"${TAG}" && \
bash ~/agave-src-"${TAG}"/scripts/cargo-install-all.sh --validator-only ~/.local/share/solana/install/releases/"${TAG}" && \
ln --force --no-dereference --symbolic ~/.local/share/solana/install/releases/"${TAG}" ~/.local/share/solana/install/active_release && \
solana --version
```

Adjust `CARGO_BUILD_JOBS` based on your system's capabilities. If the validator is running, use a lower value (e.g., 8).

## Keypair Management

### Generate Keypairs

**Run as: sol user**

```bash
# Create wallets directory
mkdir -p ~/wallets

# Generate validator identity keypair
solana-keygen new --outfile ~/wallets/validator-identity.json

# Generate vote account keypair (store securely off-site)
solana-keygen new --outfile ~/wallets/vote-account.json

# Generate withdrawer keypair (store securely off-site)
solana-keygen new --outfile ~/wallets/withdrawer.json

# Test key recovery (optional)
solana-keygen recover --outfile ~/wallets/test-recovery.json
```

> **Note:** The key generation method above is suitable for testing and development. For production environments, follow the secure key management procedures outlined in the [Cold Key Management Guide](cold-key-management.md) to ensure maximum security for your validator keys.

### Validator Key Security Strategy

To follow best practices and reduce risk, only **essential keypairs** are kept on the validator. Others are stored safely in cold storage (e.g., password manager).

| Keypair | Location | Purpose |
|---------|----------|---------|
| `identity-keypair` | On the validator | Signs blocks, votes, and communicates with the cluster. Required to run the validator. |
| `vote-account-keypair` | Cold storage | Manages the vote account. Only needed to create the account or change its authority. Not needed for validator runtime. |
| `withdrawer-keypair` | Cold storage | Used to withdraw staking rewards. Only needed when collecting rewards, not for running the validator. |

### Configure Validator Identity

**Run as: sol user**

```bash
# Set the validator identity
solana config set --keypair ~/wallets/validator-identity.json

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
keypair_path: /home/sol/wallets/validator-identity.json
address_labels:
  '11111111111111111111111111111111': System Program
commitment: confirmed
EOT
```

### Create Startup Script

**Run as: sol user**

```bash
# Create startup script
cat > ~/start-validator.sh << EOT
#!/bin/bash

exec agave-validator \\
  --identity ~/wallets/validator-identity.json \\
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
  --ledger ~/ledger \\
  --accounts ~/accounts \\
  --snapshots ~/snapshots \\
  --log ~/log/validator.log \\
  --limit-ledger-size \\
  --full-rpc-api
EOT

# Make the script executable
chmod +x ~/start-validator.sh
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
# Create symbolic links in home directory
ln -s /mnt/ledger ~/ledger
ln -s /mnt/accounts ~/accounts
ln -s /mnt/snapshots ~/snapshots

# Create log directory
mkdir -p ~/log
```

### Configure Log Rotation

**Run as: root or user with sudo privileges**

```bash
# Create logrotate configuration
sudo cat > /etc/logrotate.d/solana << EOT
/home/sol/log/*.log {
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

### Create Systemd Service

**Run as: root or user with sudo privileges**

```bash
# Create systemd service file
sudo cat > /etc/systemd/system/validator.service << EOT
[Unit]
Description=Solana Validator
After=network.target network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
LimitNOFILE=2000000
LogRateLimitIntervalSec=0
User=sol
Environment=SOLANA_METRICS_CONFIG=host=https://metrics.solana.com:8086,db=testnet,u=testnet_write,p=password
Environment=PATH=/home/sol/.local/share/solana/install/active_release/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/sol/start-validator.sh

[Install]
WantedBy=multi-user.target
EOT

# Reload systemd
sudo systemctl daemon-reload
```

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
# Monitor validator startup
agave-validator --ledger ~/ledger monitor
```

The validator startup process includes:
1. Finding an available RPC node
2. Downloading snapshot (~90 GB for mainnet)
3. Loading ledger state from snapshot
4. Catching up to the cluster

This can take 30+ minutes on mainnet.

### Check Catch-up Status

**Run as: sol user**

```bash
# Check if validator has caught up to the cluster
solana catchup --keypair ~/wallets/validator-identity.json --our-localhost
```

## Monitoring and Maintenance

### Log Analysis

**Run as: sol user**

```bash
# View recent logs
tail -f ~/log/validator.log

# Search for errors
grep --extended-regexp 'ERROR|WARN' ~/log/validator.log
```

### Updating Agave

**Run as: sol user**

To update to a new version:

```bash
# Define new version
export TAG=v2.2.7

# Clone and build new version
git clone https://github.com/anza-xyz/agave.git --depth 1 --branch $TAG ~/agave-src-$TAG
bash ~/agave-src-$TAG/scripts/cargo-install-all.sh --validator-only ~/.local/share/solana/install/releases/$TAG

# Update symbolic link
ln --force --no-dereference --symbolic ~/.local/share/solana/install/releases/$TAG ~/.local/share/solana/install/active_release

# Verify installation
solana --version

# Clean up
rm -rf ~/agave-src-$TAG
```

**Run as: root or user with sudo privileges**

```bash
# Restart the validator service
sudo systemctl restart validator.service
```

## Testnet Setup and Vote Account Registration

### Register for the Solana Foundation Delegation Program

Before getting testnet SOL, you should register for the Solana Foundation Delegation Program:

1. Visit [https://solana.org/delegation-program](https://solana.org/delegation-program)
2. Click on "Apply now" to start the application process
3. Complete the KYC (Know Your Customer) verification
4. Submit your application

This program provides several benefits:
- Testnet participation support
- Vote cost coverage for new validators
- Stake matching (1:1 up to 100,000 SOL)
- Residual delegation for eligible validators

### Getting Testnet SOL

To get testnet SOL, you have several options:

1. **Solana Testnet Faucet**:
   - Visit [https://www.testnetfaucet.org/](https://www.testnetfaucet.org/)
   - Enter your wallet address to receive 2 testnet SOL
   - Wait for the transaction to confirm

2. **Solana Discord Community**:
   - Join the [main Solana Discord](https://discord.gg/solana)
   - **Note:** It is against the guidelines to ask for testnet SOL on the Solana Discord
   - Instead, use the official faucet or other approved methods

3. **Testnet Validator Program**:
   - After registering for the [Solana Foundation Delegation Program](https://solana.org/delegation-program)
   - Your testnet validator will automatically be added to the testnet stake bot
   - 100 testnet validators are added monthly, so it may take a few months to be added
   - Continue voting well and start producing blocks on testnet to earn bonus stake

### Registering a Vote Account

**Run as: sol user**

```bash
# Make sure you're on testnet
solana config set --url https://api.testnet.solana.com

# Create a vote account (requires SOL)
solana create-vote-account \
  --keypair ~/wallets/validator-identity.json \
  --vote-account ~/wallets/vote-account.json \
  --authority ~/wallets/validator-identity.json \
  --commission 10

# Verify the vote account was created
solana vote-account ~/wallets/vote-account.json
```

### Starting Voting and Delegating

**Run as: sol user**

```bash
# Update your validator startup script with the vote account public key
# Replace YOUR_VOTE_ACCOUNT_PUBKEY with the actual public key
sed -i "s/YOUR_VOTE_ACCOUNT_PUBKEY/$(solana-keygen pubkey ~/wallets/vote-account.json)/" ~/start-validator.sh

# Restart the validator service
sudo systemctl restart validator.service

# Check if the validator is voting
solana validators | grep $(solana-keygen pubkey ~/wallets/validator-identity.json)
```

### Important Notes on Voting

1. **No-Vote Flag**: If you want to run the validator without voting (for testing or initial setup), add the `--no-vote` flag to your startup script:
   ```bash
   exec agave-validator \
     --identity ~/wallets/validator-identity.json \
     --no-vote \
     # ... other options ...
   ```

2. **Commission Rate**: The commission rate (10% in the example) determines what percentage of staking rewards the validator keeps. The rest goes to stakers.

3. **Vote Account Authority**: The vote account authority (your validator identity) is responsible for signing votes. Make sure this keypair is secure and accessible to the validator.

4. **Monitoring Votes**: You can monitor your validator's voting performance with:
   ```bash
   solana validators | grep $(solana-keygen pubkey ~/wallets/validator-identity.json)
   ```

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Ensure the sol user has proper ownership of mount points:
     ```bash
     sudo chown -R sol:sol /mnt/snapshots
     sudo chown -R sol:sol /mnt/ledger
     sudo chown -R sol:sol /mnt/accounts
     ```

2. **Validator Not Syncing**
   - Check network connectivity
   - Verify entrypoint nodes are accessible
   - Check for disk space issues

3. **High Memory Usage**
   - The validator is configured with a high file descriptor limit (2000000)
   - Monitor memory usage and consider adjusting system parameters if needed

4. **Service Crashes**
   - Check the log file for errors
   - The service is configured to restart automatically

### Log Analysis

To analyze the validator log:
```bash
tail -f ~/log/validator.log
```

To search for specific errors:
```bash
grep -i error ~/log/validator.log
```