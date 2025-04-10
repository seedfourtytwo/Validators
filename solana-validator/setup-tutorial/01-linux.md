## Solana Validator Server Bootstrap (Phase 1: Secure SSH & Users)

### 🖥️ **0. Initial Setup**

- OS: Ubuntu 24.04
- Access server via initial default user (e.g., `user1`)
---
### 👤 **1. Create Secure Users**

#### 🔐 `validator-admin` (Primary sudo admin)

`sudo adduser validator-admin sudo usermod -aG sudo validator-admin`
#### 👥 `sol` (Unprivileged, runs validator)

`sudo adduser sol --disabled-password --gecos ""`
#### 👤 `backup-admin` (Backup admin user)

`sudo adduser backup-admin sudo usermod -aG sudo backup-admin`
#### 🔒 Group for SSH access

`sudo groupadd sshusers sudo usermod -aG sshusers validator-admin sudo usermod -aG sshusers sol sudo usermod -aG sshusers backup-admin`

---
### 🔑 **2. Generate and Install SSH Keys**

#### ✅ From WSL for each user:

`ssh-keygen -t ed25519 -C "<username>@<hostname>" -f ~/.ssh/<username>`

> Example for `validator-admin`:  
> `ssh-keygen -t ed25519 -C "validator-admin@server" -f ~/.ssh/validator-admin`
#### 📤 Copy pub key to server:

`scp ~/.ssh/<username>.pub validator-admin@<server-ip>:/tmp/`
#### 🛠 On server:

`sudo mkdir -p /home/<username>/.ssh sudo mv /tmp/<username>.pub /home/<username>/.ssh/authorized_keys sudo chown -R <username>:<username> /home/<username>/.ssh sudo chmod 700 /home/<username>/.ssh sudo chmod 600 /home/<username>/.ssh/authorized_keys`

---
### 🔐 **3. SSH Hardening**

#### 🔧 Create hardened SSH config file:

`sudo nano /etc/ssh/sshd_config.d/99-hardened.conf`
#### Paste config:

`HostKey /etc/ssh/ssh_host_ed25519_key HostKey /etc/ssh/ssh_host_rsa_key  PermitRootLogin no AllowGroups sshusers StrictModes yes PasswordAuthentication no PubkeyAuthentication yes AuthorizedKeysFile .ssh/authorized_keys ChallengeResponseAuthentication no X11Forwarding no ClientAliveInterval 100 PerSourceMaxStartups 1  KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,gss-curve25519-sha256-,diffie-hellman-group16-sha512,gss-group16-sha512-,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha256 Ciphers aes256-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-gcm@openssh.com,aes128-ctr MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com HostKeyAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256 CASignatureAlgorithms sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256 GSSAPIKexAlgorithms gss-curve25519-sha256-,gss-group16-sha512- HostbasedAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256 PubkeyAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256`
#### 🔁 Reload SSH:

`sudo systemctl reload ssh`

---
### 🧪 **4. Test SSH Logins**

Install WSL to SSH as reguarl windows ssh client cannot handle these hardened SSH settings

From WSL:

`ssh -i ~/.ssh/validator-admin validator-admin@<server-ip> ssh -i ~/.ssh/sol sol@<server-ip> ssh -i ~/.ssh/backup-admin backup-admin@<server-ip>`

---
### 💾 **5. Back Up All Private Keys**

For each `~/.ssh/<username>` key:
- Copy contents of the private key file
- Save to:
    - 🔐 Secure password manager
    - 🔒 Encrypted USB drive or GPG folder
    - 💾 External secure storage
___
SSH audit with https://github.com/jtesta/ssh-audit locally from wsl to the server
___
## Firewall Hardening with `nftables` (Replacing UFW & iptables)

This guide covers how to:
- Fully disable and clean out `ufw` and legacy `iptables`
- Set up a **clean, minimal, and efficient** `nftables` firewall
- Secure a **Solana validator** node (or similar server)
---
### 🧹 Step 1: Cleanup Script (Disable UFW & Reset iptables)

#### Disable and reset UFW:

`sudo ufw disable || true sudo ufw --force reset`
#### Set iptables default policies to avoid lockout:

`sudo iptables --policy INPUT ACCEPT sudo iptables --policy FORWARD ACCEPT sudo iptables --policy OUTPUT ACCEPT`
#### Flush, delete, and zero all iptables rules:

`sudo iptables --flush sudo iptables --delete-chain sudo iptables --zero`
#### Clean special iptables tables:

`sudo iptables --table nat --flush sudo iptables --table nat --delete-chain sudo iptables --table mangle --flush sudo iptables --table mangle --delete-chain sudo iptables --table raw --flush sudo iptables --table raw --delete-chain`

---
### 🔧 Step 2: Install and Enable `nftables`

#### Install:
`sudo apt update sudo apt install nftables -y`
#### Enable and start:

`sudo systemctl enable --now nftables`

---
### 📝 Step 3: Create `/etc/nftables.conf`

`sudo nano /etc/nftables.conf`
#### Example config for Solana validator (edit as needed):
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority filter; policy drop;

        ct state established accept
        udp dport 8000-10000 accept
        ct state related accept
        ct state invalid drop
        iif lo accept
        tcp dport 8000 accept

        # Allow Solana RPC packets requests from these IPs
        tcp dport 8899 ip saddr {
            77.200.151.32
        } accept

        # Allow Prometheus exporter metrics access from tehse IPs
        tcp dport 9100 ip saddr {
            77.200.151.32
        } accept

        tcp dport ssh ct state new limit rate 12/minute accept
        ip protocol icmp icmp type echo-request limit rate 5/second accept

        log prefix "[nftables] DROP: "
    }

    chain output {
        type filter hook output priority filter; policy accept;
    }

    chain forward {
        type filter hook forward priority filter; policy drop;
    }
}

📌 Replace `YOUR_PUBLIC_IP` with your home IP or a monitoring server that needs access to the RPC of the validator.

Note, in the future try to change the order of 
		udp dport 8000-10000 accept
        ct state related accept
        ct state invalid drop
To see if dropping invalid packets fore checking them against udp ports have a performance impact. Need to find a way to measure it. Could use "counter" before every rule

---
### ✅ Step 4: Load and Verify the Ruleset

#### Load manually (if needed):

`sudo nft -f /etc/nftables.conf`
or
`sudo systemctl enable --now nftables`
#### View active rules:

`sudo nft list ruleset`
#### Confirm service is running:

`sudo systemctl status nftables`

___
# Set up disk management
as per current validator config notes