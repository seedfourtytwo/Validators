Docker
Client: Docker Engine - Community

Docker Compose config file:
/home/chris/solana-monitoring/docker-compose.yml
version: "3.8"
services:
  grafana:
    image: grafana/grafana
    container_name: solana-monitoring-grafana-1
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SERVER_ROOT_URL=https://77.200.151.32/
      - GF_SERVER_SERVE_FROM_SUB_PATH=true
    volumes:
      - grafana-storage:/var/lib/grafana
  prometheus:
    image: prom/prometheus
    container_name: solana-monitoring-prometheus-1
    restart: unless-stopped
    ports:
      - "9090:9090"  # REMOVE this if Prometheus is internal-only and not needed outside
    volumes:
      - prometheus-storage:/etc/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
volumes:
  grafana-storage:
  prometheus-storage:
 Version: 28.0.4
Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.22.0
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.34.0
    Path:     /usr/libexec/docker/cli-plugins/docker-compose
Server:
 Containers: 2
  Running: 2
  Paused: 0
  Stopped: 0
 Images: 2
 Server Version: 28.0.4
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 05044ec0a9a75232cad458027ca83437aae3f4da
 runc version: v1.2.5-0-g59923ef
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.8.0-57-generic
 Operating System: Ubuntu 24.04.2 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 20
 Total Memory: 62.57GiB
 Name: ubuntu
 ID: ec44e3e9-9f6f-4017-be25-5ef311243831
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
