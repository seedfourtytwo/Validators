Node Exporter (run as node_exporter user)
From; https://github.com/prometheus/node_exporter
Service: node_exporter
/etc/systemd/system/node_exporter.service

Content:
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter --web.listen-address=:9110 --collector.hwmon --collector.cpu_thermal

[Install]
WantedBy=multi-user.target