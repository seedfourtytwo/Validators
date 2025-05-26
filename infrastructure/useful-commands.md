# Useful Command Sheet

## Table of Contents
- [1. Solana](#1-solana)
  - [Check Validator Catchup Status](#check-validator-catchup-status)
  - [Check Stakes for Vote Account](#check-stakes-for-vote-account)
  - [Other Useful Solana Commands](#other-useful-solana-commands)
  - [Check Block Production (RPC & CLI)](#check-block-production-rpc--cli)
  - [Check Validator Info and Vote Account](#check-validator-info-and-vote-account)
- [2. JITO](#2-jito)
- [3. Service Checks (All Servers)](#3-service-checks-all-servers)
- [4. Docker](#4-docker)
- [5. Log Checks](#5-log-checks)
- [References](#references)

---

## 1. Solana

### Check Validator Catchup Status
```sh
solana catchup --url https://api.testnet.solana.com JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF
```
- **Description:** Checks how far your validator is from the cluster tip. Replace the public key with your validator identity if needed.

### Check Stakes for Vote Account
```sh
solana stakes 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGG
```
- **Description:** Shows all stake accounts delegated to your vote account.

### Other Useful Solana Commands
```sh
solana balance <ADDRESS>                # Check SOL balance of an address
solana epoch-info                       # Get current epoch and slot info
solana validators                       # List all validators and their status (with commission, skip rate, etc)
solana leader-schedule                  # Show current leader schedule
solana block-production                 # Show block production stats for all validators
solana validator-info get <IDENTITY_PUBKEY>   # Get validator info registered on-chain
solana vote-account <VOTE_PUBKEY>            # Show detailed info about a vote account
solana block <BLOCK_NUMBER>                   # Show details for a specific block
solana slot                                   # Get the current slot
```
- **Descriptions:**
  - `solana validators`: Shows all validators, their status, commission, skip rate, and more.
  - `solana block-production`: Shows block production stats for all validators in the current epoch.
  - `solana validator-info get`: Fetches on-chain info registered by a validator.
  - `solana vote-account`: Shows vote account status, credits, authorized voters, etc.
  - `solana block`: Shows details for a specific block (useful for debugging or research).
  - `solana slot`: Shows the current slot number.

### Check Block Production (RPC & CLI)
#### Using Solana CLI
```sh
solana block-production --identity <IDENTITY_PUBKEY> [--epoch <EPOCH_NUMBER>]
```
- **Description:** Shows block production stats for your validator. Add `--epoch <EPOCH_NUMBER>` to specify a particular epoch.

#### Using RPC (curl)
```sh
curl -X POST https://api.testnet.solana.com \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"getBlockProduction",
    "params": [
      {
        "identity": "JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF" // Replace with your validator identity
      }
    ]
  }'
```
- **To specify an epoch:** Add an `epoch` field to the params object:
```sh
curl -X POST https://api.testnet.solana.com \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"getBlockProduction",
    "params": [
      {
        "identity": "<IDENTITY_PUBKEY>",
        "epoch": <EPOCH_NUMBER>
      }
    ]
  }'
```
- **Description:** Returns block production stats for your validator. Replace `<IDENTITY_PUBKEY>` and `<EPOCH_NUMBER>` as needed.

### Check Validator Info and Vote Account
```sh
solana validator-info get <IDENTITY_PUBKEY>
solana vote-account <VOTE_PUBKEY>
```
- **Description:**
  - `validator-info get`: Shows on-chain info registered by your validator (e.g., name, website, details).
  - `vote-account`: Shows vote account status, credits, authorized voters, and more.

---

## 2. JITO

### JITO Upgrade Plan
- See: [JITO Validator Upgrade Guide](solana-validator/upgrade-jito.md)

### Get Latest JITO Version
```sh
git ls-remote --tags https://github.com/jito-foundation/jito-solana.git | tail -n1
```
- **Description:** Shows the latest available JITO release tag.

### Build and Install Latest JITO (see upgrade guide for details)
```sh
# Set version (replace with latest tag from above)
export JITO_RELEASE_VERSION=v2.2.14-jito

# Clone and build
cd ~/builds
rm -rf jito-solana-$JITO_RELEASE_VERSION

git clone --recurse-submodules https://github.com/jito-foundation/jito-solana.git \
    --branch $JITO_RELEASE_VERSION jito-solana-$JITO_RELEASE_VERSION
cd jito-solana-$JITO_RELEASE_VERSION
./cargo build --release --bin agave-validator

# See full steps in the upgrade guide for symlinking and service restart
```

---

## 3. Service Checks (All Servers)

### Check Validator Service
```sh
sudo systemctl status validator.service
```
- **Description:** Shows the status of the validator service.

### Start/Stop/Restart Validator
```sh
sudo systemctl start validator.service
sudo systemctl stop validator.service
sudo systemctl restart validator.service
```

### Check Monitoring Services
```sh
sudo systemctl status solana-exporter.service
sudo systemctl status node_exporter.service
```

### Check Services on All Servers (via SSH)
```sh
ssh user@server 'systemctl status validator.service'
ssh user@server 'systemctl status solana-exporter.service'
ssh user@server 'systemctl status node_exporter.service'
```
- **Tip:** Use a script or Ansible for batch checks across multiple servers.

---

## 4. Docker

### List Running Containers
```sh
docker ps
```

### List All Containers (including stopped)
```sh
docker ps -a
```

### Check Logs for a Container
```sh
docker logs <container_name>
```

### Restart a Container
```sh
docker restart <container_name>
```

### Update and Rebuild Monitoring Stack (if using docker-compose)
```sh
cd /path/to/monitoring_stack
docker-compose pull
docker-compose up -d
```
- **Description:** Updates and restarts your monitoring stack. Adjust the path as needed.

---

## 5. Log Checks

### Tail Validator Logs
```sh
tail -f /home/sol/validators/data/log/validator.log
```

### Search for Errors or Warnings
```sh
grep -E 'ERROR|WARN' /home/sol/validators/data/log/validator.log
```

### Check JITO MEV Activity
```sh
grep -a "tip" /home/sol/validators/data/log/validator.log | grep "payment"
```

### Check Logs for Monitoring Services
```sh
journalctl -u solana-exporter.service -n 100
journalctl -u node_exporter.service -n 100
```

---

## References
- [JITO Validator Upgrade Guide](solana-validator/upgrade-jito.md)
- [Solana CLI Reference](https://docs.solana.com/cli/usage)
- [Your Monitoring Stack Setup](solana-validator/setup-tutorials/monitoring.md) 