# Solana Validator Cold Key Generation Guide

## Table of Contents
- [Critical Security Warnings](#critical-security-warnings)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Downloads](#software-downloads)
  - [Security Checklist](#security-checklist)
- [Key Generation Process](#key-generation-process)
  - [Environment Setup](#environment-setup)
  - [Binary Verification](#binary-verification)
  - [Key Generation](#key-generation)
  - [Backup and Verification](#backup-and-verification)
  - [Clean Up](#clean-up)
- [Key Management](#key-management)
  - [Storage Requirements](#storage-requirements)
  - [Usage Guidelines](#usage-guidelines)
  - [Recovery Procedures](#recovery-procedures)
- [Security Considerations](#security-considerations)
- [Incident Response](#incident-response)

## Critical Security Warnings
⚠️ **READ BEFORE PROCEEDING**:
- Never generate validator keys on an internet-connected machine
- Never store private keys or seed phrases in digital format (no photos, no digital backups)
- Never share seed phrases or private keys with anyone, including Solana support
- Loss of keys means permanent loss of access to validator rewards
- Compromise of keys could result in loss of all staked funds

## Overview
This guide outlines the secure process for generating and managing Solana validator keys using an air-gapped system, ensuring private keys are never exposed to an internet-connected environment.

## Prerequisites

### Hardware Requirements
- Dedicated offline PC for key generation
- 2x USB drives:
  - USB Drive 1: For bootable Linux installation
  - USB Drive 2: For transferring public keys
- Cold storage solution (encrypted USB drive or hardware security module)
- Paper for seed phrase backup
- Optional: Metal backup tool (e.g., Cryptosteel, Billfodl)

### Software Downloads
- Ubuntu Desktop 22.04.3 LTS:
  - Download: https://ubuntu.com/download/desktop
  - SHA256 checksum: https://ubuntu.com/download/desktop/thank-you?version=22.04.3&architecture=amd64

- Solana CLI tools:
  - Download page: https://docs.solana.com/cli/install-solana-cli-tools
  - Latest release: https://github.com/solana-labs/solana/releases/latest
  - Binaries by OS:
    - Linux: solana-release-x86_64-unknown-linux-gnu.tar.bz2
    - macOS: solana-release-x86_64-apple-darwin.tar.bz2
    - Windows: solana-release-x86_64-pc-windows-msvc.tar.bz2

- USB writing software:
  - Windows: https://rufus.ie/
  - Cross-platform: https://www.balena.io/etcher/

### Security Checklist
1. **Hardware Security**:
   - [ ] Dedicated PC has never been connected to internet
   - [ ] No wireless/bluetooth devices present
   - [ ] No network cables connected
   - [ ] USB ports are clean

2. **Physical Security**:
   - [ ] Private location with no cameras
   - [ ] No unauthorized persons present
   - [ ] Windows covered
   - [ ] Phone cameras covered

3. **Storage Preparation**:
   - [ ] Cold storage devices are new/wiped
   - [ ] Backup materials ready
   - [ ] Multiple secure storage locations prepared

## Key Generation Process

### Environment Setup

1. **Prepare Boot Media**:
   - On an internet-connected computer:
     ```bash
     # Download and verify Ubuntu ISO as described above
     # Use Rufus or BalenaEtcher to create bootable USB (USB1)
     ```
   - Copy Solana binary to second USB drive (USB2):
     - Download appropriate Solana release
     - Verify checksum
     - Copy to USB2

2. **Boot to Live Ubuntu**:
   - Connect USB1 (Ubuntu) to air-gapped PC
   - Power on PC and enter boot menu:
     - Usually F12, F2, or DEL key during startup
     - Select USB boot option
   - Select "Try Ubuntu without installing"
   - Wait for Ubuntu desktop to load

3. **Verify Air-Gap**:
   ```bash
   # Verify no network interfaces are active
   nmcli device status
   # Should show all devices as 'disconnected' or 'unavailable'
   
   # Disable wireless and bluetooth
   rfkill block all
   
   # Verify block
   rfkill list
   # Should show all wireless/bluetooth as 'blocked'
   ```

4. **Mount and Install Solana Tools**:
   ```bash
   # Create working directory
   mkdir -p ~/validator-keys
   cd ~/validator-keys
   
   # Mount USB2 (replace sdX1 with actual device, find with 'lsblk')
   sudo mkdir -p /mnt/usb
   sudo mount /dev/sdX1 /mnt/usb
   
   # Copy Solana binary
   cp /mnt/usb/solana-release-*.tar.bz2 .
   
   # Extract Solana tools
   tar -xjf solana-release-*.tar.bz2
   
   # Add to path
   export PATH="$HOME/validator-keys/solana-release/bin:$PATH"
   
   # Verify installation
   solana --version
   solana-keygen --version
   ```

5. **Prepare Key Generation Environment**:
   ```bash
   # Create directories for keys and public keys
   mkdir -p ~/validator-keys/keypairs
   mkdir -p ~/validator-keys/pubkeys
   
   # Set restrictive permissions
   chmod 700 ~/validator-keys/keypairs
   ```

### Binary Verification
1. Verify Ubuntu ISO:
   ```bash
   wget -q https://ubuntu.com/gpg-key -O ubuntu.gpg
   gpg --verify SHA256SUMS.gpg SHA256SUMS
   sha256sum -c SHA256SUMS 2>&1 | grep OK
   ```

2. Verify Solana binary:
   ```bash
   curl -sSfL https://raw.githubusercontent.com/solana-labs/solana/master/install/solana-release-x86_64-unknown-linux-gnu.yml | shasum -a 256
   ```

### Key Generation
Generate three keypairs:

1. **Identity Keypair**:
   ```bash
   solana-keygen new --outfile identity-keypair.json
   ```

2. **Vote Account Keypair**:
   ```bash
   solana-keygen new --outfile vote-account-keypair.json
   ```

3. **Withdrawer Keypair**:
   ```bash
   solana-keygen new --outfile withdrawer-keypair.json
   ```

### Backup and Verification
1. Record seed phrases on paper
2. Verify each backup:
   ```bash
   solana-keygen verify <SEED_PHRASE> <KEYPAIR_FILE>
   ```
3. Extract public keys:
   ```bash
   solana-keygen pubkey identity-keypair.json > identity-pubkey.txt
   solana-keygen pubkey vote-account-keypair.json > vote-pubkey.txt
   solana-keygen pubkey withdrawer-keypair.json > withdrawer-pubkey.txt
   ```

### Clean Up
1. Reboot to clear RAM
2. Verify no key material remains:
   ```bash
   find / -type f -exec grep -l "PRIVATE KEY" {} \;
   find / -name "*keypair*" 2>/dev/null
   ```

## Key Management

### Storage Requirements
- **Identity Keypair**: Required on validator
- **Vote Account Keypair**: Cold storage after account creation
- **Withdrawer Keypair**: Cold storage only

### Usage Guidelines
1. **Initial Setup**:
   ```bash
   solana create-vote-account vote-account-keypair.json identity-keypair.json withdrawer-pubkey.txt
   solana config set --vote-account <VOTE_PUBKEY>
   ```

2. **Regular Operation**:
   - Identity keypair for validator operation
   - Vote account public key in config
   - Other keys remain in cold storage

### Recovery Procedures
- Regular backup verification
- Test recovery procedures
- Document recovery steps
- Store recovery instructions separately from keys

## Security Considerations
- Use tamper-evident storage
- Monitor vote account activity
- Verify recipient addresses multiple times
- Use offline system for withdrawals
- Document all key operations
- Regular recovery testing

## Incident Response
1. **On Suspected Compromise**:
   - Secure remaining keys
   - Create new keypairs
   - Transfer stake to new vote account
   - Document incident

2. **Recovery Steps**:
   - Update validator identity
   - Communicate with delegators
   - Review and improve procedures


