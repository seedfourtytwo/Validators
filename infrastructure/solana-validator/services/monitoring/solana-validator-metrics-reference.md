# Solana Validator Light Mode Metrics Reference

## Overview
This document provides a comprehensive reference for metrics available through the Solana Exporter running in light mode on the validator. Light mode only collects metrics that are unique to the validator node being queried and cannot be obtained from public RPCs. This document uses the exact metric names as they appear in the exporter output for accurate reference when creating Grafana dashboards.

## Table of Contents
- [Node Metrics](#node-metrics)
  - [Identity and Health](#identity-and-health)
  - [Block and Slot](#block-and-slot)
  - [Epoch Information](#epoch-information)
  - [Transaction Data](#transaction-data)
- [Validator Metrics](#validator-metrics)
  - [Credits](#credits)
  - [Leader Slots](#leader-slots)
- [Cluster Metrics](#cluster-metrics)
  - [Network Status](#network-status)
  - [Validator Count](#validator-count)
- [Grafana Query Examples](#grafana-query-examples)
  - [Critical Monitoring Queries](#critical-monitoring-queries)
  - [Health Status Queries](#health-status-queries)
  - [Performance Queries](#performance-queries)
- [Usage Notes](#usage-notes)
  - [Metric Labels](#metric-labels)
  - [Distinctions from Full Mode](#distinctions-from-full-mode)

## Node Metrics

### Identity and Health

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_node_identity` | gauge | Node identity of validator (value is always 1) | `solana_node_identity{identity="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"}` |
| `solana_node_is_healthy` | gauge | Whether the node is healthy (1=healthy, 0=unhealthy) | `solana_node_is_healthy` |
| `solana_node_version` | gauge | Node version of Solana | `solana_node_version{version="2.2.8"}` |
| `solana_node_num_slots_behind` | gauge | Number of slots the node is behind the latest cluster confirmed slot | `solana_node_num_slots_behind` |

These metrics provide fundamental information about the validator node's identity, health status, and software version. They require direct validator access and are not available from public RPCs.

### Block and Slot

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_node_block_height` | gauge | Current block height of the node | `solana_node_block_height` |
| `solana_node_slot_height` | gauge | Current slot number | `solana_node_slot_height` |
| `solana_node_minimum_ledger_slot` | gauge | Lowest slot in the node's ledger | `solana_node_minimum_ledger_slot` |
| `solana_node_first_available_block` | gauge | Slot of the lowest confirmed block not purged from the ledger | `solana_node_first_available_block` |

These metrics track the validator's current position in the blockchain and ledger state. They provide insight into the validator's synchronization status and ledger pruning.

### Epoch Information

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_node_epoch_number` | gauge | Current epoch number | `solana_node_epoch_number` |
| `solana_node_epoch_first_slot` | gauge | First slot of the current epoch (inclusive) | `solana_node_epoch_first_slot` |
| `solana_node_epoch_last_slot` | gauge | Last slot of the current epoch (inclusive) | `solana_node_epoch_last_slot` |

These metrics track epoch boundaries and progression, which is critical for understanding the validator's schedule and performance cycles.

### Transaction Data

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_node_transactions_total` | gauge | Total number of transactions processed without error since genesis | `solana_node_transactions_total` |

This metric tracks the total transaction throughput of the network from the validator's perspective.

## Validator Metrics

### Credits

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_validator_current_epoch_credits` | gauge | Current epoch credits for the validator | `solana_validator_current_epoch_credits{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"}` |
| `solana_validator_total_credits` | gauge | Total accumulated credits for the validator since genesis | `solana_validator_total_credits{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"}` |

These metrics track the validator's participation in voting, which directly affects rewards and overall performance evaluation.

### Leader Slots

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_validator_leader_slots_total` | counter | Number of slots processed, grouped by nodekey and status | `solana_validator_leader_slots_total{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF",status="valid"}` |

This metric tracks leader slot performance, with status values of "valid" or "skipped", which is crucial for validator performance monitoring.

## Cluster Metrics

### Network Status

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_cluster_active_stake` | gauge | Total active stake (in SOL) of the cluster | `solana_cluster_active_stake` |
| `solana_cluster_last_vote` | gauge | Most recent voted-on slot of the cluster | `solana_cluster_last_vote` |
| `solana_cluster_root_slot` | gauge | Max root slot of the cluster | `solana_cluster_root_slot` |
| `solana_cluster_slots_by_epoch_total` | counter | Number of slots processed by the cluster by status and epoch | `solana_cluster_slots_by_epoch_total{epoch="775",status="valid"}` |

These metrics provide information about the network's current state and progress from the validator's perspective.

### Validator Count

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `solana_cluster_validator_count` | gauge | Total number of validators in the cluster by state | `solana_cluster_validator_count{state="current"}` |

This metric provides a count of active and delinquent validators in the network.

## Grafana Query Examples

### Critical Monitoring Queries

```
# Validator health status
solana_node_is_healthy

# Slots behind the network
solana_node_num_slots_behind

# Current vs expected leader slots (success rate)
sum(solana_validator_leader_slots_total{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF",status="valid"}) / 
(sum(solana_validator_leader_slots_total{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF",status="valid"}) + 
sum(solana_validator_leader_slots_total{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF",status="skipped"}))
```

### Health Status Queries

```
# Validator version
solana_node_version

# Epoch progression
(solana_node_slot_height - solana_node_epoch_first_slot) / 
(solana_node_epoch_last_slot - solana_node_epoch_first_slot) * 100

# Ledger health (how much history is kept)
solana_node_slot_height - solana_node_minimum_ledger_slot
```

### Performance Queries

```
# Credit earning rate (credits per hour)
rate(solana_validator_total_credits{nodekey="JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF"}[1h])

# Transaction rate
rate(solana_node_transactions_total[5m])
```

## Usage Notes

### Metric Labels

The Solana exporter in light mode uses several key labels:
- `identity`: Used with `solana_node_identity` to identify the validator
- `nodekey`: Used with validator-specific metrics to identify the validator
- `version`: Used with `solana_node_version` to indicate the Solana software version
- `status`: Used with slot metrics to indicate "valid" or "skipped"
- `state`: Used with validator count metrics to indicate "current" or "delinquent"
- `epoch`: Used to identify epoch-specific metrics

### Distinctions from Full Mode

Light mode metrics focus on validator-specific information that requires direct access to the validator node. For comprehensive monitoring, these metrics should be combined with public RPC metrics collected from a home server running the exporter in full mode.

In a distributed monitoring setup:
1. The validator runs Solana exporter in light mode to minimize resource usage
2. A home server runs Solana exporter in full mode using public RPCs
3. Prometheus combines these data sources for complete monitoring
4. Grafana dashboards display the unified metrics with proper source labels 