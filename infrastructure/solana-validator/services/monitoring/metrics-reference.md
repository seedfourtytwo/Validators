# Solana Validator Metrics Reference

## Overview

This document provides a comprehensive reference of all metrics available from our monitoring exporters:
- **Solana Exporter**: Provides Solana-specific metrics including validator performance, vote statistics, and blockchain status
- **Node Exporter**: Provides system-level metrics including CPU, memory, disk, and network performance
- **Prometheus Server**: Provides metrics about the monitoring system itself
- **Go Runtime**: Provides metrics about the Go applications running on the system

## Table of Contents

1. [Solana Exporter Metrics](#solana-exporter-metrics)
   - [Validator Metrics](#validator-metrics)
   - [Network Metrics](#network-metrics)
   - [Performance Metrics](#performance-metrics)
   - [JITO-specific Metrics](#jito-specific-metrics)
2. [Node Exporter Metrics](#node-exporter-metrics)
   - [CPU Metrics](#cpu-metrics)
   - [Memory Metrics](#memory-metrics)
   - [Disk Metrics](#disk-metrics)
   - [Network Metrics](#network-metrics-1)
   - [System Metrics](#system-metrics)
3. [Prometheus Server Metrics](#prometheus-server-metrics)
   - [Scrape Metrics](#scrape-metrics)
   - [Target Metrics](#target-metrics)
   - [HTTP Metrics](#http-metrics)
4. [Go Runtime Metrics](#go-runtime-metrics)
   - [Memory Metrics](#go-memory-metrics)
   - [Garbage Collection Metrics](#garbage-collection-metrics)
   - [Goroutine Metrics](#goroutine-metrics)

## Solana Exporter Metrics

### Validator Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_validator_activated_stake` | gauge | Amount of SOL currently staked to this validator |
| `solana_validator_commission` | gauge | Current commission percentage charged by the validator |
| `solana_validator_delinquent` | gauge | Boolean (0/1) indicating if validator is delinquent |
| `solana_validator_last_vote` | gauge | Slot height of the validator's last vote |
| `solana_validator_root_slot` | gauge | Current root slot of the validator |
| `solana_validator_current_slot` | gauge | Current slot the validator is processing |
| `solana_validator_vote_credits` | gauge | Cumulative credits earned by the validator |
| `solana_validator_skip_rate` | gauge | Rate of skipped leader slots as a percentage |
| `solana_validator_identity_balance` | gauge | SOL balance of the validator's identity account |
| `solana_validator_vote_account_balance` | gauge | SOL balance of the validator's vote account |
| `solana_validator_epoch_credits` | gauge | Credits earned in the current epoch |
| `solana_validator_software_version` | gauge | Version of the Solana software running |
| `solana_validator_leader_slots` | counter | Number of leader slots assigned to the validator |
| `solana_validator_blocks_produced` | counter | Number of blocks produced by the validator |

### Network Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_block_height` | gauge | Current block height of the Solana blockchain |
| `solana_block_time` | gauge | Timestamp of the latest block |
| `solana_epoch` | gauge | Current epoch number |
| `solana_epoch_progress` | gauge | Percentage progress through the current epoch |
| `solana_slot` | gauge | Current global slot |
| `solana_slots_in_epoch` | gauge | Total number of slots in the current epoch |
| `solana_transaction_count` | counter | Total number of transactions processed |
| `solana_active_validators` | gauge | Number of active validators in the network |
| `solana_delinquent_validators` | gauge | Number of delinquent validators in the network |
| `solana_current_stake` | gauge | Total amount of SOL staked in the network |
| `solana_circulating_supply` | gauge | Total circulating supply of SOL |

### Performance Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `solana_tower_distance` | gauge | Tower distance for the validator |
| `solana_transaction_confirmation_time` | histogram | Time to confirm transactions |
| `solana_rpc_request_count` | counter | Number of RPC requests processed |
| `solana_vote_transaction_count` | counter | Number of vote transactions sent |
| `solana_transaction_error_count` | counter | Number of transaction errors |
| `solana_vote_transaction_signature_count` | counter | Number of vote signatures |
| `solana_transaction_success_rate` | gauge | Percentage of transactions successfully processed |
| `solana_validator_catchup_time` | gauge | Time taken to catch up to the cluster |

### JITO-specific Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `jito_mev_reward_total` | counter | Total MEV rewards earned |
| `jito_tip_payment_count` | counter | Number of tip payments received |
| `jito_bundle_execution_count` | counter | Number of bundles executed |
| `jito_block_engine_latency` | gauge | Latency in communication with the block engine |
| `jito_relayer_connection_status` | gauge | Status of connection to the JITO relayer (0/1) |

## Node Exporter Metrics

### CPU Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `node_cpu_seconds_total` | counter | Seconds the CPUs spent in each mode (idle, user, system, etc.) |
| `node_cpu_frequency_hertz` | gauge | CPU frequency in Hertz |
| `node_cpu_guest_seconds_total` | counter | Seconds the CPUs spent in guest mode |
| `node_cpu_core_throttles_total` | counter | Number of times a CPU core has been throttled |
| `node_cpu_package_throttles_total` | counter | Number of times CPU packages have been throttled |
| `node_cpu_scaling_frequency_hertz` | gauge | Current scaled CPU frequency |
| `node_cpu_scaling_frequency_max_hertz` | gauge | Maximum scaled CPU frequency |
| `node_cpu_scaling_frequency_min_hertz` | gauge | Minimum scaled CPU frequency |
| `node_load1` | gauge | 1-minute load average |
| `node_load5` | gauge | 5-minute load average |
| `node_load15` | gauge | 15-minute load average |
| `node_pressure_cpu_waiting_seconds_total` | counter | CPU pressure stall time in seconds |

### Memory Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `node_memory_MemTotal_bytes` | gauge | Total memory in bytes |
| `node_memory_MemFree_bytes` | gauge | Free memory in bytes |
| `node_memory_MemAvailable_bytes` | gauge | Available memory in bytes |
| `node_memory_Buffers_bytes` | gauge | Buffers memory in bytes |
| `node_memory_Cached_bytes` | gauge | Cached memory in bytes |
| `node_memory_SwapTotal_bytes` | gauge | Total swap space in bytes |
| `node_memory_SwapFree_bytes` | gauge | Free swap space in bytes |
| `node_memory_SwapCached_bytes` | gauge | Cached swap in bytes |
| `node_memory_Active_bytes` | gauge | Active memory in bytes |
| `node_memory_Inactive_bytes` | gauge | Inactive memory in bytes |
| `node_memory_Dirty_bytes` | gauge | Dirty memory in bytes |
| `node_memory_Writeback_bytes` | gauge | Memory in writeback in bytes |
| `node_memory_HugePages_Total` | gauge | Total huge pages |
| `node_memory_HugePages_Free` | gauge | Free huge pages |

### Disk Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `node_disk_io_now` | gauge | Number of I/Os currently in progress |
| `node_disk_io_time_seconds_total` | counter | Total seconds spent doing I/Os |
| `node_disk_read_bytes_total` | counter | Total bytes read from disk |
| `node_disk_read_time_seconds_total` | counter | Total seconds spent reading from disk |
| `node_disk_writes_completed_total` | counter | Total writes completed |
| `node_disk_write_bytes_total` | counter | Total bytes written to disk |
| `node_disk_write_time_seconds_total` | counter | Total seconds spent writing to disk |
| `node_filesystem_avail_bytes` | gauge | Filesystem space available in bytes |
| `node_filesystem_free_bytes` | gauge | Filesystem free space in bytes |
| `node_filesystem_size_bytes` | gauge | Filesystem size in bytes |
| `node_filesystem_readonly` | gauge | Filesystem readonly status (0/1) |
| `node_filesystem_files` | gauge | Filesystem total file nodes |
| `node_filesystem_files_free` | gauge | Filesystem free file nodes |

### Network Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `node_network_receive_bytes_total` | counter | Total bytes received over network |
| `node_network_receive_packets_total` | counter | Total packets received over network |
| `node_network_receive_drop_total` | counter | Total received packets dropped |
| `node_network_receive_errs_total` | counter | Total receive errors |
| `node_network_transmit_bytes_total` | counter | Total bytes transmitted over network |
| `node_network_transmit_packets_total` | counter | Total packets transmitted |
| `node_network_transmit_drop_total` | counter | Total transmitted packets dropped |
| `node_network_transmit_errs_total` | counter | Total transmission errors |
| `node_network_speed_bytes` | gauge | Network device speed in bytes |
| `node_network_up` | gauge | Network device up status (0/1) |
| `node_network_mtu_bytes` | gauge | Network device MTU in bytes |

### System Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `node_boot_time_seconds` | gauge | Node boot time in seconds since epoch |
| `node_context_switches_total` | counter | Total context switches |
| `node_forks_total` | counter | Total number of forks |
| `node_intr_total` | counter | Total number of interrupts |
| `node_nprocs` | gauge | Number of processes |
| `node_processes_state` | gauge | Number of processes in each state |
| `node_time_seconds` | gauge | System time in seconds since epoch |
| `node_scrape_collector_duration_seconds` | gauge | Duration of collector scrape |
| `node_scrape_collector_success` | gauge | Whether the collector scrape was successful |
| `node_textfile_scrape_error` | gauge | Error with textfiles |
| `node_timex_offset_seconds` | gauge | Time offset in seconds |
| `node_timex_sync_status` | gauge | Is clock synchronized (0/1) |
| `node_uname_info` | gauge | System information from uname |
| `node_entropy_available_bits` | gauge | Bits of available entropy |
| `node_hwmon_temp_celsius` | gauge | Hardware monitor temperature in Celsius |
| `node_hwmon_power_average_watt` | gauge | Hardware monitor power usage |

## Prometheus Server Metrics

### Scrape Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `prometheus_target_interval_length_seconds` | summary | Actual intervals between scrapes |
| `prometheus_target_scrape_pool_targets` | gauge | Current number of targets in this scrape pool |
| `prometheus_target_scrapes_sample_duplicate_timestamp_total` | counter | Total number of samples rejected due to duplicate timestamps |
| `prometheus_target_scrapes_sample_out_of_order_total` | counter | Total number of samples rejected due to ordering issues |
| `prometheus_target_sync_length_seconds` | summary | Actual interval to sync the scrape pool |

### Target Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `prometheus_sd_discovered_targets` | gauge | Current number of discovered targets |
| `prometheus_sd_received_updates_total` | counter | Total number of update events received from the SD providers |
| `prometheus_target_metadata_cache_bytes` | gauge | The number of bytes used for storing metric metadata in the cache |
| `prometheus_target_metadata_cache_entries` | gauge | Total number of metric metadata entries in the cache |

### HTTP Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `prometheus_http_request_duration_seconds` | histogram | Histogram of latencies for HTTP requests |
| `prometheus_http_requests_total` | counter | Counter of HTTP requests |
| `prometheus_http_response_size_bytes` | histogram | Histogram of response size for HTTP requests |
| `promhttp_metric_handler_requests_in_flight` | gauge | Current number of scrapes being served |
| `promhttp_metric_handler_requests_total` | counter | Total number of scrapes by HTTP status code |

## Go Runtime Metrics

### Go Memory Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `go_memstats_alloc_bytes` | gauge | Number of bytes allocated and still in use |
| `go_memstats_alloc_bytes_total` | counter | Total number of bytes allocated, even if freed |
| `go_memstats_heap_alloc_bytes` | gauge | Number of heap bytes allocated and still in use |
| `go_memstats_heap_idle_bytes` | gauge | Number of heap bytes waiting to be used |
| `go_memstats_heap_inuse_bytes` | gauge | Number of heap bytes that are in use |
| `go_memstats_heap_objects` | gauge | Number of allocated objects |
| `go_memstats_heap_released_bytes` | gauge | Number of heap bytes released to OS |
| `go_memstats_heap_sys_bytes` | gauge | Number of heap bytes obtained from system |
| `go_memstats_next_gc_bytes` | gauge | Number of heap bytes when next garbage collection will take place |

### Garbage Collection Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `go_gc_duration_seconds` | summary | A summary of the pause duration of garbage collection cycles |
| `go_gc_cycles_automatic_gc_cycles_total` | counter | Count of completed GC cycles generated by the Go runtime |
| `go_gc_cycles_forced_gc_cycles_total` | counter | Count of completed GC cycles forced by the application |
| `go_gc_cycles_total_gc_cycles_total` | counter | Count of all completed GC cycles |
| `go_gc_heap_allocs_bytes_total` | counter | Cumulative sum of memory allocated to the heap |
| `go_gc_heap_frees_bytes_total` | counter | Cumulative sum of heap memory freed by the garbage collector |
| `go_gc_heap_goal_bytes` | gauge | Heap size target for the end of the GC cycle |
| `go_gc_heap_live_bytes` | gauge | Heap memory occupied by live objects from the previous GC |

### Goroutine Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `go_goroutines` | gauge | Number of goroutines that currently exist |
| `go_threads` | gauge | Number of OS threads created |
| `go_info` | gauge | Information about the Go environment |
| `go_sched_goroutines_goroutines` | gauge | Count of live goroutines |
| `go_sched_gomaxprocs_threads` | gauge | The current runtime.GOMAXPROCS setting |

## Using These Metrics

### Critical Metrics to Monitor

For Solana validators, these metrics are particularly important to monitor:

1. **Validator Health**
   - `solana_validator_delinquent` - Should be 0
   - `solana_validator_skip_rate` - Should be low (<5%)
   - `solana_validator_last_vote` - Should be recent

2. **System Health**
   - `node_filesystem_avail_bytes` - Watch for disk space issues
   - `node_memory_MemAvailable_bytes` - Watch for memory pressure
   - `node_cpu_seconds_total{mode="iowait"}` - High values indicate disk bottlenecks
   - `node_load1` - Watch for sustained high loads

3. **Network Health**
   - `node_network_transmit_errs_total` and `node_network_receive_errs_total` - Should be minimal
   - `node_network_receive_bytes_total` and `node_network_transmit_bytes_total` - Monitor bandwidth usage

4. **JITO MEV Metrics**
   - `jito_mev_reward_total` - Monitor MEV rewards earned
   - `jito_tip_payment_count` - Track tip payments received
   - `jito_relayer_connection_status` - Verify connection to JITO infrastructure

5. **Monitoring System Health**
   - `prometheus_target_interval_length_seconds` - Ensure scrape intervals are consistent
   - `go_memstats_heap_inuse_bytes` - Monitor memory usage of exporters
   - `prometheus_target_scrapes_sample_out_of_order_total` - Watch for metric collection issues

### Recommended Alerts

Set up alerts for:
- Validator becoming delinquent
- Skip rate exceeding threshold (e.g., >5%)
- Disk space below threshold (e.g., <15%)
- Memory available below threshold
- High system load for extended periods
- Network errors increasing
- JITO relayer connection failures
- Prometheus target scrape failures

### Grafana Dashboard Integration

These metrics can be imported into Grafana dashboards. Recommended dashboard configurations:

1. **Validator Overview Dashboard**: High-level status of validator health
2. **System Performance Dashboard**: Detailed system metrics
3. **Network Dashboard**: Network performance and errors
4. **Disk I/O Dashboard**: Detailed disk performance metrics
5. **JITO MEV Dashboard**: Focus on MEV-related metrics and rewards
6. **Monitoring Health Dashboard**: Status of the monitoring system itself

For dashboard templates, visit the [Grafana Dashboard Repository](https://grafana.com/grafana/dashboards/) and search for "Solana" or "Node Exporter". 