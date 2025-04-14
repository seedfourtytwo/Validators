# Users and Groups Configuration

## Overview
This document describes the important users and groups in the Solana validator system, focusing on custom users and those with significant roles.

## System Users

### Root User
- **Username**: root
- **UID**: 0
- **Shell**: /bin/bash
- **Purpose**: Superuser account with full system access
- **Security Note**: Direct root login is disabled via SSH

### Service Users

#### System Services
- **systemd-network** (UID: 998)
  - Purpose: Manages network configuration
  - Shell: /usr/sbin/nologin
- **systemd-timesync** (UID: 997)
  - Purpose: Handles system time synchronization
  - Shell: /usr/sbin/nologin
- **systemd-resolve** (UID: 992)
  - Purpose: Manages DNS resolution
  - Shell: /usr/sbin/nologin

#### Application Services
- **www-data** (UID: 33)
  - Purpose: Web server user
  - Shell: /usr/sbin/nologin
- **sshd** (UID: 109)
  - Purpose: SSH daemon service
  - Shell: /usr/sbin/nologin

## Custom Users

### Administrative Users
- **validator-admin** (UID: 1001)
  - Groups: validator-admin, sudo, users, sshusers
  - Purpose: Primary administrative user
  - Shell: /bin/bash
  - Capabilities: Full sudo access, SSH access
  - Services: Manages validator configuration and monitoring
  - Note: Primary account for system administration and validator management

- **backup-admin** (UID: 1004)
  - Groups: backup-admin, sudo, users, sshusers
  - Purpose: Backup administration
  - Shell: /bin/bash
  - Capabilities: Sudo access, SSH access
  - Note: Secondary administrative account for redundancy

### Service Users
- **sol** (UID: 1002)
  - Groups: sol, users, sshusers
  - Purpose: Runs the Solana validator
  - Shell: /bin/bash
  - Services: 
    - Solana validator
    - Validator monitoring

- **node_exporter** (UID: 1005)
  - Groups: node_exporter, video
  - Purpose: Runs Prometheus node exporter
  - Shell: /bin/false
  - Services:
    - System metrics collection
    - Hardware monitoring

## Important Groups

### Security Groups
- **sudo** (GID: 27)
  - Purpose: Administrative privileges
  - Members: validator-admin, backup-admin

- **sshusers** (GID: 1003)
  - Purpose: SSH access control
  - Members: validator-admin, sol, backup-admin

### Service Groups
- **users** (GID: 100)
  - Purpose: Standard user access
  - Members: validator-admin, sol, backup-admin

- **video** (GID: 44)
  - Purpose: Video device access
  - Members: node_exporter

### Application Groups
- **validator-admin** (GID: 1001)
  - Purpose: Validator administration
  - Members: validator-admin

- **sol** (GID: 1002)
  - Purpose: Solana validator management
  - Members: sol

- **backup-admin** (GID: 1004)
  - Purpose: Backup administration
  - Members: backup-admin

- **node_exporter** (GID: 1005)
  - Purpose: Node exporter service
  - Members: node_exporter

## Security Considerations

### User Access Control
1. **SSH Access**
   - Restricted to sshusers group
   - Password authentication disabled
   - Root login disabled

2. **Sudo Access**
   - Limited to trusted administrative users
   - Requires password for sudo commands

3. **Service Accounts**
   - Most service accounts use /usr/sbin/nologin or /bin/false
   - Limited shell access for security

### Adding New Users
```bash
# Create new user
sudo useradd -m -s /bin/bash username

# Add to necessary groups
sudo usermod -a -G group1,group2 username

# Set password
sudo passwd username
```

### Removing Users
```bash
# Remove user and home directory
sudo userdel -r username

# Remove from groups
sudo usermod -G "" username
```

### Group Management
```bash
# Create new group
sudo groupadd groupname

# Add user to group
sudo usermod -a -G groupname username

# Remove user from group
sudo gpasswd -d username groupname
```