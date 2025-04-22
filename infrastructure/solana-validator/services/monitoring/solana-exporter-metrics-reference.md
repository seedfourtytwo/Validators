# Solana Exporter Metrics Reference

## Overview
This document provides a comprehensive reference for metrics available through the Solana Exporter that are relevant for monitoring Solana validators. Each section groups related metrics with descriptions, relevance for validator operations, example Prometheus queries, and importantly, whether they can be obtained from public RPCs or require direct validator access.

## Table of Contents
- [Validator Metrics](#validator-metrics)
  - [Stake and Commission](#stake-and-commission)
  - [Vote and Slot](#vote-and-slot)
  - [Status and Version](#status-and-version)
- [Network Metrics](#network-metrics)
  - [Slot and Epoch](#slot-and-epoch)
  - [Validator Count](#validator-count)
  - [Supply and Stake](#supply-and-stake)
- [Performance Metrics](#performance-metrics)
  - [Vote Performance](#vote-performance)
  - [Block and Slot Time](#block-and-slot-time)
  - [Transaction Performance](#transaction-performance)
- [Derived Metrics](#derived-metrics)
  - [Skip Rate Analysis](#skip-rate-analysis)
  - [Vote Credit Analysis](#vote-credit-analysis)
- [Source Availability](#source-availability)
  - [Public RPC Available Metrics](#public-rpc-available-metrics)
  - [Validator-Only Metrics](#validator-only-metrics)
- [Recommended Metrics for Remote Monitoring](#recommended-metrics-for-remote-monitoring)
  - [Critical Metrics](#critical-metrics)
  - [Important Derived Metrics](#important-derived-metrics)
- [Example Prometheus Configuration](#example-prometheus-configuration)

## Validator Metrics

### Stake and Commission

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_validator_activated_stake` | Current activated stake in SOL | Public RPC | `solana_validator_activated_stake{pubkey="<validator_identity>"}` |
| `solana_validator_commission` | Current commission percentage | Public RPC | `solana_validator_commission{pubkey="<validator_identity>"}` |
| `solana_validator_delinquent` | Whether validator is delinquent (1=yes, 0=no) | Public RPC | `solana_validator_delinquent{pubkey="<validator_identity>"}` |
| `solana_validator_active_stake` | Validator's currently active stake | Public RPC | `solana_validator_active_stake{pubkey="<validator_identity>"}` |
| `solana_validator_epoch_credits` | Credits earned in current epoch | Public RPC | `solana_validator_epoch_credits{pubkey="<validator_identity>"}` |

These metrics track the validator's stake, commission settings, and status in the network. They are all available via public RPCs and don't require direct validator access.

### Vote and Slot

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_validator_last_vote` | Slot height of the last vote | Public RPC | `solana_validator_last_vote{pubkey="<validator_identity>"}` |
| `solana_validator_root_slot` | Current root slot | Public RPC | `solana_validator_root_slot{pubkey="<validator_identity>"}` |
| `solana_validator_credits` | Total vote credits earned | Public RPC | `solana_validator_credits{pubkey="<validator_identity>"}` |
| `solana_validator_skip_rate` | Vote skip rate as percentage | Public RPC | `solana_validator_skip_rate{pubkey="<validator_identity>"}` |
| `solana_validator_current_epoch_credits` | Credits earned in current epoch | Public RPC | `solana_validator_current_epoch_credits{pubkey="<validator_identity>"}` |
| `solana_validator_total_credits` | Total accumulated credits since genesis | Public RPC | `solana_validator_total_credits{pubkey="<validator_identity>"}` |

These metrics track vote-related performance and are crucial for monitoring validator health. They can be retrieved from public RPCs.

### Status and Version

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_validator_version` | Solana software version | Validator RPC | `solana_validator_version{pubkey="<validator_identity>"}` |
| `solana_validator_health` | Validator health status (1=healthy, 0=unhealthy) | Validator RPC | `solana_validator_health{pubkey="<validator_identity>"}` |
| `solana_validator_leader_slots` | Upcoming leader slots in schedule | Public RPC | `solana_validator_leader_slots{pubkey="<validator_identity>"}` |
| `solana_validator_balance` | Validator identity account balance | Public RPC | `solana_validator_balance{pubkey="<validator_identity>"}` |
| `solana_validator_vote_account_balance` | Validator vote account balance | Public RPC | `solana_validator_vote_account_balance{pubkey="<validator_identity>"}` |

Some of these metrics (version and health) require direct access to the validator's RPC, while others can be obtained from public sources.

## Network Metrics

### Slot and Epoch

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_network_slot` | Current slot height | Public RPC | `solana_network_slot` |
| `solana_network_epoch` | Current epoch number | Public RPC | `solana_network_epoch` |
| `solana_network_epoch_progress` | Progress through current epoch (%) | Public RPC | `solana_network_epoch_progress` |
| `solana_network_slots_in_epoch` | Total slots in current epoch | Public RPC | `solana_network_slots_in_epoch` |
| `solana_network_remaining_slots_in_epoch` | Remaining slots in current epoch | Public RPC | `solana_network_remaining_slots_in_epoch` |

These metrics track network-wide slot and epoch progress and are available from public RPCs.

### Validator Count

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_network_validator_count` | Total number of validators | Public RPC | `solana_network_validator_count` |
| `solana_network_active_validators` | Number of active validators | Public RPC | `solana_network_active_validators` |
| `solana_network_delinquent_validators` | Number of delinquent validators | Public RPC | `solana_network_delinquent_validators` |

These metrics track the state of validators across the network and are available from public RPCs.

### Supply and Stake

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_network_active_stake` | Total active stake in SOL | Public RPC | `solana_network_active_stake` |
| `solana_network_current_stake` | Current stake in SOL | Public RPC | `solana_network_current_stake` |
| `solana_network_total_supply` | Total SOL supply | Public RPC | `solana_network_total_supply` |
| `solana_network_circulating_supply` | Circulating SOL supply | Public RPC | `solana_network_circulating_supply` |
| `solana_network_staking_yield` | Current staking yield (estimated APY) | Public RPC | `solana_network_staking_yield` |

These metrics provide information about the SOL economics and staking rates. They are available from public RPCs.

## Performance Metrics

### Vote Performance

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_performance_tower_distance` | Tower vote distance | Validator RPC | `solana_performance_tower_distance{pubkey="<validator_identity>"}` |
| `solana_performance_vote_credits_per_slot` | Credits earned per slot | Public RPC | `rate(solana_validator_total_credits{pubkey="<validator_identity>"}[1h]) / rate(solana_network_slot[1h])` |
| `solana_performance_vote_success_rate` | Percentage of successful votes | Validator RPC | `solana_performance_vote_success_rate{pubkey="<validator_identity>"}` |
| `solana_performance_slots_skipped` | Number of slots skipped | Public RPC | Derived from skip rate |

Some of these metrics require direct validator access, while others can be derived from public RPC metrics.

### Block and Slot Time

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_performance_block_time` | Average block time (ms) | Public RPC | `solana_performance_block_time` |
| `solana_performance_slot_time` | Average slot time (ms) | Public RPC | `solana_performance_slot_time` |
| `solana_performance_skip_rate` | Network skip rate (%) | Public RPC | `solana_performance_skip_rate` |
| `solana_performance_block_height` | Current block height | Public RPC | `solana_performance_block_height` |

These metrics track network timing performance and are available from public RPCs.

### Transaction Performance

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_performance_transaction_count` | Total transaction count | Public RPC | `solana_performance_transaction_count` |
| `solana_performance_transactions_per_second` | Current TPS | Public RPC | `rate(solana_performance_transaction_count[1m])` |
| `solana_performance_transactions_per_slot` | Average transactions per slot | Public RPC | `rate(solana_performance_transaction_count[5m]) / rate(solana_network_slot[5m])` |
| `solana_performance_max_transaction_capacity` | Maximum transaction capacity | Public RPC | `solana_performance_max_transaction_capacity` |

These metrics track network transaction performance and are available from public RPCs.

## Derived Metrics

### Skip Rate Analysis

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_validator_skip_rate_change` | Change in skip rate over time | Derived | `delta(solana_validator_skip_rate{pubkey="<validator_identity>"}[24h])` |
| `solana_validator_skip_rate_relative` | Skip rate relative to network average | Derived | `solana_validator_skip_rate{pubkey="<validator_identity>"} / avg(solana_validator_skip_rate)` |
| `solana_validator_consecutive_skips` | Consecutive skipped slots | Validator RPC | Requires custom instrumentation |

These derived metrics help analyze validator performance trends over time.

### Vote Credit Analysis

| Metric | Description | Source | Example Query |
|--------|-------------|--------|---------------|
| `solana_validator_credit_rate` | Credits earned per hour | Derived | `rate(solana_validator_total_credits{pubkey="<validator_identity>"}[1h])` |
| `solana_validator_credit_efficiency` | Credits earned vs expected | Derived | `rate(solana_validator_total_credits{pubkey="<validator_identity>"}[24h]) / (rate(solana_network_slot[24h]) * (1 - solana_validator_skip_rate{pubkey="<validator_identity>"} / 100))` |

These derived metrics help analyze the efficiency of the validator's voting process.

## Source Availability

### Public RPC Available Metrics
The following metrics can be obtained from public RPCs without direct validator access:

- All network-level metrics (slot, epoch, validator count, supply, stake)
- Basic validator information (activated stake, commission, delinquent status)
- Validator vote statistics (last vote, root slot, skip rate)
- Network performance metrics (block time, slot time, transaction count)

### Validator-Only Metrics
These metrics require direct access to the validator's local RPC:

- `solana_validator_version` - Software version details
- `solana_validator_health` - Internal health status
- `solana_performance_tower_distance` - Tower vote distance
- `solana_performance_vote_success_rate` - Direct vote success rate
- Detailed transaction processing metrics
- Real-time validator resource usage

## Recommended Metrics for Remote Monitoring

### Critical Metrics
When monitoring from a remote server using public RPCs, prioritize these metrics:

1. `solana_validator_delinquent` - Immediately shows validator status issues
2. `solana_validator_skip_rate` - Critical performance indicator
3. `solana_validator_last_vote` vs `solana_network_slot` - Vote lag
4. `solana_validator_activated_stake` - Track stake changes
5. `solana_network_epoch_progress` - Track epoch progress
6. `solana_validator_epoch_credits` - Performance in current epoch

### Important Derived Metrics
1. Vote lag: `solana_network_slot - solana_validator_last_vote{pubkey="<validator_identity>"}`
2. Relative skip rate: `solana_validator_skip_rate{pubkey="<validator_identity>"} / avg(solana_validator_skip_rate)`
3. Epoch credit earning rate: `rate(solana_validator_epoch_credits{pubkey="<validator_identity>"}[1h])`

## Example Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'solana-exporter-home'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:9100']
    params:
      rpc_url: ['https://api.mainnet-beta.solana.com']
      validator_identity: ['JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF']
```

For your setup, you would replace:
- `localhost:9100` with the address where your Solana exporter will run on your home server
- The public RPC URL with your preferred endpoint
- The validator identity with your validator's public key 