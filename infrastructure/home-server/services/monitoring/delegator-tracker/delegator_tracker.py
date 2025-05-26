#!/usr/bin/env python3
import json
import datetime
import os
import requests

# Directory for output files
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Your vote account
vote_account = "3TEX5gBjcZCzAz3AYT2BQrwpDTSUd5FtszPs7yx9iGGL"

# Public testnet RPC URL
rpc_url = "https://api.testnet.solana.com"

# Get delegators data from RPC
def get_delegators():
    # Get stake accounts delegated to the vote account
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getProgramAccounts",
        "params": [
            "Stake11111111111111111111111111111111111111",
            {
                "filters": [
                    {
                        "memcmp": {
                            "offset": 124,
                            "bytes": vote_account
                        }
                    }
                ],
                "encoding": "jsonParsed"
            }
        ]
    }
    
    response = requests.post(rpc_url, json=payload)
    data = response.json()
    
    if 'result' not in data:
        print(f"Error in RPC response: {data}")
        return [], 0
    
    # Parse delegators
    delegators = []
    for account in data['result']:
        try:
            stake_account = account['pubkey']
            parsed_data = account['account']['data']['parsed']['info']
            
            # Extract delegation info
            delegation = parsed_data['stake']['delegation']
            stake_amount = float(delegation['stake']) / 1_000_000_000
            activation_epoch = delegation.get('activationEpoch', 'unknown')
            
            # Extract authorities
            meta = parsed_data['meta']
            stake_authority = meta.get('authorized', {}).get('staker')
            withdraw_authority = meta.get('authorized', {}).get('withdrawer')
            
            # Get name label for known accounts
            name = "Unknown"
            if stake_authority == "spa8QF2uL9Z5EkYKFeVKNWjgTJgkwV5CMkdKHZwn3P6":
                name = "Solana Foundation"
            elif stake_authority == "JDa72CkixfF1JD9aYZosWqXyFCZwMpnVjR15bVBW2QRF":
                name = "Validator Operator"
            elif stake_authority == "973cJp85knY7bTuXEt3hRPGc4DB7W7Nbo6Egdbw3s3EF":
                name = "Validator operator"
                
            delegators.append({
                'stake_account': stake_account,
                'address': stake_authority,
                'name': name,
                'withdraw_authority': withdraw_authority,
                'amount_sol': stake_amount,
                'activation_epoch': activation_epoch
            })
        except (KeyError, TypeError) as e:
            print(f"Error parsing account {account.get('pubkey', 'unknown')}: {e}")
    
    # Get total stake
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getVoteAccounts",
        "params": []
    }
    
    response = requests.post(rpc_url, json=payload)
    data = response.json()
    
    total_stake = None
    for category in ['current', 'delinquent']:
        for validator in data['result'][category]:
            if validator['votePubkey'] == vote_account:
                total_stake = float(validator['activatedStake']) / 1_000_000_000
                break
    
    return delegators, total_stake

# Get current data
delegators, total_stake = get_delegators()

# Read existing data if it exists
output_file = os.path.join(output_dir, "delegators.json")
historical_data = []
if os.path.exists(output_file):
    try:
        with open(output_file, 'r') as f:
            existing_data = json.load(f)
            if isinstance(existing_data, list):
                historical_data = existing_data
            else:
                historical_data = [existing_data]
    except json.JSONDecodeError:
        historical_data = []

# Sort by epoch (highest first)
delegators.sort(key=lambda x: int(x.get('activation_epoch', 0)), reverse=True)

# Mark all current delegators as 'staking'
for d in delegators:
    d['status'] = 'staking'

# Load previous delegators from the last data point (if any)
previous_delegators = []
if historical_data:
    previous_delegators = historical_data[-1].get('delegators', [])

previous_accounts = set(d['stake_account'] for d in previous_delegators)
current_accounts = set(d['stake_account'] for d in delegators)

# Find unstaking accounts
unstaking_accounts = previous_accounts - current_accounts

# Add unstaking accounts to the output with status 'unstaking'
for d in previous_delegators:
    if d['stake_account'] in unstaking_accounts:
        d_copy = d.copy()
        d_copy['status'] = 'unstaking'
        delegators.append(d_copy)

# Calculate total captured stake
def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

total_captured_stake = sum(safe_float(d.get('amount_sol', 0)) for d in delegators)

# Create the current data point
current_data = {
    "timestamp": datetime.datetime.now().isoformat(),
    "total_delegators": len(delegators),
    "total_stake_reported": total_stake,
    "total_stake_captured": total_captured_stake,
    "delegators": delegators
}

# Add current data to historical data
historical_data.append(current_data)

# Keep only last 24 hours of data (assuming hourly updates)
historical_data = [d for d in historical_data 
                  if (datetime.datetime.now() - datetime.datetime.fromisoformat(d['timestamp'])).total_seconds() <= 86400]

# Write to JSON file
with open(output_file, 'w') as f:
    json.dump(historical_data, f, indent=2)

print(f"Delegator data saved to {output_file}")
print(f"Reported validator stake: {total_stake} SOL")
print(f"Captured stake: {total_captured_stake} SOL")
print(f"Number of delegators: {len(delegators)}") 