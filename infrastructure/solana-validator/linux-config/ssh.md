# SSH Configuration

## Overview
This document describes the hardened SSH configuration for the Solana validator. The configuration focuses on security best practices and is specifically tuned for validator operations.

## Configuration File
- Location: `/etc/ssh/sshd_config.d/99-hardened.conf`
- Purpose: Additional SSH security settings
- Note: This file complements the main sshd_config file

## Complete Configuration
Here's the exact configuration file that should be placed at `/etc/ssh/sshd_config.d/99-hardened.conf`:

```bash
# Host keys
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# Access control
PermitRootLogin no
AllowGroups sshusers
StrictModes yes

# Authentication
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
ChallengeResponseAuthentication no

# Session control
X11Forwarding no
ClientAliveInterval 100
PerSourceMaxStartups 1

# Cryptographic Hardening
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,gss-curve25519-sha256-,diffie-hellman-group16-sha512,gss-group16-sha512-,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha256
Ciphers aes256-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-gcm@openssh.com,aes128-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com
HostKeyAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256
CASignatureAlgorithms sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256
GSSAPIKexAlgorithms gss-curve25519-sha256-,gss-group16-sha512-
HostbasedAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256
PubkeyAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256
```

## Configuration Explanation

### Host Keys
- Uses both ED25519 and RSA host keys for maximum compatibility
- ED25519 provides better security and performance
- RSA is included for legacy support

### Access Control
- Root login is disabled for security
- Access is restricted to users in the `sshusers` group
- StrictModes ensures proper file permissions

### Authentication
- Password authentication is disabled
- Only public key authentication is allowed
- Challenge-response authentication is disabled

### Session Control
- X11 forwarding is disabled
- Connection timeout is set to 100 seconds
- Connection attempts are limited to prevent brute force attacks

### Cryptographic Hardening
- Uses modern, secure key exchange algorithms
- Implements strong encryption ciphers
- Uses secure message authentication codes
- Supports modern host key algorithms
- Implements secure signature algorithms

## Complete Setup Guide

### 1. Server Preparation
```bash
# Create sshusers group if it doesn't exist
sudo groupadd sshusers

# Add validator user to the group
sudo usermod -a -G sshusers validator-admin

# Create .ssh directory with correct permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

### 2. Client-Side Setup

#### Windows (Using PowerShell)
```powershell
# Install OpenSSH if not already installed
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Generate ED25519 key (recommended)
ssh-keygen -t ed25519 -C "validator-admin"

# Or generate RSA key (if needed)
ssh-keygen -t rsa -b 4096 -C "validator-admin"

# Keys will be saved to:
# %USERPROFILE%\.ssh\id_ed25519 (private key)
# %USERPROFILE%\.ssh\id_ed25519.pub (public key)
```

#### Linux/macOS
```bash
# Generate ED25519 key (recommended)
ssh-keygen -t ed25519 -C "validator-admin"

# Or generate RSA key (if needed)
ssh-keygen -t rsa -b 4096 -C "validator-admin"

# Keys will be saved to:
# ~/.ssh/id_ed25519 (private key)
# ~/.ssh/id_ed25519.pub (public key)
```

### 3. Key Transfer

#### Windows (Using PowerShell)
```powershell
# Copy public key to validator
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh validator-admin@validator "cat >> ~/.ssh/authorized_keys"
```

#### Linux/macOS
```bash
# Copy public key to validator
ssh-copy-id validator-admin@validator
# Or manually:
cat ~/.ssh/id_ed25519.pub | ssh validator-admin@validator "cat >> ~/.ssh/authorized_keys"
```

### 4. Server-Side Key Setup
```bash
# Set correct permissions for authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Verify the key was added correctly
cat ~/.ssh/authorized_keys
```

### 5. Testing Connection
```bash
# Test SSH connection
ssh validator-admin@validator

# If successful, you should connect without a password prompt
```

### 6. Backup Procedures

#### Client-Side Backup (Windows)
```powershell
# Create backup directory
New-Item -ItemType Directory -Path "$env:USERPROFILE\ssh_backup" -Force

# Copy SSH keys
Copy-Item "$env:USERPROFILE\.ssh\*" "$env:USERPROFILE\ssh_backup\"

# Export registry settings (if using Pageant or similar)
reg export "HKEY_CURRENT_USER\Software\SimonTatham\PuTTY" "$env:USERPROFILE\ssh_backup\putty_settings.reg"
```

#### Client-Side Backup (Linux/macOS)
```bash
# Create backup directory
mkdir -p ~/ssh_backup

# Copy SSH keys
cp -r ~/.ssh/* ~/ssh_backup/

# Create archive with timestamp
tar -czf ~/ssh_backup_$(date +%Y%m%d).tar.gz ~/ssh_backup/
```

#### Server-Side Backup
```bash
# Backup SSH configuration
sudo cp /etc/ssh/sshd_config.d/99-hardened.conf /etc/ssh/sshd_config.d/99-hardened.conf.backup

# Backup authorized keys
cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup

# Create full SSH backup with timestamp
sudo tar -czf /root/ssh_backup_$(date +%Y%m%d).tar.gz /etc/ssh/ ~/.ssh/
```

### 7. Key Rotation (Every 6-12 months)
```bash
# Generate new key pair
ssh-keygen -t ed25519 -C "validator-admin"

# Copy new public key to validator
ssh-copy-id validator-admin@validator

# Test new key
ssh validator-admin@validator

# Once confirmed working, remove old key from validator
ssh validator-admin@validator "sed -i '/old_key_comment/d' ~/.ssh/authorized_keys"
```

## Security Audit
After applying these settings, it's recommended to audit the SSH configuration using:
```bash
# Install ssh-audit
git clone https://github.com/jtesta/ssh-audit.git
cd ssh-audit
./ssh-audit.py validator
```
