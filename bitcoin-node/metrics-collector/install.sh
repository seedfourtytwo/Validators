#!/bin/bash

# Exit on error
set -e

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
    echo "Please edit .env with your specific configuration"
fi

# Create systemd service file
sudo tee /etc/systemd/system/bitcoin-metrics.service << EOF
[Unit]
Description=Bitcoin Metrics Collector
After=bitcoind.service
Requires=bitcoind.service

[Service]
Type=simple
User=bitcoin
Group=bitcoin
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=$(pwd)/venv/bin/python src/collector.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable bitcoin-metrics
sudo systemctl start bitcoin-metrics

echo "Installation complete. Check status with: sudo systemctl status bitcoin-metrics" 