Secure Grafana Deployment with Docker and NGINX Reverse Proxy

🧱 Overview
Grafana runs in Docker.

NGINX acts as a reverse proxy to expose Grafana securely over HTTPS.

Self-signed SSL certificate is used.

Rate limiting is applied to login and API endpoints.

Grafana is served at the root URL (no subpath).


🗂 Directory Structure
solana-monitoring/
├── docker-compose.yml
├── grafana-config/
│   └── grafana.ini
├── /etc/nginx/sites-available/grafana        <- Symlinked to sites-enabled
└── /etc/nginx/ssl/
    ├── grafana.crt
    └── grafana.key

🐳 Docker Compose Configuration
File: solana-monitoring/docker-compose.yml

services:
  grafana:
    image: grafana/grafana
    container_name: solana-monitoring-grafana-1
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./grafana-config:/etc/grafana

  prometheus:
    image: prom/prometheus
    container_name: solana-monitoring-prometheus-1
    restart: unless-stopped
    ports:
      - "9090:9090"  # Optional, can be removed
    volumes:
      - prometheus-storage:/etc/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

volumes:
  grafana-storage:
  prometheus-storage:
nginx config: /etc/nginx/nginx.conf

⚙️ Grafana Configuration
File: solana-monitoring/grafana-config/grafana.ini

[server]
root_url = https://77.200.151.32/
🚫 No serve_from_sub_path is needed since Grafana is served at root /.


🌐 NGINX Reverse Proxy Configuration
File: /etc/nginx/sites-available/grafana

server {
    listen 443 ssl;
    server_name 77.200.151.32;

    ssl_certificate     /etc/nginx/ssl/grafana.crt;
    ssl_certificate_key /etc/nginx/ssl/grafana.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # Static assets: no rate limiting
    location ~ ^/public/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Cookie $http_cookie;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
    }

    # Login/API: rate-limited
    location ~ ^/(login|api|logout) {
        limit_req zone=grafana_limit burst=5 nodelay;
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Cookie $http_cookie;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
    }

    # Default fallback
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Cookie $http_cookie;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
    }
}
Also add this rate limit zone to your global NGINX config (/etc/nginx/nginx.conf or conf.d/limits.conf):

limit_req_zone $binary_remote_addr zone=grafana_limit:10m rate=10r/s;


🔐 SSL Certificate (Self-Signed)
Generated with:

sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/grafana.key \
  -out /etc/nginx/ssl/grafana.crt \
  -subj "/CN=77.200.151.32"

🧪 Validation Checklist
curl -vk https://77.200.151.32/public/build/grafana.dark.css returns 200

No redirect loops to /login

Assets like .js and .css load in browser

Login screen is styled

docker exec shows correct /etc/grafana/grafana.ini


🧰 Commands Summary
docker compose down
docker compose up -d

# Check config loaded:
docker exec -it solana-monitoring-grafana-1 grep root_url /etc/grafana/grafana.ini

# Restart nginx
gsudo nginx -t
sudo systemctl reload nginx

# Validate asset path
curl -vk https://77.200.151.32/public/build/grafana.dark.css

