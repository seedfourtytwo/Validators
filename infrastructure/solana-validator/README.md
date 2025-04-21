# 🧬 Solana Validator

Testnet Solana validator running on dedicated bare metal hardware with secure key management and optimized performance.

## 📊 Status & Identity
- **Network**: Testnet
- **Validator Identity**: [JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF](https://www.validators.app/validators/JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF?locale=en&network=testnet) 🔗
- **Vote Account**: `3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL`
- **Program**: [Solana Foundation Delegation Program (SFDP)](https://solana.com/foundation/delegation-program)

## 🔑 Key Management
Validator keys are managed using secure cold storage procedures:
- [Cold Key Generation & Management](cold-key-management.md)
- Identity and vote account keys follow BIP44 standard

> Note: Current keys use recovery path `m/44'/501'/0'/0'`  
> Recovery command:  
> ```bash
> solana-keygen recover 'prompt://?full-path=m/44'/501'/0'/0'' --outfile keypair.json
> ```

## 🧱 Hardware Specifications
| Component | Details |
|-----------|---------|
| CPU | AMD Ryzen 9 7950X (16C/32T) |
| RAM | 128 GB DDR5 |
| Storage | 2 TB NVMe + 2x 1 TB NVMe |
| Network | 10 Gbps (330 TB/month) |
| Location | Fiberstate Datacenter |

## 🔧 Core Services
- **Validator**: [JITO](services/jito.md) (Solana client with MEV capabilities)
- **Previous Implementation**: [Agave](services/agave.md) (Standard Solana client)
- **Metrics**: 
  - [Node Exporter](services/monitoring/node-exporter.md)
  - [Node Exporter Metrics Reference](services/monitoring/node-exporter-metrics-reference.md)
  - [Solana Exporter](services/monitoring/solana-exporter.md)
  - [Metrics Reference](services/monitoring/metrics-reference.md)
  - [Public Dashboard](https://metric.seed42.co/public-dashboards/94ca941675e947cb877619494cf95d80)

## 🌐 Network Configuration
| Port | Protocol | Use | Access |
|------|----------|-----|---------|
| 8000–10000 | UDP | TPU | Public |
| 8899 | TCP | RPC | Local |
| 8900 | TCP | Gossip | Public |
| 22 | TCP | SSH | Restricted |

## ⚙️ System Configuration
- [System Optimization](linux-config/optimization.md)
- [Disk Management](linux-config/disk-management.md)
- [Log Rotation](linux-config/log-rotation.md)
- [Firewall Rules](linux-config/firewall.md)
- [SSH Configuration](linux-config/ssh.md)
- [Users & Groups](linux-config/users-groups.md)
- [File Structure](linux-config/file-structure.md)

## 🛠️ Quick Commands
```bash
# Service Control
sudo systemctl {start|stop|restart} validator.service

# Switch between JITO and Agave
sudo sed -i 's/VALIDATOR_TYPE=jito/VALIDATOR_TYPE=agave/' /etc/default/validator  # Switch to Agave
sudo sed -i 's/VALIDATOR_TYPE=agave/VALIDATOR_TYPE=jito/' /etc/default/validator  # Switch to JITO
sudo systemctl restart validator.service

# Monitoring
grep -a "tip" /home/sol/validators/data/log/validator.log | grep "payment"  # Check JITO MEV activity
solana catchup --url https://api.testnet.solana.com JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF  # Check catchup status
curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1, "method":"getBlockHeight"}' http://localhost:8899  # Check local height
/home/sol/validators/jito/active --ledger /home/sol/validators/data/ledger monitor  # Monitor validator directly

# Log Check
grep -E 'ERROR|WARN' /home/sol/validators/data/log/validator.log
tail -f /home/sol/validators/data/log/validator.log

# Metrics
curl -s localhost:9100/metrics | grep solana_validator_active_stake  # Check active stake
```

## 📚 Additional Resources
- [Setup Tutorials](setup-tutorials/)
- [JITO Configuration Guide](services/jito.md)

## 🙏 Acknowledgments
> Special thanks to [Nordstar](https://nordstar.one/) 🔗 for his invaluable help and guidance on Discord in setting up this validator. 
> Don't hesitate to delegate to them.

## 🚀 Next Major Milestone
- **Important**: Having successfully implemented JITO MEV capabilities on our testnet validator, our next focus is:
- Optimizing MEV rewards through enhanced monitoring and performance tuning
- Preparing for potential mainnet deployment with increased stake
- Implementing advanced alerting for MEV opportunities and performance metrics
- Exploring additional validator services and infrastructure improvements