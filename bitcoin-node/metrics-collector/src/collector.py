#!/usr/bin/env python3
import os
import time
import json
from pathlib import Path
from prometheus_client import start_http_server, Gauge, Counter
from bitcoinrpc.authproxy import AuthServiceProxy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bitcoin RPC configuration
BITCOIN_RPC_HOST = os.getenv('BITCOIN_RPC_HOST', '127.0.0.1')
BITCOIN_RPC_PORT = os.getenv('BITCOIN_RPC_PORT', '8332')
BITCOIN_COOKIE_PATH = os.getenv('BITCOIN_COOKIE_PATH', str(Path.home() / '.bitcoin' / '.cookie'))
METRICS_PORT = int(os.getenv('METRICS_PORT', '9332'))

# Prometheus metrics
BLOCK_HEIGHT = Gauge('bitcoin_block_height', 'Current block height')
VERIFICATION_PROGRESS = Gauge('bitcoin_verification_progress', 'Blockchain verification progress')
DIFFICULTY = Gauge('bitcoin_difficulty', 'Current mining difficulty')
MEMPOOL_SIZE = Gauge('bitcoin_mempool_size', 'Number of transactions in mempool')
MEMPOOL_BYTES = Gauge('bitcoin_mempool_bytes', 'Size of mempool in bytes')
PEER_COUNT = Gauge('bitcoin_peer_count', 'Number of connected peers')
MEMORY_USAGE = Gauge('bitcoin_memory_usage_bytes', 'Memory usage in bytes')

def get_rpc_connection():
    """Create and return an RPC connection to Bitcoin Core using cookie authentication."""
    try:
        # Try cookie authentication first
        return AuthServiceProxy(f"http://{BITCOIN_RPC_HOST}:{BITCOIN_RPC_PORT}")
    except Exception as e:
        print(f"Cookie authentication failed: {e}")
        # Fall back to username/password if environment variables are set
        rpc_user = os.getenv('BITCOIN_RPC_USER')
        rpc_password = os.getenv('BITCOIN_RPC_PASSWORD')
        if rpc_user and rpc_password:
            return AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{BITCOIN_RPC_HOST}:{BITCOIN_RPC_PORT}")
        raise Exception("No valid authentication method available")

def collect_metrics():
    """Collect metrics from Bitcoin Core."""
    try:
        rpc = get_rpc_connection()
        
        # Get blockchain info
        blockchain_info = rpc.getblockchaininfo()
        BLOCK_HEIGHT.set(blockchain_info['blocks'])
        VERIFICATION_PROGRESS.set(blockchain_info['verificationprogress'])
        DIFFICULTY.set(blockchain_info['difficulty'])
        
        # Get mempool info
        mempool_info = rpc.getmempoolinfo()
        MEMPOOL_SIZE.set(mempool_info['size'])
        MEMPOOL_BYTES.set(mempool_info['bytes'])
        
        # Get network info
        network_info = rpc.getnetworkinfo()
        PEER_COUNT.set(network_info['connections'])
        
        # Get memory info
        memory_info = rpc.getmemoryinfo()
        MEMORY_USAGE.set(memory_info['used']['total'])
        
    except Exception as e:
        print(f"Error collecting metrics: {e}")

def main():
    """Main function to start the metrics server."""
    print(f"Starting Bitcoin metrics collector on port {METRICS_PORT}")
    start_http_server(METRICS_PORT)
    
    while True:
        collect_metrics()
        time.sleep(15)  # Collect metrics every 15 seconds

if __name__ == '__main__':
    main() 