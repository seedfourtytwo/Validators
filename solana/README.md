# 🧬 Solana Validator

Testnet Solana validator running on dedicated bare metal. Built from source, secured with offline key management and full monitoring.

---
The server is rented from https://www.fiberstate.com/ at a cost of USD 135.95/Month

## 🧱 Hardware & Specs

| Component       | Details                                  |
|----------------|-------------------------------------------|
| **IP Address**  | `38.97.62.158`                            |
| **OS**          | Ubuntu 24.04                              |
| **CPU**         | AMD Ryzen 9 7950X (16 Cores / 32 Threads) |
| **RAM**         | 128 GB DDR5                               |
| **Storage**     | 2 TB NVMe + 1 TB NVMe + 1 TB NVMe         |
| **Network**     | 10 Gbps (330 TB/month usage cap)          |

---

## 🛠️ OS & Core System Setup

- OS: Ubuntu 22.04
- SSH: Hardened (key-only, no root)
- Users: validator-admi / admin-backup / sol / node_exporter
- Swap: disabled
- Firewall: UFW or `nftables`

---

## 🚀 Solana Installation & Configuration

1. Install Rust and build Solana from source.
2. Configure service: [See `validator.service.md`](./validator.service.md)
3. Generate validator/vote keys on air-gapped system.
4. Sync and join the mainnet-beta cluster.

---

## 🌐 Network

| Port        | Protocol | Use                     |
|-------------|----------|--------------------------|
| 8000–10000  | UDP      | TPU (Transaction layer)  |
| 8899        | TCP      | JSON-RPC (local only)    |
| 8900        | TCP      | Gossip                   |
| 22          | TCP      | SSH (restricted)         |

- RPC not exposed publicly
- Fail2ban + port access control in place

---

## 📊 Monitoring

→ See [`../../infrastructure/monitoring.md`](../../infrastructure/monitoring.md)

- Node Exporter + Prometheus
- Solana metrics exposed
- Grafana dashboards
- Alerts on validator performance and uptime

---

## 🔐 Security Measures

- Cold wallet storage
- SSH audit with [`ssh-audit`](https://github.com/jtesta/ssh-audit)
- Aggressive `fail2ban` config
- Physical protection at colocation site

---

## 📌 Status

| Metric           | Value       |
|------------------|-------------|
| Cluster          | mainnet-beta|
| Uptime           | XX days     |
| Last Restart     | YYYY-MM-DD  |
| Stake (if any)   | N/A (Test)  |

---

## 🧪 Rebuilding from Scratch

See [../../docs/rebuild.md](../../docs/rebuild.md) for full steps if this server needs to be rebuilt.
