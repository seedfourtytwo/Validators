# Firewall Configuration

## Overview
This document describes the nftables firewall configuration for the home server, which provides network security and access control for various services.

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

## Configuration File
- Location: `/etc/nftables.conf`
- Type: nftables ruleset
- Default Policy: Drop for input/forward, Accept for output

## Firewall Rules

### Input Chain Rules
1. **Solana Exporter Log WebSocket**
   - Port: 8081 (TCP)
   - Allowed Sources:
     - LAN: 192.168.1.0/24
     - OVH Web Server: 188.165.53.185
     - Home Public IP: Home IP
   - Rules:
     ```bash
     ip saddr 192.168.1.0/24 tcp dport 8081 accept
     ip saddr 188.165.53.185 tcp dport 8081 accept
     ip saddr Home IP tcp dport 8081 accept
     ```

2. **Loopback Interface**
   - Accept all traffic on loopback interface
   - Rule: `iif lo accept`

3. **Connection State**
   - Drop invalid connections
   - Accept established and related connections
   - Rules:
     ```bash
     ct state invalid drop
     ct state established,related accept
     ```

4. **SSH Access**
   - Source: LAN (192.168.1.0/24)
   - Port: 22 (TCP)
   - Rate Limit: 12 connections per minute
   - Rule: `ip saddr 192.168.1.0/24 tcp dport 22 ct state new limit rate 12/minute accept`

5. **Web Services**
   - Grafana (Internal): Port 3000
   - HTTP (NGINX): Port 80
   - HTTPS (NGINX): Port 443
   - Rules:
     ```bash
     tcp dport 3000 accept
     tcp dport 80 accept
     tcp dport 443 accept
     ```

6. **Monitoring**
   - Prometheus: Port 9090
   - Source: LAN only (192.168.1.0/24)
   - Interface: enp3s0
   - Rule: `iifname "enp3s0" ip saddr 192.168.1.0/24 tcp dport 9090 accept`

7. **Blockchain Nodes**
   - Ethereum Node:
     - P2P TCP: Port 30303
     - P2P UDP: Port 30303
   - Bitcoin Node:
     - P2P TCP: Port 8333
   - Rules:
     ```bash
     tcp dport 30303 accept
     udp dport 30303 accept
     tcp dport 8333 accept
     ```

8. **ICMP (Ping)**
   - Rate Limited: 5 pings per second
   - Rule: `ip protocol icmp icmp type echo-request limit rate 5/second accept`

9. **Logging**
   - Log all dropped packets
   - Prefix: "[nftables] DROP: "
   - Rule: `log prefix "[nftables] DROP: " flags all counter`

### Output Chain
- Default Policy: Accept
- No specific rules defined

### Forward Chain
- Default Policy: Drop
- No specific rules defined

## Security Considerations
1. Default deny policy for incoming traffic
2. Rate limiting on SSH and ICMP
3. LAN-only access for sensitive services (Prometheus)
4. Logging of dropped packets for security monitoring
5. Explicit allow rules for required services
6. Restricted access to Solana Exporter Log WebSocket (port 8081) to trusted IPs only

## Complete Configuration File
```bash
#!/usr/sbin/nft -f

flush ruleset

############################################
# FILTER TABLE (Main Firewall Policy)
############################################

table inet filter {
  chain input {
    type filter hook input priority filter; policy drop;

    # Home server solana exporter logs websocket
    ip saddr 192.168.1.0/24 tcp dport 8081 accept
    ip saddr 188.165.53.185 tcp dport 8081 accept
    ip saddr Home IP tcp dport 8081 accept

    # Loopback and established connections
    iif lo accept
    ct state invalid drop
    ct state established,related accept

    # SSH from LAN (rate limited)
    ip saddr 192.168.1.0/24 tcp dport 22 ct state new limit rate 12/minute accept

    # Grafana internal and reverse proxy ports
    tcp dport 3000 accept        # internal (localhost)
    tcp dport 80 accept          # HTTP (NGINX)
    tcp dport 443 accept         # HTTPS (NGINX)

    # Prometheus from LAN only
    iifname "enp3s0" ip saddr 192.168.1.0/24 tcp dport 9090 accept

    # Ethereum node P2P traffic
    tcp dport 30303 accept
    udp dport 30303 accept

    #Bitcoin full node port
    tcp dport 8333 accept

    # ICMP Ping (rate limited)
    ip protocol icmp icmp type echo-request limit rate 5/second accept

    # Log dropped packets for debugging
    log prefix "[nftables] DROP: " flags all counter
  }

  chain output {
    type filter hook output priority filter; policy accept;
  }

  chain forward {
    type filter hook forward priority filter; policy drop;
  }
}