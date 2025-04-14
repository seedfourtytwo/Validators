# 🧬 Solana Validator

Testnet Solana validator running on dedicated bare metal hardware with secure key management and optimized performance.

## 📊 Status & Identity
- **Network**: Testnet
- **Validator Identity**: [JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF](https://www.validators.app/validators/JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF?locale=en&network=testnet)
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
- **Validator**: [Agave](services/agave.md) (Solana client)
- **Metrics**: 
  - [Node Exporter](services/node-exporter.md)
  - [Solana Exporter](services/solana-exporter.md)
  - [Public Dashboard](https://metric.seed42.co/goto/0_8z3r0HR?orgId=1)

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

# Monitoring
agave-validator --ledger ~/ledger monitor
solana catchup --our-localhost --keypair ~/wallets/validator-identity.json

# Log Check
grep -E 'ERROR|WARN' ~/log/validator.log
```

## 📚 Additional Resources
- [Setup Tutorials](../setup-tutorials/)

## 🙏 Acknowledgments
> Special thanks to [Nordstar](https://nordstar.one/) for his invaluable help and guidance on Discord in setting up this validator. 
> Don't hesitate to delegat to them

## 🚀 Next Major Milestone
> **Important**: The next critical step in our validator setup will be implementing MEV (Maximal Extractable Value) capabilities through JITO integration on testnet. This will enable:
> - Enhanced block building and propagation via JITO's testnet infrastructure
> - Access to JITO's MEV infrastructure for testing and development
> - Integration with JITO's block builder network on testnet
> - Testing of MEV strategies in a safe environment before mainnet deployment