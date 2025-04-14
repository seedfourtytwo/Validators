# Grafana Dashboards Configuration

## Overview
This document contains the JSON configurations for Grafana dashboards. Each dashboard is stored as a separate JSON file in the `/home/chris/solana-monitoring/grafana-config/dashboards/` directory.

## Dashboard Files
| Dashboard | File Path | Status | Last Updated |
|-----------|-----------|--------|--------------|
| System Metrics | `/home/chris/solana-monitoring/grafana-config/dashboards/system-metrics.json` | Planned | - |
| Validator Performance | `/home/chris/solana-monitoring/grafana-config/dashboards/validator-performance.json` | Planned | - |
| Network Health | `/home/chris/solana-monitoring/grafana-config/dashboards/network-health.json` | Planned | - |

## Dashboard Templates
Each dashboard JSON will follow this structure:
```json
{
  "annotations": {
    "list": []
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "links": [],
  "liveNow": false,
  "panels": [],
  "refresh": "15s",
  "schemaVersion": 38,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "UTC",
  "title": "Dashboard Title",
  "version": 0,
  "weekStart": ""
}
```

## Future Updates
1. **Dashboard Configurations**
   - [ ] System Metrics Dashboard
   - [ ] Validator Performance Dashboard
   - [ ] Network Health Dashboard

2. **Alert Configurations**
   - [ ] System Health Alerts
   - [ ] Validator Performance Alerts
   - [ ] Network Health Alerts

3. **Dashboard Features**
   - [ ] Custom Variables
   - [ ] Annotations
   - [ ] Time Range Controls
   - [ ] Refresh Settings

## Import/Export Procedures
```bash
# Export dashboard
curl -X GET "http://localhost:3000/api/dashboards/uid/{uid}" \
  -H "Authorization: Bearer {api_key}" \
  -o dashboard.json

# Import dashboard
curl -X POST "http://localhost:3000/api/dashboards/db" \
  -H "Authorization: Bearer {api_key}" \
  -H "Content-Type: application/json" \
  -d @dashboard.json
```
