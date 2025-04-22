# Nginx Reverse Proxy Setup

## Overview
This document describes the Nginx reverse proxy configuration used to securely expose Grafana and other services via HTTPS at metric.seed42.co. The setup includes SSL certificate generation, rate limiting, and security hardening.

## Current Status
| Component | Status | Notes |
|-----------|---------|-------|
| Nginx | Running | System service |
| SSL Certificate | Active | Self-signed certificate |
| Grafana Proxy | Active | HTTPS at metrics.seed42.co |
| Rate Limiting | Active | Applied to login and logout endpoints |

## Directory Structure
```
/etc/nginx/
├── nginx.conf
├── sites-available/
│   └── grafana
├── sites-enabled/
│   └── grafana -> ../sites-available/grafana
└── ssl/
    ├── grafana.crt
    └── grafana.key
```

## Nginx Configuration

### Main Configuration
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

### Grafana Site Configuration
File: `/etc/nginx/sites-available/grafana`
```nginx
server {
    listen 443 ssl;
    server_name [home ip];

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
```

## HTTP to HTTPS Redirection
The current configuration does not include an explicit HTTP to HTTPS redirection. To implement this, you would need to add a separate server block that listens on port 80 and redirects all HTTP traffic to HTTPS. Here's how to implement it:

```nginx
# Add this server block to /etc/nginx/sites-available/grafana
server {
    listen 80;
    server_name [home ip];
    return 301 https://$server_name$request_uri;
}
```

This server block:
1. Listens on port 80 (HTTP)
2. Matches the same server_name as the HTTPS server
3. Returns a 301 (permanent) redirect to the same URL but with HTTPS
4. Preserves the original request URI

After adding this configuration, all HTTP traffic will be automatically redirected to HTTPS, ensuring that users always access the service securely.

## SSL Certificate Generation

### Self-Signed Certificate
```bash
# Create SSL directory
sudo mkdir -p /etc/nginx/ssl

# Generate self-signed certificate
sudo openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/grafana.key \
  -out /etc/nginx/ssl/grafana.crt \
  -subj "/CN=[home ip]"
```

### Let's Encrypt Certificate (Future)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d [home ip]

# Auto-renewal is configured by default
```

## Security Hardening

### Nginx Security Headers
Add to server block in site configuration:
```nginx
# Security headers
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options SAMEORIGIN;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### SSL Configuration
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

## Maintenance Procedures

### Configuration Testing
```bash
# Test Nginx configuration
sudo nginx -t

# Reload Nginx after changes
sudo systemctl reload nginx
```

### Certificate Renewal
```bash
# Check certificate expiration
sudo openssl x509 -in /etc/nginx/ssl/grafana.crt -noout -dates

# Renew Let's Encrypt certificate (when implemented)
sudo certbot renew
```

### Log Analysis
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

### Common Issues
1. **502 Bad Gateway**
   - Check if Grafana is running
   - Verify port 3000 is accessible
   - Check firewall settings

2. **SSL Certificate Errors**
   - Verify certificate paths
   - Check certificate expiration
   - Ensure proper permissions

3. **Rate Limiting Issues**
   - Check rate limit configuration
   - Verify client IP detection
   - Review burst settings

### Debugging Commands
```bash
# Check Nginx status
sudo systemctl status nginx

# View open ports
sudo netstat -tulpn | grep nginx

# Test SSL configuration
curl -vI https://[home ip]
```
