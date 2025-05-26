# Solana Exporter Log WebSocket Server

This service streams live logs from the `solana-exporter` systemd service and the Bitcoin node to a web page using WebSockets.

## Endpoints

- **Solana Exporter Logs:**
  - Endpoint: `/sol-public-metrics-logs`
  - Streams logs from `journalctl -u solana-exporter.service -f`
- **Bitcoin Node Logs:**
  - Endpoint: `/bitcoin-node-logs`
  - Streams logs from `/mnt/bitcoin-node/debug.log`

Both endpoints are available on the same WebSocket server port (default: 18081).

## Features
- On connection, the last 10 log lines are sent to the client before streaming new lines in real time.
- Designed for easy extension to more log sources in the future.

## Setup

1. **Install dependencies:**
   ```sh
   npm install
   ```

2. **Run the server:**
   ```sh
   npm start
   ```
   This will start a WebSocket server on `ws://localhost:18081`.

3. **View the logs:**
   Open `public/index.html` in your browser (or serve it with a static file server).
   - The page will connect to the WebSocket and display live logs as they arrive.
   - To view Solana logs, connect to `ws://<server-ip>:18081/sol-public-metrics-logs`
   - To view Bitcoin logs, connect to `ws://<server-ip>:18081/bitcoin-node-logs`

## Running as a systemd Service

To run the log-websocket-server automatically and reliably, set it up as a systemd service:

1. **Create the service file:**
   Create `/etc/systemd/system/log-websocket-server.service` with the following content:
   ```ini
   [Unit]
   Description=Solana Exporter Log WebSocket Server
   After=network.target

   [Service]
   Type=simple
   User=chris
   WorkingDirectory=/home/chris/log-websocket-server
   ExecStart=/usr/bin/node /home/chris/log-websocket-server/server.js
   Restart=on-failure
   Environment=NODE_ENV=production

   [Install]
   WantedBy=multi-user.target
   ```
   *(Adjust `User`, `WorkingDirectory`, and `ExecStart` if your setup is different. Use `which node` to confirm the node path.)*

2. **Reload systemd and enable the service:**
   ```sh
   sudo systemctl daemon-reload
   sudo systemctl enable log-websocket-server
   sudo systemctl start log-websocket-server
   ```

3. **Check service status:**
   ```sh
   sudo systemctl status log-websocket-server
   ```

4. **View logs:**
   ```sh
   journalctl -u log-websocket-server -f
   ```

## How it works
- The server spawns `journalctl -u solana-exporter.service -f` and streams its output to all connected WebSocket clients on `/sol-public-metrics-logs`.
- The server tails `/mnt/bitcoin-node/debug.log` and streams its output to all connected WebSocket clients on `/bitcoin-node-logs`.
- The frontend connects to the desired WebSocket endpoint and appends new log lines to the page.
- On connect, the last 10 log lines are sent to the client.

## Troubleshooting
- **Permissions:**
  - The user running the Node.js server must have permission to read the systemd journal for `solana-exporter.service` and `/mnt/bitcoin-node/debug.log`.
  - If you see permission errors, try running with `sudo` or add your user to the `systemd-journal` and `bitcoin` groups:
    ```sh
    sudo usermod -aG systemd-journal $USER
    sudo usermod -aG bitcoin $USER
    sudo chmod 640 /mnt/bitcoin-node/debug.log
    ```
- **Port issues:**
  - If port 18081 is in use, change the port in `server.js` and update your Nginx proxy config.
- **Remote access:**
  - To access the log viewer from another machine, ensure port 8081 (Nginx) is open and proxied to 18081.

## Security Note
This is a simple demo and does not include authentication. For production use, consider adding access controls. 