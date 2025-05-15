# 🔄 JITO Validator Upgrade Guide

This guide documents the process of upgrading the JITO validator software to a new version.

## Prerequisites
- Administrative access (sudo privileges)
- Build environment with required dependencies
- Sufficient system resources (8+ CPU cores for build)
- Current validator running and healthy
- At least 20GB of free disk space for build process

## Pre-Upgrade Steps

### 1. Check System Resources
```bash
# As regular user (not root)
# Check available disk space (need at least 20GB free)
df -h /home

# As root user: Clean system packages if needed
sudo apt-get clean
```

### 2. Build Environment Setup
```bash
# As regular user (not root)
# Create and enter build directory
mkdir -p ~/builds
cd ~/builds

# Set target version
export JITO_RELEASE_VERSION=v2.2.14-jito
export CARGO_NET_GIT_FETCH_WITH_CLI=true

# OPTIONAL: Setup build cache (only if you have sccache installed)
# To install sccache: cargo install sccache
# Then uncomment the line below:
# export RUSTC_WRAPPER=sccache

# Ensure correct Rust toolchain
rustup install 1.84.1
rustup default 1.84.1
```

### 3. Clone and Build
```bash
# Make sure you're in the builds directory
cd ~/builds

# Remove old clone if it exists
rm -rf jito-solana-$JITO_RELEASE_VERSION

# Clone JITO repository with all required submodules
git clone --recurse-submodules https://github.com/jito-foundation/jito-solana.git \
    --branch $JITO_RELEASE_VERSION jito-solana-$JITO_RELEASE_VERSION

# Enter the repository directory
cd jito-solana-$JITO_RELEASE_VERSION

# Build validator binary (takes ~12 minutes)
# If build fails with sccache, unset it first: unset RUSTC_WRAPPER
./cargo build --release --bin agave-validator
```

### Troubleshooting Build Issues

#### 1. Rust Toolchain Issues
If you encounter toolchain errors:
```bash
# Verify Rust version
rustc --version    # Should show 1.84.1

# If wrong version, set correct one:
rustup default 1.84.1
```

#### 2. Build Cache Issues
If you encounter sccache errors:
```bash
# Remove sccache and build without it
unset RUSTC_WRAPPER
./cargo build --release --bin agave-validator
```

#### 3. Missing Submodules
If you encounter errors about missing files or dependencies:
```bash
# IMPORTANT: Make sure you're in the repository directory first
cd ~/builds/jito-solana-$JITO_RELEASE_VERSION

# Then initialize and update submodules
git submodule update --init --recursive

# If the above doesn't work, start fresh with a new clone:
cd ~/builds
rm -rf jito-solana-$JITO_RELEASE_VERSION
git clone --recurse-submodules https://github.com/jito-foundation/jito-solana.git \
    --branch $JITO_RELEASE_VERSION jito-solana-$JITO_RELEASE_VERSION
```

### 4. Verify Build Output
```bash
# Verify the binary exists and is executable
ls -l target/release/agave-validator

# Check the version
./target/release/agave-validator --version
```

### 5. Install New Version
```bash
# As regular user, verify the build location
echo "Build location: $HOME/builds/jito-solana-$JITO_RELEASE_VERSION/target/release/agave-validator"

# Switch to admin user and run these commands:
# Create version directory
sudo mkdir -p /home/sol/validators/jito/versions/v2.2.14-jito

# Copy binary with explicit paths
sudo cp /home/sol/builds/jito-solana-v2.2.14-jito/target/release/agave-validator \
    /home/sol/validators/jito/versions/v2.2.14-jito/

# Set correct ownership and permissions
sudo chown -R sol:sol /home/sol/validators/jito/versions/v2.2.14-jito
sudo chmod +x /home/sol/validators/jito/versions/v2.2.14-jito/agave-validator

# Verify the copy was successful
ls -l /home/sol/validators/jito/versions/v2.2.14-jito/agave-validator
```

### 6. Update Symlink
```bash
# As admin user
# Remove existing symlink
sudo rm /home/sol/validators/jito/active

# Create new symlink with explicit paths
sudo ln -sf /home/sol/validators/jito/versions/v2.2.14-jito/agave-validator \
    /home/sol/validators/jito/active

# Verify symlink and version
ls -l /home/sol/validators/jito/active
/home/sol/validators/jito/active --version
```

### 7. Restart Validator Service
```bash
# Stop the validator service
sudo systemctl stop validator.service

# Start the validator service
sudo systemctl start validator.service

# Verify service status
sudo systemctl status validator.service
```

### 8. Monitor Validator
```bash
# Watch the validator logs
tail -f /home/sol/validators/data/log/validator.log

# Check catchup status (in a separate terminal)
solana catchup --url https://api.testnet.solana.com JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF

# Monitor validator performance
/home/sol/validators/jito/active --ledger /home/sol/validators/data/ledger monitor
```

### 9. Verify Upgrade Success
Check the following:
- Validator is processing blocks
- No error messages in logs
- Catchup is complete or in progress
- Vote transactions are being submitted
- Block production is working (if leader slot is assigned)

If any issues are encountered, see the Rollback Procedure below.

## Post-Upgrade Verification

### 1. Check Service Status
```bash
sudo systemctl status validator.service
```

### 2. Monitor Logs
```bash
tail -f /home/sol/validators/data/log/validator.log
```

### 3. Verify Operation
```bash
# Check catchup status
solana catchup --url https://api.testnet.solana.com JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF

# Monitor validator
/home/sol/validators/jito/active --ledger /home/sol/validators/data/ledger monitor
```

### 4. Clean Up Build Directory
```bash
# Return to builds directory
cd ~/builds

# Remove build directory after successful upgrade
rm -rf jito-solana-$JITO_RELEASE_VERSION


## Common Issues

### 1. Symlink Points to Directory
If the symlink points to the version directory instead of the binary:
```bash
# Symptom
/home/sol/validators/jito/active --version
-bash: /home/sol/validators/jito/active: Is a directory

# Fix
sudo rm /home/sol/validators/jito/active
sudo ln -sf /home/sol/validators/jito/versions/v2.2.13-jito/agave-validator /home/sol/validators/jito/active
```

### 2. Permission Issues
If encountering permission issues:
```bash
# Fix ownership
sudo chown -R sol:sol /home/sol/validators/jito

# Fix permissions
sudo chmod +x /home/sol/validators/jito/versions/v2.2.13-jito/agave-validator
```

### 3. Insufficient Disk Space
If encountering disk space issues:
```bash
# Check what's using space
du -h --max-depth=1 ~/builds

# Clean up old builds
cd ~/builds
ls -td jito-solana-v* | tail -n +3 | xargs rm -rf

# Clean up cargo cache if needed
cargo cache --autoclean
```

## Rollback Procedure

If issues are encountered after upgrade:

1. Stop the validator:
```bash
sudo systemctl stop validator.service
```

2. Switch back to previous version:
```bash
sudo rm /home/sol/validators/jito/active
sudo ln -sf /home/sol/validators/jito/versions/v2.2.13-jito/agave-validator /home/sol/validators/jito/active

# Verify rollback version
/home/sol/validators/jito/active --version
```

3. Start the validator:
```bash
sudo systemctl start validator.service
```

4. Monitor logs:
```bash
tail -f /home/sol/validators/data/log/validator.log
```

## Version History

| Version | Date | Notes |
|---------|------|-------|
| v2.2.14 | 2025-05-20 | Current version |
| v2.2.13 | 2025-05-12 | Previous version |
| v2.2.8 | Previous | Previous stable version | 