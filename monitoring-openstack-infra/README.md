# OpenStack Infrastructure Monitoring

` This Project is for setting up Monitoring stack where node-exporter is installed on the VM or node you want to monitor.`

` Prometheus, Grafana and alert-manager is running in docker container using docker-compose. `

` Installation Script for Node exporter install_node_exporter.sh `

# Clone the Repo
` git clone  `

` cd openstack-infrastructure-monitoring/ `

# Make changes to prometheus.yml, alertmanager.yml, datasource.yml accordingly .
` docker-compose up -d `

` docker ps -a `

` chmod +x install_node_exporter.sh `

`./install_node_exporter.sh `

`systemctl status node_exporter.service `

`systemctl status node_exporter `

`docker build -t `

`docker run -d -p 9090:9090 prometheus:1.7 `

`docker run -d -p 3000:3000 --name grafana grafana/grafana:6.5.0 `

`docker run -v /root/prometheus/alertmanager-data:/opt/bitnami/data bitnami/alertmanager:latest `
