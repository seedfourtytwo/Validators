# 🧬 Solana Validator

Testnet Solana validator running on dedicated bare metal.

---
The server is rented from https://www.fiberstate.com/ at a cost of USD 135.95/Month

## 🧱 Hardware & Specs

| Component       | Details                                   |
|----------------|--------------------------------------------|
| **IP Address**  | `38.97.62.158`                            |
| **OS**          | Ubuntu 24.04                              |
| **CPU**         | AMD Ryzen 9 7950X (16 Cores / 32 Threads) |
| **RAM**         | 128 GB DDR5                               |
| **Storage**     | 2 TB NVMe + 1 TB NVMe + 1 TB NVMe         |
| **Network**     | 10 Gbps (330 TB/month usage cap)          |

---
Ubuntu is setup and tailored specifically for Solana
 - Optimization  (link to /linux-config/optimization.md)
 - Disk setup (link to /linux-config/disk-management.md)
 - log-rotation (link to /linux-config/log-rotation.md)

We are running 3 main services:
Agave - the Solana client (link to /services/agave.md)
Node exporter - exports live hardware information for monitoring (link to /services/node-exporter.md)
Solana exporter - exports Solana related metrics for monitoring (link to /services/solana-exporter.md)

The server is behinf a firewall that only allows the needed traffic - see (link to /linux-config/firewall)





Start stop and monitor:

sudo systemctl start validator.service
sudo systemctl stop validator.service
sudo systemctl restart validator.service


Once started check the status with
agave-validator --ledger ~/ledger monitor
and
solana catchup --our-localhost --keypair ~/wallets/validator-identity.json

Tail logs for warning with
grep --extended-regexp 'ERROR|WARN' ~/log/validator.log



## 🌐 Network

| Port        | Protocol | Use                     |
|-------------|----------|--------------------------|
| 8000–10000  | UDP      | TPU (Transaction layer)  |
| 8899        | TCP      | JSON-RPC (local only)    |
| 8900        | TCP      | Gossip                   |
| 22          | TCP      | SSH (restricted)         |

- RPC not exposed publicly
