Solana needs fast disks and specific layouts:

Layout:

Device	Partition	Size	Mount Point	Type	Purpose
sda	p1	10.9T	/mnt/ethereum-testnet	ext4	Ethereum Testnet Data
sdb	p1	10.9T	/mnt/archive	ext4	Archive Storage
nvme0n1	p1	931.5G	/mnt/eigenlayer	ext4	EigenLayer Data
nvme1n1	p1	1G	/boot/efi	vfat	EFI Boot
p2	464.7G	/	ext4	Root OS

fstab config:
/dev/disk/by-uuid/3e5d93c5-5fd9-49e5-a45f-4111e45d4797 / ext4 defaults 0 1
/dev/disk/by-uuid/42D4-6143 /boot/efi vfat defaults 0 1
/swap.img       none    swap    sw      0       0
UUID=42a0f296-06bf-4531-818c-acaed4bdb772 /mnt/ethereum-testnet ext4 defaults,noatime,nodiratime 0 2
UUID=32bf1fa3-1f3b-435c-8997-16da40841b33 /mnt/eigenlayer ext4 defaults,noatime,nodiratime 0 2
UUID=3e2329d4-d961-4de0-b886-8e14b1f65e95 /mnt/archive ext4 defaults,noatime,nodiratime 0 2
