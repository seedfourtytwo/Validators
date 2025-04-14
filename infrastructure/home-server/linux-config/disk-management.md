# Disk Management Configuration

## Overview
This document describes the disk layout and storage configuration for the home server, optimized for running blockchain nodes and validation services.

## Disk Layout

| Device   | Partition | Size      | Mount Point           | Type  | Purpose                |
|----------|-----------|-----------|----------------------|-------|------------------------|
| sda      | sda1      | 10.9T     | /mnt/ethereum-testnet| ext4  | Ethereum Testnet Data  |
| sdb      | sdb1      | 5T        | /mnt/bitcoin-node    | ext4  | Bitcoin Node Data      |
|          | sdb2      | 5.9T      | /mnt/archive        | ext4  | Archive Storage        |
| nvme0n1  | nvme0n1p1 | 931.5G    | /mnt/eigenlayer     | ext4  | EigenLayer Data        |
| nvme1n1  | nvme1n1p1 | 1G        | /boot/efi           | vfat  | EFI Boot              |
|          | nvme1n1p2 | 464.7G    | /                   | ext4  | Root OS               |

## Mount Configuration
The following entries are configured in `/etc/fstab`:

```bash
# Root filesystem
/dev/disk/by-uuid/3e5d93c5-5fd9-49e5-a45f-4111e45d4797 / ext4 defaults 0 1

# EFI Boot partition
/dev/disk/by-uuid/42D4-6143 /boot/efi vfat defaults 0 1

# Swap file
/swap.img none swap sw 0 0

# Ethereum Testnet Node Data
UUID=42a0f296-06bf-4531-818c-acaed4bdb772 /mnt/ethereum-testnet ext4 defaults,noatime,nodiratime 0 2

# EigenLayer Operator Tools & Configs (NVMe)
UUID=32bf1fa3-1f3b-435c-8997-16da40841b33 /mnt/eigenlayer ext4 defaults,noatime,nodiratime 0 2

# Archive/Snapshots/Blobs for AVSs
UUID=49da7ec4-31ad-4b55-b933-3da6fb1d45cf /mnt/archive ext4 defaults,noatime,nodiratime 0 2

# Bitcoin ledger storage
UUID=0ac9203d-7381-466e-9bc5-5669337f1df3 /mnt/bitcoin-node ext4 defaults,noatime,nodiratime 0 2
```

## Performance Optimizations
- `noatime`: Disables updating of file access times
- `nodiratime`: Disables updating of directory access times
- These optimizations reduce disk writes and improve performance for blockchain node operations
