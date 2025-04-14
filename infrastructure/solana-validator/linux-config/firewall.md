# 🛡️ Firewall Configuration

## Overview
My validator uses nftables for firewall management, providing robust network security with rate limiting and specific access controls for different services.

## Initial Setup
Before applying the nftables configuration, we need to clean up any existing firewall rules. Here's the setup script:

```bash
#!/bin/bash
set -e          # Exit on errors
set -x          # Print commands on screen

# Disable ufw
sudo ufw disable || true
sudo ufw --force reset

# Set policy: Accept all traffic (avoids ssh lockout)
sudo iptables --policy INPUT ACCEPT
sudo iptables --policy FORWARD ACCEPT
sudo iptables --policy OUTPUT ACCEPT

# Flush all rules
sudo iptables --flush

# Delete all chains
sudo iptables --delete-chain

# Reset all counters
sudo iptables --zero

# Flush and delete nat, mangle and raw tables
sudo iptables --table nat --flush
sudo iptables --table nat --delete-chain
sudo iptables --table mangle --flush
sudo iptables --table mangle --delete-chain
sudo iptables --table raw --flush
sudo iptables --table raw --delete-chain
```

Save this script as `reset-firewall.sh` and run it before applying the nftables configuration. This ensures a clean slate for the new firewall rules.

## Current Configuration
Location: `/etc/nftables.conf`

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
    tcp dport 8899 ip saddr { 77.200.151.32 } accept  # RPC
    tcp dport 9100 ip saddr { 77.200.151.32 } accept  # Solana Exporter
    tcp dport 9110 ip saddr { 77.200.151.32 } accept  # Node Exporter

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

## Port Configuration

| Port Range | Protocol | Purpose | Access Control |
|------------|----------|---------|----------------|
| 8000-10000 | UDP | Solana TPU | Open |
| 8000 | TCP | Solana Gossip | Open |
| 8899 | TCP | RPC | Home IP Only |
| 9100 | TCP | Solana Exporter | Home IP Only |
| 9110 | TCP | Node Exporter | Home IP Only |
| 22 | TCP | SSH | Rate Limited |
| ICMP | - | Ping | Rate Limited |

## Security Features

### Rate Limiting
- SSH: 12 connections per minute
- ICMP: 5 requests per second
- Helps prevent brute force attacks

### Access Control
- Default policy: DROP
- Established connections: ACCEPT
- Loopback traffic: ACCEPT
- Home IP (77.200.151.32) allowed for:
  - RPC access
  - Metrics collection
  - Monitoring

### Connection Tracking
- Invalid connections dropped
- Established/related connections accepted
- Helps prevent connection spoofing

## Installation Steps

1. **Prepare System**
   ```bash
   # Save the reset script
   sudo nano reset-firewall.sh
   # Make it executable
   sudo chmod +x reset-firewall.sh
   # Run the reset script
   sudo ./reset-firewall.sh
   ```

2. **Install nftables**
   ```bash
   # Install nftables if not already installed
   sudo apt update
   sudo apt install nftables
   ```

3. **Configure Firewall**
   ```bash
   # Create nftables configuration
   sudo nano /etc/nftables.conf
   # Make it executable
   sudo chmod +x /etc/nftables.conf
   # Apply configuration
   sudo nft -f /etc/nftables.conf
   ```

4. **Verify Installation**
   ```bash
   # Check if nftables is running
   sudo systemctl status nftables
   # List current rules
   sudo nft list ruleset
   ```

## Maintenance

### Reloading Rules
```bash
# After making changes to /etc/nftables.conf
sudo nft -f /etc/nftables.conf
```

### Monitoring
```bash
# View current rules
sudo nft list ruleset

# Monitor dropped packets
sudo nft list ruleset | grep counter
```