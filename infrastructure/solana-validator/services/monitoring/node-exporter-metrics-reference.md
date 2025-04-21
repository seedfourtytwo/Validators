# Node Exporter Metrics Reference

## Overview
This document provides a comprehensive reference for metrics available through the Prometheus Node Exporter that are relevant for monitoring Solana validators. Each section groups related metrics with descriptions, relevance for validator operations, and example Prometheus queries.

## Table of Contents
- [CPU Metrics](#cpu-metrics)
- [Memory Metrics](#memory-metrics)
- [Disk Metrics](#disk-metrics)
- [Network Metrics](#network-metrics)
- [File System Metrics](#file-system-metrics)
- [System Metrics](#system-metrics)
- [Temperature Metrics](#temperature-metrics)
- [Process Metrics](#process-metrics)

## CPU Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `node_cpu_seconds_total{mode="user"}` | CPU time spent in user mode | Tracks validator processing | `rate(node_cpu_seconds_total{mode="user"}[5m]) * 100` |
| `node_cpu_seconds_total{mode="system"}` | CPU time spent in kernel mode | Tracks system overhead | `rate(node_cpu_seconds_total{mode="system"}[5m]) * 100` |
| `node_cpu_seconds_total{mode="idle"}` | CPU time spent idle | Shows available CPU capacity | `rate(node_cpu_seconds_total{mode="idle"}[5m]) * 100` |
| `node_cpu_seconds_total{mode="iowait"}` | CPU time spent waiting for I/O | Identifies disk bottlenecks | `avg(rate(node_cpu_seconds_total{mode="iowait"}[5m])) * 100` |
| `node_cpu_seconds_total{mode="irq"}` | CPU time spent servicing interrupts | Shows hardware interrupt load | `rate(node_cpu_seconds_total{mode="irq"}[5m]) * 100` |
| `node_cpu_seconds_total{mode="softirq"}` | CPU time spent servicing soft interrupts | Shows network/task switching load | `rate(node_cpu_seconds_total{mode="softirq"}[5m]) * 100` |

### CPU Usage Percentage
```
# Overall CPU Usage (%)
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

### I/O Wait Percentage
```
# I/O Wait (%)
avg(rate(node_cpu_seconds_total{mode="iowait"}[5m])) * 100
```

## Memory Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `node_memory_MemTotal_bytes` | Total memory available | Baseline for capacity planning | `node_memory_MemTotal_bytes / 1024 / 1024 / 1024` (GB) |
| `node_memory_MemFree_bytes` | Free memory | Raw unused memory | `node_memory_MemFree_bytes / 1024 / 1024 / 1024` (GB) |
| `node_memory_MemAvailable_bytes` | Available memory (includes reclaimable) | Effective free memory for applications | `node_memory_MemAvailable_bytes / 1024 / 1024 / 1024` (GB) |
| `node_memory_Buffers_bytes` | Memory used for file buffers | File system buffers | `node_memory_Buffers_bytes / 1024 / 1024 / 1024` (GB) |
| `node_memory_Cached_bytes` | Memory used for file cache | Disk cache for performance | `node_memory_Cached_bytes / 1024 / 1024 / 1024` (GB) |
| `node_memory_SwapTotal_bytes` | Total swap space | Swap capacity | `node_memory_SwapTotal_bytes / 1024 / 1024 / 1024` (GB) |
| `node_memory_SwapFree_bytes` | Free swap space | Unused swap | `node_memory_SwapFree_bytes / 1024 / 1024 / 1024` (GB) |
| `node_vmstat_pswpin` | Pages swapped in | Indicates memory pressure | `rate(node_vmstat_pswpin[5m])` |
| `node_vmstat_pswpout` | Pages swapped out | Indicates memory pressure | `rate(node_vmstat_pswpout[5m])` |

### Memory Usage Percentage
```
# Memory Usage (%)
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

### Used Memory (Excluding Cache/Buffers)
```
# Used Memory (GB)
(node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Buffers_bytes - node_memory_Cached_bytes) / 1024 / 1024 / 1024
```

### Swap Usage
```
# Swap Usage (%)
100 * (1 - (node_memory_SwapFree_bytes / node_memory_SwapTotal_bytes))
```

## Disk Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `node_disk_io_time_seconds_total` | Time spent doing I/O | Overall disk busyness | `rate(node_disk_io_time_seconds_total{device="nvme0n1"}[5m]) * 100` |
| `node_disk_reads_completed_total` | Total read operations completed | Read operations | `rate(node_disk_reads_completed_total{device="nvme0n1"}[5m])` |
| `node_disk_writes_completed_total` | Total write operations completed | Write operations | `rate(node_disk_writes_completed_total{device="nvme0n1"}[5m])` |
| `node_disk_read_bytes_total` | Total bytes read | Read throughput | `rate(node_disk_read_bytes_total{device="nvme0n1"}[5m]) / 1024 / 1024` (MB/s) |
| `node_disk_written_bytes_total` | Total bytes written | Write throughput | `rate(node_disk_written_bytes_total{device="nvme0n1"}[5m]) / 1024 / 1024` (MB/s) |
| `node_disk_read_time_seconds_total` | Time spent reading (seconds) | Read latency | `rate(node_disk_read_time_seconds_total{device="nvme0n1"}[5m]) / rate(node_disk_reads_completed_total{device="nvme0n1"}[5m]) * 1000` (ms) |
| `node_disk_write_time_seconds_total` | Time spent writing (seconds) | Write latency | `rate(node_disk_write_time_seconds_total{device="nvme0n1"}[5m]) / rate(node_disk_writes_completed_total{device="nvme0n1"}[5m]) * 1000` (ms) |

### Disk IOPS
```
# Read IOPS
rate(node_disk_reads_completed_total{device="nvme0n1"}[5m])

# Write IOPS
rate(node_disk_writes_completed_total{device="nvme0n1"}[5m])
```

### Disk Throughput
```
# Read Throughput (MB/s)
rate(node_disk_read_bytes_total{device="nvme0n1"}[5m]) / 1024 / 1024

# Write Throughput (MB/s)
rate(node_disk_written_bytes_total{device="nvme0n1"}[5m]) / 1024 / 1024
```

### Disk Latency
```
# Read Latency (ms)
rate(node_disk_read_time_seconds_total{device="nvme0n1"}[5m]) / rate(node_disk_reads_completed_total{device="nvme0n1"}[5m]) * 1000

# Write Latency (ms)
rate(node_disk_write_time_seconds_total{device="nvme0n1"}[5m]) / rate(node_disk_writes_completed_total{device="nvme0n1"}[5m]) * 1000
```

## Network Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `node_network_receive_bytes_total` | Total bytes received | Network throughput in | `rate(node_network_receive_bytes_total{device="enp11s0f1np1"}[5m]) / 1024 / 1024` (MB/s) |
| `node_network_transmit_bytes_total` | Total bytes transmitted | Network throughput out | `rate(node_network_transmit_bytes_total{device="enp11s0f1np1"}[5m]) / 1024 / 1024` (MB/s) |
| `node_network_receive_packets_total` | Total packets received | Network packet rate in | `rate(node_network_receive_packets_total{device="enp11s0f1np1"}[5m])` |
| `node_network_transmit_packets_total` | Total packets transmitted | Network packet rate out | `rate(node_network_transmit_packets_total{device="enp11s0f1np1"}[5m])` |
| `node_network_receive_errs_total` | Receive errors | Network health | `rate(node_network_receive_errs_total{device="enp11s0f1np1"}[5m])` |
| `node_network_transmit_errs_total` | Transmit errors | Network health | `rate(node_network_transmit_errs_total{device="enp11s0f1np1"}[5m])` |
| `node_network_receive_drop_total` | Dropped receive packets | Network congestion | `rate(node_network_receive_drop_total{device="enp11s0f1np1"}[5m])` |
| `node_network_transmit_drop_total` | Dropped transmit packets | Network congestion | `rate(node_network_transmit_drop_total{device="enp11s0f1np1"}[5m])` |
| `node_netstat_Tcp_CurrEstab` | Current established TCP connections | Network connection status | `node_netstat_Tcp_CurrEstab` |
| `node_netstat_Udp_InDatagrams` | UDP datagrams received | UDP traffic (vote transactions) | `rate(node_netstat_Udp_InDatagrams[5m])` |
| `node_netstat_Udp_OutDatagrams` | UDP datagrams sent | UDP traffic (vote transactions) | `rate(node_netstat_Udp_OutDatagrams[5m])` |

### Network Traffic Rate
```
# Receive Bandwidth (MB/s)
rate(node_network_receive_bytes_total{device="enp11s0f1np1"}[5m]) / 1024 / 1024

# Transmit Bandwidth (MB/s)
rate(node_network_transmit_bytes_total{device="enp11s0f1np1"}[5m]) / 1024 / 1024
```

### Network Error Rate (%)
```
# Receive Error Rate (%)
100 * increase(node_network_receive_errs_total{device="enp11s0f1np1"}[12h]) / increase(node_network_receive_packets_total{device="enp11s0f1np1"}[12h])

# Transmit Error Rate (%)
100 * increase(node_network_transmit_errs_total{device="enp11s0f1np1"}[12h]) / increase(node_network_transmit_packets_total{device="enp11s0f1np1"}[12h])
```

### Total Network Traffic
```
# Daily Received (TB)
increase(node_network_receive_bytes_total{device="enp11s0f1np1"}[24h]) / 1024 / 1024 / 1024 / 1024

# Monthly Received (TB)
increase(node_network_receive_bytes_total{device="enp11s0f1np1"}[30d]) / 1024 / 1024 / 1024 / 1024
```

## File System Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `node_filesystem_size_bytes` | Filesystem size | Total disk space | `node_filesystem_size_bytes{mountpoint="/mnt/ledger"} / 1024 / 1024 / 1024` (GB) |
| `node_filesystem_free_bytes` | Filesystem free space | Available space | `node_filesystem_free_bytes{mountpoint="/mnt/ledger"} / 1024 / 1024 / 1024` (GB) |
| `node_filesystem_avail_bytes` | Filesystem available space | Usable space | `node_filesystem_avail_bytes{mountpoint="/mnt/ledger"} / 1024 / 1024 / 1024` (GB) |
| `node_filefd_allocated` | Allocated file descriptors | File handle usage | `node_filefd_allocated` |
| `node_filefd_maximum` | Maximum file descriptors | File handle limit | `node_filefd_maximum` |

### Disk Usage Percentage
```
# Disk Usage (%)
100 - ((node_filesystem_avail_bytes{mountpoint="/mnt/ledger"} / node_filesystem_size_bytes{mountpoint="/mnt/ledger"}) * 100)
```

### File Descriptor Usage
```
# File Descriptor Usage
node_filefd_allocated

# File Descriptor Usage (%)
100 * node_filefd_allocated / node_filefd_maximum
```

## System Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `node_load1` | 1-minute load average | Short-term system load | `node_load1` |
| `node_load5` | 5-minute load average | Medium-term system load | `node_load5` |
| `node_load15` | 15-minute load average | Long-term system load | `node_load15` |
| `node_boot_time_seconds` | System boot time | Server uptime reference | `node_boot_time_seconds` |
| `node_time_seconds` | Current system time | Time reference | `node_time_seconds` |
| `node_procs_running` | Number of processes running | Process management | `node_procs_running` |
| `node_procs_blocked` | Number of processes blocked | Process health | `node_procs_blocked` |

### System Uptime
```
# System Uptime (seconds)
node_time_seconds - node_boot_time_seconds
```

### System Load vs Cores
```
# Load per CPU core (1min average)
node_load1 / count without(cpu, mode) (node_cpu_seconds_total{mode="idle"})
```

## Temperature Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `node_hwmon_temp_celsius` | Hardware temperature sensors | System temperature | `node_hwmon_temp_celsius{chip="pci0000:00_0000:00:18_3",sensor="temp1"}` |
| `node_hwmon_temp_crit_celsius` | Critical temperature threshold | Temperature limits | `node_hwmon_temp_crit_celsius{chip="nvme_nvme0",sensor="temp1"}` |
| `node_hwmon_temp_max_celsius` | Maximum temperature threshold | Temperature limits | `node_hwmon_temp_max_celsius{chip="nvme_nvme0",sensor="temp1"}` |

### CPU Temperature
```
# CPU Temperature (Tctl)
node_hwmon_temp_celsius{chip="pci0000:00_0000:00:18_3",sensor="temp1"}
```

### Drive Temperatures
```
# NVMe Drive Temperatures
node_hwmon_temp_celsius{chip=~"nvme_nvme.*",sensor="temp1"}
```

## Process Metrics

| Metric | Description | Relevance for Validators | Example Query |
|--------|-------------|--------------------------|---------------|
| `process_cpu_seconds_total` | CPU time consumed by process | Process CPU usage | `rate(process_cpu_seconds_total{job="solana"}[5m]) * 100` |
| `process_resident_memory_bytes` | Resident memory size | Process memory usage | `process_resident_memory_bytes{job="solana"} / 1024 / 1024 / 1024` (GB) |
| `process_virtual_memory_bytes` | Virtual memory size | Process virtual memory | `process_virtual_memory_bytes{job="solana"} / 1024 / 1024 / 1024` (GB) |
| `process_open_fds` | Open file descriptors by process | Process file handles | `process_open_fds{job="solana"}` |
| `process_max_fds` | Maximum file descriptors by process | Process file handle limit | `process_max_fds{job="solana"}` |
| `process_start_time_seconds` | Process start time | Process uptime reference | `process_start_time_seconds{job="solana"}` |

### Process Uptime
```
# Process Uptime (seconds)
time() - process_start_time_seconds{job="solana"}
```

### Process CPU Usage
```
# Process CPU Usage (%)
rate(process_cpu_seconds_total{job="solana"}[5m]) * 100
```

## Recommended Metrics for Solana Validators

For Solana validators, the following metrics are particularly important to monitor:

### Critical Metrics
- CPU Usage: `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
- Memory Usage: `100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))`
- Swap Activity: `rate(node_vmstat_pswpin[5m]) + rate(node_vmstat_pswpout[5m])`
- Disk Utilization (Ledger): `rate(node_disk_io_time_seconds_total{device="nvme0n1"}[5m]) * 100`
- Disk Utilization (Accounts): `rate(node_disk_io_time_seconds_total{device="nvme1n1"}[5m]) * 100`
- I/O Wait: `avg(rate(node_cpu_seconds_total{mode="iowait"}[5m])) * 100`
- Network Bandwidth: `rate(node_network_receive_bytes_total{device="enp11s0f1np1"}[5m]) / 1024 / 1024`
- Disk Space (Ledger): `100 - ((node_filesystem_avail_bytes{mountpoint="/mnt/ledger"} / node_filesystem_size_bytes{mountpoint="/mnt/ledger"}) * 100)`
- CPU Temperature: `node_hwmon_temp_celsius{chip="pci0000:00_0000:00:18_3",sensor="temp1"}`
- File Descriptors: `node_filefd_allocated`

### Important Derived Metrics
- System Load vs Capacity: `node_load1 / count without(cpu, mode) (node_cpu_seconds_total{mode="idle"})`
- Network Error Rate: `100 * increase(node_network_receive_errs_total{device="enp11s0f1np1"}[1h]) / increase(node_network_receive_packets_total{device="enp11s0f1np1"}[1h])`
- Disk Write Latency (Accounts): `rate(node_disk_write_time_seconds_total{device="nvme1n1"}[5m]) / rate(node_disk_writes_completed_total{device="nvme1n1"}[5m]) * 1000`
- Disk Write Latency (Ledger): `rate(node_disk_write_time_seconds_total{device="nvme0n1"}[5m]) / rate(node_disk_writes_completed_total{device="nvme0n1"}[5m]) * 1000`
- System Uptime: `node_time_seconds - node_boot_time_seconds`