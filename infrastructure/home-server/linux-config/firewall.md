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
    # Accept loopback and established connections
    iif lo accept
    ct state invalid drop
    ct state established,related accept
    # SSH from LAN or specific IP
    ip saddr 192.168.1.0/24 tcp dport 22 ct state new limit rate 12/minute accept
    # Grafana
    tcp dport 3000 accept
    # Prometheus
    tcp dport 9090 accept
    # Ethereum P2P (TCP and UDP)
    tcp dport 30303 accept
    udp dport 30303 accept
    # Optional: ICMP for ping
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
