# Solana Delegator Tracker

A Python-based service that tracks and monitors delegations to your Solana validator. It provides near real-time data about stake accounts, delegation amounts, and delegator information through a simple HTTP API, which can be visualized in Grafana.

## Table of Contents
- [Features](#features)
- [Components](#components)
  - [Data Collector](#1-data-collector-delegator_trackerpy)
  - [HTTP Server](#2-http-server-delegator-tracker-http-serverpy)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
- [Grafana Configuration](#grafana-configuration)
- [Understanding the Data](#understanding-the-data)
  - [Stake Account Structure](#stake-account-structure)
  - [Known Delegators](#known-delegators)
  - [JSON Data Structure](#json-data-structure)
- [Monitoring](#monitoring)

## Features
- Hourly updates of delegator information
- Tracks individual stake accounts and amounts
- Maintains 24-hour historical data
- Identifies known delegators (e.g., Solana Foundation)
- Simple HTTP API for data access
- Grafana integration via Infinity plugin

## Components

### 1. Data Collector (`delegator_tracker.py`)
- Fetches delegator data from Solana RPC
- Processes stake account information
- Maintains historical data (24 hours)
- Runs hourly via systemd timer

### 2. HTTP Server (`delegator-tracker-http-server.py`)
- Serves JSON data via HTTP
- CORS enabled for Grafana access
- Simple GET endpoint at root path

## Installation

### Prerequisites
- Python 3.x
- `requests` library: `pip3 install requests`
- Systemd (for service management)
- Grafana with Infinity plugin

### Setup Steps

1. Update validator vote account in `delegator_tracker.py`:
```python
vote_account = "YOUR_VOTE_ACCOUNT"
```

2. Make scripts executable:
```bash
chmod +x delegator_tracker.py delegator-tracker-http-server.py
```

3. Create systemd service files:

`/etc/systemd/system/delegator-tracker.service`:
```ini
[Unit]
Description=Update Delegator Data

[Service]
Type=oneshot
ExecStart=/home/chris/solana-monitoring/solana-exporter/delegator-tracker/delegator_tracker.py
User=chris
Group=chris
WorkingDirectory=/home/chris/solana-monitoring/solana-exporter/delegator-tracker
```

`/etc/systemd/system/delegator-tracker-http.service`:
```ini
[Unit]
Description=Delegator Tracker HTTP Server
After=network.target

[Service]
ExecStart=/home/chris/solana-monitoring/solana-exporter/delegator-tracker/delegator-tracker-http-server.py
Restart=always
User=chris
Group=chris
WorkingDirectory=/home/chris/solana-monitoring/solana-exporter/delegator-tracker

[Install]
WantedBy=multi-user.target
```

`/etc/systemd/system/delegator-tracker.timer`:
```ini
[Unit]
Description=Run Delegator Tracker Hourly

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

4. Enable and start services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable delegator-tracker.timer
sudo systemctl enable delegator-tracker-http.service
sudo systemctl start delegator-tracker.timer
sudo systemctl start delegator-tracker-http.service
```

## Grafana Configuration

1. Install Infinity plugin:
```bash
grafana-cli plugins install yesoreyeram-infinity-datasource
systemctl restart grafana-server
```

2. Add data source:
- Name: `delegators`
- URL: `http://localhost:8080`
- Type: `JSON`
- Parser: `Backend`

3. Create dashboard panel:
- Title: "Active Delegations (1h refresh)"
- Query:
  - Type: JSON
  - Parser: Backend
  - Root Selector: `$[-1].delegators[*]`
  - Columns:
    - Owner Address (address)
    - Stake (SOL) (amount_sol)
    - Delegator (name)
    - Epoch (activation_epoch)
    - Stake Account ID (stake_account)
    - Withdrawal Authority (withdraw_authority)

## Understanding the Data

### Stake Account Structure
Each delegation consists of:
- **Owner Address**: The wallet controlling the stake
- **Stake Account**: Unique account holding staked SOL
- **Withdrawal Authority**: Address with withdrawal permissions

### Known Delegators
The script identifies these special accounts:
- Solana Foundation (`spa8QF2uL9Z5EkYKFeVKNWjgTJgkwV5CMkdKHZwn3P6`)
- Validator Operator (`JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF`)

### JSON Data Structure
```json
[
  {
    "timestamp": "2024-04-24T07:00:00.000000",
    "total_delegators": 6,
    "total_stake_reported": 34051.172718636,
    "total_stake_captured": 35571.741800029,
    "delegators": [
      {
        "stake_account": "2vipbgjPyeKai6E7MYnC7K5fGfhuGferWSK7CshhR2ZU",
        "address": "spa8QF2uL9Z5EkYKFeVKNWjgTJgkwV5CMkdKHZwn3P6",
        "name": "Solana Foundation",
        "withdraw_authority": "mvines9iiHiQTysrwkJjGf2gb9Ex9jXJX8ns3qwf2kN",
        "amount_sol": 26519.630691842,
        "activation_epoch": "773"
      }
    ]
  }
]
```

## Monitoring

Check service status:
```bash
sudo systemctl status delegator-tracker.timer
sudo systemctl status delegator-tracker-http.service
```

View logs:
```bash
journalctl -u delegator-tracker.service
journalctl -u delegator-tracker-http.service
``` 