Ethereum Eigenlayer (WIP)
Ethereum & EigenLayer Validator Setup (In Progress)
🧱 General Info
Component	Status	Notes
Geth (Execution)	Manual startup	Using Holesky testnet; multiple runs via CLI
Lighthouse	Manual startup	Tested with various checkpoint sync URLs
Prysm	Manual startup	Also tested as alternative to Lighthouse
EigenLayer	Directory prep	Symlinks and data directories set, no service yet
⚙️ Geth (Execution Client)
Field	Value
Binary	geth
Data Dir	/mnt/ethereum-testnet/geth-holesky
Network	Holesky (via --networkid 17000 or --holesky)
RPC Port	8545 (HTTP)
WS Port	8546
P2P Port	30303
Auth RPC Port	8551 (used by consensus clients)
JWT Secret	/secrets/jwtsecret
Sync Mode	snap
Extras	--metrics, --pprof, --verbosity 3, --allow-insecure-unlock
Startup Method	Manual CLI
⚙️ Consensus Clients (Beacon Chain)
1. Lighthouse
Field	Value
Binary	lighthouse
Mode	lighthouse bn (beacon node)
Data Dir	/mnt/ethereum-testnet/lighthouse-holesky
Execution URL	http://localhost:8551
JWT Secret	/mnt/ethereum-testnet/geth-holesky/geth/jwtsecret (or /secrets/)
Checkpoint URLs	Used multiple: ethstaker.cc, chainsafe.io, stakely.io, etc.
Startup Method	Manual CLI
2. Prysm
Field	Value
Binary	beacon-chain
Data Dir	/mnt/ethereum-testnet/prysm-holesky
Execution URL	http://localhost:8551
JWT Secret	/secrets/jwtsecret
Checkpoint URL	https://holesky.beaconstate.info
Flags	--accept-terms-of-use, --holesky, --monitoring-host
Startup Method	Manual CLI
📁 Directories and Symlinks
Path / Symlink	Purpose / Contents
/mnt/ethereum-testnet	Base directory for Ethereum Holesky data
/mnt/ethereum-testnet/geth-holesky	Geth execution client data
/mnt/ethereum-testnet/lighthouse-holesky	Lighthouse beacon chain data
/mnt/ethereum-testnet/prysm-holesky	Prysm beacon chain data
/mnt/eigenlayer	Placeholder for EigenLayer validator
~/eigenlayer → /mnt/eigenlayer	Symlink for convenience
/mnt/avss/eigenda	Placeholder for Eigenda node
~/eigenda → /mnt/avss/eigenda	Symlink for convenience
