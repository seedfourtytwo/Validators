const WebSocket = require('ws');
const { spawn } = require('child_process');

const wss = new WebSocket.Server({ port: 8081 });

wss.on('connection', (ws) => {
  console.log('Client connected');
});

const journal = spawn('journalctl', ['-u', 'solana-exporter.service', '-f']);

journal.stdout.on('data', (data) => {
  const lines = data.toString().split('\n').filter(Boolean);
  lines.forEach(line => {
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(line);
      }
    });
  });
});

journal.stderr.on('data', (data) => {
  console.error(`journalctl error: ${data}`);
});

journal.on('close', (code) => {
  console.log(`journalctl process exited with code ${code}`);
});

console.log('WebSocket server started on ws://localhost:8081'); 