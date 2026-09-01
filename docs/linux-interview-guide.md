# Linux

Pointer-style interview notes for Linux and networking. Facts sit in tables,
actions in command blocks, traps under **Gotchas**.

- **Owns:** OS and network fundamentals — process, memory, cgroup, namespace,
  TCP/IP, DNS, CIDR — stated once here, linked from the Git and Docker guides.
- **Failures:** [troubleshooting scenarios](#troubleshooting-scenarios) follow
  **Symptom -> Check -> Cause -> Fix -> Prevent**.
- **Safety:** destructive commands are marked; run the read-only form first.

## Contents

- **Fundamentals:** [OS and Linux fundamentals](#os-and-linux-fundamentals) ·
  [Filesystem](#filesystem) · [LVM](#lvm) · [Permissions](#permissions) ·
  [SELinux vs AppArmor](#selinux-vs-apparmor)
- **Processes and resources:**
  - [Processes](#processes) · [Process priority and scheduling](#process-priority-and-scheduling)
  - [cgroups and namespaces](#cgroups-and-namespaces) · [Resource limits with ulimit](#resource-limits-with-ulimit)
  - [CPU load average](#cpu-load-average) · [Memory](#memory) · [Concurrency problems](#concurrency-problems)
- **Networking:** [Networking fundamentals](#networking-fundamentals) ·
  [nftables vs iptables](#nftables-vs-iptables) · [DNS](#dns) ·
  [IP addressing and CIDR](#ip-addressing-and-cidr) ·
  [Network interfaces and diagnostics](#network-interfaces-and-diagnostics)
- **Services and reference:** [SSH](#ssh) ·
  [systemd and journald](#systemd-and-journald) · [Nginx](#nginx) ·
  [Command reference](#command-reference) ·
  [Troubleshooting scenarios](#troubleshooting-scenarios)

## OS and Linux fundamentals

**Docs:** [man pages](https://man7.org/linux/man-pages/) ·
[kernel docs](https://docs.kernel.org/)

An OS arbitrates CPU, memory, storage, and devices between processes and exposes
them through system calls.

| Term | One-line answer |
| :--- | :--- |
| Layers | Hardware -> kernel (devices, memory, filesystems, scheduling, IPC, context switching, syscalls) -> shell -> userland utilities |
| Linux traits | Multi-user, multitasking, UNIX-like, GPL-licensed, portable from embedded devices to mainframes |
| UNIX vs Linux | UNIX = proprietary, vendor-tied (AIX, HP-UX, Solaris); Linux = open kernel, many distros, hardware-portable |
| Kernel types | Linux is **monolithic** (all services in one address space, fast, fault-prone) with loadable modules; microkernel (QNX) keeps only scheduling, IPC, memory in kernel space; hybrid (NT, XNU) mixes both |
| Boot order | Firmware (UEFI/BIOS) -> boot loader (GRUB 2, or `systemd-boot` on UEFI) -> kernel -> `initramfs` -> `init` (systemd) -> target units |
| `root` | UID 0, bypasses permission checks; use `sudo` for attributable, scoped privilege |
| Daemon | Background service with no controlling terminal; name ends in `d` (`sshd`, `crond`) |
| Shells | `sh` = POSIX scripting shell (`dash` on Debian); `bash` default interactive, `zsh` on macOS; `ksh` on commercial UNIX; `csh`/`tcsh` poor for scripting |
| `vi` modes | Command (default, `Esc`), Insert (`i`/`a`/`o`), last-line ex (`:w`, `:q!`, `:%s/old/new/g`) |

| Gotcha | Detail |
| :--- | :--- |
| No `root` SSH login | Set `PermitRootLogin no` and use `sudo`, so privileged actions stay attributable |
| `#!/bin/sh` is not bash | Arrays and `[[ ]]` break where `/bin/sh` is `dash`; declare `#!/usr/bin/env bash` or write POSIX `sh` |
| No desktop on servers | It only adds attack surface |

## Filesystem

**Docs:** [`inode(7)`](https://man7.org/linux/man-pages/man7/inode.7.html) ·
[`fstab(5)`](https://man7.org/linux/man-pages/man5/fstab.5.html) · [`findmnt(8)`](https://man7.org/linux/man-pages/man8/findmnt.8.html) ·
[FHS 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)

| Path | Contents |
| :--- | :--- |
| `/`, `/root`, `/home` | Hierarchy root; root's home; users' homes |
| `/boot`, `/etc` | Kernel, `initramfs`, GRUB config; system-wide configuration |
| `/usr`, `/opt` | Installed software; self-contained third-party software |
| `/bin`, `/sbin`, `/lib` | Essential binaries and libraries; symlinks into `/usr` on modern systems |
| `/dev` | Device nodes (`/dev/sda`, `/dev/null`) |
| `/proc`, `/sys` | Virtual filesystems: kernel and process state; devices, drivers, cgroups |
| `/var` | Variable data: logs, spool, caches, `/var/lib/docker` |
| `/tmp` | World-writable temporary files, sticky bit, cleared at boot |
| `/mnt`, `/media`, `/run` | Manual mounts; removable media; runtime state on tmpfs |

### Inodes and links

An inode holds owner UID and GID, type, permissions and ACLs, size, link count,
timestamps (atime, mtime, ctime), and block pointers — but **not** the filename
or contents; names map to inodes, so hard links work (`ls -i`, `stat`, `df -i`).

| | Hard link | Symbolic link |
| :--- | :--- | :--- |
| Points to | The inode | A pathname |
| Across filesystems / to a directory | No / not permitted | Yes / yes |
| Survives deletion of original | Yes | No, becomes dangling |
| Own inode | No, shares it | Yes |
| Created with | `ln target name` | `ln -s target name` |

### Key configuration files

`/etc/passwd`, seven colon-separated fields:
`mark:x:1001:1001:mark,,,:/home/mark:/bin/bash` = username, password placeholder
(hash lives in `/etc/shadow`), UID, primary GID, GECOS, home, login shell.

| File | Purpose |
| :--- | :--- |
| `/etc/shadow` | Password hashes and ageing; root-only. A login shell of `/usr/sbin/nologin` in `/etc/passwd` marks a service account that cannot log in |
| `/etc/fstab` / `/etc/mtab` | Admin-maintained boot mounts (prefer `UUID=`) / current mounts, symlink to `/proc/self/mounts` |
| `/etc/hosts` | Local name-to-address overrides, consulted before DNS |
| `/etc/nsswitch.conf` | Resolution order for names, users, groups |
| `/etc/resolv.conf` | Resolver config: `nameserver`, `search`, `options` |
| `/proc` | In-memory kernel and process state; `/proc/sys` tunables via `sysctl` |

Mount workflow: mount manually, confirm with `findmnt`, then add the same line
to `/etc/fstab` so it survives reboot.

**Gotchas**

- A filesystem can exhaust **inodes** while `df -h` shows free space; the
  symptom is "No space left on device" from millions of small cache or session
  files. Check `df -i`.
- A bad `/etc/fstab` entry can leave the host unbootable. Check it with
  `findmnt --verify --tab-file /etc/fstab` before rebooting. `mount -a` is not a
  dry run — it really mounts every entry; `mount -af` is the fake run that parses
  and simulates without calling the mount syscall.
- `/etc/resolv.conf` is generated on hosts running `systemd-resolved` or
  NetworkManager; edit the manager's config or the change is overwritten.

## LVM

**Docs:** [`lvm(8)`](https://man7.org/linux/man-pages/man8/lvm.8.html) ·
[`lvextend(8)`](https://man7.org/linux/man-pages/man8/lvextend.8.html)

Stack: `physical volume (PV) -> volume group (VG) -> logical volume (LV) -> filesystem`.

- **PV** (`pvcreate`): a disk or partition handed to LVM.
- **VG** (`vgcreate`): pools PVs so free extents can go to any LV.
- **LV** (`lvcreate`): the block device (`/dev/vgdata/lvapp`) you format and mount.

```bash
sudo pvs; sudo vgs; sudo lvs                 # inspect before changing anything
sudo lvextend -r -L +10G /dev/vgdata/lvapp   # grow LV and filesystem together
```

| Gotcha | Detail |
| :--- | :--- |
| Missing `-r` | The block device grows but the filesystem does not |
| **Shrinking is destructive** | Filesystem-dependent, usually needs unmounting, destroys data if the filesystem is not shrunk first — take and verify a backup first |
| Snapshot is not a backup | Copy-on-write on the same disks: a short crash-consistent window, invalid once its VG fills |

## Permissions

**Docs:** [`chmod(1)`](https://man7.org/linux/man-pages/man1/chmod.1.html) ·
[`acl(5)`](https://man7.org/linux/man-pages/man5/acl.5.html)

Three bits (`r`=4, `w`=2, `x`=1) for three classes: user, group, others.

| Permission | On a file | On a directory |
| :--- | :--- | :--- |
| Read (4) | Read contents | List entries |
| Write (2) | Modify contents | Create, rename, **delete** entries |
| Execute (1) | Run it | Enter it and access entries by name |

```bash
chmod 650 test.txt        # user rw-, group r-x, others ---
chmod 644 file; chmod 755 script.sh
chmod ug+rw test.txt      # symbolic: who (u,g,o,a) + op (+,-,=) + bits
chmod o-rwx secret.txt; chmod a=r file; chown user:group file
umask 022                 # default mask: files 644, directories 755
```

| Special bit | Numeric | Effect | Example |
| :--- | :---: | :--- | :--- |
| SUID | 4000 | Runs with the owner's privileges (`rwsr-xr-x`) | `/usr/bin/passwd` |
| SGID | 2000 | Binary: group's privileges. Directory: new entries inherit its group (`rwxrwsr-x`) | shared project dirs |
| Sticky | 1000 | In a shared directory, only the file's owner, the directory's owner, or root may delete or rename an entry (`rwxrwxrwt`) | `/tmp` |

```bash
chmod 4755 binary; chmod 2775 shared_dir; chmod 1777 /tmp
find / -xdev -perm -4000 -type f 2>/dev/null   # audit SUID, one filesystem
```

| Gotcha | Detail |
| :--- | :--- |
| Directory write allows delete | Deleting or renaming a file needs write on the **directory**, not the file — hence the sticky bit on `/tmp`, which narrows that to the file's owner, the directory's owner, and root |
| Unnecessary SUID-root binaries | Standard privilege-escalation route; audit with `-xdev` per local filesystem (a scan from `/` is expensive and can enter network mounts) and review results before changing any bit |

## SELinux vs AppArmor

**Docs:** [`selinux(8)`](https://man7.org/linux/man-pages/man8/selinux.8.html) ·
[`apparmor(7)`](https://man7.org/linux/man-pages/man7/apparmor.7.html)

Mode bits and ACLs are **discretionary** access control (the owner can grant
access). Both of these add **mandatory access control (MAC)**: policy can deny
an action that Unix permissions allow.

| | SELinux | AppArmor |
| :--- | :--- | :--- |
| Model | Labels every subject and object; rules allow type interactions | Profiles programs by pathname and allowed operations |
| Distributions | RHEL, Fedora, Amazon Linux | Ubuntu, Debian, SUSE |
| Modes | Enforcing, permissive, disabled | Enforce, complain, disabled per profile |
| Strength / first checks | Fine-grained, robust across path changes; `getenforce`, `ausearch -m AVC` | Easier to adopt; `aa-status`, journal `DENIED` |

| Gotcha | Detail |
| :--- | :--- |
| **Never disable MAC to fix a denial** | Confirm the expected path and label, read the audit event, make the smallest policy change |
| SELinux repair | `restorecon -Rv /path` repairs labels, `semanage fcontext` persists a mapping, `chcon` alone is temporary |
| AppArmor repair | Edit the profile, test in complain mode, reload with `apparmor_parser` |

## Processes

**Docs:** [`ps(1)`](https://man7.org/linux/man-pages/man1/ps.1.html) ·
[`top(1)`](https://man7.org/linux/man-pages/man1/top.1.html)

| | Process | Thread |
| :--- | :--- | :--- |
| Address space | Its own | Shared with siblings |
| Create and switch cost | Heavier (needs an address-space switch) | Lighter |
| Isolation | Isolated by default | None inside the process |
| Communication | IPC: pipes, sockets, shared memory, signals | Shared memory, needs locking |
| Failure blast radius | One process dies | Usually the whole process dies |

The kernel tracks each task in a process control block: PID, PPID, state,
priority, register context, memory maps, open file descriptors. Threads are
tasks sharing memory (`clone()`): cheap IPC, but locking brings races/deadlocks.

| State | Meaning |
| :---: | :--- |
| `R` | Running or runnable |
| `S` | Interruptible sleep, waiting on an event (normal idle) |
| `D` | Uninterruptible sleep, blocked in the kernel on disk or network I/O |
| `T` / `Z` | Stopped by a signal or debugger / zombie: finished, not yet reaped |

| | Zombie | Orphan |
| :--- | :--- | :--- |
| Definition | Exited, exit status still in the process table | Parent exited first |
| Cause | Parent never called `wait()` | Normal, not an error |
| Fix | Cannot be killed; fix or restart the **parent**; `init` reaps on parent death | None; re-parented to PID 1 |

Find them with `ps -eo pid,ppid,stat,cmd | awk '$3 ~ /^Z/'`.

`top` columns: `PR`/`NI` kernel priority (lower is favoured) and nice; `VIRT` mapped
address space; `RES` resident set in RAM — the number that matters; `SHR` its shared
part; `%CPU` one-CPU share (>100% threaded); `%MEM` `RES`/RAM; `TIME+` cumulative CPU.

**Gotchas**

- Many processes in `D` state means a storage problem: they cannot be killed (blocked in a kernel call) and load climbs while CPU is idle.
- Summing `RES` across processes **over-counts**, because shared pages are counted once per process.
- A few zombies are normal; a growing count is a bug in the parent.

## Process priority and scheduling

**Docs:** [`sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html) ·
[CFS design](https://docs.kernel.org/scheduler/sched-design-CFS.html)

Linux schedules normal tasks with **CFS**: CPU time in proportion to weight, not by
strict priority. Nice sets that weight: `-20` (most favoured) to `19`, default `0`,
shown `PR = 20 + NI`, ~10% per step; lowering needs root, any user may raise theirs.

| Policy | Use |
| :--- | :--- |
| `SCHED_OTHER` (CFS) | Default for normal processes; nice applies here |
| `SCHED_BATCH` / `SCHED_IDLE` | CPU-bound background work / runs only when nothing else wants the CPU |
| `SCHED_FIFO` / `SCHED_RR` | Real-time, priority 1-99, always preempts normal tasks |

Separate concerns: disk I/O priority is `ionice -c 3`; a hard CPU cap is a cgroup
quota (`systemd-run -p CPUQuota=20%`); OOM kill bias is `/proc/<pid>/oom_score_adj`.
Syntax: [Process management and priority](#process-management-and-priority).

**Gotchas.** Nice is a **relative weight**, not a reservation: no effect on an
idle machine, large effect under contention, and it cannot cap CPU. A
busy-looping `SCHED_FIFO` task can make the whole machine unresponsive.

## cgroups and namespaces

**Docs:** [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) ·
[`namespaces(7)`](https://man7.org/linux/man-pages/man7/namespaces.7.html)

Namespaces give a process its own **view** of the system; cgroups **limit** what
it may consume. Both are kernel features, not container-runtime features: a
container is these two plus policy.

| Namespace | Isolates |
| :--- | :--- |
| PID | Process IDs, so the group has its own PID 1 |
| Mount (mnt) | The filesystem tree |
| Network (net) | Interfaces, routes, firewall rules, ports |
| UTS / IPC | Hostname and domain name / shared memory and semaphores |
| User | UID and GID mapping (used by user-namespace remapping) |
| Cgroup / Time | View of its own cgroup hierarchy / clock offsets |

| | cgroups v1 | cgroups v2 |
| :--- | :--- | :--- |
| Hierarchy | Separate per controller | One unified hierarchy |
| Membership | Can differ per controller | One process, one cgroup |
| Interface | Controller-specific, inconsistent | Consistent: `cpu.max`, `memory.max`, `pids.max` |
| Memory control | Weaker accounting and delegation | Better pressure, swap, and OOM controls |
| Where seen | Legacy systems | Current systemd distributions and Kubernetes |

v2 knobs: `memory.high` throttles and reclaims before failure, `memory.max` is the
hard ceiling that can trigger a cgroup OOM kill, `cpu.weight` is a relative share,
`cpu.max` a hard quota — as Docker `--cpu-shares` versus `--cpus`.

```bash
stat -fc %T /sys/fs/cgroup     # cgroup2fs means v2
systemd-cgls; systemd-cgtop
systemctl show -p CPUQuota -p MemoryMax example.service
```

| Gotcha | Detail |
| :--- | :--- |
| One without the other fails | Namespaces without cgroups let one workload starve the host; cgroups without namespaces give no isolation |
| Shared kernel | It is the isolation ceiling either way |
| Do not hand-edit control files | Prefer systemd properties (`CPUQuota=`, `MemoryMax=`, `TasksMax=`); systemd owns the hierarchy and reapplies its configuration |

## Resource limits with ulimit

**Docs:** [`getrlimit(2)`](https://man7.org/linux/man-pages/man2/getrlimit.2.html) ·
[`limits.conf(5)`](https://man7.org/linux/man-pages/man5/limits.conf.5.html)

```bash
ulimit -a                # all limits for this shell
ulimit -Sn; ulimit -Hn   # soft and hard open-file limits
ulimit -n 65536          # raise the soft limit, never above the hard limit
prlimit --pid <pid>      # limits of an existing process
```

The **soft limit** is enforced and a process may raise it up to the **hard limit**,
which only root or a capable process can raise. `nofile` exhaustion gives
`Too many open files`; `nproc` exhaustion blocks fork and thread creation.

| Where to set | How |
| :--- | :--- |
| Interactive users | `/etc/security/limits.conf` (PAM) |
| systemd services | `LimitNOFILE=`/`LimitNPROC=` in the unit — PAM limits do **not** apply |
| Containers | `--ulimit` plus cgroup limits |

**Gotchas.** `ulimit` applies to the shell and its **children only**; it never
changes a running process and cannot cap aggregate use across a service — that
is a cgroup job.

## CPU load average

**Docs:** [`uptime(1)`](https://man7.org/linux/man-pages/man1/uptime.1.html) ·
[`proc(5)`](https://man7.org/linux/man-pages/man5/proc.5.html)

Load average = tasks **running or waiting to run**, averaged over 1, 5, and 15
minutes; on Linux it also counts uninterruptible sleep (`D`), so heavy I/O raises
load while the CPU is idle. Read it relative to `nproc` (`uptime`, `/proc/loadavg`).

| Load | 1 CPU | 4 CPUs |
| :--- | :--- | :--- |
| 0.5 / 1.0 | 50% busy / fully busy, no queue | 12.5% / 25% busy |
| 4.0 | 4x oversubscribed, ~3 tasks waiting | Fully busy, no queue |
| 8.0 | Severely oversubscribed | 2x oversubscribed, ~4 tasks waiting |

- `3.84, 3.72, 2.41`: growing backlog on 1 CPU, near full on 4, fine on 16.
- Sustained above 1.0 per CPU means tasks are waiting; 1-minute above 15-minute means load is growing.
- High load with low CPU in `top` is an I/O-bound queue — confirm with `iostat -xz 1` and `D` counts in `ps`.

**Gotchas.** Load is a **count of tasks, not a percentage**. Load 2.0 is not
"200% CPU"; on a 4-CPU host it is comfortable.

## Memory

**Docs:** [`free(1)`](https://man7.org/linux/man-pages/man1/free.1.html) ·
[kernel MM admin guide](https://docs.kernel.org/admin-guide/mm/index.html)

| | Virtual (`VIRT`) | Resident (`RES`) |
| :--- | :--- | :--- |
| What it is | Total mapped address space | Portion currently in physical RAM |
| Includes | Shared libs, mapped files, reserved-but-untouched allocations | Only real pages |
| Pressure indicator | Poor, routinely huge | **The number to watch** |

Under pressure the kernel reclaims approximately least-recently-used pages:
clean file-backed pages are dropped, dirty pages written back, anonymous pages
swapped.

```bash
free -h                 # read the "available" column, not "free"
ps -eo pid,rss,vsz,comm --sort=-rss | head
cat /proc/meminfo; swapon --show
sysctl vm.swappiness    # 0-100, default 60: bias toward swapping anonymous pages
vmstat 1                # si/so columns: swap-in / swap-out
```

- **Swap sizing:** ~2x RAM up to 2 GB, roughly RAM at 2-8 GB, 4-8 GB above that,
  at least RAM for hibernation, little or none for latency-sensitive databases.
- Kubernetes historically required swap disabled for predictable accounting;
  modern kubelet can use it via `NodeSwap`, as explicit cluster policy.
- **OOM killer.** When memory cannot be reclaimed the kernel kills a process
  rather than stall, choosing by `oom_score` (mainly footprint, adjusted by
  `/proc/<pid>/oom_score_adj`, `-1000` to `1000`).
- Confirm with `dmesg -T | grep -i -E 'out of memory|killed process'`.

**Gotchas**

- "Virtual memory is disk space acting as RAM" is wrong; that describes
  **swap**, one backing store for a virtual address space.
- Low "free" is normal and by design: page cache under `buff/cache` is
  reclaimable on demand.
- Exit code 137 with no application error = OOM-killed. In a container that
  usually means the **cgroup limit**, not host exhaustion.
- Continuous swap-in/swap-out (thrashing) is a capacity problem, not a tunable.

## Concurrency problems

**Docs:** [`pthreads(7)`](https://man7.org/linux/man-pages/man7/pthreads.7.html) ·
[kernel locking](https://docs.kernel.org/locking/index.html)

Deadlock requires all four **Coffman conditions** at once: mutual exclusion,
hold and wait, no preemption, circular wait (closed chain: P0 on P1, P1 on P2,
P2 on P0). Break any one and deadlock is impossible.

| | Deadlock | Starvation | Livelock |
| :--- | :--- | :--- | :--- |
| System progress | None among those involved | Yes, others proceed | None, though state keeps changing |
| Cause | All four Coffman conditions | Unfair scheduling or allocation | Repeated conflicting retries |
| Processes | Waiting forever, holding resources | Waiting forever, holding nothing | Running but achieving nothing |
| Fix | Fixed global lock order, timeouts or `try_lock`, abort a participant | **Ageing** (raise priority as wait grows), fair queueing | Randomised back-off |

**Gotchas.** "Circular wait" is one of the four conditions, not a synonym for
deadlock; livelock is a distinct third failure mode. CFS avoids starvation for
normal tasks by design, but `SCHED_FIFO` tasks can starve them.

## Networking fundamentals

**Docs:** [RFC 9293 (TCP)](https://www.rfc-editor.org/rfc/rfc9293.html) ·
[RFC 9110 (HTTP)](https://www.rfc-editor.org/rfc/rfc9110.html) ·
[`ss(8)`](https://man7.org/linux/man-pages/man8/ss.8.html)

Mnemonic, layer 7 down to 1: All People Seem To Need Data Processing.

| Layer | Name | Function | Examples | TCP/IP | Device |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 7 | Application | Human-facing protocols | HTTP, DNS, SSH, SMTP | Application | Host, reverse proxy, WAF |
| 6 | Presentation | Encoding, encryption, compression | TLS, JPEG | Application | - |
| 5 | Session | Setup, checkpoints, teardown | RPC, NetBIOS | Application | - |
| 4 | Transport | End-to-end delivery and ports | TCP, UDP | Transport | L4 load balancer |
| 3 | Network | Addressing and routing between networks | IP, ICMP | Internet | Router |
| 2 | Data link | Framing on the local segment, MAC | Ethernet, ARP | Link | Switch |
| 1 | Physical | Bits on the medium | Cables, radio, NICs | Link | Hub, cable, NIC |

Matching layers communicate *logically*; only layer 1 has a physical medium.
Practical use: an L4 balancer forwards TCP without seeing the request, an L7
balancer parses HTTP and routes on path, host, and headers.

| | TCP | UDP |
| :--- | :--- | :--- |
| Connection | Handshake required | Connectionless |
| Reliability | ACKs, retransmission, reordering | None |
| Control | Flow control and congestion control | None |
| Use for | HTTP(S), SSH, databases, file transfer | Voice, video, gaming, metrics, DNS |

QUIC and HTTP/3 implement reliability themselves on top of UDP.

### Three-way handshake

| Step | Flag | Direction | Seq | Ack | Meaning |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `SYN` | Client -> server | `X` | - | "Connect, my sequence starts at X" |
| 2 | `SYN-ACK` | Server -> client | `Y` | `X+1` | "Accepted, mine starts at Y" |
| 3 | `ACK` | Client -> server | `X+1` | `Y+1` | "Acknowledged, established" |

States: client `SYN-SENT` -> `ESTABLISHED`; server `LISTEN` -> `SYN-RECEIVED` ->
`ESTABLISHED`. Teardown is a separate four-way `FIN`/`ACK` exchange ending in
`TIME_WAIT` on the closing side.

| Symptom | Reading |
| :--- | :--- |
| Timeout with retransmitted `SYN`s | `SYN` or `SYN-ACK` dropped: firewall or security group, missing route, or nothing listening |
| `Connection refused` | Packet arrived, host replied `RST`, no listener — a service problem, not a network problem |
| Many `TIME_WAIT` on a busy client | Normal protection against stale duplicate segments; fix with keep-alive and connection reuse, not by disabling it |
| SYN flood | Handshakes never completed, backlog exhausted; mitigate with `net.ipv4.tcp_syncookies` and a larger `tcp_max_syn_backlog` |
| Connects then freezes on large transfers | MTU mismatch plus blocked ICMP fragmentation-needed |

Inspect with `ss -tan state syn-sent` and
`sudo tcpdump -ni any 'tcp[tcpflags] & tcp-syn != 0'`.

### Ports and performance metrics

| Protocol | Port | Transport | Notes |
| :--- | :---: | :--- | :--- |
| FTP | 21 control, 20 data | TCP | Plaintext, dual channel |
| SSH / SFTP / SCP | 22 | TCP | SFTP is an SSH subsystem, not FTP |
| SMTP | 25, 465, 587 | TCP | Sending only; 587 + STARTTLS is modern submission |
| DNS | 53 | UDP, TCP | UDP for queries; TCP for zone transfer and large responses |
| HTTP / HTTPS | 80 / 443 | TCP (UDP for HTTP/3) | HTTPS is HTTP inside TLS |
| POP3 / IMAP | 110 / 143 | TCP | Retrieval; 995 / 993 over TLS |
| NTP / MySQL / PostgreSQL | 123 / 3306 / 5432 | UDP / TCP | Time sync; databases, never exposed to the internet |

- Metrics: **latency** (round-trip travel time), **packet loss** (even 1% badly
  degrades TCP throughput), **throughput** (data actually delivered, measured
  with `iperf3`), **bandwidth** (theoretical capacity), **jitter** (latency
  variance, the metric for voice and video).
- Single-stream TCP throughput is roughly window size over round-trip time — why a
  high-bandwidth intercontinental link is slow without window scaling or parallel streams.

### HTTP status codes

| Class | Meaning | Common examples |
| :--- | :--- | :--- |
| 1xx / 2xx | Informational / success | 101; 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 4xx | Client error | 400, 401, 403, 404, 409 Conflict, 429 Too Many Requests |
| 5xx | Server error | 500, 502, 503, 504 |

- Behind a proxy: **401** not authenticated versus **403** authenticated but not authorised.
- **502**: the proxy got an invalid or no response (crashed or unready backend).
- **503**: deliberately unavailable, e.g. no healthy targets.
- **504**: upstream did not answer within the timeout, so the backend is slow, not down.

### TLS

**Docs:** [RFC 8446 (TLS 1.3)](https://www.rfc-editor.org/rfc/rfc8446.html) ·
[RFC 5246 (TLS 1.2)](https://www.rfc-editor.org/rfc/rfc5246.html)

- Both versions authenticate the server certificate (hostname, validity, chain,
  trust anchor), negotiate parameters, derive shared symmetric keys, then carry
  encrypted application data.
- Flow: `ClientHello` -> `ServerHello` with certificate and key exchange -> client key share and `Finished` -> server `Finished` -> data.

| | TLS 1.2 | TLS 1.3 |
| :--- | :--- | :--- |
| Round trips before app data | 2 | 1 (0 with resumption) |
| Key share | After `ServerHello` | In the client's first message |
| Forward secrecy | Only with ECDHE; RSA key exchange lacks it | Always (ephemeral only) |
| Removed | - | RSA key exchange, static DH, CBC suites, renegotiation |

**Gotchas.** Disable TLS 1.2 RSA key exchange: no forward secrecy. TLS 1.3
**0-RTT early data is replayable** — use it only for idempotent requests, never
for payments or state changes.

### File transfer protocols

**Docs:** [RFC 959 (FTP)](https://www.rfc-editor.org/rfc/rfc959.html) ·
[`sftp(1)`](https://man.openbsd.org/sftp.1)

| | FTP | FTPS | SFTP |
| :--- | :--- | :--- | :--- |
| Transport | TCP 21 + data channel | FTP plus TLS | SSH subsystem on TCP 22 |
| Encryption / ports | None / multiple | Yes / multiple | Yes by default / one |
| Key authentication | No | No | Yes (SSH keys) |
| Verdict | Never on untrusted networks | Legacy compatibility | **Default choice**, works unattended in CI/CD |

- FTP data channel, **active** (`PORT`): the server connects from TCP 20 back to
  the client, which client NAT and firewalls usually block.
- **Passive** (`PASV`/`EPSV`): the client connects to a high server port, needing
  an allowed, advertised passive-port range on the server.

## nftables vs iptables

**Docs:** [`nft(8)`](https://man7.org/linux/man-pages/man8/nft.8.html) ·
[`iptables(8)`](https://man7.org/linux/man-pages/man8/iptables.8.html)

| | `iptables` | `nftables` |
| :--- | :--- | :--- |
| Tools | Separate per family (IPv4, IPv6, ARP, bridge) | One `nft` command and language |
| Updates | Rule-by-rule | Atomic ruleset replacement |
| Features / status | Basic matches; legacy, often the `iptables-nft` frontend | Sets, maps, native dual-stack; modern default |

Both configure Netfilter hooks. Base chains attach to `input` (to this host),
`output` (from it), and `forward` (routed through). NAT is separate: source NAT
or masquerade rewrites outbound sources, destination NAT inbound destinations.

```bash
sudo nft list ruleset                  # read-only inspection
sudo iptables-save                     # read-only legacy/compat view
iptables --version                     # is this iptables-nft?
sudo nft -c -f rules.nft               # syntax-check without applying
sudo nft list ruleset > rules.backup   # back up before an approved change
```

| Gotcha | Detail |
| :--- | :--- |
| **Never flush a remote host's firewall interactively** | One mistake cuts off SSH with no recovery path |
| Change safely | Use a console or out-of-band session, validate first, keep an automatic rollback timer, and apply through the distribution's persistent firewall service |
| Do not mix managers | Direct `nft` changes alongside firewalld, UFW, Docker, or Kubernetes let the manager overwrite or bypass your rules |

## DNS

**Docs:** [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.html) ·
[`dig(1)`](https://man7.org/linux/man-pages/man1/dig.1.html) ·
[`resolv.conf(5)`](https://man7.org/linux/man-pages/man5/resolv.conf.5.html)

What happens when you type a URL:

1. Parse and check HSTS, so `http://` may be rewritten before any packet leaves.
2. Resolve: browser cache -> OS cache and `/etc/hosts` -> recursive resolver ->
   root -> TLD -> authoritative, each answer cached for its TTL.
3. TCP handshake to 443, TLS handshake with certificate validation, HTTP request
   and response, render.
4. First-visit latency lives in DNS and the TLS handshake, then round-trip time;
   a CDN, keep-alive, and TLS session resumption address all three.

| Record | Purpose |
| :--- | :--- |
| `A` / `AAAA` | Name to IPv4 / IPv6 address |
| `CNAME` | Alias to another **name**; cannot coexist with other records at the same name, so invalid at a zone apex |
| `ALIAS` / `ANAME` | Provider apex alias: resolves to a name but behaves like `A` and can coexist |
| `MX` / `NS` | Mail exchanger plus preference / authoritative nameservers |
| `PTR` | Address to name (reverse DNS, mail reputation) |
| `SRV` | Host **and port** for a named service (SIP, XMPP, Kubernetes) |
| `TXT` | Arbitrary text: SPF, DKIM, DMARC, verification tokens |
| `SOA` / `CAA` | Zone metadata (serial, refresh, negative-cache TTL) / which CAs may issue |
| `URL` | Provider feature, **not a DNS record type**: returns an HTTP 301 |

Chains are legal (`blog.example.com CNAME x.github.io CNAME y.fastly.net A
185.31.17.133`). Choose `A` when the address is stable, `CNAME` to follow
someone else's name, `ALIAS` for apex-level aliasing.

- **TTL:** how long a resolver may cache an answer, trading query volume against
  propagation speed. Before a planned migration lower it to 60s a day ahead,
  change, verify, then raise it.
- **Transport:** UDP 53 for ordinary queries; TCP 53 for zone transfers (AXFR,
  IXFR) and oversized responses, common with DNSSEC; DoT (853), DoH (443) add privacy.
- **DNS as a load balancer:** multiple `A` records give round robin; providers add
  latency-based, geolocation, weighted, and failover routing with health checks.
- **Limits** (why a real load balancer sits behind it): caching delays removal,
  DNS sees no connection counts or server load, clients may pin to one answer.
- Use DNS for coarse geographic distribution, an L4/L7 balancer within a region.

**Gotchas.** A "5-minute DNS cutover" is optimistic: some resolvers and many
runtimes cache beyond the TTL — Java caches resolved addresses for the process
lifetime unless `networkaddress.cache.ttl` is set.

## IP addressing and CIDR

**Docs:** [RFC 4632 (CIDR)](https://www.rfc-editor.org/rfc/rfc4632.html) ·
[RFC 1918](https://www.rfc-editor.org/rfc/rfc1918.html)

CIDR writes a network as `address/prefix-length`, the prefix counting leading network
bits: `10.0.0.0/24` = 24 network bits, 8 host bits, 256 addresses. It replaced class
A/B/C: right-sized allocations, adjacent prefixes aggregated into one route (supernetting).

| Prefix | Mask | Total | Usable hosts | Usable in AWS subnet |
| :--- | :--- | ---: | ---: | ---: |
| `/16` | 255.255.0.0 | 65,536 | 65,534 | 65,531 |
| `/20` | 255.255.240.0 | 4,096 | 4,094 | 4,091 |
| `/22` | 255.255.252.0 | 1,024 | 1,022 | 1,019 |
| `/24` | 255.255.255.0 | 256 | 254 | 251 |
| `/26` | 255.255.255.192 | 64 | 62 | 59 |
| `/28` | 255.255.255.240 | 16 | 14 | 11 |
| `/30` | 255.255.255.252 | 4 | 2 | - |
| `/32` | 255.255.255.255 | 1 | 1 (single host) | - |

Total = 2^(32 - prefix); two are unusable in a normal network (all-zeros network,
all-ones broadcast). AWS reserves five per subnet (network, VPC router, DNS, future
use, broadcast), so `/28` gives 11 usable; `/28` to `/16` is the AWS size range.

- **Subnetting by hand.** `192.168.10.0/26`: 6 host bits, so blocks are 64 wide —
  `.0/26`, `.64/26`, `.128/26`, `.192/26`; in the first, `.0` is the network,
  `.63` the broadcast, `.1`-`.62` assignable.
- Shortcut: block size = 256 minus the last non-zero mask octet. Verify with `ipcalc 192.168.10.0/26`.

| Range type | CIDR |
| :--- | :--- |
| RFC 1918 private | `10.0.0.0/8` (16.7M), `172.16.0.0/12` (1M), `192.168.0.0/16` (65,536) |
| Carrier-grade NAT (RFC 6598) | `100.64.0.0/10` |
| Loopback | `127.0.0.0/8` |
| Link-local | `169.254.0.0/16`; `169.254.169.254` is cloud metadata |
| Documentation (TEST-NET-1/2/3) | `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` |
| Multicast / reserved | `224.0.0.0/4` / `240.0.0.0/4` |

- Only the first row is RFC 1918 private space; the rest must not be described as
  such. Private ranges are not globally routed, so IPv4 hosts need NAT for egress.
- Planning: size subnets from expected hosts plus growth, keep the same prefix
  across availability zones, reserve contiguous space per region or environment
  so future ranges aggregate into one route.
- `/31` is for point-to-point links; `/32` is a single host, as in firewall rules.

**Gotchas**

- **Never let ranges overlap** between environments or accounts: overlapping
  CIDRs make VPC peering, VPN, and any later merger impossible without
  renumbering — the most common irreversible network design mistake.
- Cloud metadata at `169.254.169.254` is local-only but can expose credentials.
  Require IMDSv2 on EC2 and block untrusted containers from reaching it.

## Network interfaces and diagnostics

**Docs:** [`ip(8)`](https://man7.org/linux/man-pages/man8/ip.8.html) ·
[`ethtool(8)`](https://man7.org/linux/man-pages/man8/ethtool.8.html)

- `ifconfig` and `netstat` are deprecated and often not installed: use `ip addr`,
  `ip link`, `ip route`, `ip neigh`, and `ss`.
- Fields worth knowing: `HWaddr` (MAC, first three octets identify the vendor),
  `inet`/`inet6` addresses (IPv6 link-local scope is not routable), `Bcast`/`Mask`,
  `MTU` (normally 1500 on Ethernet), `UP` (administratively enabled) versus
  `RUNNING` (has carrier).

| Counter | Meaning |
| :--- | :--- |
| `RX errors` | Malformed frames: CRC, length, alignment, FIFO |
| `RX dropped` | Discarded frames, e.g. unexpected VLAN tags |
| `RX overruns` | NIC ring buffer filled faster than the kernel drained it |
| `TX carrier` / `TX collisions` | Carrier lost (flapping link) / duplex mismatch on a switched link |

`ping` sends ICMP echo requests and answers "is it reachable, and how fast".
`traceroute` sends packets with increasing TTL so each router returns ICMP
time-exceeded, answering "where does it break or slow down".

**Gotchas**

- Rising `overruns` or `dropped` on a busy host usually means CPU starvation or
  an undersized ring buffer, not a cable fault. Check `ethtool -S` and `-g`.
- Jumbo frames (MTU 9000) need support end to end. One lower-MTU hop plus
  blocked ICMP silently drops large packets while small ones succeed.
- Middle traceroute hops showing `* * *` are usually routers deprioritising
  ICMP, not a fault; only the **final hop** matters. Prefer `mtr` for per-hop
  loss over time.

## SSH

**Docs:** [`sshd_config(5)`](https://man.openbsd.org/sshd_config.5) ·
[`ssh_config(5)`](https://man.openbsd.org/ssh_config.5) ·
[OpenSSH manual](https://www.openssh.com/manual.html)

Key-based login: the private key stays on your machine, the public key goes in
`~/.ssh/authorized_keys`, and the server verifies a signature — nothing reusable
crosses the network.

```bash
ssh-keygen -t ed25519 -C "user@laptop"
ssh-copy-id user@remote-host
ssh-add ~/.ssh/id_ed25519
ssh -v user@remote-host          # -v diagnoses auth failures
```

| Setting | Recommendation |
| :--- | :--- |
| Key type | `ed25519`; `rsa -b 4096` only where ed25519 is unsupported |
| `~/.ssh` / `authorized_keys` | `700` / `600`, owned by the user |
| `PasswordAuthentication` / `PermitRootLogin` | `no` once keys are in place |
| Agent forwarding (`ssh -A`) | Sparingly: it lets the remote host use your agent |

```text
# ~/.ssh/config
Host bastion
  HostName bastion.example.com
  User ec2-user
Host app-*
  ProxyJump bastion
  IdentityFile ~/.ssh/id_ed25519
```

**Gotchas.** Wrong permissions or ownership on `~/.ssh` or `authorized_keys`
make `sshd` silently fall back to password auth — the most common key-auth
failure. Diagnose with `ssh -v` and the server's auth log.

## systemd and journald

**Docs:** [`systemd.service(5)`](https://man7.org/linux/man-pages/man5/systemd.service.5.html) ·
[`journalctl(1)`](https://man7.org/linux/man-pages/man1/journalctl.1.html)

- systemd is PID 1: starts and supervises services, orders boot dependencies,
  activates sockets and timers, tracks processes in cgroups, sends output to journald.
- **Unit types:** `.service`, `.socket`, `.timer`, `.mount`, `.path`, `.target`.
- **States:** `active (running)` up, `active (exited)` one-shot completed,
  `activating` waiting on a dependency, `failed` start or runtime failure.

```ini
[Unit]
Description=Example API
After=network-online.target
Wants=network-online.target

[Service]
User=app
ExecStart=/opt/example/bin/server
Restart=on-failure
RestartSec=5s
EnvironmentFile=-/etc/example/environment
LimitNOFILE=65536
NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

```bash
systemctl edit example.service      # override under /etc/systemd/system/<unit>.d/
systemctl daemon-reload             # after any unit change
systemctl cat example.service       # vendor unit plus overrides
journalctl -u example.service --since '30 min ago'
journalctl -u example.service -p warning..alert; journalctl -b -1
systemd-analyze critical-chain      # slow boot dependencies
```

| Gotcha | Detail |
| :--- | :--- |
| Do not edit vendor units | Package upgrades replace `/usr/lib/systemd/system` — use `systemctl edit` |
| `enable` does not start | It only creates boot-time dependencies; add `--now` to start immediately |
| Journal loss at reboot | Needs `Storage=persistent` in `journald.conf` or an existing `/var/log/journal` |
| Prefer `reload` | Where the daemon supports it; `restart` drops the process and live connections |

## Nginx

**Docs:** [Nginx documentation](https://nginx.org/en/docs/) ·
[`ngx_http_rewrite_module`](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html)

Config lives in `/etc/nginx/nginx.conf`, with server blocks under
`/etc/nginx/conf.d/` or `sites-available/` symlinked into `sites-enabled/`. HTTP
to HTTPS redirect:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx   # always validate before reloading
```

| Gotcha | Detail |
| :--- | :--- |
| `return 301`, not regex `rewrite` | Faster and clearer; use `302` while testing so a mistake is not cached by browsers and search engines |
| Keep `$request_uri` | It preserves path and query string; redirecting to `https://$host` alone silently drops both |
| Behind TLS termination | Redirect on `$http_x_forwarded_proto = "http"`, or you create a redirect loop |
| `reload` vs `restart` | `reload` replaces workers gracefully; `restart` drops connections |

## Command reference

Syntax grouped by task, linking back to the concept that explains it.

### System, memory, and CPU

```bash
pwd; whoami; id; hostname; uname -a; uptime; date; last; who; history
hostnamectl set-hostname web01   # persistent hostname change
free -h                          # -m/-g for units; read "available", not "free"
cat /proc/meminfo; swapon --show; vmstat 1 5   # memory, swap, I/O, CPU samples
top; htop; nproc; lscpu; mpstat -P ALL 1
```

Interpretation: [Memory](#memory), [CPU load average](#cpu-load-average).

### Files, contents, and disk usage

```bash
ls -al; ls -lh; ls -lt; ls -R; ls -i   # long, human, by time, recursive, inodes
lsof; lsof /var/log/app.log; lsof -i :8080; lsof +L1   # see note below
mkdir -p a/{b,c}; tree a/; stat file; file archive.bin; touch file1
cp -a src/ dest/             # archive mode: recursive, preserves everything
mv file2 dir/; rmdir emptydir; cd -   # rename/move; empty dirs only; previous
rm -rf deletedir             # DESTRUCTIVE: recursive, no prompt
ln target hardlink; ln -s target symlink; readlink -f symlink

cat file; tac file; cat > file; cat file2 >> file1
less /etc/passwd; head -3 file; tail -3 file; nl file; diff -u file1 file2
tail -f /var/log/syslog      # follow appended lines; -F across log rotation

df -h; df -Th; df -i         # space; with type; inode usage
du -sh folder1; du -h --max-depth=1 /var; du -ah /var/log | sort -h | tail -20
lsblk; findmnt; ncdu /var; md5sum file
```

`lsof` lists open files, which process holds one file, which listens on a port
(`-i :8080`), and deleted-but-open files (`+L1`). Inside `less`: `space`/`b`
page, `d`/`u` half page, `/pattern` then `n`, `g`/`G` start and end, `q` quit.

**Gotchas**

- `rm -rf` has no undo and no confirmation — check the path with `ls` first,
  since an unset variable expands to nothing and `rm -rf /$DIR/` becomes
  `rm -rf /`. `>` overwrites, `>>` appends; `set -o noclobber` where an
  accidental `>` would be expensive.
- "No space left on device" with free space in `df -h` means exhausted inodes
  ([Inodes and links](#inodes-and-links)) or a deleted file still held open
  (`lsof +L1`), where space returns only when the process restarts. Growing a
  volume online: [LVM](#lvm).

### Searching and text filters

```bash
find . -name "*.php"                  # quote patterns so the shell keeps them
find / -xdev -type f -name index.html 2>/dev/null   # one filesystem only
find /var/log -iname "*.LOG" -mtime +7 -size +100M  # case-insensitive, age, size
find . -name "*.tmp" -print           # review matches first
find . -name "*.tmp" -delete          # DESTRUCTIVE, cannot be undone
find . -name "*.conf" -exec grep -l listen {} +

grep -i -r "TODO" src/; grep -n "error" app.log; grep -E "error|fatal" app.log
grep -v "debug" app.log; grep -A3 -B3 "panic" app.log   # invert; context
grep -c "error" app.log               # count matching LINES
grep -o -i page test.txt | wc -l      # count occurrences, several per line
which python3; type -a python3; locate nginx.conf

sort -n nums; sort -h sizes; sort -V versions   # numeric, human, version
sort -u; sort -k2 -t, data.csv        # dedupe; second comma-separated field
sort | uniq -c | sort -rn             # frequency count (uniq needs sorted input)
cut -d: -f1 /etc/passwd               # usernames; cut -c1-10 for characters
tr 'a-z' 'A-Z' < file; tr -s ' ' < file; tr -d '\r' < file
sed 's/Hello/hi/g' f          # stdout only, file unchanged
sed -i.bak 's/Hello/hi/g' f   # in place, keeps f.bak (-i alone keeps nothing)
sed -n '10,20p' file; sed '/^#/d' config
awk '{print $1, $3}' file; awk -F: '{print $1}' /etc/passwd
awk '$3 > 100 {print $1}' data; awk '{sum += $2} END {print sum}' data
wc -l file                    # -w words, -c bytes, -m characters
paste f1 f2; tee out.log; xargs -n1 echo
```

**Gotchas**

- `grep -c` counts **lines**, not occurrences.
- Searching from `/` traverses network mounts and virtual filesystems, so narrow the start path and use `-xdev`.
- `sed` without `-i` only changes its output, which is how you test a substitution safely.

### Process management and priority

```bash
ps -ef; ps aux                    # full format; BSD format with CPU/memory
pgrep -a nginx                    # find by name without the grep line
ps -eo pid,ppid,stat,ni,comm --sort=-%cpu | head

kill 3534                         # SIGTERM: ask the process to exit
kill -9 3534                      # SIGKILL: uncatchable, no cleanup
kill -HUP 3534                    # many daemons reload configuration
pkill -f "python worker.py"; killall nginx
pstree -p; lsof -p 3534; strace -p 3534
nohup ./long-job &                # survive terminal logout
jobs; fg; bg                      # Ctrl+Z suspends the foreground job

nice -n 10 ./batch-job; sudo nice -n -5 ./job   # lower priority; negative = root
renice -n 10 -p 3534; renice -n 5 -u builduser  # running process; whole user
ionice -c 3 tar czf backup.tar.gz /data   # idle I/O class, for backups
chrt -p 3534                      # scheduling policy and RT priority
systemd-run -p CPUQuota=20% ./job # hard CPU cap via cgroup
```

**Gotchas**

- Try `kill` before `kill -9`: `SIGKILL` gives no chance to flush buffers or release locks, which is how partially written files and stale lock files appear.
- A process in `D` state ignores both because it is blocked in the kernel.
- Semantics: [Processes](#processes), [Process priority and scheduling](#process-priority-and-scheduling).

### Services, logs, users, and permissions

```bash
systemctl status nginx; systemctl start/stop/restart nginx
systemctl reload nginx           # re-read config without dropping connections
systemctl enable --now nginx; systemctl disable nginx
systemctl list-units --failed; systemctl daemon-reload
journalctl -u nginx --since '1 hour ago'; journalctl -f
journalctl -p err -b             # errors and worse since this boot
dmesg -T | tail -50              # kernel ring buffer with timestamps

groupadd devops; useradd -c "App operator" -m appuser; passwd appuser
useradd -r -s /usr/sbin/nologin appsvc   # service account, cannot log in
usermod -aG devops appuser       # APPEND to secondary groups
usermod -s /bin/bash appuser; usermod -L appuser   # shell; lock account
userdel -r appuser               # DESTRUCTIVE: also deletes home and mail spool
id appuser; groups appuser; getent passwd appuser; chage -l appuser
su - appuser; sudo -u appuser command; sudo -l; visudo

chmod -R g+w shared/; chown -R user:group dir/; chgrp devops file
getfacl file; setfacl -m u:appuser:rw file   # per-user ACLs beyond the 3 classes
```

| Gotcha | Detail |
| :--- | :--- |
| Always `usermod -aG` | Plain `-G` **replaces** the entire secondary group list, a routine way to drop someone's `sudo` or `docker` access — verify with `id` afterwards |
| Before `userdel -r` | Confirm username, home path, running processes, and data ownership with `getent passwd`, `pgrep -u`, `find <approved-path> -user <name> -print` |
| Recursive permission changes | Review with `find <path> -type f -printf '%m %p\n' \| sort -u` first; never run a recursive `chmod` from `/` or a home directory root |
| Semantics | [Permissions](#permissions) |

### Networking commands

```bash
ip -brief addr; ip route; ip neigh; ip route get 10.0.5.20
ip addr add 10.0.0.5/24 dev eth0; ip link set eth0 up
ss -ltnp                         # listening TCP sockets and owning processes
ss -tan state established; ss -s

ping -c 4 example.com; traceroute example.com; mtr example.com
ping -c 4 -M do -s 1472 host     # path MTU probe: 1472 + 28 = 1500
ipcalc 192.168.10.0/26

dig example.com; dig +short example.com; host example.com; nslookup example.com
dig @8.8.8.8 example.com MX      # specific resolver and record type
dig -x 8.8.8.8                   # reverse lookup

curl -I https://example.com      # response headers only
curl -sv https://example.com     # verbose, including the TLS handshake
curl -w '%{time_total}\n' -o /dev/null -s https://example.com
wget -c https://example.com/big.iso   # resume an interrupted download

sudo tcpdump -ni any port 443 -c 20
nc -zv host 5432                 # does the TCP port accept connections?
openssl s_client -connect example.com:443 -servername example.com
ethtool eth0                     # link speed, duplex, carrier
sudo nft list ruleset; sudo nft -c -f rules.nft   # read-only view; syntax check
```

**Gotchas**

- `nc -zv host port` is the fastest way to separate a network problem from an application problem: if the port accepts, path and firewall are fine.
- Never flush a remote ruleset over the connection you depend on — [nftables vs iptables](#nftables-vs-iptables).

### Archives, transfers, and shell productivity

```bash
tar czf backup.tar.gz /data       # create; xzf extracts, tzf lists
tar xzf backup.tar.gz -C /restore
gzip file; gunzip file.gz; zip -r archive.zip dir/; unzip archive.zip
scp -r dir/ user@host:/path/; sftp user@host
rsync -avz --progress src/ user@host:/dest/   # transfers only differences
rsync -avzn --delete src/ dest/   # DRY RUN of the destructive form; review
rsync -avz --delete src/ dest/    # DESTRUCTIVE: deletes anything not in source

command1 | command2          # pipe stdout into stdin
command > out.log            # redirect stdout (overwrite); >> appends
command 2> err.log           # stderr; > all.log 2>&1 for both streams
command1 && command2         # run only if the first succeeded; || if it failed
command &                    # background; $(command) substitutes output
!!; sudo !!; !$              # previous command; with sudo; its last argument
Ctrl+R; Ctrl+A / Ctrl+E / Ctrl+W  # history search; line start/end; delete word
alias ll='ls -alh'           # persist in ~/.bashrc
watch -n2 'kubectl get pods'; timeout 30 ./flaky-command
seq 1 5 | xargs -I{} echo item{}
```

**Gotchas**

- Prefer `rsync` over `scp` for anything large or repeated: it resumes, transfers only changed blocks, and supports `--dry-run`.
- A trailing slash on the source means "the contents of this directory" and omitting it means "this directory itself", so the wrong slash with `--delete` can empty the destination.
- Check what `!!` and `!$` expand to before running them with `sudo`.

## Troubleshooting scenarios

Collect evidence before restarting anything.

### 1. Disk full but `df -h` shows free space

- **Symptom:** writes fail with "No space left on device".
- **Check:** `df -i`; `lsof +L1`; `du -h --max-depth=1 /var | sort -h`.
- **Cause:** inode exhaustion from millions of small files, or a rotated log
  still held open by a running process.
- **Fix:** delete small-file directories, or `truncate -s 0 <file>` on the open
  log rather than deleting it; restart the holder if needed.
- **Prevent:** log rotation, alerts on both `df -h` and `df -i`, a separate
  filesystem for high-churn data.

### 2. High load average, idle CPU

- **Symptom:** load average 3x `nproc` while `top` shows low `%CPU`.
- **Check:** `ps -eo stat,comm | grep '^D'`; `iostat -xz 1`; `vmstat 1`.
- **Cause:** tasks in `D` state blocked on storage, or swap thrashing.
- **Fix:** relieve the storage bottleneck (`ionice -c 3` the offending job), or
  add memory to stop thrashing.
- **Prevent:** alert on `D`-state counts and disk latency, not just CPU. See
  [CPU load average](#cpu-load-average).

### 3. Process disappeared with no application error

- **Symptom:** the service vanishes under load; exit code 137.
- **Check:** `dmesg -T | grep -i -E 'out of memory|killed process'`;
  `journalctl -u <unit> -b`; `cat /proc/<pid>/oom_score_adj` for survivors.
- **Cause:** OOM killer, driven by host exhaustion or a cgroup `memory.max`.
- **Fix:** raise the limit or reduce footprint; cap the runtime's own heap so it
  does not size itself from host memory.
- **Prevent:** cgroup limit plus a matching in-process limit; alert on working
  set approaching the limit, not on restarts. See [Memory](#memory).

### 4. Cannot SSH after a change

- **Symptom:** the connection times out (no `SYN-ACK`) or is refused.
- **Check:** from another path, `nc -zv host 22`; on console,
  `systemctl status sshd`, `sudo nft list ruleset`, `journalctl -u sshd`.
- **Cause:** timeout = packet dropped by firewall or security group, or a
  missing route. Refused = host reachable, `sshd` not listening.
- **Fix:** restore the ruleset from `rules.backup` or start `sshd`, via console
  or out-of-band access.
- **Prevent:** never apply firewall changes over the only session; validate with
  `nft -c -f`, keep a rollback timer, keep console access working.

### 5. Small requests succeed, large transfers hang

- **Symptom:** SSH connects then freezes; large HTTP responses stall.
- **Check:** `ping -c4 -M do -s 1472 host`, reducing size until it passes;
  `ip link show` for MTU on each hop you control.
- **Cause:** MTU mismatch with ICMP fragmentation-needed blocked, so path MTU
  discovery fails.
- **Fix:** lower the MTU to the smallest path value, or allow ICMP type 3 code 4
  through the firewall.
- **Prevent:** consistent MTU end to end; never block all ICMP. See
  [Network interfaces and diagnostics](#network-interfaces-and-diagnostics).

### 6. Application fails with "Too many open files"

- **Symptom:** accept loops fail and the log shows `EMFILE`.
- **Check:** `prlimit --pid <pid>`; `ls /proc/<pid>/fd | wc -l`;
  `systemctl show -p LimitNOFILE <unit>`.
- **Cause:** the `nofile` soft limit is too low, or a descriptor leak.
- **Fix:** set `LimitNOFILE=` in the unit (PAM `limits.conf` does not apply to
  services), and fix the leak. See
  [Resource limits with ulimit](#resource-limits-with-ulimit).
- **Prevent:** set limits in configuration management; monitor descriptor counts.
