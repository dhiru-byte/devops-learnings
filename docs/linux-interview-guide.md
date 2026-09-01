# Linux

Concepts and commands for Linux and networking interview questions. The
concept sections come first; the [command reference](#command-reference) at the
end groups day-to-day syntax by task and links back to the explanation behind
each group.

## Contents

- [Operating system fundamentals](#operating-system-fundamentals)
- [Linux architecture](#linux-architecture)
- [Filesystem](#filesystem)
- [LVM](#lvm)
- [Permissions](#permissions)
- [SELinux vs AppArmor](#selinux-vs-apparmor)
- [Processes](#processes)
- [Process priority and scheduling](#process-priority-and-scheduling)
- [cgroups v1 vs v2](#cgroups-v1-vs-v2)
- [Resource limits with ulimit](#resource-limits-with-ulimit)
- [CPU load average](#cpu-load-average)
- [Memory](#memory)
- [Concurrency problems](#concurrency-problems)
- [Networking fundamentals](#networking-fundamentals)
- [nftables vs iptables](#nftables-vs-iptables)
- [DNS](#dns)
- [IP addressing and CIDR](#ip-addressing-and-cidr)
- [Network interfaces and diagnostics](#network-interfaces-and-diagnostics)
- [HTTP status codes](#http-status-codes)
- [SSH](#ssh)
- [systemd and journald](#systemd-and-journald)
- [Nginx redirect](#nginx-redirect)
- [Shell prompt customisation](#shell-prompt-customisation)
- [Command reference](#command-reference)
  - [System information](#system-information)
  - [Memory and CPU](#memory-and-cpu)
  - [Files and directories](#files-and-directories)
  - [Viewing and editing file contents](#viewing-and-editing-file-contents)
  - [Searching](#searching)
  - [Text filters](#text-filters)
  - [Counting](#counting)
  - [Disk usage](#disk-usage)
  - [Process management](#process-management)
  - [Process priority commands](#process-priority-commands)
  - [Services and logs](#services-and-logs)
  - [Users and groups](#users-and-groups)
  - [Permission commands](#permission-commands)
  - [Networking commands](#networking-commands)
  - [Archives and transfers](#archives-and-transfers)
  - [Shell productivity](#shell-productivity)

## Operating system fundamentals

### What is an operating system?

An operating system is the layer between users and hardware. It translates
user and application requests into hardware operations, and it arbitrates
access to CPU, memory, storage, and devices so that many programs can run at
once without interfering with each other.

Categories by concurrency support: single-user single-tasking, single-user
multitasking, and multi-user multitasking. Linux is multi-user multitasking.

### Functions of an operating system

| Function | What it does |
| :--- | :--- |
| Process (processor) management | Create, schedule, and terminate processes; provide synchronisation and IPC |
| Memory management | Allocate and reclaim memory; maintain each process's virtual address space |
| File management | Organise, store, retrieve, name, share, and protect files |
| Device and I/O management | Track devices, allocate them, and hide hardware-specific behaviour |
| Secondary storage management | Move data between cache, main memory, and disks |
| Security | Authenticate users and enforce permissions |
| Networking | Provide the stack that lets processes on different machines communicate |
| Communication management | Move data between processes on the same host or across the network |
| Command interpretation | Parse shell or system commands and act on resources |
| Job accounting | Track resource use per user and per job |

### What is Linux?

Linux is a UNIX-like operating system built around the Linux kernel, released by
Linus Torvalds in 1991 and developed as free software. It runs on x86, ARM,
POWER, RISC-V, and s390x, from embedded devices to mainframes, which is why it
is the default platform for servers and containers.

### UNIX vs Linux

UNIX began as proprietary software at Bell Labs and split into commercial
variants such as AIX, HP-UX, and Solaris, each tied to specific vendor hardware.
Linux is an independent, open-source kernel with a UNIX-like interface, licensed
under the GPL, packaged by many distributions, and portable across hardware.
Practically: UNIX certification and vendor support versus Linux openness,
hardware freedom, and a far larger ecosystem.

### The GNU project

GNU supplied the userland (compiler, C library, coreutils, shell) that a kernel
needs to be a usable system, and the GPL that keeps it open. The freedoms it
established are to run the software for any purpose, to study and modify it, to
redistribute copies, and to publish improvements. This is why a Linux system is
often called GNU/Linux.

### Boot loaders

The boot loader loads the kernel into memory and hands control to it.
**GRUB 2** is the standard on current distributions; it understands
filesystems, supports a menu and kernel parameters, and can chain-load other
systems. **LILO** was the earlier Linux loader and is obsolete: it stored block
lists and had to be rerun after every kernel change. `systemd-boot` is common on
UEFI-only systems.

Boot order on a modern system: firmware (UEFI/BIOS) to boot loader (GRUB) to
kernel to `initramfs` to `init` (systemd) to target units.

### The root account

`root` is UID 0, the superuser, and it bypasses permission checks. It can create
and manage users, change any file, and load kernel modules.

In practice you do not log in as root. Administrators use `sudo` so that every
privileged action is attributable in the audit log and scoped by
`/etc/sudoers`. Disabling direct root SSH login (`PermitRootLogin no`) is
standard hardening.

### Desktop environments

A Linux system can have several desktop environments installed, such as GNOME
and KDE, and you choose one at the login screen; the choice persists until you
change it. One is normally enough, and some applications integrate better with
the toolkit of their own environment. On servers, no desktop environment is
installed at all, since it only adds attack surface and resource use.

### vi modes

- **Command mode:** the mode `vi` starts in; keystrokes are navigation and
  editing operators.
- **Insert mode:** entered with `i`, `a`, or `o`; keystrokes are inserted as
  text. `Esc` returns to command mode.
- **Last-line (ex) mode:** entered with `:` from command mode, for commands such
  as `:w`, `:q!`, and `:%s/old/new/g`.

## Linux architecture

Linux is a set of concentric layers. Hardware sits at the centre; user programs
sit on the outside. Each layer only talks to the ones next to it.

| Layer | Role | Examples |
| :--- | :--- | :--- |
| Hardware | Physical machine | CPU, RAM, disks, NICs |
| Kernel | Owns devices, memory, filesystems, and scheduling; exposes system calls | VFS, device drivers, multitasking |
| Shell | Reads commands, starts programs, returns output | `bash`, `sh`, `zsh`, `ksh` |
| Utilities | Userland programs invoked through the shell | `ls`, `cat`, `vi`, `awk`, `sort` |

**Hardware** is the physical layer.

**Kernel** is the core that manages communication between software and
hardware. It owns scheduling, memory management, the filesystem layer, device
drivers, and the network stack, and it exposes all of that through system calls.

**Shell** is the interface that reads user commands, invokes programs, and
returns output. Where the kernel is the innermost layer, the shell is the
outermost.

**Utilities** are the userland programs that make the system usable: coreutils,
text processing tools, networking tools, and package management.

### Kernel types

- **Monolithic:** all OS services run in a single kernel address space. Fast,
  because there is no message passing between subsystems, but a fault anywhere
  can take down the system. Linux is monolithic, with loadable modules so
  drivers can be added at runtime.
- **Microkernel:** only the minimum (scheduling, IPC, basic memory management)
  runs in kernel space, while drivers and filesystems run as user-space
  servers. More robust and smaller, at the cost of IPC overhead. QNX and Minix
  are examples.
- **Hybrid:** a microkernel design with performance-critical services pulled
  back into the kernel. Windows NT and XNU (macOS) are examples.
- **Exokernel:** exposes hardware resources almost directly and leaves
  abstractions to applications; mainly a research design.

Kernel responsibilities to name in an interview: process scheduling,
inter-process communication, synchronisation, context switching, memory
management, and system-call handling.

### Shells

| Shell | Notes |
| :--- | :--- |
| `sh` (Bourne) | The original scripting shell; today usually a link to `dash` or `bash` in POSIX mode |
| `bash` | The default interactive shell on most distributions |
| `dash` | Small, fast POSIX shell used as `/bin/sh` on Debian and Ubuntu |
| `ksh` (Korn) | Bourne-compatible with additions; common on commercial UNIX |
| `csh` / `tcsh` | C-like syntax; poor for scripting |
| `zsh` | Bash-compatible enough for daily use, richer completion; default on macOS |

Write portable scripts against `sh`, or declare `#!/usr/bin/env bash`
explicitly. A script with a `#!/bin/sh` shebang that uses bash-only syntax such
as arrays or `[[ ]]` breaks on Debian, where `/bin/sh` is `dash`.

## Filesystem

### Filesystem hierarchy

| Path | Contents |
| :--- | :--- |
| `/` | Root of the entire hierarchy |
| `/root` | Home directory of the root user |
| `/home` | Home directories of regular users |
| `/boot` | Kernel, `initramfs`, and boot loader files such as GRUB configuration |
| `/etc` | System-wide configuration, for example `/etc/passwd`, `/etc/fstab` |
| `/usr` | Installed software: `/usr/bin`, `/usr/lib`, `/usr/share` |
| `/opt` | Self-contained third-party software |
| `/bin`, `/sbin` | Essential user and administrator binaries; symlinks into `/usr` on modern systems |
| `/lib` | Shared libraries and kernel modules |
| `/dev` | Device nodes, for example `/dev/sda`, `/dev/null` |
| `/proc` | Virtual filesystem of kernel and process state, for example `/proc/cpuinfo` |
| `/sys` | Virtual filesystem exposing devices, drivers, and cgroups |
| `/var` | Variable data: logs, spool, caches, `/var/lib/docker` |
| `/tmp` | Temporary files, world-writable, often cleared at boot |
| `/mnt` | Mount point for temporary manual mounts |
| `/media` | Mount point for removable media |
| `/run` | Runtime state since boot, on tmpfs, for example PID and socket files |

### Inodes

An inode is the on-disk data structure holding a file's metadata and the
pointers to its data blocks. The filename is not part of the inode: a directory
entry maps a name to an inode number, which is what makes hard links possible.

An inode holds owner UID, group GID, file type, permission bits and ACLs, size,
link count, timestamps (access, modification, inode change), and the block
pointers. It does **not** hold the filename or the file contents.

```bash
ls -i file            # inode number
stat file             # all inode fields in readable form
df -i                 # inode usage per filesystem
```

A filesystem can run out of inodes while free space remains, which shows up as
"No space left on device" with `df -h` looking healthy. Millions of tiny files,
typically cache or session files, are the usual cause; check `df -i`.

### Hard links vs symbolic links

A **hard link** is an additional directory entry pointing at the same inode. All
names are equal; the data is freed only when the link count reaches zero and no
process holds the file open. Renaming or moving one name does not affect the
others.

A **symbolic link** is a small file whose content is a path. It behaves like a
Windows shortcut and can point at a file, a directory, or nothing at all.

| | Hard link | Symbolic link |
| :--- | :--- | :--- |
| Points to | The inode | A pathname |
| Across filesystems | No | Yes |
| To a directory | Not permitted | Yes |
| Survives deletion of the original | Yes | No, becomes a dangling link |
| Own inode | No, shares it | Yes |
| Created with | `ln target name` | `ln -s target name` |

### Configuration and virtual filesystems

**`/etc/passwd`** holds one colon-separated line per account. Example:

```text
mark:x:1001:1001:mark,,,:/home/mark:/bin/bash
```

| Field | Example | Meaning |
| :---: | :--- | :--- |
| 1 | `mark` | Username |
| 2 | `x` | Password placeholder; the hash lives in `/etc/shadow` |
| 3 | `1001` | UID |
| 4 | `1001` | Primary GID |
| 5 | `mark,,,` | GECOS comment (full name and optional contact fields) |
| 6 | `/home/mark` | Home directory |
| 7 | `/bin/bash` | Login shell |

`/etc/shadow` is readable only by root. A shell of `/usr/sbin/nologin` marks a
service account that cannot log in.

**`/etc/fstab`** is the administrator-maintained list of filesystems to mount at
boot, with device (preferably by `UUID=`), mount point, type, options, dump, and
fsck order. A wrong entry can leave the system unbootable, so validate with
`mount -a` before rebooting.

**`/etc/mtab`** is the system-maintained list of currently mounted filesystems;
on modern systems it is a symlink to `/proc/self/mounts`. A connected but
unmounted disk does not appear there. Use `findmnt` to read mounts.

The relationship: mount a device manually, confirm it in `/etc/mtab` or
`findmnt`, then add the equivalent line to `/etc/fstab` so it mounts on boot or
on `mount -a`.

**`/etc/hosts`** maps hostnames to addresses locally and is consulted before
DNS, per `/etc/nsswitch.conf`. It is the quickest way to pin or override a name
during testing.

```text
127.0.0.1     localhost
192.168.49.2  hello-world.info
```

**`/etc/resolv.conf`** configures the resolver library: `nameserver` entries to
query, plus `search` domains and `options`. On hosts running
`systemd-resolved` or NetworkManager it is generated, so edit the manager's
configuration instead or the change is overwritten.

```text
nameserver 10.0.80.11
nameserver 10.0.80.12
search example.internal
```

**`/proc`** is a virtual filesystem created in memory at boot and gone at
shutdown. It exposes kernel and per-process state as readable files and is the
main channel between kernel space and user space: `/proc/cpuinfo`,
`/proc/meminfo`, `/proc/loadavg`, `/proc/<pid>/status`, `/proc/<pid>/fd`, and
writable tunables under `/proc/sys` reached through `sysctl`.

### Daemons

A daemon is a background service process with no controlling terminal. It waits
for requests, serves them, and returns to waiting. Names conventionally end in
`d`: `sshd`, `crond`, `dockerd`. On current distributions daemons are managed by
systemd units:

```bash
systemctl status sshd
systemctl enable --now sshd
journalctl -u sshd --since '1 hour ago'
```

## LVM

Logical Volume Manager adds a flexible layer between disks and filesystems:

`physical volume (PV) -> volume group (VG) -> logical volume (LV) -> filesystem`

- A **PV** is a disk or partition initialised with `pvcreate`.
- A **VG** pools one or more PVs with `vgcreate`; free extents in the pool can
  be assigned to any LV.
- An **LV** is the block device created with `lvcreate`, such as
  `/dev/vgdata/lvapp`. Put a filesystem on it and mount it normally.

Typical online growth:

```bash
sudo pvs; sudo vgs; sudo lvs          # inspect before changing anything
sudo lvextend -r -L +10G /dev/vgdata/lvapp
```

`-r` grows the filesystem after the LV. Without it, the block device grows but
the filesystem does not. Extending is routine; shrinking is risky, filesystem
dependent, usually requires unmounting, and can destroy data if the filesystem
is not shrunk first. Take and verify a backup before any shrink.

An LVM snapshot is copy-on-write and useful for a short, crash-consistent backup
window, not as a durable backup: it shares the same disks, consumes VG space as
the origin changes, and becomes invalid if that space fills.

## Permissions

Three permission bits apply to three identity classes: user (owner), group, and
others.

| Permission | On a file | On a directory |
| :--- | :--- | :--- |
| Read (r, 4) | Read the contents | List the entries |
| Write (w, 2) | Modify the contents | Create, rename, delete entries |
| Execute (x, 1) | Run it | Enter it and access entries by name |

Numeric form adds the bits per class:

```bash
chmod 650 test.txt    # user rw- (4+2), group r-x (4+1), others --- (0)
chmod 644 file        # owner read/write, everyone else read
chmod 755 script.sh   # owner all, others read and execute
```

Symbolic form combines who (`u`, `g`, `o`, `a`), an operator (`+`, `-`, `=`),
and which bits (`r`, `w`, `x`):

```bash
chmod ug+rw test.txt      # add read and write for user and group
chmod o-rwx secret.txt    # remove all access for others
chmod a=r file            # set exactly read for everyone
chown user:group file
umask 022                 # default mask: new files 644, new directories 755
```

Note that write permission on a **directory** is what allows deleting a file
inside it, regardless of the file's own permissions. That is why `/tmp` needs
the sticky bit.

### Special bits

| Bit | Numeric | Effect |
| :--- | :--- | :--- |
| SUID | 4000 | Executable runs with the owner's privileges, for example `/usr/bin/passwd` |
| SGID | 2000 | On a binary, runs with the group's privileges; on a directory, new entries inherit the directory's group |
| Sticky | 1000 | In a shared directory, only the owner of a file may delete it, for example `/tmp` |

```bash
chmod 4755 binary      # SUID, shows as rwsr-xr-x
chmod 2775 shared_dir  # SGID, shows as rwxrwsr-x
chmod 1777 /tmp        # sticky, shows as rwxrwxrwt
find / -xdev -perm -4000 -type f 2>/dev/null   # audit one local filesystem
```

Unnecessary SUID root binaries are a standard privilege-escalation route; audit
them and remove the bit where it is not needed. A scan from `/` can be expensive
and can enter network mounts; prefer `find / -xdev ...` per local filesystem,
run it in a low-traffic period, and inspect results before changing permissions.

Reference: [SUID, SGID and the sticky bit](https://www.redhat.com/sysadmin/suid-sgid-sticky-bit)

## SELinux vs AppArmor

Traditional mode bits and ACLs are discretionary access control: an owner can
grant access. SELinux and AppArmor add **mandatory access control (MAC)**, so a
policy can deny an action even when Unix permissions allow it.

| | SELinux | AppArmor |
| :--- | :--- | :--- |
| Policy model | Labels every subject and object; rules allow type interactions | Profiles programs by pathname and allowed operations |
| Common distributions | RHEL, Fedora, CentOS Stream, Amazon Linux | Ubuntu, Debian, SUSE |
| Modes | Enforcing, permissive, disabled | Enforce, complain, disabled per profile |
| Strength | Fine-grained and robust across path changes | Easier to read and adopt |
| First diagnostics | `getenforce`, `ausearch -m AVC`, `sealert` | `aa-status`, kernel/journal `DENIED` messages |

Do not disable MAC to fix a denial. Confirm the application is using the
expected path and label, inspect the audit event, and make the smallest policy
change. For SELinux, `restorecon -Rv /path` repairs expected labels and
`semanage fcontext` makes a custom mapping persistent; `chcon` alone is
temporary. For AppArmor, update the named profile, test in complain mode, then
reload it with `apparmor_parser`.

## Processes

### Process vs thread

A process is a program in execution with its own virtual address space. A thread
is a unit of execution inside a process; threads of one process share the
address space but each has its own stack and registers.

| | Process | Thread |
| :--- | :--- | :--- |
| Weight | Heavier | Lighter |
| Address space | Its own | Shared with siblings |
| Creation and teardown cost | Higher | Lower |
| Context switch cost | Higher, needs an address-space switch | Lower |
| Isolation | Isolated by default | None inside the process |
| Communication | IPC: pipes, sockets, shared memory, signals | Shared memory directly, needs locking |
| Failure blast radius | One process dies | Usually the whole process dies |

The kernel tracks each process through a task structure (the process control
block) holding PID, parent PID, state, priority, register context, memory maps,
and open file descriptors. Threads can be implemented at kernel level, at user
level, or as a hybrid; Linux implements them as tasks sharing memory, created by
`clone()`.

Shared state is the trade-off: threads communicate cheaply but require locking,
which is where deadlocks and race conditions come from. Processes cost more but
fail independently.

### Process states

| State in `ps`/`top` | Meaning |
| :--- | :--- |
| `R` | Running or runnable, on a CPU or waiting for one |
| `S` | Interruptible sleep, waiting on an event, the normal idle state |
| `D` | Uninterruptible sleep, usually blocked on disk or network I/O |
| `T` | Stopped by a signal or a debugger |
| `Z` | Zombie, finished but not yet reaped |

Many processes in `D` state are the signature of a storage problem: the
processes cannot be killed because they are inside a kernel call, and load
average climbs even though CPU is idle.

### Zombie and orphan processes

A **zombie** (`Z`, "defunct") has finished executing, but its exit status is
still in the process table because the parent has not called `wait()`. It holds
no memory or CPU, only a table entry. A few are normal; a growing count is a bug
in the parent, and the fix is to restart or fix the parent, since a zombie
cannot be killed. When the parent dies, `init` adopts and reaps them.

An **orphan** is a process whose parent exited first. It keeps running and is
re-parented to `init` (PID 1). Orphans are not an error, unlike zombies.

```bash
ps -eo pid,ppid,stat,cmd | awk '$3 ~ /^Z/'   # list zombies and their parents
```

### `top` output columns

| Column | Meaning |
| :--- | :--- |
| `PID` | Process ID |
| `USER` | Owner |
| `PR` | Kernel scheduling priority, lower is more favoured |
| `NI` | Nice value, `-20` to `19`, user-settable |
| `VIRT` | Total virtual address space mapped |
| `RES` | Resident set: physical RAM currently in use |
| `SHR` | Portion of `RES` that is shared, for example shared libraries |
| `S` | Process state |
| `%CPU` | Share of one CPU's time since the last refresh; can exceed 100% for multi-threaded processes |
| `%MEM` | `RES` as a percentage of total physical memory |
| `TIME+` | Cumulative CPU time, to hundredths of a second |
| `COMMAND` | Command name or full command line |

`RES` is the number that matters for memory pressure. Summing `RES` across
processes over-counts, because shared pages are counted once per process.

Reference: [How to use top](https://www.howtogeek.com/668986/how-to-use-the-linux-top-command-and-understand-its-output/)

## Process priority and scheduling

Linux schedules normal tasks with **CFS** (the Completely Fair Scheduler), which
allocates CPU time in proportion to a task's weight rather than running a strict
priority queue. Nice value sets that weight.

### Nice and priority

- **Nice (`NI`)** ranges from `-20` (most favoured) to `19` (least favoured),
  default `0`. It is a hint about relative CPU share, not a reservation.
- **Priority (`PR`)** is what the kernel shows: for normal tasks
  `PR = 20 + NI`, so nice `0` displays as `PR 20` and nice `-20` as `PR 0`.
  Real-time tasks display as `RT` or a negative value.
- Each step of nice changes the task's CPU weight by roughly 10%, so nice `-5`
  against nice `0` is a large difference under contention and no difference at
  all on an idle machine.
- **Lowering** a nice value (raising priority) requires root. Any user may
  raise their own nice value, which is irreversible without privileges.

Syntax for setting and changing priority is in
[Process priority commands](#process-priority-commands).

### Scheduling policies

| Policy | Use |
| :--- | :--- |
| `SCHED_OTHER` (CFS) | Default for all normal processes; nice applies here |
| `SCHED_BATCH` | CPU-bound background work; the scheduler assumes no interactivity |
| `SCHED_IDLE` | Runs only when nothing else wants the CPU |
| `SCHED_FIFO` / `SCHED_RR` | Real-time, priority 1 to 99, always preempts normal tasks |

Real-time policies (`chrt -f 50 ./app`) preempt everything below them, so a
busy-looping real-time task can make a machine unresponsive. Use them only for
genuine latency requirements.

### Related controls

- **I/O priority** is separate from CPU priority. A backup that starves the disk
  needs `ionice -c 3 tar ...` (idle class), not `nice`.
- **cgroups** are the right tool for enforcing shares between workloads, and are
  what containers and systemd use. `systemd-run -p CPUQuota=20% ./job` caps a
  job at 20% of one CPU, which `nice` cannot do because nice only sets relative
  weight.
- **OOM priority** is also separate: `/proc/<pid>/oom_score_adj` biases which
  process the kernel kills under memory pressure.

## cgroups v1 vs v2

Control groups account for and limit CPU, memory, I/O, process count, and other
resources for a process tree. Containers and systemd services are cgroups with
namespaces and policy layered on top.

| | cgroups v1 | cgroups v2 |
| :--- | :--- | :--- |
| Hierarchy | Separate hierarchy per controller | One unified hierarchy |
| Process membership | A process can be in different groups per controller | One process belongs to one cgroup |
| Interface | Controller-specific and inconsistent | Consistent files such as `cpu.max`, `memory.max`, `pids.max` |
| Memory control | Weaker accounting and delegation | Better pressure, swap, and OOM controls |
| Modern default | Legacy and compatibility systems | Current systemd distributions and Kubernetes |

Detect the mode with `stat -fc %T /sys/fs/cgroup`: `cgroup2fs` means v2.
Inspect a service with `systemctl status`, `systemd-cgls`, and
`systemd-cgtop`. Prefer systemd properties such as `CPUQuota=`,
`MemoryMax=`, `TasksMax=`, and `IOWeight=` over writing control files by hand,
because systemd owns the hierarchy and reapplies the configuration.

In v2, `memory.high` throttles and reclaims before failure, while `memory.max`
is the hard ceiling that can trigger a cgroup OOM kill. `cpu.weight` is a
relative share under contention; `cpu.max` is a hard quota. The distinction is
the same as Docker `--cpu-shares` versus `--cpus`.

## Resource limits with ulimit

`ulimit` is a shell builtin that reads and sets per-process resource limits.
Children inherit the limits, so it affects only programs launched from that
shell; it does not retroactively change an existing process.

```bash
ulimit -a                 # inspect all limits
ulimit -Sn / ulimit -Hn  # soft and hard open-file limits
ulimit -n 65536          # raise the soft limit, but never above the hard limit
prlimit --pid <pid>      # inspect limits of an existing process
```

The **soft limit** is the enforced value a process may raise up to the **hard
limit**. Only root or a process with the needed capability can raise the hard
limit. Common failures are `Too many open files` (`nofile`) and inability to
create threads or processes (`nproc`).

Persistent interactive-user limits belong in `/etc/security/limits.conf` or
`limits.d`, but systemd services do not use PAM limits: set
`LimitNOFILE=`, `LimitNPROC=`, and related directives in the unit. For
containers, use the runtime's `--ulimit` plus cgroup limits; `ulimit` alone does
not constrain aggregate resource use across a service.

## CPU load average

Load average is the number of tasks that are **running or waiting to run**,
averaged over the last 1, 5, and 15 minutes. On Linux it also counts tasks in
uninterruptible sleep (`D` state), so heavy disk or network I/O raises load even
when the CPU is idle.

```bash
uptime
# 15:42:01 up 9 days,  2:14,  2 users,  load average: 3.84, 3.72, 2.41
cat /proc/loadavg
nproc                 # number of logical CPUs, the denominator
```

Read it **relative to the CPU count**, because one logical CPU runs one task at
a time.

| Load | 1 CPU | 4 CPUs |
| :--- | :--- | :--- |
| 0.5 | 50% busy, no queue | 12.5% busy, mostly idle |
| 1.0 | Fully busy, no queue | 25% busy |
| 4.0 | 4x oversubscribed, about 3 tasks waiting | Fully busy, no queue |
| 8.0 | Severely oversubscribed | 2x oversubscribed, about 4 tasks waiting |

So for the example `3.84, 3.72, 2.41`:

- On a **1-CPU** host this is a serious backlog: demand is about 3.8 times
  capacity, and it has been rising over the last 15 minutes (2.41 to 3.84).
- On a **4-CPU** host it is near full utilisation with little or no queueing.
- On a **16-CPU** host it is roughly 24% utilised and unremarkable.

Practical reading:

- Divide by `nproc` to get a utilisation ratio. Sustained above 1.0 per CPU
  means tasks are waiting.
- Compare the three numbers to get direction: 1-minute above 15-minute means the
  load is growing, the reverse means it is draining.
- High load with low CPU utilisation in `top` means the queue is I/O-bound.
  Confirm with `iostat -xz 1` and by counting `D`-state tasks in
  `ps -eo stat,comm`.
- Load average is a count of tasks, not a percentage. A load of 2.0 is not "200%
  CPU"; on a 4-CPU host it is comfortable.

## Memory

### Virtual vs resident memory

**Virtual memory** is the abstraction that gives each process its own
contiguous address space, backed by a mix of physical RAM, files mapped into
memory, and swap. `VIRT` in `top` is the total size of that mapped address
space, which includes shared libraries, memory-mapped files, and reserved but
untouched allocations. It is routinely far larger than actual usage and is a
poor indicator of pressure.

**Resident memory** (`RES`) is the part of that address space currently held in
physical RAM. This is the number to watch. Under pressure, the kernel reclaims
resident pages using an approximate least-recently-used policy: clean
file-backed pages are dropped, dirty pages are written back, and anonymous
pages go to swap.

A common wrong statement is "virtual memory is disk space that acts as RAM".
That describes **swap**, which is only one backing store for a virtual address
space.

```bash
free -h                # total, used, free, buff/cache, available
cat /proc/meminfo       # detailed kernel view
ps -eo pid,rss,vsz,comm --sort=-rss | head
```

In `free`, read the **available** column, not **free**. Page cache under
`buff/cache` is reclaimable on demand, so a healthy Linux host normally shows
very little truly free memory, and that is by design.

### Swap

Swap is disk or file space the kernel uses to hold anonymous pages that do not
fit in RAM, letting the system keep running past physical capacity at a very
large latency cost.

```bash
swapon --show
free -h
sysctl vm.swappiness            # 0 to 100, default 60: bias toward swapping anonymous pages
```

Sizing, replacing the old "twice physical RAM" rule, which came from systems
with a few hundred megabytes of memory:

- Small hosts (up to 2 GB RAM): about twice RAM.
- Mid-range (2 to 8 GB): roughly equal to RAM.
- Large servers (8 GB and above): 4 to 8 GB is normally sufficient, unless you
  need hibernation, which requires swap at least the size of RAM.
- Latency-sensitive databases often run with little or no swap and rely on
  correct sizing plus monitoring instead, because swapping a database is worse
  than failing fast.
- Kubernetes historically required swap to be disabled, and many production
  clusters still do that for predictable memory accounting. Modern kubelet can
  use swap when `failSwapOn: false` and the `NodeSwap` feature is enabled. Set
  `memorySwap.swapBehavior` to `NoSwap` (Pods do not use swap) or
  `LimitedSwap` (bounded use for supported cgroup v2 configurations). Treat this
  as an explicit cluster policy: verify the Kubernetes version, container
  runtime, cgroup mode, and eviction behaviour rather than assuming swap is
  either always forbidden or always safe.

Continuous swap-in and swap-out (thrashing) is a capacity problem, not something
to tune away; check `vmstat 1` columns `si` and `so`.

### The OOM killer

When memory cannot be reclaimed, the kernel picks a process and kills it rather
than letting the whole system stall. It chooses by `oom_score`, which is driven
mainly by memory footprint and adjusted by
`/proc/<pid>/oom_score_adj` (`-1000` to `1000`).

```bash
dmesg -T | grep -i -E 'out of memory|killed process'
cat /proc/<pid>/oom_score
```

A process that vanishes with no application-level error and exit code 137 was
almost certainly OOM-killed. In a container, that usually means the cgroup
memory limit, not host exhaustion.

## Concurrency problems

### Deadlock

A deadlock is a cycle of processes each holding a resource and waiting for one
held by another, so none can proceed. All four Coffman conditions must hold at
once:

- **Mutual exclusion:** a resource can be held by only one process at a time.
- **Hold and wait:** a process holding a resource can request another.
- **No preemption:** resources cannot be forcibly taken back.
- **Circular wait:** a closed chain exists, for example P0 waits on P1, P1 waits
  on P2, and P2 waits on P0.

Break any one condition and deadlock becomes impossible. The practical fix is to
break circular wait by acquiring locks in a globally fixed order, or to break
hold-and-wait with timeouts and `try_lock`.

### Starvation

Starvation is a process that is ready to run but keeps being passed over,
because higher-priority work continuously takes the resource it needs. Unlike
deadlock, the system as a whole makes progress; one participant does not.

Causes: strict priority scheduling without ageing, unfair resource allocation
policies, random selection instead of queueing, and simple resource shortage.

The standard remedy is **ageing**: raise a waiting process's effective priority
the longer it waits, which guarantees it eventually runs. Linux CFS avoids
starvation for normal tasks by design, since it distributes time by weight
rather than by strict priority, but real-time policies (`SCHED_FIFO`) can starve
normal tasks.

### Deadlock vs starvation vs livelock

| | Deadlock | Starvation | Livelock |
| :--- | :--- | :--- | :--- |
| System progress | None among the involved processes | Yes, others proceed | None, though state keeps changing |
| Cause | All four Coffman conditions hold | Unfair scheduling or allocation | Repeated conflicting retries or back-offs |
| Blocked processes | Waiting forever, holding resources | Waiting forever, holding nothing | Actively running but achieving nothing |
| Resolution | Break a condition, or detect and abort a participant | Ageing, fair queueing | Randomised back-off |

Note that "circular wait" is one of the four deadlock conditions, not another
name for deadlock, and livelock is a distinct third failure mode rather than
another name for starvation.

## Networking fundamentals

### OSI model

The OSI model describes seven layers that systems use to communicate over a
network. It was the first standard reference model and remains the shared
vocabulary for isolating faults, even though the internet actually runs on the
simpler four-layer TCP/IP model.

Mnemonic, application down to physical: All People Seem To Need Data Processing.

| Layer | Name | Function | Examples |
| :---: | :--- | :--- | :--- |
| 7 | Application | Human-facing protocols; applications access network services | HTTP, DNS, SSH, SMTP |
| 6 | Presentation | Encoding, encryption, compression | TLS, JPEG |
| 5 | Session | Session establishment, checkpoints, and teardown | RPC, NetBIOS |
| 4 | Transport | End-to-end delivery and ports | TCP, UDP |
| 3 | Network | Addressing and routing between networks | IP, ICMP, routers |
| 2 | Data link | Framing on the local segment, MAC addresses | Ethernet, ARP, switches |
| 1 | Physical | Bits on the medium | Cables, radio, NICs, hubs |

Matching layers on two hosts communicate *logically* (HTTP to HTTP, TCP to TCP).
Only layer 1 has a real physical medium between machines.

TCP/IP collapses the same stack into four layers. Hardware sits at the bottom
of that mapping:

| OSI | TCP/IP | Typical device |
| :--- | :--- | :--- |
| 7 Application, 6 Presentation, 5 Session | Application | Host / reverse proxy / WAF |
| 4 Transport | Transport | Layer-4 load balancer |
| 3 Network | Internet / Network | Router |
| 2 Data link | Network interface / Link | Switch |
| 1 Physical | Network interface / Link | Hub, cable, NIC |

The mapping matters when reading load balancer documentation: a "layer 4" load
balancer forwards TCP connections without seeing the request, while a "layer 7"
load balancer parses HTTP and can route on path, host, and headers.

### TCP

TCP is connection-oriented and reliable. It numbers bytes, acknowledges receipt,
retransmits what is lost, reorders what arrives out of sequence, and applies
flow control so a fast sender cannot overwhelm a slow receiver, plus congestion
control so it cannot overwhelm the network. Use it when every byte matters: HTTP
and HTTPS, SSH, database connections, file transfer.

### UDP

UDP is connectionless. It sends datagrams with no handshake, no
acknowledgements, no retransmission, and no ordering guarantee, which makes it
faster and lower-overhead but unreliable. Use it when timeliness beats
completeness: video and voice, gaming, metrics, and DNS. Applications that need
reliability over UDP implement it themselves, as QUIC and HTTP/3 do.

### The TCP three-way handshake

The handshake establishes a connection and synchronises both sides' sequence
numbers before any data flows.

| Step | Flag | Direction | Sequence | Acknowledgement | Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SYN` | Client to server | `X` | - | "I want to connect, my sequence starts at X" |
| 2 | `SYN-ACK` | Server to client | `Y` | `X + 1` | "Accepted, and my sequence starts at Y" |
| 3 | `ACK` | Client to server | `X + 1` | `Y + 1` | "Acknowledged, connection established" |

State transitions: the client goes `SYN-SENT` then `ESTABLISHED`; the server
goes `LISTEN`, `SYN-RECEIVED`, then `ESTABLISHED`. Teardown is a separate
four-way exchange of `FIN` and `ACK`, ending in `TIME_WAIT` on the closing side.

Operational reading:

- **Connection timeouts with retransmitted `SYN`s** mean the `SYN` or the
  `SYN-ACK` is being dropped: a firewall or security group rule, a missing
  route, or nothing listening on the port. `ss -tan state syn-sent` and
  `tcpdump -ni any 'tcp[tcpflags] & tcp-syn != 0'` distinguish them.
- **Connection refused** is different: the packet arrived and the host replied
  with `RST` because no process is listening. That is a service problem, not a
  network problem.
- **SYN flood** is a denial-of-service attack that sends `SYN` packets and never
  completes the handshake, exhausting the backlog. Mitigations are SYN cookies
  (`net.ipv4.tcp_syncookies`) and a larger `tcp_max_syn_backlog`.
- **Many sockets in `TIME_WAIT`** on a busy client is normal; it protects
  against stale duplicate segments. Fix it with connection reuse and keep-alive,
  not by disabling the protection.
- A successful handshake does not guarantee data flows. An MTU mismatch with
  blocked ICMP fragmentation-needed messages lets small packets through and
  hangs large transfers, the classic "SSH connects then freezes" symptom.

### Core protocols and ports

| Protocol | Layer | Port | Transport | Notes |
| :--- | :---: | :---: | :--- | :--- |
| SSH / SFTP / SCP | 7 | 22 | TCP | Remote shell and file transfer; SFTP is an SSH subsystem, not FTP |
| SMTP | 7 | 25, 465, 587 | TCP | Sending mail only; 587 with STARTTLS is the modern submission port |
| DNS | 7 | 53 | UDP, TCP | UDP for queries, TCP for zone transfer and large responses |
| HTTP | 7 | 80 | TCP | Plaintext web traffic |
| POP3 / IMAP | 7 | 110 / 143 | TCP | Retrieving mail; 995 and 993 over TLS |
| NTP | 7 | 123 | UDP | Time synchronisation |
| HTTPS | 7 | 443 | TCP (QUIC over UDP for HTTP/3) | HTTP inside TLS |
| FTP | 7 | 21 control, 20 data | TCP | Plaintext, dual channel |
| MySQL / PostgreSQL | 7 | 3306 / 5432 | TCP | Never expose to the internet |
| TCP / UDP | 4 | - | - | Transport itself; ports belong to this layer |

HTTPS wraps HTTP in TLS, which provides encryption against eavesdropping,
integrity against tampering, and server authentication through certificates.
It is what defeats man-in-the-middle attacks and is mandatory for anything
handling user data.

### TLS 1.2 vs TLS 1.3 handshake

Both versions authenticate the server's certificate, negotiate cryptographic
parameters, derive shared symmetric traffic keys, and then carry encrypted
application data. The important difference is round trips and what is encrypted.

**TLS 1.2, normally two round trips before HTTP data:**

1. Client sends `ClientHello` with supported versions, cipher suites, random
   value, and extensions.
2. Server returns `ServerHello`, certificate chain, and key-exchange parameters.
3. Client validates the hostname, validity, chain, and trust anchor; sends its
   key-exchange value and `Finished`.
4. Server derives the same session keys and sends `Finished`. Application data
   can now flow.

With modern ECDHE, both sides contribute ephemeral values, giving forward
secrecy. Older TLS 1.2 RSA key exchange lacks it and should be disabled.

**TLS 1.3, one round trip:** the client's first message already includes
key-share candidates. The server selects one and sends its certificate,
signature, and `Finished` in one response; the client validates and returns its
`Finished`, then sends application data. TLS 1.3 removes obsolete RSA key
exchange, static Diffie-Hellman, CBC suites, and renegotiation, and encrypts
more of the handshake.

Session resumption avoids a full certificate exchange. TLS 1.3 can send
**0-RTT early data**, but it is replayable, so use it only for idempotent
requests and never for operations such as payments or state changes.

### FTP, FTPS, and SFTP

**FTP** uses two channels. The client always opens the control connection to
server TCP 21:

- In **active mode**, the client sends its chosen address and port with `PORT`;
  the server opens the data connection from server TCP 20 back to that client
  port. Client-side NAT and firewalls commonly block this unsolicited inbound
  connection.
- In **passive mode**, the client sends `PASV`/`EPSV`; the server returns a
  high port and the client opens the data connection to it. This works better
  through client NAT, but the server firewall and security group must allow and
  the FTP server must advertise a configured passive-port range.

FTP sends credentials and data in plaintext and should not be used on an
untrusted network.

**FTPS** is FTP with a TLS layer added, comparable to HTTP becoming HTTPS. It
keeps the multi-port design, so it is awkward behind NAT and strict firewall or
security group rules.

**SFTP** is not FTP at all: it is a subsystem of SSH running over port 22. One
port, encrypted by default, and it supports SSH key authentication, which is
what makes it usable in an unattended CI/CD pipeline. It is the default choice.

### Measuring network performance

- **Latency:** time for data to travel from source to destination, usually
  reported as round-trip time.
- **Packet loss:** fraction of transmitted packets that never arrive; even 1%
  badly degrades TCP throughput.
- **Throughput:** data actually delivered per unit time, measured with `iperf3`.
- **Bandwidth:** the theoretical maximum capacity of the link.
- **Jitter:** variance in latency; the metric that matters for voice and video.

Throughput on a single TCP stream is bounded by roughly window size divided by
round-trip time, which is why a high-bandwidth intercontinental link still
transfers a large file slowly without window scaling or parallel streams.

## nftables vs iptables

Both configure the Linux kernel's Netfilter packet-processing hooks. `iptables`
is the older frontend with separate tools and rule sets for IPv4, IPv6, ARP,
and bridges. `nftables` is the modern replacement: one `nft` command, one rules
language, atomic ruleset updates, reusable sets/maps, and native dual-stack
rules.

On many current distributions, `iptables` is the compatibility frontend
`iptables-nft`, which translates commands into nftables rules. Check
`iptables --version` before assuming legacy mode; mixing direct `nft` changes
with a firewall manager such as firewalld, UFW, Docker, or Kubernetes can cause
the manager to overwrite or bypass your rules.

```bash
sudo nft list ruleset                  # read-only inspection
sudo iptables-save                     # read-only legacy/compatibility view
sudo nft -c -f rules.nft               # syntax-check without applying
sudo nft list ruleset > rules.backup   # back up before an approved change
```

Packets traverse base chains attached to hooks such as `input` (addressed to
this host), `output` (created here), and `forward` (routed through the host).
NAT is separate: source NAT/masquerade changes outbound source addresses and
destination NAT changes the inbound destination.

Never flush a remote host's firewall interactively: one mistake can cut off SSH
and leave no recovery path. Use a console or out-of-band session, keep an
automatic rollback timer, validate first, and apply through the distribution's
persistent firewall service.

## DNS

### What happens when you type a URL

1. **URL parsing and HSTS.** The browser splits the URL into scheme, host, and
   path, and checks its HSTS list. If the host is listed, `http://` is rewritten
   to `https://` before any packet is sent.
2. **Name resolution.** The browser checks its own cache, then the OS cache and
   `/etc/hosts`, then asks the configured recursive resolver. The resolver, if it
   has nothing cached, queries a **root** server, then the **TLD** server for
   `.com`, then the **authoritative** server for the domain, and returns the
   address. Each answer is cached for its TTL.
3. **TCP handshake.** `SYN`, `SYN-ACK`, `ACK` to the server on port 443.
4. **TLS handshake.** Cipher negotiation, certificate presentation and
   validation against the trust store, and key exchange producing a symmetric
   session key. TLS 1.3 completes this in one round trip, and session resumption
   in zero.
5. **HTTP request and response.** The browser sends `GET /`, a server such as
   Nginx handles it or proxies to the application, and the response returns with
   a status code and body.
6. **Rendering.** HTML is parsed into the DOM, CSS into the CSSOM, the two
   combine into the render tree, layout computes geometry, and paint and
   compositing produce pixels. Subresources trigger more requests, reusing the
   connection.

Where latency actually goes: DNS resolution and the TLS handshake on a first
visit, then round-trip time on subsequent requests. A CDN, connection keep-alive,
and TLS session resumption address all three. Render-blocking CSS in `<head>`
and deferred JavaScript exist for the same reason: the critical rendering path
needs the CSSOM early and should not wait on scripts.

### Record types

| Record | Purpose |
| :--- | :--- |
| `A` | Hostname to IPv4 address |
| `AAAA` | Hostname to IPv6 address |
| `CNAME` | Alias to another name; cannot coexist with other records at the same name, so not valid at a zone apex |
| `ALIAS` / `ANAME` | Provider-specific apex alias; resolves to another name but behaves like an `A` record and can coexist with other records |
| `MX` | Mail exchanger for the domain, with a preference value |
| `NS` | Authoritative nameservers for a zone |
| `PTR` | Address to hostname, the reverse of `A`, used in reverse DNS and mail reputation |
| `SRV` | Host **and port** for a named service, used by SIP, XMPP, and Kubernetes |
| `TXT` | Arbitrary text; carries SPF, DKIM, DMARC, and domain-verification tokens |
| `SOA` | Zone metadata: primary server, serial, refresh, and negative-cache TTL |
| `CAA` | Which certificate authorities may issue for the domain |
| `URL` | Provider feature, not a DNS record type: returns an HTTP 301 redirect |

Chained example:

```text
blog.dnsimple.com.      CNAME  aetrion.github.io.
aetrion.github.io.      CNAME  github.map.fastly.net.
github.map.fastly.net.  A      185.31.17.133
```

Rules worth stating: `A`, `AAAA`, and `ALIAS` resolve a name to an address;
`CNAME` and `ALIAS` must point at a name, not an address; a `URL` record is a
redirect, so the browser address bar changes, while the others are invisible to
the user. Use `A` when the address is known and stable, `CNAME` when you want to
follow someone else's name, and `ALIAS` when you need apex-level aliasing.

Full list: [DNS record types](https://www.nslookup.io/learning/dns-record-types)

### TTL

TTL is how long a resolver may cache an answer before asking again. It is the
trade-off between query volume and change propagation: a 24-hour TTL keeps load
low but means a change can take a day to be visible everywhere.

The operational pattern before a planned migration is to lower the TTL to 60
seconds a day or two ahead, make the change, verify, then raise it again. Note
that a "5-minute DNS cutover" is optimistic in practice, because some resolvers
and many application runtimes cache beyond the TTL. Java in particular caches
resolved addresses for the process lifetime unless
`networkaddress.cache.ttl` is set.

### Transport

DNS uses **UDP port 53** for ordinary queries and responses, because a single
small exchange does not justify a TCP handshake and a failed query can simply be
retried. It uses **TCP port 53** for zone transfers (AXFR/IXFR) and whenever a
response is too large for the negotiated UDP size, which is common with DNSSEC.
DNS over TLS (853) and DNS over HTTPS (443) add privacy.

### DNS as a load balancer

Yes, DNS can distribute traffic. Returning several `A` records for one name
spreads clients across addresses (round robin), and providers add
latency-based, geolocation, weighted, and failover routing on top, with health
checks removing unhealthy endpoints.

Its limits are the reason a real load balancer still sits behind it: client and
intermediate caching means removal is not immediate, DNS has no view of
connection counts or server load, and clients may pin to one answer for a long
time. DNS is therefore the right tool for coarse geographic and regional
distribution, and a layer 4 or layer 7 load balancer for distribution within a
region.

## IP addressing and CIDR

**CIDR** (Classless Inter-Domain Routing) writes a network as
`address/prefix-length`, where the prefix length is the number of leading bits
that identify the network. `10.0.0.0/24` means the first 24 bits are the
network, leaving 8 bits, so 256 addresses.

It replaced the fixed class A/B/C system, in which the only choices were 8, 16,
and 24 bit networks. An organisation needing 400 addresses had to take a class B
of 65,536 and waste the rest. Arbitrary prefix lengths allow right-sized
allocations, and adjacent prefixes can be aggregated into one routing table
entry (supernetting), which is what slowed routing table growth and extended the
usable life of IPv4.

### Prefix reference

| Prefix | Subnet mask | Total addresses | Usable hosts | Usable in an AWS subnet |
| :--- | :--- | ---: | ---: | ---: |
| `/16` | 255.255.0.0 | 65,536 | 65,534 | 65,531 |
| `/20` | 255.255.240.0 | 4,096 | 4,094 | 4,091 |
| `/22` | 255.255.252.0 | 1,024 | 1,022 | 1,019 |
| `/24` | 255.255.255.0 | 256 | 254 | 251 |
| `/26` | 255.255.255.192 | 64 | 62 | 59 |
| `/28` | 255.255.255.240 | 16 | 14 | 11 |
| `/30` | 255.255.255.252 | 4 | 2 | - |
| `/32` | 255.255.255.255 | 1 | 1 (a single host) | - |

Total addresses are 2 to the power of (32 minus prefix). Two are unusable in a
normal network: the all-zeros network address and the all-ones broadcast
address. AWS reserves five per subnet (network, VPC router, DNS, future use, and
broadcast), which is why a `/28` gives 11 usable addresses there, and why a
`/28` is the smallest and a `/16` the largest subnet AWS accepts.

### Working out a subnet by hand

For `192.168.10.0/26`: the prefix leaves 6 host bits, so blocks are 64
addresses wide and the subnets are `192.168.10.0/26`, `.64/26`, `.128/26`, and
`.192/26`. Within the first, `.0` is the network address, `.63` is the
broadcast, and `.1` to `.62` are assignable.

The shortcut is that the block size is 256 minus the last non-zero mask octet:
a `/26` mask ends in 192, and 256 minus 192 is 64.

```bash
ipcalc 192.168.10.0/26            # network, broadcast, host range
ip route get 10.0.5.20            # which route and interface would be used
ip -brief addr                    # interface addresses with prefixes
```

### RFC 1918 private IPv4 ranges

| Range | CIDR | Size |
| :--- | :--- | :--- |
| 10.0.0.0 to 10.255.255.255 | `10.0.0.0/8` | 16.7 million |
| 172.16.0.0 to 172.31.255.255 | `172.16.0.0/12` | 1 million |
| 192.168.0.0 to 192.168.255.255 | `192.168.0.0/16` | 65,536 |

These ranges are private-use address space and are not globally routed on the
internet, so IPv4 hosts using them need NAT for internet egress.

### Special-use IPv4 ranges

These are **not RFC 1918 private space** and must not be described as such:

| CIDR | Purpose |
| :--- | :--- |
| `100.64.0.0/10` | Shared address space for carrier-grade NAT (RFC 6598) |
| `127.0.0.0/8` | Loopback; packets never leave the host |
| `169.254.0.0/16` | Link-local autoconfiguration; `169.254.169.254` is also used by cloud metadata services |
| `192.0.2.0/24` | TEST-NET-1, documentation examples |
| `198.51.100.0/24` | TEST-NET-2, documentation examples |
| `203.0.113.0/24` | TEST-NET-3, documentation examples |
| `224.0.0.0/4` | Multicast |
| `240.0.0.0/4` | Reserved |

Cloud metadata at `169.254.169.254` is routable only from the local workload
environment but can expose credentials. On EC2 require IMDSv2 and block
untrusted containers or proxies from reaching it.

### Planning a network

- Size subnets from expected host count plus growth, then keep the same prefix
  across availability zones so the plan is readable.
- Never let ranges overlap between environments or accounts. Overlapping CIDRs
  make VPC peering, VPN, and any later merger impossible without renumbering,
  and this is the single most common irreversible network design mistake.
- Reserve contiguous space per region or environment so future ranges can be
  aggregated into one route.
- Note that `/31` and `/32` are special cases: `/31` is used for point-to-point
  links and `/32` denotes a single host, which is the form used in security
  group and firewall rules.

References: [CIDR explained](https://www.youtube.com/watch?v=z07HTSzzp3o),
[binary numbers](https://www.javatpoint.com/binary-numbers-list)

## Network interfaces and diagnostics

### Reading interface state

`ifconfig` is deprecated and not installed by default on current distributions.
Use the `ip` suite: `ip addr`, `ip link`, `ip route`, `ip neigh`, and `ss` in
place of `netstat`. The `ifconfig` fields still appear in older documentation, so
know what they mean.

| Field | Meaning |
| :--- | :--- |
| `Link encap` | Interface type, for example Ethernet or Local Loopback |
| `HWaddr` | MAC address; the first three octets identify the vendor |
| `inet addr` | IPv4 address |
| `inet6 addr` | IPv6 address, with `Scope` link-local (not routable) or global |
| `Bcast` | Broadcast address |
| `Mask` | Subnet mask |
| `MTU` | Maximum transmission unit, normally 1500 bytes on Ethernet |
| `UP` | Interface is administratively enabled |
| `RUNNING` | Interface has carrier and can pass data |
| `BROADCAST`, `MULTICAST` | Interface supports broadcast and multicast |
| `RX/TX packets`, `bytes` | Totals received and transmitted |
| `RX errors` | Malformed frames: CRC, length, alignment, FIFO overruns |
| `RX dropped` | Frames discarded, for example unexpected VLAN tags |
| `RX overruns` | The NIC ring buffer filled faster than the kernel drained it |
| `TX carrier` | Carrier lost, typically a flapping link or duplex mismatch |
| `TX collisions` | Ethernet collisions; nonzero on a modern switched link means a duplex mismatch |
| `txqueuelen` | Transmit queue length |

Rising `overruns` or `dropped` on a busy host usually points to CPU starvation
or an undersized ring buffer rather than a cable fault; check with
`ethtool -S <iface>` and `ethtool -g <iface>`.

MTU is worth understanding because mismatches produce confusing failures. Jumbo
frames (MTU 9000) improve throughput on networks that support them end to end,
but a single hop with a lower MTU, combined with blocked ICMP, causes large
packets to be dropped silently while small ones succeed.

Interface, socket, path-MTU, and link-layer commands are in
[Networking commands](#networking-commands).

Reference: [ifconfig](https://www.computerhope.com/unix/uifconfi.htm)

### Ping vs traceroute

`ping` sends ICMP echo requests and tells you whether a host answers and with
what round-trip time. It answers "is it reachable".

`traceroute` maps the path. It sends packets with increasing TTL so each router
along the route returns an ICMP time-exceeded message, revealing hop by hop
which routers are involved and how long each leg takes. It answers "where does
it break or slow down".

Reading traceroute output correctly matters: middle hops showing `* * *` or high
latency are often just routers deprioritising ICMP, not a fault. Only the final
hop's latency and loss are meaningful. `mtr` is better in practice because it
samples continuously and shows loss per hop over time.

## HTTP status codes

| Class | Meaning | Common examples |
| :--- | :--- | :--- |
| 1xx | Informational, protocol-level | 101 Switching Protocols |
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 4xx | Client error | 400, 401 Unauthorized, 403 Forbidden, 404, 409 Conflict, 429 Too Many Requests |
| 5xx | Server error | 500, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

The ones to know cold when debugging behind a proxy or load balancer:

- **401 vs 403:** 401 means not authenticated, 403 means authenticated but not
  authorised.
- **502** means the proxy reached the upstream but got an invalid or no
  response, usually a crashed or unready backend.
- **503** means the service is deliberately unavailable, for example no healthy
  targets behind a load balancer.
- **504** means the upstream did not answer within the proxy's timeout, so the
  backend is slow rather than down.

Reference: [HTTP status codes](https://restfulapi.net/http-status-codes/)

## SSH

### Key-based login without a password

```bash
ssh-keygen -t ed25519 -C "user@laptop"     # generate a key pair
ssh-copy-id user@remote-host               # append the public key to the remote authorized_keys
ssh-add ~/.ssh/id_ed25519                  # load the private key into the agent
ssh user@remote-host                       # no password prompt
```

How it works: the private key stays on your machine, the public key goes into
`~/.ssh/authorized_keys` on the server, and the server verifies a signature you
produce with the private key. Nothing reusable crosses the network.

Practical detail:

- Prefer `ed25519` over `rsa`: shorter keys, faster, and no key-size decision to
  get wrong. Use `rsa -b 4096` only where `ed25519` is unsupported.
- Permissions are enforced by `sshd` and are the usual reason key auth silently
  falls back to a password: `~/.ssh` must be `700` and `authorized_keys` `600`,
  owned by the user. Diagnose with `ssh -v` and the server's auth log.
- `ssh-agent` holds the decrypted key so a passphrase-protected key is still
  convenient. Use `ssh -A` agent forwarding sparingly, since it lets the remote
  host use your agent.
- Once keys are in place, set `PasswordAuthentication no` and
  `PermitRootLogin no` in `/etc/ssh/sshd_config`.
- Use `~/.ssh/config` for per-host settings, including `ProxyJump` for bastion
  access:

```text
Host bastion
  HostName bastion.example.com
  User ec2-user

Host app-*
  ProxyJump bastion
  User ec2-user
  IdentityFile ~/.ssh/id_ed25519
```

## systemd and journald

systemd is PID 1 on most Linux distributions. It starts and supervises services,
orders boot dependencies, activates sockets and timers, tracks processes in
cgroups, and records service output in journald.

Unit types include `.service`, `.socket`, `.timer`, `.mount`, `.path`, and
`.target`. Useful service states are:

- `active (running)`: the process is up;
- `active (exited)`: a one-shot setup completed successfully;
- `failed`: start or runtime failure; inspect `systemctl status` and the journal;
- `activating`: start is still in progress or waiting on a dependency.

```ini
[Unit]
Description=Example API
After=network-online.target
Wants=network-online.target

[Service]
User=app
Group=app
WorkingDirectory=/opt/example
ExecStart=/opt/example/bin/server
Restart=on-failure
RestartSec=5s
EnvironmentFile=-/etc/example/environment
NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

Use `systemctl edit example.service` for an override under
`/etc/systemd/system/example.service.d/`; do not edit a vendor unit under
`/usr/lib/systemd/system`, because package upgrades replace it. After changing a
unit run `systemctl daemon-reload`, then `restart` if required. `enable` only
creates boot-time dependencies; `--now` also starts the service immediately.

journald indexes logs by fields such as unit, PID, priority, and boot:

```bash
systemctl status example.service
journalctl -u example.service --since '30 min ago'
journalctl -u example.service -p warning..alert
journalctl -b -1                         # previous boot
journalctl -o json-pretty -n 1           # structured fields
systemd-analyze critical-chain           # slow boot dependencies
systemctl cat example.service            # vendor unit plus overrides
```

Configure persistence and size in `/etc/systemd/journald.conf`; without
`Storage=persistent` or an existing `/var/log/journal`, logs may be lost at
reboot. Prefer `reload` when a daemon supports it; `restart` drops the process
and potentially live connections.

## Nginx redirect

Nginx configuration lives in `/etc/nginx/nginx.conf`, with per-site server
blocks under `/etc/nginx/conf.d/` or `/etc/nginx/sites-available/` symlinked
into `sites-enabled/`.

Redirect all HTTP traffic to HTTPS:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}
```

Practical detail:

- `return 301` is the right construct; a `rewrite` with a regular expression
  does the same thing more slowly and less clearly.
- Use `301` for a permanent move, since browsers and search engines cache it,
  and `302` while testing so a mistake is not cached.
- `$request_uri` preserves the path and query string. Redirecting to
  `https://$host` alone silently drops both.
- Always validate before reloading: `nginx -t` then `systemctl reload nginx`.
  Reload replaces workers gracefully without dropping connections; restart does
  not.
- Behind a load balancer that terminates TLS, redirect on
  `$http_x_forwarded_proto = "http"` instead, otherwise you create a redirect
  loop.

## Shell prompt customisation

`PS1` defines the primary prompt. Set it in `~/.bashrc` for interactive bash
shells, or `~/.bash_profile` on macOS where login shells are the norm.

```bash
PS1='\u@\h:\w\$ '                              # user@host:dir$
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\w\$ '   # green user@host, then default colour
PS1='\d \T \w\$ '                              # date, 24-hour time, working directory
```

Common escapes: `\u` user, `\h` short hostname, `\w` working directory, `\W`
its basename, `\d` date, `\T` 12-hour time, `\t` 24-hour time, `\$` shows `#`
for root and `$` otherwise.

Wrap colour codes in `\[` and `\]`. Without them bash miscounts the prompt
width, and long command lines wrap over themselves. A prompt that shows the
current Kubernetes context, AWS profile, or Git branch is worth the setup on a
machine that touches production.

## Command reference

Day-to-day syntax grouped by task. Each group links back to the concept section
that explains the behaviour behind it. Commands that delete data or change
system state are marked; run the read-only form first and confirm the target
before running the destructive one.

### System information

```bash
pwd                          # print working directory
whoami                       # current username
id                           # UID, GID, and group membership
hostname                     # current hostname
hostnamectl set-hostname web01   # change it persistently
uname -a                     # kernel name, version, and architecture
uptime                       # time since boot, users, and load average
date                         # current date and time
cal                          # this month's calendar
last                         # recent logins
who                          # who is logged in now
history                      # commands from this shell session
man pwd                      # manual page for a command
clear                        # clear the terminal, same as Ctrl+L
echo testing                 # print text to stdout
```

### Memory and CPU

```bash
free -h                      # memory in human-readable units
free -m                      # in megabytes; -b bytes, -k kilobytes, -g gigabytes
cat /proc/meminfo            # detailed kernel memory accounting
swapon --show                # active swap devices and usage
vmstat 1 5                   # five one-second samples: memory, swap, I/O, CPU
vmstat -s                    # memory statistics as a list
top                          # live process and resource view
htop                         # top with a nicer interface, if installed
nproc                        # number of logical CPUs
lscpu                        # CPU model, cores, sockets, caches
cat /proc/cpuinfo            # per-CPU detail
mpstat -P ALL 1              # per-CPU utilisation over time
```

How to read these numbers, including why `available` matters more than `free`
and how load relates to CPU count, is in [Memory](#memory) and
[CPU load average](#cpu-load-average).

### Files and directories

```bash
ls                           # list entries
ls -al                       # long format, including dotfiles
ls -lh                       # long format with human-readable sizes
ls -lt                       # newest first; add -r to reverse
ls -R                        # recurse into subdirectories
ls -i                        # show inode numbers
lsof                         # open files and the processes holding them
lsof /var/log/app.log        # which process holds one file
lsof -i :8080                # which process listens on a port

touch file1 file2            # create empty files, or update timestamps
mkdir mydir
mkdir -p Technology/{Devops/{docker,ansible,kubernetes},Cloud/{AWS,Azure,GCP}}
tree Technology/             # verify the structure; ls -R also works

cp image.jpg Downloads/
cp -rvfp ./Technology /home/Technology   # recursive, verbose, force, preserve attributes
cp -a src/ dest/             # archive mode: recursive and preserves everything

mv file2 Technology/         # move
mv sample.txt kernelfile     # rename a file
mv ktdir kerneldir           # rename a directory

rmdir emptydir               # remove an empty directory only
rm -rf deletedir             # destructive: removes recursively without prompting

ln target hardlink           # hard link: same inode, same filesystem only
ln -s target symlink         # symbolic link: a path, may cross filesystems

stat file                    # inode metadata: owner, size, links, timestamps
file archive.bin             # identify content type
readlink -f symlink          # resolve to the final absolute path
```

`mkdir -p` with brace expansion creates the whole tree in one command:

```text
Technology/
├── Cloud
│   ├── AWS
│   ├── Azure
│   └── GCP
└── Devops
    ├── ansible
    ├── docker
    └── kubernetes
```

`rm -rf` has no undo and no confirmation. Check the path with `ls` first,
especially when it contains a variable, since an unset variable expands to
nothing and `rm -rf /$DIR/` becomes `rm -rf /`.

The difference between the two link types is explained in
[Hard links vs symbolic links](#hard-links-vs-symbolic-links).

#### Changing directory

```bash
cd /            # root directory
cd ~            # home directory; plain cd does the same
cd ..           # parent directory
cd -            # previous directory
```

### Viewing and editing file contents

```bash
cat file                     # print the whole file
cat > file                   # write from stdin, overwriting; end with Ctrl+D
cat >> file                  # append from stdin
cat file2 >> file1           # append file2 to file1
cat file1 file2 > file3      # concatenate into a new file
tac file                     # print lines in reverse order

less /etc/passwd             # page through a file
head /etc/passwd             # first 10 lines
head -3 /etc/passwd          # first 3 lines
tail /etc/passwd             # last 10 lines
tail -3 /etc/passwd          # last 3 lines
tail -f /var/log/syslog      # follow appended lines
tail -F /var/log/syslog      # follow across log rotation

nl file                      # number the lines
diff file1 file2             # line differences
diff -u file1 file2          # unified diff, the format patches use
md5sum file                  # checksum, for verifying a transfer
```

`>` overwrites and `>>` appends. Both create the file if it does not exist. Use
`set -o noclobber` in a shell where an accidental `>` would be expensive.

Inside `less`: `space` or `f` forward one screen, `b` back one screen, `d` and
`u` half a screen, `/pattern` search forward, `n` next match, `g` and `G` start
and end, `v` open the file in your editor, `q` quit. `less` is preferable to
`more` because it scrolls backwards and does not load the whole file.

Editing modes in `vi` are described in [vi modes](#vi-modes).

### Searching

```bash
find . -name "process.txt"           # by name, from the current directory
find / -xdev -type d -name techno 2>/dev/null     # one filesystem; scanning / can be slow
find / -xdev -type f -name index.html 2>/dev/null # avoid network/pseudo filesystems
find . -type f -name "*.php"         # by pattern; quote it so the shell does not expand it
find . -iname "*.LOG"                # case-insensitive
find /var/log -mtime +7              # modified more than 7 days ago
find /var/log -size +100M            # larger than 100 MB
find . -name "*.tmp" -print          # inspect matches first
find . -name "*.tmp" -delete         # destructive; run only after reviewing -print
find . -name "*.conf" -exec grep -l listen {} +   # run a command on the matches

grep hello sample                    # lines containing a pattern
grep -i hello sample                 # case-insensitive
grep -r "TODO" src/                  # recurse through a directory
grep -n "error" app.log              # with line numbers
grep -v "debug" app.log              # invert: lines not matching
grep -c "error" app.log              # count matching lines
grep -o -i page test.txt | wc -l     # count occurrences, including several per line
grep -A3 -B3 "panic" app.log         # 3 lines of context each side
grep -E "error|fatal" app.log        # extended regular expression

locate nginx.conf                    # query the filename database, needs updatedb
which python3                        # first match in PATH
type -a python3                      # every match, plus aliases and builtins
```

`grep -c` counts **lines** that match. To count total occurrences when a line
can match more than once, use `grep -o` and pipe to `wc -l`.

Searching from `/` can traverse huge network mounts and changing virtual
filesystems. Narrow the starting path where possible; `-xdev` stays on one
filesystem and redirecting permission errors keeps results readable.
`find ... -delete` cannot be undone: run the exact expression with `-print`
first and quote patterns so the shell does not expand them prematurely.

### Text filters

Filters read stdin and write stdout, so they compose with pipes.

```bash
sort sample.txt              # alphabetic order
sort -n numbers.txt          # numeric order, so 9 sorts before 10
sort -h sizes.txt            # human-readable numbers, so 2K sorts before 1M
sort -r sample.txt           # descending
sort -u sample.txt           # sort and drop duplicates
sort -k2 -t, data.csv        # by the second comma-separated field
sort | uniq -c | sort -rn    # frequency count, highest first

cut -d: -f1 /etc/passwd      # first colon-delimited field: usernames
cut -d ' ' -f1 sample.txt    # first space-delimited field
cut -c1-10 file              # first 10 characters of each line

tr 'a-z' 'A-Z' < file        # translate characters
tr -s ' ' < file             # squeeze repeated spaces
tr -d '\r' < file            # strip carriage returns from a Windows file

sed 's/Hello/hi/g' sample.txt        # substitute on stdout, file unchanged
sed -i 's/Hello/hi/g' sample.txt     # edit the file in place, no backup
sed -i.bak 's/Hello/hi/g' sample.txt # in place, keeping sample.txt.bak
sed -n '10,20p' file                 # print only lines 10 to 20
sed '/^#/d' config                   # drop comment lines

awk '{print $1, $3}' file            # select fields
awk -F: '{print $1}' /etc/passwd     # with a field separator
awk '$3 > 100 {print $1}' data       # filter on a field value
awk '{sum += $2} END {print sum}' data   # aggregate

uniq -c sorted.txt           # count adjacent duplicates; input must be sorted
wc -l file                   # count lines
paste file1 file2            # join files side by side
tee out.log                  # write stdout to a file and pass it along
xargs -n1 echo               # turn stdin lines into command arguments
```

`sort -n` is numeric and `sort -d` is dictionary order, which ignores
punctuation and is not numeric. Sorting version-numbered output needs
`sort -V`, and sorting `du` output needs `sort -h`.

`sed` without `-i` only changes its output, which is what makes it safe to test
a substitution before committing to it. Prefer `-i.bak` on a file you cannot
easily regenerate.

### Counting

```bash
wc -l Linux.md               # lines
wc -w Linux.md               # words
wc -c Linux.md               # bytes
wc -m Linux.md               # characters, which differs from bytes for UTF-8
```

### Disk usage

```bash
df -h                        # free space per filesystem
df -Th                       # include the filesystem type
df -i                        # inode usage, the other way to run out of space
du -sh folder1               # total size of one directory
du -h --max-depth=1 /var     # size of each immediate subdirectory
du -ah /var/log | sort -h | tail -20    # the 20 largest entries
lsblk                        # block devices, partitions, and mount points
mount | column -t            # currently mounted filesystems
findmnt                      # mounts as a readable tree
ncdu /var                    # interactive disk usage browser, if installed
```

"No space left on device" while `df -h` shows free space has two causes.
Exhausted inodes are the first, described in [Inodes](#inodes). The second is a
deleted file still held open by a process (`lsof +L1`), in which case the space
returns only when that process restarts.

Growing a logical volume online is covered in [LVM](#lvm).

### Process management

```bash
ps                           # your processes in this terminal
ps -ef                       # every process, full format
ps aux                       # every process, BSD format with CPU and memory shares
ps -ef | grep nginx          # find a process by name
pgrep -a nginx               # same result without the grep line itself
ps -eo pid,ppid,stat,ni,comm --sort=-%cpu | head

kill 3534                    # send SIGTERM: ask the process to exit
kill -9 3534                 # SIGKILL: cannot be caught, no cleanup
kill -HUP 3534               # SIGHUP: many daemons reload configuration
pkill -f "python worker.py"  # by command line pattern
killall nginx                # by process name

pstree -p                    # process hierarchy with PIDs
lsof -p 3534                 # files and sockets held by one process
strace -p 3534               # system calls, for a hung process
nohup ./long-job &           # survive terminal logout
jobs / fg / bg               # shell job control
Ctrl+Z                       # suspend the foreground job
```

Try `kill` before `kill -9`. `SIGKILL` gives the process no chance to flush
buffers or release locks, which is how partially written files and stale lock
files appear. A process stuck in `D` state ignores both, because it is blocked
in the kernel.

Process states, zombies, and orphans are explained in [Processes](#processes),
which also shows how to list zombies and their parents.

### Process priority commands

The relationship between `PR` and `NI`, and the cases where nice has no effect
at all, are in
[Process priority and scheduling](#process-priority-and-scheduling).

```bash
nice -n 10 ./batch-job           # start with a lower priority
sudo nice -n -5 ./latency-job    # start with a higher priority; negative needs root
renice -n 10 -p 3534             # change a running process by PID
renice -n 5 -u builduser         # change every process of a user
ps -fl -C "perl test.pl"         # verify the nice value took effect
ps -eo pid,ni,pri,comm --sort=ni | head
ionice -c 3 tar czf backup.tar.gz /data   # idle I/O class, for backups
chrt -p 3534                     # scheduling policy and real-time priority
systemd-run -p CPUQuota=20% ./job # hard CPU cap through a cgroup
```

Reference: [nice and renice examples](https://www.thegeekstuff.com/2013/08/nice-renice-command-examples/)

### Services and logs

```bash
systemctl status nginx
systemctl start nginx / stop nginx / restart nginx
systemctl reload nginx           # re-read configuration without dropping connections
systemctl enable --now nginx     # start now and on boot
systemctl disable nginx
systemctl list-units --failed    # everything currently broken
systemctl daemon-reload          # after editing a unit file

journalctl -u nginx              # logs for one unit
journalctl -u nginx --since '1 hour ago'
journalctl -f                    # follow all logs
journalctl -p err -b             # errors and worse since this boot
journalctl --disk-usage          # how much space the journal uses

dmesg -T | tail -50              # kernel ring buffer with timestamps
```

Prefer `reload` over `restart` for a web server or proxy: reload replaces
workers gracefully, restart drops in-flight connections. Unit file structure and
overrides are in [systemd and journald](#systemd-and-journald).

### Users and groups

`usermod` modifies an existing account: group membership, login shell, home
directory, username, expiry, and lock state.

```bash
groupadd devops
useradd -c "Application operator" -m appuser   # create the account and home
useradd -r -s /usr/sbin/nologin appsvc   # service account that cannot log in
passwd appuser                   # set or change a password
usermod -aG devops appuser       # append; without -a, replace all secondary groups
usermod -s /bin/bash appuser     # change the login shell
usermod -d /home/appuser2 -m appuser     # move the home directory
usermod -L appuser               # lock the account
userdel appuser                  # delete the account
userdel -r appuser               # destructive: also deletes home and mail spool
id appuser                       # verify UID, GID, and groups
groups appuser                   # group membership only
getent passwd appuser            # entry from all identity sources
chage -l appuser                 # password ageing and expiry
su - appuser                     # switch user with a login shell
sudo -u appuser command          # run one command as another user
sudo -l                          # what the current user is allowed to run
visudo                           # edit sudoers with syntax validation
```

Always use `usermod -aG`. `usermod -G` replaces the entire secondary group list,
which is a routine way to remove someone's `sudo` or `docker` access by
accident. Verify with `id` afterwards. Before `userdel -r`, confirm the username,
home path, running processes, and data ownership with `getent passwd`, `pgrep
-u`, and `find <approved-path> -user <name> -print`; the command permanently
removes the home directory and mail spool.

The account fields these commands write are described in
[Configuration and virtual filesystems](#configuration-and-virtual-filesystems).

### Permission commands

Numeric and symbolic `chmod` forms, the special bits, and what each bit means on
a file versus a directory are in [Permissions](#permissions). The commands below
cover what that section does not.

```bash
chmod -R g+w shared/             # recursive; check the tree before running it
chown -R user:group dir/
chgrp devops file
getfacl file                     # per-user ACLs beyond the three classes
setfacl -m u:appuser:rw file     # grant one user access without changing the group
```

Recursive permission changes are easy to over-apply. Review the target with
`find <path> -type f -printf '%m %p\n' | sort -u` first, and never run a
recursive `chmod` from `/` or a home directory root.

### Networking commands

```bash
ip -brief addr                   # interface addresses
ip addr add 10.0.0.5/24 dev eth0
ip link set eth0 up
ip route                         # routing table
ip route get 10.0.5.20           # which route a destination would take
ip neigh                         # ARP table
ifconfig                         # deprecated; use ip on current systems

ss -ltnp                         # listening TCP sockets and owning processes
ss -tan state established        # established connections
ss -s                            # socket summary by state
netstat -tulpn                   # deprecated equivalent of ss -tulpn

ping -c 4 google.com             # reachability and round-trip time
ping -c 4 -M do -s 1472 host     # path MTU probe: 1472 + 28 headers = 1500
traceroute google.com            # hop-by-hop path
mtr google.com                   # continuous traceroute with per-hop loss
ipcalc 192.168.10.0/26           # network, broadcast, and host range

dig example.com                  # DNS query with full detail
dig +short example.com
dig @8.8.8.8 example.com MX      # query a specific resolver for a record type
dig -x 8.8.8.8                   # reverse lookup
nslookup example.com             # simpler, older DNS client
host example.com

curl -I https://example.com      # response headers only
curl -sv https://example.com     # verbose, including the TLS handshake
curl -w '%{time_total}\n' -o /dev/null -s https://example.com   # timing
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key   # fetch to stdout
wget -c https://example.com/big.iso    # resume an interrupted download

tcpdump -ni any port 443 -c 20    # capture 20 packets on a port
nc -zv host 5432                  # test whether a TCP port accepts connections
openssl s_client -connect example.com:443 -servername example.com   # inspect a certificate
ethtool eth0                      # link speed, duplex, and carrier

sudo nft list ruleset             # read-only view of the firewall ruleset
sudo nft -c -f rules.nft          # syntax-check a ruleset without applying it
```

`nc -zv host port` is the fastest way to separate a network problem from an
application problem: if the port accepts a connection, the path and firewall are
fine and the fault is above the transport layer.

Packet capture and firewall inspection are read-only, but changing rules is not.
Never flush or replace a remote host's ruleset over the connection you depend
on; see [nftables vs iptables](#nftables-vs-iptables) for the safe procedure.
How to read interface counters and traceroute output is in
[Network interfaces and diagnostics](#network-interfaces-and-diagnostics).

### Archives and transfers

```bash
tar czf backup.tar.gz /data       # create a gzip-compressed archive
tar xzf backup.tar.gz             # extract
tar xzf backup.tar.gz -C /restore # extract into a directory
tar tzf backup.tar.gz             # list contents without extracting
gzip file / gunzip file.gz
zip -r archive.zip dir/ / unzip archive.zip

scp file user@host:/path/         # copy over SSH
scp -r dir/ user@host:/path/
rsync -avz --progress src/ user@host:/dest/     # sync, transferring only differences
rsync -avzn --delete src/ dest/   # dry run of the destructive form, review first
rsync -avz --delete src/ dest/    # destructive: deletes anything not in the source
sftp user@host                    # interactive file transfer over SSH
```

`rsync` is preferable to `scp` for anything large or repeated: it resumes, it
transfers only changed blocks, and `--dry-run` shows what it would do. Note that
a trailing slash on the source means "the contents of this directory", and
omitting it means "this directory itself", so the wrong slash combined with
`--delete` can empty the destination. Key setup for these transfers is in
[SSH](#ssh).

### Shell productivity

```bash
command1 | command2          # pipe stdout into stdin
command > out.log            # redirect stdout, overwriting
command >> out.log           # redirect stdout, appending
command 2> err.log           # redirect stderr
command > all.log 2>&1       # both streams to one file
command < input.txt          # read stdin from a file
command1 && command2         # run command2 only if command1 succeeded
command1 || command2         # run command2 only if command1 failed
command &                    # run in the background
$(command)                   # command substitution

!!                           # repeat the previous command
sudo !!                      # repeat it with sudo
!$                           # last argument of the previous command
Ctrl+R                       # search command history
Ctrl+A / Ctrl+E              # jump to start or end of the line
Ctrl+W                       # delete the previous word
alias ll='ls -alh'           # define a shortcut; put it in ~/.bashrc to persist
watch -n2 'kubectl get pods' # rerun a command every 2 seconds
timeout 30 ./flaky-command   # give up after 30 seconds
seq 1 5 | xargs -I{} echo item{}
```

Check what `!!` and `!$` expand to before running them with `sudo`; history
expansion happens without confirmation. Prompt configuration is in
[Shell prompt customisation](#shell-prompt-customisation).

Reference: [Linux commands walkthrough](https://krishnaprasadkv.github.io/Linux-Commands/)
