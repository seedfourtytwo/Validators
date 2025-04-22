# Solana Exporter Public Metrics Reference

## Overview
This document lists and describes all metrics available from the Solana Exporter running on the home server in comprehensive mode using public RPC endpoints. These metrics provide extensive information about your validator's performance in the context of the overall Solana network.

## Metrics Categories
- [Validator Metrics](#validator-metrics)
- [Network Metrics](#network-metrics)
- [Performance Metrics](#performance-metrics)
- [Go Runtime Metrics](#go-runtime-metrics)

## Usage in Prometheus Queries
Metrics can be queried in Prometheus using their name and optional label selectors. For example:

```
# Get active stake for a specific validator
solana_validator_active_stake{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"}

# Get current network slot height
solana_network_slot

# Get delinquent status for your validator
solana_validator_delinquent{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"}
```

## Validator Metrics

| Metric Name | Type | Labels | Description | Example PromQL Query |
|-------------|------|--------|-------------|---------------------|
| `solana_validator_active_stake` | gauge | nodekey, votekey | Current active stake in SOL for a validator | `solana_validator_active_stake{nodekey="YOUR_NODE_KEY"}` |
| `solana_validator_commission` | gauge | nodekey, votekey | Current commission percentage | `solana_validator_commission{nodekey="YOUR_NODE_KEY"}` |
| `solana_validator_last_vote` | gauge | nodekey, votekey | Slot height of the last vote | `solana_validator_last_vote{nodekey="YOUR_NODE_KEY"}` |
| `solana_validator_root_slot` | gauge | nodekey, votekey | Current root slot | `solana_validator_root_slot{nodekey="YOUR_NODE_KEY"}` |
| `solana_validator_delinquent` | gauge | nodekey, votekey | Whether validator is delinquent (1=yes, 0=no) | `solana_validator_delinquent{nodekey="YOUR_NODE_KEY"}` |
| `solana_validator_current_epoch_credits` | gauge | nodekey | Credits earned in the current epoch | `solana_validator_current_epoch_credits{nodekey="YOUR_NODE_KEY"}` |
| `solana_validator_total_credits` | counter | nodekey | Total vote credits earned since genesis | `solana_validator_total_credits{nodekey="YOUR_NODE_KEY"}` |

## Network Metrics

| Metric Name | Type | Labels | Description | Example PromQL Query |
|-------------|------|--------|-------------|---------------------|
| `solana_network_slot` | gauge | - | Current slot height | `solana_network_slot` |
| `solana_network_epoch` | gauge | - | Current epoch number | `solana_network_epoch` |
| `solana_network_epoch_progress` | gauge | - | Progress through current epoch (%) | `solana_network_epoch_progress` |
| `solana_network_validator_count` | gauge | - | Total number of validators | `solana_network_validator_count` |
| `solana_network_active_stake` | gauge | - | Total active stake in SOL | `solana_network_active_stake` |
| `solana_network_current_stake` | gauge | - | Current stake in SOL | `solana_network_current_stake` |

## Performance Metrics

| Metric Name | Type | Labels | Description | Example PromQL Query |
|-------------|------|--------|-------------|---------------------|
| `solana_performance_block_time` | gauge | - | Average block time (ms) | `solana_performance_block_time` |
| `solana_performance_slot_time` | gauge | - | Average slot time (ms) | `solana_performance_slot_time` |
| `solana_performance_skip_rate` | gauge | - | Network skip rate (%) | `solana_performance_skip_rate` |
| `solana_performance_transaction_count` | counter | - | Total transaction count | `solana_performance_transaction_count` |
| `solana_performance_block_height` | gauge | - | Current block height | `solana_performance_block_height` |

## Go Runtime Metrics

The Solana Exporter also exposes various Go runtime metrics that provide information about the exporter process itself:

| Metric Name | Type | Description |
|-------------|------|-------------|
| `go_goroutines` | gauge | Number of goroutines currently running |
| `go_memstats_alloc_bytes` | gauge | Bytes of allocated heap objects |
| `go_memstats_alloc_bytes_total` | counter | Total bytes allocated |
| `go_gc_duration_seconds` | summary | A summary of the pause duration of garbage collection cycles |

## Note on Comprehensive Mode

When running with the `-comprehensive-vote-account-tracking` flag, the exporter collects data for ALL validators in the network. This allows comparison of your validator's performance with others, but significantly increases the number of time series stored in Prometheus. The metrics above will have data points for each validator, with appropriate labels to distinguish them.

## Complete Metrics List

To get the complete list of metrics currently exposed by your Solana exporter, you can run:

```bash
curl http://localhost:9101/metrics | grep -v "^#" | sort | uniq
```

For metrics related specifically to your validator:

```bash
curl http://localhost:9101/metrics | grep YOUR_NODE_KEY
```

Replace `YOUR_NODE_KEY` with your validator's identity public key.

---

*Note: This metrics reference is based on Solana Exporter version [VERSION]. Some metrics may change in future versions.* 