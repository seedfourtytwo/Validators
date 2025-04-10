Firewal - NFTTABLES
Setup script to remove ufw and iptables:
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

Configuration
/etc/nftables.conf
#!/usr/sbin/nft -f
flush ruleset
table inet filter {
  chain input {
    type filter hook input priority filter; policy drop;
    iif lo accept
    ct state invalid drop
    ct state established,related accept
    # Solana TPU UDP
    udp dport 8000-10000 accept
    # Solana Gossip TCP
    tcp dport 8000 accept
    # RPC access (from home IP)
    tcp dport 8899 ip saddr { 77.200.151.32 } accept
    # Solana Exporter
    tcp dport 9100 ip saddr { 77.200.151.32 } accept
    # Node Exporter
    tcp dport 9110 ip saddr { 77.200.151.32 } accept
    # SSH access (rate limited)
    tcp dport 22 ct state new limit rate 12/minute accept
    # ICMP Ping
    ip protocol icmp icmp type echo-request limit rate 5/second accept
    log prefix "[nftables] DROP: " flags all counter
  }
  chain output {
    type filter hook output priority filter; policy accept;
  }
  chain forward {
    type filter hook forward priority filter; policy drop;
  }
}

To reload after changes:
sudo nft -f /etc/nftables.conf