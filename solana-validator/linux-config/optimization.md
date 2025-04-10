System Optimisation:
Optimization                       | Description                    | Value                                                                    | Config File                                     |
| ---------------------------------- | ------------------------------ | ------------------------------------------------------------------------ | ----------------------------------------------- |
| File Descriptors Limit         | Max open files per user        | nofile = 2000000                                                       | /etc/security/limits.d/90-solana-nofiles.conf |
| Disable Swapping               | Use swap only as last resort   | vm.swappiness = 0                                                      | /etc/sysctl.d/20-solana.conf                  |
| UDP Receive Buffer (rmem)      | Max size of UDP receive buffer | net.core.rmem_max = 134217728  <br>net.core.rmem_default = 134217728 | /etc/sysctl.d/20-solana.conf                  |
| UDP Send Buffer (wmem)         | Max size of UDP send buffer    | net.core.wmem_max = 134217728  <br>net.core.wmem_default = 134217728 | /etc/sysctl.d/20-solana.conf                  |
| Memory Map Limit               | Number of memory-mapped areas  | vm.max_map_count = 2000000                                             | /etc/sysctl.d/20-solana.conf                  |
| Max Open Handles (system-wide) | Kernel-wide open file limit    | fs.nr_open = 2147483584                                                | /etc/sysctl.d/20-solana.conf