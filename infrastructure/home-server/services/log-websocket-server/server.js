const http = require('http');
const WebSocket = require('ws');
const { spawn } = require('child_process');

// Buffers for last N log lines
const solanaLogBuffer = [];
const bitcoinLogBuffer = [];
const MAX_BUFFER = 10;

// Create a single HTTP server
const server = http.createServer();

// Solana logs WebSocket server
const wssSolana = new WebSocket.Server({ noServer: true });
wssSolana.on('connection', (ws) => {
  console.log('Client connected to /sol-public-metrics-logs');
  // Send the last 10 lines on connect
  solanaLogBuffer.forEach(line => ws.send(line));
});

// Bitcoin logs WebSocket server
const wssBitcoin = new WebSocket.Server({ noServer: true });
wssBitcoin.on('connection', (ws) => {
  console.log('Client connected to /bitcoin-node-logs');
  // Send the last 10 lines on connect
  bitcoinLogBuffer.forEach(line => ws.send(line));
});

// Handle upgrade requests for different endpoints
server.on('upgrade', (request, socket, head) => {
  if (request.url === '/sol-public-metrics-logs') {
    wssSolana.handleUpgrade(request, socket, head, (ws) => {
      wssSolana.emit('connection', ws, request);
    });
  } else if (request.url === '/bitcoin-node-logs') {
    wssBitcoin.handleUpgrade(request, socket, head, (ws) => {
      wssBitcoin.emit('connection', ws, request);
    });
  } else {
    socket.destroy();
  }
});

// Stream Solana exporter logs
const solanaJournal = spawn('journalctl', ['-u', 'solana-exporter.service', '-f']);
solanaJournal.stdout.on('data', (data) => {
  const lines = data.toString().split('\n').filter(Boolean);
  lines.forEach(line => {
    solanaLogBuffer.push(line);
    if (solanaLogBuffer.length > MAX_BUFFER) solanaLogBuffer.shift();
    wssSolana.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(line);
      }
    });
  });
});
solanaJournal.stderr.on('data', (data) => {
  console.error(`journalctl error: ${data}`);
});

// Stream Bitcoin node logs
const btcLog = spawn('tail', ['-F', '/mnt/bitcoin-node/debug.log']);
btcLog.stdout.on('data', (data) => {
  const lines = data.toString().split('\n').filter(Boolean);
  lines.forEach(line => {
    bitcoinLogBuffer.push(line);
    if (bitcoinLogBuffer.length > MAX_BUFFER) bitcoinLogBuffer.shift();
    wssBitcoin.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(line);
      }
    });
  });
});
btcLog.stderr.on('data', (data) => {
  console.error(`tail error: ${data}`);
});

// Start the HTTP/WebSocket server
const PORT = 18081;
server.listen(PORT, () => {
  console.log(`WebSocket server started on ws://localhost:${PORT}`);
  console.log(`  Solana logs:  ws://localhost:${PORT}/sol-public-metrics-logs`);
  console.log(`  Bitcoin logs: ws://localhost:${PORT}/bitcoin-node-logs`);
  // Future: Add more endpoints for system logs, etc.
}); 