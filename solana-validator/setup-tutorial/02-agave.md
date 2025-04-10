# Build Agave client from source
Follow https://github.com/agjell/sol-tutorials/blob/master/building-solana-from-source.md
___
# Keypair management:
Generate keys with:
solana-keygen new --outfile ~/wallet-keypair.json

Test recovery with:
solana-keygen recover --outfile ~/wallets/test-recovery.json


Set the validator identity with:
solana config set --keypair ~/wallets/validator-keypair.json
Set it to tesetnet:
solana config set --url https://api.testnet.solana.com
## Validator Key Security Strategy

To follow best practices and reduce risk, only **essential keypairs** are kept on the validator. Others are stored safely in cold storage (e.g., password manager).

|Keypair|Location|Purpose|
|---|---|---|
|`identity-keypair`|On the validator|Signs blocks, votes, and communicates with the cluster. Required to run the validator.|
|`vote-account-keypair`|Cold storage|Manages the vote account. Only needed to create the account or change its authority. Not needed for validator runtime.|
|`withdrawer-keypair`|Cold storage|Used to withdraw staking rewards. Only needed when collecting rewards, not for running the validator.|

---
### 🧠 Why This Setup?

- Minimizes the risk of key theft if the validator is compromised
- Keeps critical funds (vote and rewards) protected in cold storage
- Follows practices used by top validator operators
---
### ⚠️ Important:
The **vote account must be registered first**, and linked to the validator's identity.  
Once registered, you only need the vote **public key** to run the validator.
___
With the above steps and tutorial you will run into permission errors when starting the validator as the un-permissioned user needs access to the mount points. I can be fixed with
sudo chown -R sol:sol /mnt/snapshots
sudo chown -R sol:sol /mnt/ledger
sudo chown -R sol:sol /mnt/accounts
# Tips:
To build faster from source:
bash ~/agave-src-v2.1.17/scripts/cargo-install-all.sh --validator-only ~/.local/share/solana/install/releases/2.1.17

Full build command:
`export TAG=v2.1.17 && \ export CARGO_BUILD_JOBS=8 && \ export RUSTFLAGS="-C target-cpu=native" && \ git clone https://github.com/anza-xyz/agave.git --depth 1 --branch "${TAG}" ~/solana-src-"${TAG}" && \   ./solana-src-"${TAG}"/scripts/cargo-install-all.sh --validator-only ~/.local/share/solana/install/releases/"${TAG}" && \   ln --force --no-dereference --symbolic ~/.local/share/solana/install/releases/"${TAG}" ~/.local/share/solana/install/active_release && \   solana --version`

replace the value in `CARGO_BUILD_JOBS` with the amount of threads you want to use. if the validator is running, i usually build with 8