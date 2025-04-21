# 💾 Disk Management

## Overview
Solana validator requires high-performance storage with specific layouts optimized for different data types. Our setup uses three NVMe drives for optimal performance.

## Current Disk Layout

| Device    | Partition | Size    | Mount Point      | Type  | Purpose            | UUID                                    |
|-----------|-----------|---------|------------------|-------|--------------------|-----------------------------------------|
| nvme2n1   | p1        | 1G      | /boot/efi        | vfat  | EFI Boot           | 7A66-03A9                               |
|           | p2        | 1G      | /boot            | ext4  | Boot Filesystem    | 625f4e0f-0bad-46b5-a955-48b9de62c6f9   |
|           | p3        | 200G    | /                | ext4  | Root OS            | d9e75b9a-e572-4bdf-9959-2bd24ca17f5e   |
|           | p4        | 1.2T    | /mnt/snapshots   | ext4  | Solana Snapshots   | 8e3bfbd0-ea9c-4848-aac7-0980375218fc   |
|           | p5        | 461G    | [SWAP]           | swap  | Swap Partition     | 6d4ddbe1-d621-451a-87fb-382d14a6f1af   |
| nvme0n1   | p1        | 931.5G  | /mnt/ledger      | ext4  | Solana Ledger      | 8bdc3c97-5797-4503-b624-a00ce66d0290   |
| nvme1n1   | p1        | 931.5G  | /mnt/accounts    | ext4  | Solana Accounts    | a6ec09e4-5598-4f7d-83fa-7bc726811fc7   |

## Current Disk Usage
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme2n1p3  196G   48G  139G  26% /
/dev/nvme1n1p1  916G   30G  840G   4%  /mnt/accounts
/dev/nvme0n1p1  916G  505G  365G  59% /mnt/ledger
/dev/nvme2n1p4  1.2T   11G  1.1T   1%  /mnt/snapshots
/dev/nvme2n1p2  974M   97M  810M  11% /boot
/dev/nvme2n1p1  1.1G  6.2M  1.1G   1%  /boot/efi
```

## Mount Configuration
Current `/etc/fstab` configuration:
```bash
# Root filesystem
/dev/disk/by-uuid/d9e75b9a-e572-4bdf-9959-2bd24ca17f5e / ext4 defaults 0 1

# Boot partition
/dev/disk/by-uuid/625f4e0f-0bad-46b5-a955-48b9de62c6f9 /boot ext4 defaults 0 1

# EFI partition
/dev/disk/by-uuid/7A66-03A9 /boot/efi vfat defaults 0 1

# Solana data partitions
UUID=8bdc3c97-5797-4503-b624-a00ce66d0290 /mnt/ledger ext4 noatime 0 0
UUID=a6ec09e4-5598-4f7d-83fa-7bc726811fc7 /mnt/accounts ext4 noatime 0 0
UUID=8e3bfbd0-ea9c-4848-aac7-0980375218fc /mnt/snapshots ext4 noatime 0 0

# Swap partition
UUID=6d4ddbe1-d621-451a-87fb-382d14a6f1af none swap sw 0 0
```

## Performance Optimizations

### I/O Scheduler Configuration
Current scheduler settings for NVMe drives:
```
[none] mq-deadline
```
- Using `none` scheduler for optimal NVMe performance
- `mq-deadline` available as fallback if needed

### Mount Options
- `noatime`: Disables updating of file access times, reducing disk writes
- Using UUIDs for reliable device identification
- Separate partitions for different data types to optimize I/O

### Storage Allocation
- Ledger: Dedicated 931.5G NVMe drive (59% used) on nvme0n1
- Accounts: Dedicated 931.5G NVMe drive (4% used) on nvme1n1
- Snapshots: 1.2T partition (1% used) on nvme2n1
- Swap: 461G for system memory management

## Maintenance Procedures

### Disk Health Monitoring
```bash
# Monitor disk usage
df -h

# Check I/O scheduler settings
cat /sys/block/nvme*/queue/scheduler

# Monitor I/O statistics
iostat -x 1
```