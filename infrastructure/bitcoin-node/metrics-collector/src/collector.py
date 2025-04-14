#!/usr/bin/env python3
import os
import time
import json
from pathlib import Path
from prometheus_client import start_http_server, Gauge, Counter
from bitcoinrpc.authproxy import AuthServiceProxy
from dotenv import load_dotenv
import aiohttp
import asyncio

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
BITCOIN_PRICE_USD = Gauge('bitcoin_price_usd', 'Current Bitcoin price in USD')
BITCOIN_TIME_SINCE_LAST_BLOCK = Gauge('bitcoin_time_since_last_block_seconds', 'Time since last block in seconds')
BITCOIN_FEE_HIGH = Gauge('bitcoin_fee_high', 'Estimated fee rate for high priority - next block (sat/vB)')
BITCOIN_FEE_MEDIUM = Gauge('bitcoin_fee_medium', 'Estimated fee rate for medium priority - 3 blocks (sat/vB)')
BITCOIN_FEE_LOW = Gauge('bitcoin_fee_low', 'Estimated fee rate for low priority - 6 blocks (sat/vB)')
BITCOIN_SIZE_ON_DISK = Gauge('bitcoin_size_on_disk_bytes', 'Total blockchain size on disk in bytes')

# Network metrics
BITCOIN_NET_BYTES_SENT = Gauge('bitcoin_network_bytes_sent_total', 'Total bytes sent')
BITCOIN_NET_BYTES_RECV = Gauge('bitcoin_network_bytes_received_total', 'Total bytes received')
BITCOIN_CONN_INBOUND = Gauge('bitcoin_connections_inbound', 'Number of inbound connections')
BITCOIN_CONN_OUTBOUND = Gauge('bitcoin_connections_outbound', 'Number of outbound connections')

# Block metrics
BITCOIN_BLOCK_SIZE_MEAN = Gauge('bitcoin_block_size_bytes_mean', 'Average block size in bytes')
BITCOIN_BLOCK_TXS_MEAN = Gauge('bitcoin_block_transactions_mean', 'Average transactions per block')
BITCOIN_BLOCK_INTERVAL = Gauge('bitcoin_block_interval_seconds', 'Time between last two blocks')

