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

# Configuration
BITCOIN_RPC_HOST = os.getenv('BITCOIN_RPC_HOST', '127.0.0.1')
BITCOIN_RPC_PORT = os.getenv('BITCOIN_RPC_PORT', '8332')
BITCOIN_COOKIE_PATH = os.getenv('BITCOIN_COOKIE_PATH', '~/.bitcoin/.cookie')
METRICS_PORT = int(os.getenv('METRICS_PORT', '9332'))

# Prometheus metrics
BITCOIN_BLOCK_HEIGHT = Gauge('bitcoin_block_height', 'Current block height')
BITCOIN_VERIFICATION_PROGRESS = Gauge('bitcoin_verification_progress', 'Blockchain verification progress')
BITCOIN_DIFFICULTY = Gauge('bitcoin_difficulty', 'Current mining difficulty')
BITCOIN_MEMPOOL_SIZE = Gauge('bitcoin_mempool_size', 'Number of transactions in mempool')
BITCOIN_MEMPOOL_BYTES = Gauge('bitcoin_mempool_bytes', 'Size of mempool in bytes')
BITCOIN_PEER_COUNT = Gauge('bitcoin_peer_count', 'Number of connected peers')
BITCOIN_MEMORY_USAGE = Gauge('bitcoin_memory_usage_bytes', 'Memory usage in bytes')

def get_rpc_connection():
    """Establish RPC connection using cookie authentication by default"""
    try:
        # Try cookie authentication first
        cookie_path = os.getenv('BITCOIN_COOKIE_PATH')
        print(f"Trying cookie authentication with path: {cookie_path}")
        if os.path.exists(cookie_path):
            print(f"Cookie file exists at {cookie_path}")
            with open(cookie_path, 'r') as f:
                cookie_content = f.read().strip()
                print(f"Cookie content: {cookie_content}")
                # Parse cookie content
                if ':' in cookie_content:
                    username, password = cookie_content.split(':', 1)
                    print(f"Using cookie authentication with username: {username}")
                    return AuthServiceProxy(f"http://{username}:{password}@{os.getenv('BITCOIN_RPC_HOST')}:{os.getenv('BITCOIN_RPC_PORT')}")
                else:
                    print("Invalid cookie format")
                    raise Exception("Invalid cookie format")
        else:
            print(f"Cookie file does not exist at {cookie_path}")
            raise Exception("Cookie file not found")
    except Exception as e:
        print(f"Cookie authentication failed with error: {str(e)}")
        # Fall back to username/password if available
        rpc_user = os.getenv('BITCOIN_RPC_USER')
        rpc_password = os.getenv('BITCOIN_RPC_PASSWORD')
        if rpc_user and rpc_password:
            print("Falling back to username/password authentication")
            return AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{os.getenv('BITCOIN_RPC_HOST')}:{os.getenv('BITCOIN_RPC_PORT')}")
        raise Exception("No valid authentication method available")

def collect_metrics():
    """Collect metrics from Bitcoin Core"""
    try:
        rpc = get_rpc_connection()
        
        # Get blockchain info
        try:
            blockchain_info = rpc.getblockchaininfo()
            BITCOIN_BLOCK_HEIGHT.set(blockchain_info['blocks'])
            BITCOIN_VERIFICATION_PROGRESS.set(blockchain_info['verificationprogress'])
            BITCOIN_DIFFICULTY.set(blockchain_info['difficulty'])
            print("Successfully collected blockchain metrics")
        except Exception as e:
            print(f"Error collecting blockchain metrics: {str(e)}")
        
        # Get mempool info
        try:
            mempool_info = rpc.getmempoolinfo()
            BITCOIN_MEMPOOL_SIZE.set(mempool_info['size'])
            BITCOIN_MEMPOOL_BYTES.set(mempool_info['bytes'])
            print("Successfully collected mempool metrics")
        except Exception as e:
            print(f"Error collecting mempool metrics: {str(e)}")
        
        # Get network info
        try:
            network_info = rpc.getnetworkinfo()
            BITCOIN_PEER_COUNT.set(network_info['connections'])
            print("Successfully collected network metrics")
        except Exception as e:
            print(f"Error collecting network metrics: {str(e)}")
        
        # Get memory info
        try:
            memory_info = rpc.getmemoryinfo()
            print(f"Memory info response: {json.dumps(memory_info, indent=2)}")  # Debug print
            if isinstance(memory_info, dict):
                if 'locked' in memory_info:
                    locked_info = memory_info['locked']
                    if isinstance(locked_info, dict) and 'used' in locked_info:
                        BITCOIN_MEMORY_USAGE.set(locked_info['used'])
                        print("Successfully collected memory metrics")
                    else:
                        print(f"Unexpected locked info structure: {locked_info}")
                else:
                    print(f"Memory info keys: {memory_info.keys()}")
            else:
                print(f"Unexpected memory info type: {type(memory_info)}")
        except Exception as e:
            print(f"Error collecting memory metrics: {str(e)}")
        
    except Exception as e:
        print(f"Error in collect_metrics: {str(e)}")

def run_metrics_server():
    """Run the metrics server"""
    start_http_server(METRICS_PORT)
    print(f"Starting Bitcoin metrics collector on port {METRICS_PORT}")
    
    while True:
        collect_metrics()
        time.sleep(15)  # Collect metrics every 15 seconds

if __name__ == '__main__':
    run_metrics_server() 