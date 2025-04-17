# Solana Validator Server Setup Guide

## Table of Contents
1. [Initial Server Setup](#initial-server-setup)
2. [User Management and SSH Security](#user-management-and-ssh-security)
3. [Firewall Configuration with nftables](#firewall-configuration-with-nftables)
4. [Disk Management and Storage Optimization](#disk-management-and-storage-optimization)
5. [System Updates and Optimization](#system-updates-and-optimization)
6. [Service Management](#service-management)
7. [File Structure and Permissions](#file-structure-and-permissions)
8. [Network Configuration](#network-configuration)
9. [Performance Tuning](#performance-tuning)
10. [Security Hardening](#security-hardening)
11. [Backup and Recovery](#backup-and-recovery)

## Initial Server Setup

### Prerequisites
- A fresh Ubuntu 24.04 server installation
- Root or sudo access to the server
- SSH access to the server
- Basic understanding of Linux commands

### Initial Access
1. Connect to your server using SSH:
   ```bash
   ssh user@server-ip
   ```

2. Update the system packages:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. Install essential tools:
   ```bash
   sudo apt install -y curl wget git htop net-tools dnsutils jq tmux vim
   ```

4. Set the hostname (replace `validator` with your preferred hostname):
   ```bash
   sudo hostnamectl set-hostname validator
   ```

5. Configure timezone:
   ```bash
   sudo timedatectl set-timezone UTC
   ```

6. Enable NTP synchronization:
   ```bash
   sudo systemctl enable systemd-timesyncd
   sudo systemctl start systemd-timesyncd
   ```

7. Configure system locale:
   ```bash
   sudo locale-gen en_US.UTF-8
   sudo update-locale LANG=en_US.UTF-8
   ```

8. Create a swap file (if not already present):
   ```bash
   # Check if swap exists
   free -h
   
   # If no swap, create a 32GB swap file
   sudo fallocate -l 32G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   
   # Make swap permanent
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

9. Configure system limits:
   ```bash
   # Edit system limits
   sudo nano /etc/security/limits.conf
   
   # Add these lines at the end
   * soft nofile 65535
   * hard nofile 65535
   * soft nproc 65535
   * hard nproc 65535
   ```

10. Configure kernel parameters:
    ```bash
    # Edit sysctl configuration
    sudo nano /etc/sysctl.conf
    
    # Add these lines at the end
    # Increase system limits
    fs.file-max = 1000000
    fs.nr_open = 1000000
    
    # Network optimization
    net.core.rmem_default = 134217728
    net.core.wmem_default = 134217728
    net.core.rmem_max = 134217728
    net.core.wmem_max = 134217728
    net.ipv4.tcp_rmem = 4096 65536 134217728
    net.ipv4.tcp_wmem = 4096 65536 134217728
    net.ipv4.tcp_mem = 65536 131072 134217728
    net.ipv4.tcp_fin_timeout = 30
    net.ipv4.tcp_keepalive_time = 300
    net.ipv4.tcp_keepalive_intvl = 10
    net.ipv4.tcp_keepalive_probes = 5
    
    # Apply changes
    sudo sysctl -p
    ```

11. Configure automatic security updates:
    ```bash
    sudo apt install -y unattended-upgrades
    sudo dpkg-reconfigure -plow unattended-upgrades
    ```

At this point, you have a basic server setup with essential security measures and optimizations. The next sections will cover user management, SSH security, and more advanced configurations.

## User Management and SSH Security

### Creating Users and Groups

1. Create the primary admin user:
   ```bash
   sudo adduser validator-admin
   sudo usermod -aG sudo validator-admin
   ```

2. Create the Solana validator user (unprivileged):
   ```bash
   sudo adduser sol --disabled-password --gecos ""
   ```

3. Create a backup admin user:
   ```bash
   sudo adduser backup-admin
   sudo usermod -aG sudo backup-admin
   ```

4. Create the node exporter user:
   ```bash
   sudo adduser --system --group --shell /bin/false node_exporter
   sudo usermod -aG video node_exporter
   ```

5. Create a group for SSH access and add users to it:
   ```bash
   sudo groupadd sshusers
   sudo usermod -aG sshusers validator-admin
   sudo usermod -aG sshusers sol
   sudo usermod -aG sshusers backup-admin
   ```

### SSH Key Setup

1. On your local machine (WSL recommended for Windows users), generate SSH keys for each user:
   ```bash
   # For validator-admin
   ssh-keygen -t ed25519 -C "validator-admin@server" -f ~/.ssh/validator-admin
   
   # For sol user
   ssh-keygen -t ed25519 -C "sol@server" -f ~/.ssh/sol
   
   # For backup-admin
   ssh-keygen -t ed25519 -C "backup-admin@server" -f ~/.ssh/backup-admin
   ```

2. Copy the public keys to the server:
   ```bash
   # For validator-admin
   scp ~/.ssh/validator-admin.pub validator-admin@server-ip:/tmp/
   
   # For sol user
   scp ~/.ssh/sol.pub sol@server-ip:/tmp/
   
   # For backup-admin
   scp ~/.ssh/backup-admin.pub backup-admin@server-ip:/tmp/
   ```

3. On the server, set up the authorized_keys files:
   ```bash
   # For validator-admin
   sudo mkdir -p /home/validator-admin/.ssh
   sudo mv /tmp/validator-admin.pub /home/validator-admin/.ssh/authorized_keys
   sudo chown -R validator-admin:validator-admin /home/validator-admin/.ssh
   sudo chmod 700 /home/validator-admin/.ssh
   sudo chmod 600 /home/validator-admin/.ssh/authorized_keys
   
   # For sol user
   sudo mkdir -p /home/sol/.ssh
   sudo mv /tmp/sol.pub /home/sol/.ssh/authorized_keys
   sudo chown -R sol:sol /home/sol/.ssh
   sudo chmod 700 /home/sol/.ssh
   sudo chmod 600 /home/sol/.ssh/authorized_keys
   
   # For backup-admin
   sudo mkdir -p /home/backup-admin/.ssh
   sudo mv /tmp/backup-admin.pub /home/backup-admin/.ssh/authorized_keys
   sudo chown -R backup-admin:backup-admin /home/backup-admin/.ssh
   sudo chmod 700 /home/backup-admin/.ssh
   sudo chmod 600 /home/backup-admin/.ssh/authorized_keys
   ```

### SSH Hardening

1. Create a hardened SSH configuration file:
   ```bash
   sudo nano /etc/ssh/sshd_config.d/99-hardened.conf
   ```

2. Add the following configuration:
   ```
   HostKey /etc/ssh/ssh_host_ed25519_key
   HostKey /etc/ssh/ssh_host_rsa_key
   
   PermitRootLogin no
   AllowGroups sshusers
   StrictModes yes
   PasswordAuthentication no
   PubkeyAuthentication yes
   AuthorizedKeysFile .ssh/authorized_keys
   ChallengeResponseAuthentication no
   X11Forwarding no
   ClientAliveInterval 100
   PerSourceMaxStartups 1
   
   KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,gss-curve25519-sha256-,diffie-hellman-group16-sha512,gss-group16-sha512-,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha256
   
   Ciphers aes256-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-gcm@openssh.com,aes128-ctr
   
   MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com
   
   HostKeyAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256
   
   CASignatureAlgorithms sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256
   
   GSSAPIKexAlgorithms gss-curve25519-sha256-,gss-group16-sha512-
   
   HostbasedAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256
   
   PubkeyAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256
   ```

3. Reload the SSH service:
   ```bash
   sudo systemctl reload ssh
   ```

### Testing SSH Access

1. Test SSH access for each user:
   ```bash
   # For validator-admin
   ssh -i ~/.ssh/validator-admin validator-admin@server-ip
   
   # For sol user
   ssh -i ~/.ssh/sol sol@server-ip
   
   # For backup-admin
   ssh -i ~/.ssh/backup-admin backup-admin@server-ip
   ```

### Securing Private Keys

1. Back up all private keys securely:
   - Copy the contents of each private key file (`~/.ssh/validator-admin`, `~/.ssh/sol`, `~/.ssh/backup-admin`)
   - Store them in:
     - A secure password manager
     - An encrypted USB drive
     - A GPG-encrypted folder
     - External secure storage

2. Run an SSH audit to verify your configuration:
   ```bash
   git clone https://github.com/arthepsy/ssh-audit.git ~/validators/monitoring/ssh-audit
   cd ~/validators/monitoring/ssh-audit
   ./ssh-audit.py server-ip
   ```

### Additional SSH Security Measures

1. Set up SSH key rotation reminders:
   ```bash
   # Create a reminder script
   sudo nano /usr/local/bin/ssh-key-reminder
   ```

2. Add the following content:
   ```bash
   #!/bin/bash
   echo "SSH keys should be rotated every 90 days for security."
   echo "Last rotation: $(date -r ~/.ssh/id_ed25519 +%Y-%m-%d 2>/dev/null || echo 'Unknown')"
   ```

3. Make the script executable:
   ```bash
   sudo chmod +x /usr/local/bin/ssh-key-reminder
   ```

4. Add it to the .bashrc file for each user:
   ```bash
   echo "/usr/local/bin/ssh-key-reminder" >> ~/.bashrc
   ```

At this point, you have a secure SSH setup with proper user management. The next section will cover firewall configuration with nftables.

## Firewall Configuration with nftables

### Initial Setup

1. Clean up existing firewall rules:
   ```bash
   # Disable ufw
   sudo ufw disable || true
   sudo ufw --force reset

   # Set iptables policies to avoid lockout
   sudo iptables --policy INPUT ACCEPT
   sudo iptables --policy FORWARD ACCEPT
   sudo iptables --policy OUTPUT ACCEPT

   # Flush all rules
   sudo iptables --flush
   sudo iptables --delete-chain
   sudo iptables --zero

   # Clean special tables
   sudo iptables --table nat --flush
   sudo iptables --table nat --delete-chain
   sudo iptables --table mangle --flush
   sudo iptables --table mangle --delete-chain
   sudo iptables --table raw --flush
   sudo iptables --table raw --delete-chain
   ```

2. Install and enable nftables:
   ```bash
   sudo apt update
   sudo apt install nftables -y
   sudo systemctl enable --now nftables
   ```

3. Create the nftables configuration:
   ```bash
   sudo nano /etc/nftables.conf
   ```

4. Add the following configuration:
   ```bash
   #!/usr/sbin/nft -f

   flush ruleset

   table inet filter {
     chain input {
       type filter hook input priority filter; policy drop;

       # Allow loopback traffic
       iif lo accept
       
       # Connection tracking
       ct state invalid drop
       ct state established,related accept

       # Solana Network Ports
       udp dport 8000-10000 accept  # TPU UDP
       tcp dport 8000 accept        # Gossip TCP

       # Restricted Access Services
       tcp dport 8899 ip saddr { [home ip] } accept  # RPC
       tcp dport 9100 ip saddr { [home ip] } accept  # Solana Exporter
       tcp dport 9110 ip saddr { [home ip] } accept  # Node Exporter

       # Management Access
       tcp dport 22 ct state new limit rate 12/minute accept  # SSH
       ip protocol icmp icmp type echo-request limit rate 5/second accept  # ICMP

       # Logging
       log prefix "[nftables] DROP: " flags all counter
     }

     chain output {
       type filter hook output priority filter; policy accept;
     }

     chain forward {
       type filter hook forward priority filter; policy drop;
     }
   }
   ```

5. Apply the configuration:
   ```bash
   sudo chmod +x /etc/nftables.conf
   sudo nft -f /etc/nftables.conf
   ```

6. Verify the configuration:
   ```bash
   sudo nft list ruleset
   sudo systemctl status nftables
   ```

### Port Configuration Summary

| Port Range | Protocol | Purpose | Access Control |
|------------|----------|---------|----------------|
| 8000-10000 | UDP | Solana TPU | Open |
| 8000 | TCP | Solana Gossip | Open |
| 8899 | TCP | RPC | Home IP Only |
| 9100 | TCP | Solana Exporter | Home IP Only |
| 9110 | TCP | Node Exporter | Home IP Only |
| 22 | TCP | SSH | Rate Limited |
| ICMP | - | Ping | Rate Limited |

### Security Features

1. Rate Limiting:
   - SSH: 12 connections per minute
   - ICMP: 5 requests per second
   - Prevents brute force attacks

2. Access Control:
   - Default policy: DROP
   - Established connections: ACCEPT
   - Loopback traffic: ACCEPT
   - Home IP ([home ip]) allowed for:
     - RPC access
     - Metrics collection
     - Monitoring

3. Connection Tracking:
   - Invalid connections dropped
   - Established/related connections accepted
   - Prevents connection spoofing

## Disk Management and Storage Optimization

### Initial Disk Setup

1. Identify available disks:
   ```bash
   lsblk
   ```

2. Create partitions for each disk:
   ```bash
   # For system disk (assuming /dev/sda)
   sudo parted /dev/sda mklabel gpt
   sudo parted /dev/sda mkpart primary ext4 1MiB 100%
   
   # For data disk (assuming /dev/sdb)
   sudo parted /dev/sdb mklabel gpt
   sudo parted /dev/sdb mkpart primary ext4 1MiB 100%
   ```

3. Format partitions:
   ```bash
   # Format system partition
   sudo mkfs.ext4 /dev/sda1
   
   # Format data partition
   sudo mkfs.ext4 /dev/sdb1
   ```

4. Create mount points:
   ```bash
   sudo mkdir -p /mnt/data
   ```

5. Update /etc/fstab:
   ```bash
   sudo nano /etc/fstab
   ```
   Add these lines:
   ```
   /dev/sda1  /      ext4  defaults,noatime,discard  0  1
   /dev/sdb1  /mnt/data  ext4  defaults,noatime,discard  0  2
   ```

6. Mount partitions:
   ```bash
   sudo mount -a
   ```

### Performance Optimization

1. Configure I/O scheduler:
   ```bash
   # Set deadline scheduler for better performance
   echo deadline | sudo tee /sys/block/sda/queue/scheduler
   echo deadline | sudo tee /sys/block/sdb/queue/scheduler
   
   # Make changes permanent
   echo 'ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/scheduler}="deadline"' | sudo tee /etc/udev/rules.d/60-scheduler.rules
   ```

2. Optimize filesystem parameters:
   ```bash
   # Edit fstab to add performance options
   sudo nano /etc/fstab
   ```
   Update mount options:
   ```
   /dev/sda1  /      ext4  defaults,noatime,discard,commit=60  0  1
   /dev/sdb1  /mnt/data  ext4  defaults,noatime,discard,commit=60  0  2
   ```

3. Configure read-ahead:
   ```bash
   # Set optimal read-ahead values
   sudo blockdev --setra 16384 /dev/sda
   sudo blockdev --setra 16384 /dev/sdb
   
   # Make changes permanent
   echo 'ACTION=="add|change", KERNEL=="sd[a-z]", RUN+="/sbin/blockdev --setra 16384 %N"' | sudo tee /etc/udev/rules.d/60-readahead.rules
   ```

### Monitoring and Maintenance

1. Install monitoring tools:
   ```bash
   sudo apt install -y iotop sysstat
   ```

2. Set up disk monitoring:
   ```bash
   # Enable sysstat
   sudo systemctl enable sysstat
   sudo systemctl start sysstat
   
   # Configure iostat collection
   sudo nano /etc/default/sysstat
   ```
   Set:
   ```
   ENABLED="true"
   ```

## System Updates and Optimization

### System Updates

1. Configure automatic updates:
   ```bash
   sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
   ```
   Add:
   ```
   Unattended-Upgrade::Allowed-Origins {
       "${distro_id}:${distro_codename}";
       "${distro_id}:${distro_codename}-security";
       "${distro_id}ESMApps:${distro_codename}-apps-security";
   };
   
   Unattended-Upgrade::Package-Blacklist {
   };
   
   Unattended-Upgrade::DevRelease "auto";
   Unattended-Upgrade::Remove-Unused-Dependencies "true";
   Unattended-Upgrade::Automatic-Reboot "false";
   Unattended-Upgrade::Automatic-Reboot-Time "02:00";
   ```

2. Enable automatic updates:
   ```bash
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

### System Optimization

1. Configure system limits:
   ```bash
   sudo nano /etc/security/limits.conf
   ```
   Add:
   ```
   * soft nofile 65535
   * hard nofile 65535
   * soft nproc 65535
   * hard nproc 65535
   ```

2. Optimize kernel parameters:
   ```bash
   sudo nano /etc/sysctl.conf
   ```
   Add:
   ```
   # System limits
   fs.file-max = 1000000
   fs.nr_open = 1000000
   
   # Network optimization
   net.core.rmem_default = 134217728
   net.core.wmem_default = 134217728
   net.core.rmem_max = 134217728
   net.core.wmem_max = 134217728
   net.ipv4.tcp_rmem = 4096 65536 134217728
   net.ipv4.tcp_wmem = 4096 65536 134217728
   net.ipv4.tcp_mem = 65536 131072 134217728
   net.ipv4.tcp_fin_timeout = 30
   net.ipv4.tcp_keepalive_time = 300
   net.ipv4.tcp_keepalive_intvl = 10
   net.ipv4.tcp_keepalive_probes = 5
   ```

3. Apply kernel parameters:
   ```bash
   sudo sysctl -p
   ```

## Service Management

### System Services

1. Disable unnecessary services:
   ```bash
   sudo systemctl disable bluetooth
   sudo systemctl disable cups
   sudo systemctl disable avahi-daemon
   sudo systemctl disable ModemManager
   sudo systemctl disable wpa_supplicant
   ```

2. Configure service limits:
   ```bash
   sudo nano /etc/systemd/system.conf
   ```
   Add:
   ```
   DefaultLimitNOFILE=65535
   DefaultLimitNPROC=65535
   ```

3. Reload systemd:
   ```bash
   sudo systemctl daemon-reload
   ```

### Log Management

1. Configure log rotation:
   ```bash
   sudo nano /etc/logrotate.d/custom
   ```
   Add:
   ```
   /var/log/*.log {
       daily
       rotate 7
       compress
       delaycompress
       missingok
       notifempty
       create 0640 root root
   }
   ```

## File Structure and Permissions

### Directory Structure

1. Create standard directories:
   ```bash
   sudo mkdir -p /opt/applications
   sudo mkdir -p /var/log/applications
   sudo mkdir -p /etc/applications
   ```

2. Set proper permissions:
   ```bash
   sudo chmod 755 /opt/applications
   sudo chmod 755 /var/log/applications
   sudo chmod 755 /etc/applications
   ```

### Security Hardening

1. Configure file permissions:
   ```bash
   sudo find / -type f -perm -4000 -ls
   sudo find / -type f -perm -2000 -ls
   ```

2. Set up audit logging:
   ```bash
   sudo apt install -y auditd
   sudo systemctl enable auditd
   sudo systemctl start auditd
   ```

## Network Configuration

### Network Optimization

1. Configure network parameters:
   ```bash
   sudo nano /etc/sysctl.conf
   ```
   Add:
   ```
   # Network security
   net.ipv4.tcp_syncookies = 1
   net.ipv4.tcp_max_syn_backlog = 2048
   net.ipv4.tcp_synack_retries = 2
   net.ipv4.tcp_syn_retries = 5
   
   # Network performance
   net.core.netdev_max_backlog = 2500
   net.core.somaxconn = 65535
   net.ipv4.tcp_max_tw_buckets = 1440000
   ```

2. Apply network settings:
   ```bash
   sudo sysctl -p
   ```

## Performance Tuning

### System Tuning

1. Install performance tools:
   ```bash
   sudo apt install -y sysstat iotop htop
   ```

2. Configure performance monitoring:
   ```bash
   sudo nano /etc/default/sysstat
   ```
   Set:
   ```
   ENABLED="true"
   ```

## Security Hardening

### System Security

1. Install security tools:
   ```bash
   sudo apt install -y rkhunter lynis
   ```

2. Run security audit:
   ```bash
   sudo lynis audit system
   sudo rkhunter --update
   sudo rkhunter --propupd
   sudo rkhunter --check
   ```

## Backup and Recovery

### Backup Configuration

1. Create backup directories:
   ```bash
   sudo mkdir -p /backup/system
   sudo mkdir -p /backup/config
   ```

2. Create backup script:
   ```bash
   sudo nano /usr/local/bin/system-backup
   ```
   Add:
   ```bash
   #!/bin/bash
   
   # Set backup date
   BACKUP_DATE=$(date +%Y%m%d)
   
   # Backup system configurations
   tar -czf /backup/config/config_${BACKUP_DATE}.tar.gz /etc/
   
   # Backup user configurations
   tar -czf /backup/config/home_${BACKUP_DATE}.tar.gz /home/
   
   # Backup system logs
   tar -czf /backup/system/logs_${BACKUP_DATE}.tar.gz /var/log/
   
   # Clean old backups (keep last 7 days)
   find /backup -type f -mtime +7 -delete
   ```

3. Make backup script executable:
   ```bash
   sudo chmod +x /usr/local/bin/system-backup
   ```

4. Add to crontab:
   ```bash
   sudo crontab -e
   ```
   Add:
   ```
   0 2 * * * /usr/local/bin/system-backup
   ```

At this point, you have a fully configured and optimized Linux system ready for the next phase of setup. The system includes:
- Secure user management
- Hardened SSH configuration
- Optimized firewall
- Efficient disk management
- System performance tuning
- Security hardening
- Automated backups
- Monitoring tools

The next steps would involve installing and configuring the specific applications needed for your use case.