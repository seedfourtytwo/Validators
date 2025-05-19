# Home Router Configuration

## Network Information
- External IP: [home ip]
- Internal IP: 192.168.1.1
- Provider: SFR
- Network Performance:
  - Upload: ~95Mbps (Latency: ~75ms)
  - Download: ~95Mbps (Latency: ~250ms)

## Port Forwarding Configuration
### Ethereum Node
- P2P Sync
  - Protocol: TCP
  - Port: 30303
  - Destination: 192.168.1.210
- Peer Discovery
  - Protocol: UDP
  - Port: 30303
  - Destination: 192.168.1.210

### Web Services
- Nginx/Grafana
  - Protocol: TCP
  - Ports: 
    - 443 (HTTPS)
    - 80 (HTTP)
  - Destination: 192.168.1.210
- Log WebSocket
  - Protocol: TCP
  - Port: 8081
  - Destination: 192.168.1.210