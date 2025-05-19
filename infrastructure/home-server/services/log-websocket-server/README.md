# Solana Exporter Log WebSocket Server

This service streams live logs from the `solana-exporter` systemd service to a web page using WebSockets.

## Setup

1. **Install dependencies:**
   ```sh
   npm install
   ```

2. **Run the server:**
   ```sh
   npm start
   ```
   This will start a WebSocket server on `ws://localhost:8081`.

3. **View the logs:**
   Open `public/index.html` in your browser (or serve it with a static file server).

   - The page will connect to the WebSocket and display live logs as they arrive.

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
- The server spawns `journalctl -u solana-exporter.service -f` and streams its output to all connected WebSocket clients.
- The frontend connects to the WebSocket and appends new log lines to the page.

## Troubleshooting
- **Permissions:**
  - The user running the Node.js server must have permission to read the systemd journal for `solana-exporter.service`.
  - If you see permission errors, try running with `sudo` or add your user to the `systemd-journal` group:
    ```sh
    sudo usermod -aG systemd-journal $USER
    ```
- **Port issues:**
  - If port 8081 is in use, change the port in `server.js`.
- **Remote access:**
  - To access the log viewer from another machine, ensure port 8081 is open and use your server's IP address in the frontend WebSocket URL.

## Security Note
This is a simple demo and does not include authentication. For production use, consider adding access controls. 