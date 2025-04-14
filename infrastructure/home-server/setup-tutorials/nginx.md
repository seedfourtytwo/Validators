# Nginx Setup Tutorial

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Directory Structure Setup](#directory-structure-setup)
4. [Configuration Files](#configuration-files)
5. [SSL Certificate Generation](#ssl-certificate-generation)
6. [Firewall Configuration](#firewall-configuration)
7. [Reverse Proxy Setup](#reverse-proxy-setup)
8. [Security Hardening](#security-hardening)
9. [Maintenance & Management](#maintenance--management)
10. [Troubleshooting](#troubleshooting)

## Prerequisites
- Ubuntu/Debian-based system
- Root or sudo access
- Domain name (metric.seed42.co) pointing to your server
- Basic understanding of Nginx configuration
- Access to ports 80 and 443

## Installation

### 1. Install Nginx
```bash
# Update package lists
sudo apt update

# Install Nginx
sudo apt install nginx -y

# Verify installation
nginx -v
```

### 2. Start and Enable Nginx
```bash
# Start Nginx
sudo systemctl start nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

## Directory Structure Setup
```bash
# Create SSL directory
sudo mkdir -p /etc/nginx/ssl

# Create sites-available and sites-enabled directories if they don't exist
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# Set proper permissions
sudo chown -R www-data:www-data /etc/nginx/ssl
sudo chmod -R 600 /etc/nginx/ssl
```

## Configuration Files

### 1. Main Nginx Configuration
File: `/etc/nginx/nginx.conf`
```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;

error_log /var/log/nginx/error.log;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
    # multi_accept on;
}

http {
    ##
    # Basic Settings
    ##

    # Rate limit for selected locations (login/logout)
    limit_req_zone $binary_remote_addr zone=grafana_limit:10m rate=10r/s;

    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    # server_tokens off;

    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ##
    # SSL Settings
    ##

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
    ssl_prefer_server_ciphers on;

    ##
    # Logging Settings
    ##

    access_log /var/log/nginx/access.log;

    ##
    # Gzip Settings
    ##

    gzip on;

    # gzip_vary on;
    # gzip_proxied any;
    # gzip_comp_level 6;
    # gzip_buffers 16 8k;
    # gzip_http_version 1.1;
    # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    ##
    # Virtual Host Configs
    ##

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 2. Grafana Site Configuration
File: `/etc/nginx/sites-available/grafana`
```nginx
server {
    listen 443 ssl;
    server_name metric.seed42.co;

    ssl_certificate     /etc/nginx/ssl/grafana.crt;
    ssl_certificate_key /etc/nginx/ssl/grafana.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # Optional: Log 503s for debugging
    error_page 503 @custom_503;
    location @custom_503 {
        access_log /var/log/nginx/grafana_503.log;
        return 503;
    }

    # Static assets (not rate-limited)
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

    # API - not rate limited to avoid dashboard errors
    location ~ ^/api/ {
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

    # Login/Logout - rate limited
    location ~ ^/(login|logout) {
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

    # Everything else
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

# HTTP to HTTPS redirection
server {
    listen 80;
    server_name metric.seed42.co;
    return 301 https://$server_name$request_uri;
}
```

### 3. Enable Site Configuration
```bash
# Create symbolic link to enable the site
sudo ln -s /etc/nginx/sites-available/grafana /etc/nginx/sites-enabled/

# Remove default site if it exists
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## SSL Certificate Generation

### 1. Self-Signed Certificate
```bash
# Generate self-signed certificate
sudo openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/grafana.key \
  -out /etc/nginx/ssl/grafana.crt \
  -subj "/CN=metric.seed42.co"
```

### 2. Let's Encrypt Certificate (Recommended for Production)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d metric.seed42.co

# Auto-renewal is configured by default
# Test auto-renewal
sudo certbot renew --dry-run
```

## Firewall Configuration

### 1. Required Ports
| Port | Service | Direction | Purpose |
|------|---------|-----------|----------|
| 80 | HTTP | Inbound | HTTP to HTTPS redirection |
| 443 | HTTPS | Inbound | Secure web access |

### 2. NFTables Configuration
File: `/etc/nftables.conf`
```bash
# Add to your existing nftables configuration
table inet filter {
    chain input {
        # Allow HTTP and HTTPS
        tcp dport 80 accept
        tcp dport 443 accept
    }
}
```

### 3. Apply NFTables Rules
```bash
# Test the configuration
sudo nft -f /etc/nftables.conf

# If test is successful, apply the rules
sudo nft -f /etc/nftables.conf

# Verify rules
sudo nft list ruleset
```

## Reverse Proxy Setup

### 1. Grafana Configuration
Ensure Grafana is configured to work with the reverse proxy:

File: `/home/chris/solana-monitoring/grafana-config/grafana.ini`
```ini
[server]
root_url = https://metric.seed42.co/
serve_from_sub_path = false

[auth.anonymous]
enabled = false
```

### 2. Docker Compose Configuration
Update your Docker Compose file to use host networking:

File: `/home/chris/solana-monitoring/docker-compose.yml`
```yaml
services:
  grafana:
    image: grafana/grafana
    container_name: solana-monitoring-grafana-1
    restart: unless-stopped
    network_mode: host
    environment:
      - GF_SERVER_ROOT_URL=https://metric.seed42.co/
      - GF_SERVER_SERVE_FROM_SUB_PATH=true
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./grafana-config:/etc/grafana
```

## Security Hardening

### 1. Nginx Security Headers
Add to server block in site configuration:
```nginx
# Security headers
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options SAMEORIGIN;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### 2. SSL Configuration
Add to server block in site configuration:
```nginx
# SSL configuration
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;
ssl_stapling off;
ssl_stapling_verify off;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

### 3. Rate Limiting
The configuration already includes rate limiting for login/logout endpoints:
```nginx
# Rate limit for selected locations (login/logout)
limit_req_zone $binary_remote_addr zone=grafana_limit:10m rate=10r/s;
```

## Maintenance & Management

### 1. Configuration Testing
```bash
# Test Nginx configuration
sudo nginx -t

# Reload Nginx after changes
sudo systemctl reload nginx
```

### 2. Certificate Renewal
```bash
# Check certificate expiration
sudo openssl x509 -in /etc/nginx/ssl/grafana.crt -noout -dates

# Renew Let's Encrypt certificate (when implemented)
sudo certbot renew
```

### 3. Log Analysis
```bash
# View access logs
sudo tail -f /var/log/nginx/access.log

# View error logs
sudo tail -f /var/log/nginx/error.log

# Check for rate limiting
sudo grep "limiting requests" /var/log/nginx/error.log

# Check for 503 errors (specific to Grafana)
sudo tail -f /var/log/nginx/grafana_503.log
```

## Troubleshooting

### 1. Common Issues

#### 502 Bad Gateway
```bash
# Check if Grafana is running
docker ps | grep grafana

# Verify port 3000 is accessible
nc -zv localhost 3000

# Check firewall settings
sudo nft list ruleset
```

#### SSL Certificate Errors
```bash
# Verify certificate paths
ls -la /etc/nginx/ssl/

# Check certificate expiration
sudo openssl x509 -in /etc/nginx/ssl/grafana.crt -noout -dates

# Ensure proper permissions
sudo chmod 600 /etc/nginx/ssl/grafana.key
sudo chmod 644 /etc/nginx/ssl/grafana.crt
```

#### Rate Limiting Issues
```bash
# Check rate limit configuration
grep -A 5 "limit_req_zone" /etc/nginx/nginx.conf

# Verify client IP detection
curl -I https://metric.seed42.co/login

# Review burst settings
grep -A 5 "limit_req zone=grafana_limit" /etc/nginx/sites-available/grafana
```

### 2. Debugging Commands
```bash
# Check Nginx status
sudo systemctl status nginx

# View open ports
sudo netstat -tulpn | grep nginx

# Test SSL configuration
curl -vI https://metric.seed42.co
```

### 3. Reset Procedures
```bash
# Stop Nginx
sudo systemctl stop nginx

# Backup configuration
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
sudo cp /etc/nginx/sites-available/grafana /etc/nginx/sites-available/grafana.backup

# Restore from backup
sudo cp /etc/nginx/nginx.conf.backup /etc/nginx/nginx.conf
sudo cp /etc/nginx/sites-available/grafana.backup /etc/nginx/sites-available/grafana

# Start Nginx
sudo systemctl start nginx
``` 