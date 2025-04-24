# Solana Exporter Public Metrics Reference

## Overview
This document lists and describes all metrics available from the Solana Exporter running on the home server in comprehensive mode using public RPC endpoints. These metrics provide extensive information about your validator's performance in the context of the overall Solana network.

## Metrics Categories
- [Validator Metrics](#validator-metrics)
- [Cluster Metrics](#cluster-metrics)
- [Node Metrics](#node-metrics)
- [Go Runtime Metrics](#go-runtime-metrics)

## Usage in Prometheus Queries
Metrics can be queried in Prometheus using their name and optional label selectors. For example:

```
# Get active stake for a specific validator
solana_validator_active_stake{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"}

# Get current cluster slot height
solana_node_slot_height

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

## Cluster Metrics

| Metric Name | Type | Labels | Description | Example PromQL Query |
|-------------|------|--------|-------------|---------------------|
| `solana_cluster_active_stake` | gauge | - | Total active stake in SOL for the entire cluster | `solana_cluster_active_stake` |
| `solana_cluster_last_vote` | gauge | - | Most recent voted-on slot of the cluster | `solana_cluster_last_vote` |
| `solana_cluster_root_slot` | gauge | - | Max root slot of the cluster | `solana_cluster_root_slot` |
| `solana_cluster_slots_by_epoch_total` | counter | epoch, status | Number of slots processed by the cluster by status and epoch | `solana_cluster_slots_by_epoch_total{epoch="775",status="valid"}` |
| `solana_cluster_validator_count` | gauge | state | Total number of validators in the cluster by state | `solana_cluster_validator_count{state="current"}` |

## Node Metrics

| Metric Name | Type | Labels | Description | Example PromQL Query |
|-------------|------|--------|-------------|---------------------|
| `solana_node_slot_height` | gauge | - | The current slot number | `solana_node_slot_height` |
| `solana_node_epoch_number` | gauge | - | The current epoch number | `solana_node_epoch_number` |
| `solana_node_epoch_first_slot` | gauge | - | Current epoch's first slot (inclusive) | `solana_node_epoch_first_slot` |
| `solana_node_epoch_last_slot` | gauge | - | Current epoch's last slot (inclusive) | `solana_node_epoch_last_slot` |
| `solana_node_is_healthy` | gauge | - | Whether the node is healthy (1=yes, 0=no) | `solana_node_is_healthy` |
| `solana_node_identity` | gauge | identity | Node identity | `solana_node_identity` |
| `solana_node_version` | gauge | version | Node version of Solana | `solana_node_version` |
| `solana_node_block_height` | gauge | - | The current block height of the node | `solana_node_block_height` |
| `solana_node_minimum_ledger_slot` | gauge | - | The lowest slot in the node's ledger | `solana_node_minimum_ledger_slot` |
| `solana_node_first_available_block` | gauge | - | The slot of the lowest confirmed block not purged | `solana_node_first_available_block` |
| `solana_node_num_slots_behind` | gauge | - | The number of slots the node is behind the cluster | `solana_node_num_slots_behind` |
| `solana_node_transactions_total` | gauge | - | Total number of transactions processed | `solana_node_transactions_total` |

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

## Metrics Mapping from Previous Versions

If you're familiar with older versions of the exporter, here's how the metrics have been renamed:

| Old Metric Name | New Metric Name | Description |
|-----------------|----------------|-------------|
| `solana_network_slot` | `solana_node_slot_height` | Current slot height |
| `solana_network_epoch` | `solana_node_epoch_number` | Current epoch number |
| `solana_network_epoch_progress` | Derived from `solana_node_epoch_first_slot` and `solana_node_epoch_last_slot` | Calculate with: `(solana_node_slot_height - solana_node_epoch_first_slot) / (solana_node_epoch_last_slot - solana_node_epoch_first_slot) * 100` |
| `solana_network_validator_count` | `solana_cluster_validator_count{state="current"}` | Total number of active validators |
| `solana_network_active_stake` | `solana_cluster_active_stake` | Total active stake in SOL |
| `solana_performance_block_time` | - | No direct equivalent in newer versions |
| `solana_performance_slot_time` | - | No direct equivalent in newer versions |
| `solana_performance_skip_rate` | Can be derived from `solana_cluster_slots_by_epoch_total` | Calculate with: `sum(solana_cluster_slots_by_epoch_total{status="skipped"}) / (sum(solana_cluster_slots_by_epoch_total{status="skipped"}) + sum(solana_cluster_slots_by_epoch_total{status="valid"})) * 100` |
| `solana_performance_transaction_count` | `solana_node_transactions_total` | Total transaction count |
| `solana_performance_block_height` | `solana_node_block_height` | Current block height |

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

*Note: This metrics reference is based on Solana Exporter version from the seedfourtytwo fork.* 