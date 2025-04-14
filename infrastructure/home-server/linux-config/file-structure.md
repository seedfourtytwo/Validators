# File Structure Configuration

## Overview
This document describes the key directories and configuration files on the home server, organized by their purpose and location.

## Mount Points and Data Directories

| Path                    | Type      | Purpose                                    | Mount Device   |
|------------------------|-----------|--------------------------------------------|-----------------|
| /mnt/ethereum-testnet  | Directory | Ethereum Testnet Node Data                 | /dev/sda1       |
| /mnt/bitcoin-node      | Directory | Bitcoin Node Data                          | /dev/sdb1       |
| /mnt/archive           | Directory | Archive Storage & AVS Data                 | /dev/sdb2       |
| /mnt/eigenlayer        | Directory | EigenLayer Data & Configurations           | /dev/nvme0n1p1  |
| /                      | Directory | Root Filesystem                            | /dev/nvme1n1p2  |
| /boot/efi              | Directory | EFI Boot Partition                         | /dev/nvme1n1p1  |

## Configuration Files

| Path                    | Type        | Purpose                                   |
|------------------------|-------------|--------------------------------------------|
| /etc/fstab             | Config File | Disk Mount Configuration                   |
| /etc/nftables.conf     | Config File | Firewall Rules                             |
| /etc/ssh/sshd_config   | Config File | SSH Server Configuration                   |
| /etc/docker/daemon.json| Config File | Docker Daemon Configuration                |
| /etc/prometheus/       | Directory   | Prometheus Configuration                   |
| /etc/grafana/          | Directory   | Grafana Configuration                      |

## Service Directories

| Path                    | Type      | Purpose                                    |
|------------------------|-----------|--------------------------------------------|
| /var/lib/docker        | Directory | Docker Containers & Images                 |
| /opt/bitcoin           | Directory | Bitcoin Node Configuration                 |
| /opt/ethereum          | Directory | Ethereum Node Configuration                |
| /opt/eigenlayer        | Directory | EigenLayer Configuration                   |

## Log Directories

| Path                    | Type      | Purpose                                    |
|------------------------|-----------|--------------------------------------------|
| /var/log/              | Directory | System Logs                                |
| /var/log/docker/       | Directory | Docker Container Logs                      |
| /var/log/bitcoin/      | Directory | Bitcoin Node Logs                          |
| /var/log/ethereum/     | Directory | Ethereum Node Logs                         |

