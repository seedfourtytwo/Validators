Agave (run as sol user)
From: https://github.com/anza-xyz/agave
Config:
 /home/sol/.config/solana/cli/config.yml

Content:
Config File: /home/sol/.config/solana/cli/config.yml
RPC URL: https://api.testnet.solana.com
WebSocket URL: wss://api.testnet.solana.com/ (computed)
Keypair Path: /home/sol/wallets/validator-identity.json
Commitment: confirmed
Service: 
validator.service
/etc/systemd/system/solana-validator.service

Content:
[Unit]
Description=Solana Validator
After=network.target network-online.target
Wants=network-online.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
LimitNOFILE=2000000
LogRateLimitIntervalSec=0
User=sol
Environment=SOLANA_METRICS_CONFIG=host=https://metrics.solana.com:8086,db=testnet,u=testnet_write,p=password
Environment=PATH=/home/sol/.local/share/solana/install/active_release/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/sol/start-validator.sh
[Install]
WantedBy=multi-user.target
Startup Script:
/home/sol/start-validator.sh

Content:
#!/bin/bash
exec agave-validator \
  --identity ~/wallets/validator-identity.json \
  --vote-account 3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL \
  --entrypoint entrypoint.testnet.solana.com:8001 \
  --entrypoint entrypoint2.testnet.solana.com:8001 \
  --entrypoint entrypoint3.testnet.solana.com:8001 \
  --known-validator 5D1fNXzvv5NjV1ysLjirC4WY92RNsVH18vjmcszZd8on \
  --known-validator dDzy5SR3AXdYWVqbDEkVFdvSPCtS9ihF5kJkHCtXoFs \
  --known-validator Ft5fbkqNa76vnsjYNwjDZUXoTWpP7VYm3mtsaQckQADN \
  --known-validator eoKpUABi59aT4rR9HGS3LcMecfut9x7zJyodWWP43YQ \
  --known-validator 9QxCLckBiJc783jnMvXZubK4wH86Eqqvashtrwvcsgkv \
  --expected-genesis-hash 4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY \
  --only-known-rpc \
  --rpc-port 8899 \
  --private-rpc \
  --dynamic-port-range 8000-8020 \
  --wal-recovery-mode skip_any_corrupted_record \
  --ledger ~/ledger \
  --accounts ~/accounts \
  --snapshots ~/snapshots \
  --log ~/log/validator.log \
  --limit-ledger-size