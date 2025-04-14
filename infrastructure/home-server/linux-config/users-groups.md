# Users and Groups Configuration

## Overview
This document describes the important users and groups in the home server system, focusing on custom users and those with significant roles.

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
- **postfix** (UID: 112)
  - Purpose: Mail server service
  - Shell: /usr/sbin/nologin
- **glances** (UID: 110)
  - Purpose: System monitoring service
  - Shell: /usr/sbin/nologin

## Custom Users

### Administrative Users
- **chris** (UID: 1000)
  - Groups: chris, adm, cdrom, sudo, dip, plugdev, lxd, docker, sshusers
  - Purpose: Primary administrative user
  - Shell: /bin/bash
  - Capabilities: Full sudo access, Docker access, SSH access
  - Services: Currently manages Grafana and Prometheus
  - Note: Consider creating dedicated monitoring users (e.g., grafana, prometheus) for better service isolation

- **backupadmin** (UID: 1001)
  - Groups: backupadmin, sudo, users, sshusers
  - Purpose: Backup administration
  - Shell: /bin/bash
  - Capabilities: Sudo access, SSH access

### Service Users
- **telegram_bot** (UID: 1002)
  - Groups: telegram_bot, users
  - Purpose: Runs Telegram bot service
  - Shell: /bin/bash

- **bitcoin** (UID: 1004)
  - Groups: bitcoin, users, systemd-journal
  - Purpose: Runs Bitcoin node and collector services
  - Shell: /bin/bash
  - Services: 
    - Bitcoin Core node
    - Bitcoin metrics collector

- **prysm** (UID: 111)
  - Groups: prysm
  - Purpose: Runs Prysm Ethereum client
  - Shell: /usr/sbin/nologin

## Important Groups

### Security Groups
- **sudo** (GID: 27)
  - Purpose: Administrative privileges
  - Members: chris, backupadmin

- **sshusers** (GID: 1003)
  - Purpose: SSH access control
  - Members: chris, backupadmin

### Service Groups
- **docker** (GID: 988)
  - Purpose: Docker container management
  - Members: chris

- **systemd-journal** (GID: 999)
  - Purpose: System logging access
  - Members: bitcoin

### Application Groups
- **bitcoin** (GID: 1004)
  - Purpose: Bitcoin node management
  - Members: bitcoin

- **prysm** (GID: 111)
  - Purpose: Prysm client management
  - Members: prysm

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
   - Most service accounts use /usr/sbin/nologin
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

## Future Considerations
1. **Service Separation**
   - Create dedicated users for monitoring services:
     - grafana (Grafana service)
     - prometheus (Prometheus service)
   - Create dedicated users for collection services:
     - bitcoin-collector (Bitcoin metrics collection)
     - prysm-collector (Prysm metrics collection)
   - Benefits:
     - Better security isolation
     - Easier permission management
     - Clearer service ownership
     - Simplified troubleshooting