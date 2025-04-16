Below are some more system tuning to explore for the Solana validator given by https://nordstar.one/

```bash
# Performance Tuning Profile for Solana Validator
[main]
summary=Solana validator system tuning

[cpu]
governor=performance
energy_performance_preference=performance
force_latency=cstate.id:0|1
min_perf_pct=100

[acpi]
platform_profile=performance

[vm]
transparent_hugepages=never

[sysctl]
vm.swappiness=0
vm.max_map_count=1048576
vm.dirty_ratio = 40
vm.dirty_background_ratio = 10
net.core.rmem_max=134217728
net.core.rmem_default=134217728
net.core.wmem_max=134217728
net.core.wmem_default=134217728
fs.nr_open=2147483584
kernel.numa_balancing=0

[bootloader]
cmdline=ipv6.disable=1 amd_pstate=active pcie_aspm=off pcie_port_pm=off iommu=pt
```

### Reference Documentation
| Resource | Description | Link |
|----------|-------------|------|
| Red Hat Tuned | Comprehensive guide for system tuning and optimization | [Red Hat Performance Tuning Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/performance_tuning_guide/chap-red_hat_enterprise_linux-performance_tuning_guide-tuned#tuned-plugins) |