Solana needs fast disks and specific layouts:

Layout:

Device	Partition	Size	Mount Point	Type	Purpose
nvme2n1	p1	1G	/boot/efi	vfat	EFI Boot
p2	1G	/boot	ext4	Boot Filesystem
p3	200G	/	ext4	Root OS
p4	1.2T	/mnt/snapshots	ext4	Solana Snapshots
p5	461G	swap	swap	Swap Partition
nvme0n1	p1	931G	/mnt/ledger	ext4	Solana Ledger
nvme1n1	p1	931G	/mnt/accounts	ext4	Solana Accounts

fstab config:
/dev/disk/by-uuid/d9e75b9a-e572-4bdf-9959-2bd24ca17f5e / ext4 defaults 0 1
/dev/disk/by-uuid/625f4e0f-0bad-46b5-a955-48b9de62c6f9 /boot ext4 defaults 0 1
/dev/disk/by-uuid/7A66-03A9 /boot/efi vfat defaults 0 1
UUID=8bdc3c97-5797-4503-b624-a00ce66d0290      /mnt/ledger     ext4  noatime  0 0
UUID=a6ec09e4-5598-4f7d-83fa-7bc726811fc7    /mnt/accounts   ext4  noatime  0 0
UUID=8e3bfbd0-ea9c-4848-aac7-0980375218fc   /mnt/snapshots  ext4  noatime  0 0
UUID=6d4ddbe1-d621-451a-87fb-382d14a6f1af        none            swap  sw       0 0
