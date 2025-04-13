## Bitcoin Core Full Node Setup on Linux (from Source)

### ✅ Goal

Deploy a production-grade, secure Bitcoin full node on a Linux server:

- Built from source with PGP verification
    
- Dedicated user + disk partition
    
- `systemd` managed
    
- Hardened permissions
    
- Syncing from Genesis block (mainnet)
    

---

### 🧰 Environment

- **User**: `bitcoin` (non-privileged)
    
- **Data directory**: `/mnt/bitcoin-node` (on dedicated HDD partition)
    
- **Binary install location**: `/opt/bitcoin`
    
- **OS**: Ubuntu Server (no desktop)
    
- **Firewall**: `nftables` (with P2P port 8333 opened)
    

---

## 1️⃣ Partitioning & Filesystem Prep

Disk was partitioned with `fdisk` into two ext4 partitions:

- `/mnt/archive` (5.9TB)
    
- `/mnt/bitcoin-node` (5TB)
    

Mounted via `/etc/fstab` with options:

fstab

CopyEdit

`UUID=... /mnt/bitcoin-node ext4 defaults,noatime,nodiratime 0 2`

Formatted with:

bash

CopyEdit

`sudo mkfs.ext4 /dev/sdb1 sudo mkdir -p /mnt/bitcoin-node sudo chown bitcoin:bitcoin /mnt/bitcoin-node`

---

## 2️⃣ Build Bitcoin Core from Source

### 📥 Download and Verify

bash

CopyEdit

`git clone https://github.com/bitcoin/bitcoin.git cd bitcoin git checkout v28.1 git verify-tag v28.1`

Import key if needed:

bash

CopyEdit

`gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys 152812300785C96444D3334D17565732E08E5E41`

### ⚙️ Build

bash

CopyEdit

`./autogen.sh ./configure --without-gui --disable-tests --disable-bench --enable-wallet make -j$(nproc)`

### 🚚 Deploy the Binaries

bash

CopyEdit

`sudo mkdir -p /opt/bitcoin sudo cp src/bitcoind src/bitcoin-cli /opt/bitcoin/ sudo chown root:root /opt/bitcoin/* sudo chmod 755 /opt/bitcoin/*`

---

## 3️⃣ Systemd Service

Create `/etc/systemd/system/bitcoind.service`:

ini

CopyEdit

`[Unit] Description=Bitcoin daemon After=network.target  [Service] User=bitcoin Group=bitcoin ExecStart=/opt/bitcoin/bitcoind -datadir=/mnt/bitcoin-node -nodaemon ExecStop=/opt/bitcoin/bitcoin-cli -datadir=/mnt/bitcoin-node stop Type=simple Restart=on-failure PrivateTmp=true ProtectHome=true NoNewPrivileges=true  [Install] WantedBy=multi-user.target`

Then reload and start:

bash

CopyEdit

`sudo systemctl daemon-reexec sudo systemctl daemon-reload sudo systemctl start bitcoind sudo systemctl enable bitcoind`

---

## 4️⃣ Config File (Optional)

Place at `/mnt/bitcoin-node/bitcoin.conf`:

ini

CopyEdit

`server=1 daemon=0 txindex=1 rpcuser=bitcoinrpc rpcpassword=your_secure_password`

You can generate a secure RPC password:

bash

CopyEdit

`xxd -l 16 -p /dev/urandom`

---

## 5️⃣ Firewall (nftables)

Allow incoming P2P port (8333) + LAN-only RPC if needed:

nftables

CopyEdit

`tcp dport 8333 accept`

---

## 6️⃣ Monitoring Sync Progress

Manual check:

bash

CopyEdit

`bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo`

Auto-refresh:

bash

CopyEdit

`watch -n 10 'bitcoin-cli -datadir=/mnt/bitcoin-node getblockchaininfo | grep -E "blocks|headers|verificationprogress"'`

Example output:

json

CopyEdit

`"blocks": 32161, "headers": 891895, "verificationprogress": 0.000027,`

---

## 📌 Notes

- Full blockchain size: ~600GB+ as of 2025
    
- Initial sync (IBD) takes time but ensures full validation
    
- Node will auto-restart on failure and boot
    

---

## 🛡️ Security Best Practices

- Binary in `/opt` for clean systemd compatibility
    
- Home dir for `bitcoin` is `chmod 700` (private)
    
- Systemd does not use symlinks or rely on $PATH
    
- Hardened service via:
    
    - `PrivateTmp`
        
    - `ProtectHome`
        
    - `NoNewPrivileges`
        

---

## 🔁 Maintenance & Upgrade Path

To upgrade:

bash

CopyEdit

`sudo -u bitcoin -s cd ~/bitcoin git fetch --tags git checkout v29.0 git verify-tag v29.0 make clean ./configure ... make -j$(nproc) sudo cp src/bitcoind src/bitcoin-cli /opt/bitcoin/ sudo systemctl restart bitcoind`