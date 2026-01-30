#!/bin/bash

#sudo -i
mkdir opt/
curl -LO "https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz"
tar -xvf node_exporter-0.17.0.linux-amd64.tar.gz -C opt/

cat << EOF >/etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter

[Service]
User=root
ExecStart=/home/ubuntu/opt/node_exporter-0.17.0.linux-amd64/node_exporter

[Install]
WantedBy=default.target
EOF

systemctl daemon-reload
systemctl enable node_exporter.service
systemctl start node_exporter.service
systemctl status node_exporter.service
rm -rf node_exporter-0.17.0.linux-amd64.tar.gz