# UTXO metrics
BITCOIN_UTXO_COUNT = Gauge('bitcoin_utxo_count', 'Total number of unspent transaction outputs')
BITCOIN_UTXO_SIZE = Gauge('bitcoin_utxo_size_bytes', 'Total size of UTXO set in bytes')

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
            BITCOIN_SIZE_ON_DISK.set(blockchain_info['size_on_disk'])
            
            # Get latest block time
            latest_block_hash = rpc.getbestblockhash()
            latest_block = rpc.getblock(latest_block_hash)
            time_since_last_block = time.time() - latest_block['time']
            BITCOIN_TIME_SINCE_LAST_BLOCK.set(time_since_last_block)
            print("Successfully collected blockchain metrics")
        except Exception as e:
            print(f"Error collecting blockchain metrics: {str(e)}")
        
        # Get mempool info and fee estimates
        try:
            mempool_info = rpc.getmempoolinfo()
            BITCOIN_MEMPOOL_SIZE.set(mempool_info['size'])
            BITCOIN_MEMPOOL_BYTES.set(mempool_info['bytes'])
            
            # Get fee estimates for different priorities
            # Convert BTC/kB to sat/vB (* 100000000 / 1000)
            high_priority = rpc.estimatesmartfee(1)  # Next block
            if 'feerate' in high_priority:
                BITCOIN_FEE_HIGH.set(high_priority['feerate'] * 100000)  # Convert to sat/vB
            
            medium_priority = rpc.estimatesmartfee(3)  # Within 3 blocks
            if 'feerate' in medium_priority:
                BITCOIN_FEE_MEDIUM.set(medium_priority['feerate'] * 100000)  # Convert to sat/vB
            
            low_priority = rpc.estimatesmartfee(6)  # Within 6 blocks
            if 'feerate' in low_priority:
                BITCOIN_FEE_LOW.set(low_priority['feerate'] * 100000)  # Convert to sat/vB
            
            print("Successfully collected mempool metrics")
        except Exception as e:
            print(f"Error collecting mempool metrics: {str(e)}")
        
        # Get network info with detailed stats
        try:
            network_info = rpc.getnetworkinfo()
            BITCOIN_PEER_COUNT.set(network_info['connections'])
            
            # Debug print network info
            print("Network info:", network_info)
            
            # Get network totals
            net_totals = rpc.getnettotals()
            print("Network totals:", net_totals)
            
            # Set bytes sent/received from net totals instead of networkinfo
            BITCOIN_NET_BYTES_SENT.set(net_totals.get('totalbytessent', 0))
            BITCOIN_NET_BYTES_RECV.set(net_totals.get('totalbytesrecv', 0))
            
            # Count inbound vs outbound connections more accurately
            peers_info = rpc.getpeerinfo()
            inbound = 0
            outbound = 0
            
            for peer in peers_info:
                # Debug print to see peer info structure
                print(f"Peer connection type: {peer.get('connection_type', 'unknown')}")
                
                # Check various fields that might indicate connection direction
                if (peer.get('inbound', False) or 
                    peer.get('connection_type', '') == 'inbound' or 
                    peer.get('addr_relay_enabled', False)):
                    inbound += 1
                else:
                    outbound += 1
            
            print(f"Found {inbound} inbound and {outbound} outbound connections")
            BITCOIN_CONN_INBOUND.set(inbound)
            BITCOIN_CONN_OUTBOUND.set(outbound)
            print("Successfully collected network metrics")
        except Exception as e:
            print(f"Error collecting network metrics: {str(e)}")
            
        # Get block stats
        try:
            # Get stats for last 100 blocks
            height = blockchain_info['blocks']
            block_stats = []
            for i in range(max(0, height - 100), height):
                stats = rpc.getblockstats(i)
                block_stats.append(stats)
            
            if block_stats:
                # Calculate averages
                avg_size = sum(stat['total_size'] for stat in block_stats) / len(block_stats)
                avg_txs = sum(stat['txs'] for stat in block_stats) / len(block_stats)
                BITCOIN_BLOCK_SIZE_MEAN.set(avg_size)
                BITCOIN_BLOCK_TXS_MEAN.set(avg_txs)
                
                # Calculate last block interval
                if len(block_stats) >= 2:
                    last_interval = block_stats[-1]['time'] - block_stats[-2]['time']
                    BITCOIN_BLOCK_INTERVAL.set(last_interval)
                    
            print("Successfully collected block stats")
        except Exception as e:
            print(f"Error collecting block stats: {str(e)}")
        
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
        
        # Get UTXO stats
        try:
            print("Starting UTXO stats collection...", flush=True)
            
            # First check if indexes are ready
            try:
                index_info = rpc.getindexinfo()
                print(f"Index info: {index_info}", flush=True)
                
                if not isinstance(index_info, dict):
                    print("Failed to get index info", flush=True)
                    return
                
                # Check if coinstatsindex is ready
                coinstats = index_info.get('coinstatsindex', {})
                if not coinstats.get('synced', False):
                    print(f"Coinstatsindex not ready. Current height: {coinstats.get('best_block_height', 0)}", flush=True)
                    return
                
                print("Coinstatsindex is ready, fetching UTXO stats...", flush=True)
                
                # Get UTXO stats using gettxoutsetinfo
                utxo_info = rpc.gettxoutsetinfo()
                print(f"Raw UTXO info: {utxo_info}", flush=True)
                
                if isinstance(utxo_info, dict):
                    # Extract and set metrics
                    txouts = utxo_info.get('txouts')
                    if txouts is not None:
                        print(f"Setting UTXO count: {txouts}", flush=True)
                        BITCOIN_UTXO_COUNT.set(txouts)
                    
                    disk_size = utxo_info.get('disk_size')
                    if disk_size is not None:
                        print(f"Setting UTXO size: {disk_size}", flush=True)
                        BITCOIN_UTXO_SIZE.set(disk_size)
                    
                    print(f"Final UTXO values - count: {BITCOIN_UTXO_COUNT._value.get()}, size: {BITCOIN_UTXO_SIZE._value.get()}", flush=True)
                else:
                    print(f"Unexpected UTXO info type: {type(utxo_info)}", flush=True)
            
            except Exception as e:
                print(f"Error getting UTXO stats: {str(e)}", flush=True)
                print(f"Error type: {type(e)}", flush=True)
                print(f"Full error details: {repr(e)}", flush=True)
        
        except Exception as e:
            print(f"Error in UTXO collection: {str(e)}", flush=True)
        
    except Exception as e:
        print(f"Error in collect_metrics: {str(e)}")

async def get_bitcoin_price():
    """Get Bitcoin price from Binance API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT') as response:
                if response.status == 200:
                    data = await response.json()
                    price = float(data['price'])
                    BITCOIN_PRICE_USD.set(price)
                    print(f"Successfully collected Bitcoin price: ${price:,.2f}")
                else:
                    print(f"Error getting Bitcoin price: HTTP {response.status}")
    except Exception as e:
        print(f"Error collecting Bitcoin price: {str(e)}")

async def collect_metrics_async():
    """Collect metrics asynchronously"""
    try:
        # Collect Bitcoin node metrics
        collect_metrics()
        # Collect Bitcoin price
        await get_bitcoin_price()
    except Exception as e:
        print(f"Error in collect_metrics_async: {str(e)}")

def run_metrics_server():
    """Run the metrics server"""
    start_http_server(METRICS_PORT)
    print(f"Starting Bitcoin metrics collector on port {METRICS_PORT}")
    
    async def run_forever():
        while True:
            await collect_metrics_async()
            await asyncio.sleep(15)  # Collect metrics every 15 seconds

    asyncio.run(run_forever())

if __name__ == '__main__':
    run_metrics_server() 