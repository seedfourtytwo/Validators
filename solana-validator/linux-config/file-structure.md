Folder / Files:
| Path / Symlink                                             | Type         | Purpose / Contents                                 |
| ---------------------------------------------------------- | ------------ | -------------------------------------------------- |
| /mnt/ledger → ~/ledger                                 | Directory    | Solana ledger data (high-write IOPS)           |
| /mnt/accounts → ~/accounts                             | Directory    | Solana accounts DB (runtime state)             |
| /mnt/snapshots → ~/snapshots                           | Directory    | Snapshots for fast validator startup           |
| /home/sol/.local/share/solana/install/releases/2.2.6             | Directory    | Built Agave binaries from source               |
| /home/sol/.local/share/solana/install/active_release → ~/agave | Symlink      | Active Agave release for CLI/systemd use |
| /home/sol/wallets                                                | Directory    | Keypair files: identity                        |
| /home/sol                                                  | Directory    | Simlinks to the above + start-validator.sh         |
| /home/sol/log                                              | Directory    | Validator log output file                          |
| /etc/systemd/system/validator.service                      | Service file | Tells Linux how to start the validator service     |
| /etc/nftables.conf                                         | config file  | firewall rules                                     |
| /etc/sol/solana-exporter                                         | Directory  | Solana exporter binaries                                     |
