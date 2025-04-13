#!/bin/bash

# Exit on any error
set -e

# Check if running as bitcoin user
if [ "$(whoami)" != "bitcoin" ]; then
    echo "This script must be run as the bitcoin user"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create systemd service directory if it doesn't exist
mkdir -p ~/.config/systemd/user/

# Create the systemd service file
cat > ~/.config/systemd/user/bitcoin-metrics.service << EOL
[Unit]
Description=Bitcoin Metrics Collector
After=bitcoind.service
Requires=bitcoind.service

[Service]
Type=simple
User=bitcoin
Group=bitcoin
WorkingDirectory=/home/bitcoin/bitcoin-metrics
Environment=PATH=/home/bitcoin/bitcoin-metrics/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/bitcoin/bitcoin-metrics/venv/bin/python src/collector.py
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOL

# Enable lingering for the bitcoin user (allows services to run after user logout)
sudo loginctl enable-linger bitcoin

# Reload systemd user daemon
systemctl --user daemon-reload

# Enable and start the service
systemctl --user enable bitcoin-metrics.service
systemctl --user start bitcoin-metrics.service

echo "Installation complete!"
echo "Service status:"
systemctl --user status bitcoin-metrics.service 