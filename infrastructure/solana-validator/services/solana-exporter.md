Solana Exporter (run as sol user)
From; https://github.com/asymmetric-research/solana-exporter
Install Go to build
Service: solana-exporter
/etc/systemd/system/solana-exporter.service

Content:
[Unit]
Description=Solana Exporter for Prometheus
After=network.target

[Service]
User=sol
WorkingDirectory=/home/sol
ExecStart=/home/sol/solana-exporter/solana-exporter \
  -rpc-url http://127.0.0.1:8899 \
  -listen-address 0.0.0.0:9100
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target