# Docker

Interview notes on Docker concepts, images, networking, storage, and runtime
behaviour, followed by [troubleshooting scenarios](#troubleshooting-scenarios)
that apply those concepts to realistic failures.

## Contents

- [Concepts](#concepts)
- [Architecture and isolation](#architecture-and-isolation)
- [Images and layers](#images-and-layers)
- [Dockerfile](#dockerfile)
- [COPY vs ADD](#copy-vs-add)
- [CMD vs ENTRYPOINT](#cmd-vs-entrypoint)
- [Container lifecycle](#container-lifecycle)
- [attach vs exec](#attach-vs-exec)
- [Networking](#networking)
- [Storage](#storage)
- [Resource limits](#resource-limits)
- [Logging](#logging)
- [Registries and image transfer](#registries-and-image-transfer)
- [Docker Compose](#docker-compose)
- [Cleanup](#cleanup)
- [Security practices](#security-practices)
- [Docker in CI/CD](#docker-in-cicd)
- [Troubleshooting scenarios](#troubleshooting-scenarios)
  - [First-response triage](#first-response-triage)
  - [1. Container exits immediately with code 0](#1-container-exits-immediately-with-code-0)
  - [2. Container killed with exit code 137](#2-container-killed-with-exit-code-137)
  - [3. Container in a restart loop](#3-container-in-a-restart-loop)
  - [4. Port is already allocated](#4-port-is-already-allocated)
  - [5. Published port is open but connections are refused](#5-published-port-is-open-but-connections-are-refused)
  - [6. One container cannot resolve another by name](#6-one-container-cannot-resolve-another-by-name)
  - [7. Container has no internet or DNS access](#7-container-has-no-internet-or-dns-access)
  - [8. No space left on device on the host](#8-no-space-left-on-device-on-the-host)
  - [9. Every build rebuilds everything](#9-every-build-rebuilds-everything)
  - [10. Build succeeds but the file is missing at runtime](#10-build-succeeds-but-the-file-is-missing-at-runtime)
  - [11. Permission denied on a mounted volume](#11-permission-denied-on-a-mounted-volume)
  - [12. Data disappeared after redeploy](#12-data-disappeared-after-redeploy)
  - [13. `docker stop` always takes ten seconds](#13-docker-stop-always-takes-ten-seconds)
  - [14. Zombie processes accumulate inside a container](#14-zombie-processes-accumulate-inside-a-container)
  - [15. Application is slow inside the container but fast on the host](#15-application-is-slow-inside-the-container-but-fast-on-the-host)
  - [16. Works on my machine, fails on the server](#16-works-on-my-machine-fails-on-the-server)
  - [17. `docker logs` returns nothing](#17-docker-logs-returns-nothing)
  - [18. A secret was baked into an image](#18-a-secret-was-baked-into-an-image)
  - [19. Cannot debug a distroless or scratch container](#19-cannot-debug-a-distroless-or-scratch-container)
  - [20. Container clock or timezone is wrong](#20-container-clock-or-timezone-is-wrong)
  - [21. Cannot connect to the Docker daemon](#21-cannot-connect-to-the-docker-daemon)
- [Examples in this repository](#examples-in-this-repository)
- [Reference](#reference)

## Concepts

### What is Docker?

Docker is a container platform that packages an application together with its
dependencies into an image, and runs that image as an isolated process on a
shared host kernel.

What it actually gives you:

- **Identical runtime everywhere.** The image contains the libraries, binaries,
  and configuration, so the same artifact runs on a laptop, in CI, and in
  production.
- **Fast start and low overhead.** A container is a process with namespaces and
  cgroups applied, so it starts in milliseconds and does not carry a guest OS.
- **Immutable, versioned artifacts.** Images are content-addressed and tagged,
  so a deployment is reproducible and a rollback is a tag change.
- **Layer caching.** Unchanged layers are reused across builds and pulls, which
  cuts both build and deploy time.
- **Density.** Many containers fit on one host because they share the kernel,
  which is what makes per-service deployment economical.

### What is a container?

A container is a running process, plus the filesystem from an image, isolated
from other processes using Linux kernel features. It has its own view of the
process tree, network stack, mounts, and hostname, but it uses the host kernel
rather than its own.

### Containers vs virtual machines

| | Virtual machine | Container |
| :--- | :--- | :--- |
| Abstracts | The machine | The application process |
| Kernel | Its own guest kernel | Shares the host kernel |
| Size | Gigabytes | Megabytes |
| Start time | Tens of seconds to minutes | Milliseconds to seconds |
| Isolation | Strong, hardware-level via hypervisor | Process-level via namespaces and cgroups |
| Overhead | Full OS per instance | One process tree per instance |

A hypervisor divides physical hardware among guest machines. A **type 1**
(bare-metal) hypervisor runs directly on the hardware, for example ESXi or KVM.
A **type 2** (hosted) hypervisor runs as an application on an existing OS, for
example VirtualBox.

The two are complementary rather than competing: in the cloud, containers
almost always run inside VMs, so the VM supplies the hard tenancy boundary and
the container supplies the packaging and density.

### Where Docker falls short

- **No real orchestration.** A single daemon does not do scheduling, rolling
  updates, or self-healing across hosts. Swarm is minimal; Kubernetes is the
  practical answer.
- **Stateful workloads need help.** Local volumes are tied to one host, so
  multi-host state needs a network volume plugin, a CSI driver, or a managed
  database outside the cluster.
- **Shared kernel is the isolation limit.** A kernel exploit or a kernel version
  requirement is not solved by a container. Windows containers need a Windows
  host, and Linux containers need a Linux kernel.
- **Observability is external.** Logs, metrics, and traces need a collection
  stack; `docker logs` on one host is not monitoring.
- **Image sprawl.** Without lifecycle policies on the registry and disciplined
  base images, storage and vulnerability surface grow steadily.

Note that "Docker has no storage option" is a common but wrong statement:
volumes, bind mounts, and tmpfs mounts are built in. See
[Storage](#storage).

## Architecture and isolation

### Components

- **Docker client (`docker`)** sends commands to the daemon over the REST API,
  by default through the `/var/run/docker.sock` Unix socket.
- **Docker daemon (`dockerd`)** builds images, manages networks and volumes, and
  drives the container lifecycle.
- **containerd** is the runtime the daemon delegates to for image pull and
  container supervision; **runc** is what actually creates the container by
  applying namespaces and cgroups.
- **Registry** stores and serves images over HTTP. Public examples are Docker
  Hub and GitHub Container Registry; private examples are Amazon ECR, Harbor,
  and Artifactory.

Because the daemon socket is root-equivalent, anyone in the `docker` group can
gain root on the host. Treat that group membership as administrator access.

### Namespaces and cgroups

Namespaces give a container its own **view** of the system; cgroups **limit**
what it may consume. Both are Linux kernel features, not Docker features.

| Namespace | What it isolates |
| :--- | :--- |
| PID | Process IDs, so the container has its own PID 1 |
| Mount (mnt) | The filesystem tree |
| Network (net) | Interfaces, routing tables, iptables rules, ports |
| UTS | Hostname and domain name |
| IPC | Shared memory and semaphores |
| User | UID and GID mapping, used by user-namespace remapping |
| Cgroup | The container's view of its own cgroup hierarchy |

cgroups enforce CPU, memory, block I/O, and process-count limits. Namespaces
without cgroups means one container can starve the host; cgroups without
namespaces means no isolation.

## Images and layers

An **image** is a read-only, layered filesystem plus configuration metadata
(entrypoint, command, environment, exposed ports, user). A **layer** is the
filesystem diff produced by one build instruction. A **container** is an image
plus a thin writable layer on top.

- Only `RUN`, `COPY`, and `ADD` create filesystem layers. Instructions such as
  `ENV`, `WORKDIR`, `EXPOSE`, `LABEL`, and `CMD` only change metadata.
- Layers are shared: ten containers from one image consume one copy of the
  image layers plus ten small writable layers.
- A layer is additive. Deleting a file in a later layer hides it but does not
  shrink the image, so `RUN rm secret.key` after a `COPY secret.key` still ships
  the secret. Remove it in the same layer, or use a multi-stage build.

```bash
docker images                             # list images
docker images -a                          # include intermediate layers
docker images --no-trunc                  # full image IDs
docker images --filter=reference='alpine' # filter by name
docker history <image>                    # per-layer size and originating instruction
docker image inspect <image>              # full configuration
```

### Creating images without a Dockerfile

```bash
docker commit <container> my-image:my-tag   # snapshot a running container
docker import archive.tar my-image:my-tag   # import a root filesystem tarball
```

Both are debugging or migration tools, not a build process: the result is not
reproducible, `commit` output has no build context recorded, and `import` drops
image history and configuration such as `ENTRYPOINT`. Production images should
come from a Dockerfile in version control.

## Dockerfile

A `Dockerfile` is the build recipe for an image. The default filename is
`Dockerfile`; use `docker build -f <path>` for anything else.

| Instruction | Purpose |
| :--- | :--- |
| `FROM` | Base image for the following instructions; starts a build stage |
| `RUN` | Execute a command in a new layer |
| `COPY` | Copy files or directories from the build context |
| `ADD` | Like `COPY`, plus remote URLs and local archive extraction |
| `CMD` | Default command or default arguments, overridable at run time |
| `ENTRYPOINT` | The executable the container always runs |
| `ENV` | Environment variable, persisted in the image and at run time |
| `ARG` | Build-time variable; not runtime configuration unless copied into `ENV`, `LABEL`, or generated files |
| `WORKDIR` | Working directory for later instructions and at run time |
| `USER` | UID/GID for later `RUN`, `CMD`, and `ENTRYPOINT` |
| `EXPOSE` | Documents the listening port; does not publish it |
| `VOLUME` | Declares a mount point that gets an anonymous volume if unmounted |
| `LABEL` | Key/value metadata such as source commit and maintainer |
| `HEALTHCHECK` | Command that reports container health |
| `STOPSIGNAL` | Signal used to stop the container, default `SIGTERM` |
| `SHELL` | Shell used for shell-form `RUN`, `CMD`, `ENTRYPOINT` |
| `ONBUILD` | Deferred instruction that runs when this image is used as a base |
| `.dockerignore` | Not an instruction: excludes paths from the build context |

`MAINTAINER` is deprecated; use `LABEL maintainer="..."` instead.

### Build practices that matter

- **Order by change frequency.** Copy dependency manifests and install
  dependencies before copying application source, so a code change does not
  invalidate the dependency layer.
- **One logical step per `RUN`.** Chain package install and cleanup in a single
  `RUN` so the cleanup actually reduces image size.
- **Always write a `.dockerignore`.** Excluding `.git`, `node_modules`, and
  build output shrinks the context sent to the daemon and prevents accidental
  inclusion of local secrets.
- **Pin base images** to a specific tag or digest. `FROM ubuntu:latest` makes
  builds non-reproducible.
- **Use multi-stage builds** so compilers and build tools stay out of the
  runtime image.
- **Run as a non-root user** with `USER`.
- **Never pass secrets through `ARG` or `ENV`.** `ENV` and `LABEL` are stored in
  the final image configuration. An `ARG` is not automatically present at run
  time or in `docker image inspect`, but it can leak through provenance,
  command history, build logs, cache metadata, or files created by a `RUN`.
  Copying it into `ENV` or `LABEL` makes it persist explicitly. Use BuildKit
  secret mounts (`RUN --mount=type=secret,...`) or inject secrets at run time.

Multi-stage example:

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/app

FROM gcr.io/distroless/static:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

### Minimal image with one package installed

Ubuntu base with only `sqlite3` installed. Note that a Dockerfile has no
end-of-line comments: `#` is only a comment when it is the first non-whitespace
character on the line, so comments must sit on their own line.

```dockerfile
FROM ubuntu:22.04

# Keep apt from prompting during the build
ENV DEBIAN_FRONTEND=noninteractive

# Install sqlite3 only, then drop the package lists in the same layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/bin/sqlite3"]
CMD ["--help"]
```

`docker run <image>` opens the sqlite3 help; `docker run <image> /data/app.db`
opens that database, because the run argument replaces `CMD` and is appended to
`ENTRYPOINT`.

## COPY vs ADD

Use `COPY` unless you specifically need one of `ADD`'s two extra behaviours.
`COPY` copies files and directories from the build context; `ADD` does that and
also fetches remote URLs and auto-extracts local archives.

| | `COPY` | `ADD` |
| :--- | :--- | :--- |
| Local files and directories | Yes | Yes |
| Remote URL as source | No | Yes |
| Auto-extract local tar archive | No | Yes, for recognised compression |
| Git repository as source | No | Yes, only with the BuildKit Dockerfile frontend |
| Behaviour predictable from the line alone | Yes | No |

Why `COPY` is the default choice:

- `ADD some.tar.gz /opt/` silently extracts, while `ADD app.jar /opt/` silently
  copies. A reviewer cannot tell which happens without knowing the file type.
- `ADD https://...` gives no checksum verification, no retry control, and leaves
  the downloaded file in a layer even after later deletion. Prefer
  `RUN curl -fsSL <url> -o file && echo "<sha> file" | sha256sum -c`, which is
  explicit and verifiable.
- Both support `--chown=user:group` and `--chmod`. Without `--chown`, files are
  owned by root regardless of the current `USER`.

Legitimate `ADD` use: unpacking a base root filesystem tarball, as official
distro images do. Git URL sources such as `ADD https://github.com/org/repo.git
/src` require BuildKit and a current Dockerfile syntax/frontend; the classic
builder does not support them. Pin a commit or tag and use `--keep-git-dir` only
when the build truly needs `.git`, otherwise the result can change between
builds.

## CMD vs ENTRYPOINT

`ENTRYPOINT` is the executable that always runs. `CMD` supplies the default
arguments, and anything you pass to `docker run` replaces `CMD`. To replace the
`ENTRYPOINT` you need `docker run --entrypoint`.

| | `ENTRYPOINT` | `CMD` |
| :--- | :--- | :--- |
| Role | Fixed executable | Default arguments or default command |
| Overridden by run arguments | No | Yes |
| Overridden by | `--entrypoint` | Trailing arguments of `docker run` |
| Inherited from base image | Yes | Yes, and reset to empty when `ENTRYPOINT` is set in a later stage |

Exec form versus shell form matters more than the choice between the two
instructions:

```dockerfile
ENTRYPOINT ["nginx", "-g", "daemon off;"]   # exec form: nginx is PID 1
ENTRYPOINT nginx -g 'daemon off;'           # shell form: /bin/sh -c is PID 1
```

With shell form the shell becomes PID 1, so `SIGTERM` from `docker stop` goes to
the shell and often is not forwarded. The container then ignores the graceful
stop and is killed by `SIGKILL` after the timeout. Always use exec form for the
process you want to receive signals.

Common combinations:

| Pattern | Result |
| :--- | :--- |
| `ENTRYPOINT ["app"]` + `CMD ["--help"]` | `docker run img` runs `app --help`; `docker run img --port 80` runs `app --port 80` |
| `CMD ["app", "--help"]` only | `docker run img` runs `app --help`; `docker run img bash` runs `bash` |
| `ENTRYPOINT ["app"]` only | Arguments always append; the image cannot easily run a shell |

Practical guidance:

- For a single-purpose image, set `ENTRYPOINT` to the binary and `CMD` to the
  default flags. This makes the image behave like the command it wraps.
- For an image people need to poke at, use `CMD` alone so `docker run img bash`
  works.
- An `ENTRYPOINT` script that ends in `exec "$@"` is the standard way to do
  setup work and still hand PID 1 to the real process.
- "ENTRYPOINT should be `/bin/sh`" is wrong: that turns every argument into a
  shell string and breaks signal handling.

## Container lifecycle

States: created, running, paused, restarting, exited, dead. `docker run` is
`docker create` plus `docker start`.

```bash
docker create --name web nginx      # create without starting
docker start web                    # start an existing container
docker run -d --name web nginx      # create and start in one step
docker run --rm -it alpine sh       # remove automatically on exit
docker stop web                     # SIGTERM, then SIGKILL after the grace period
docker stop -t 30 web               # extend the grace period to 30 seconds
docker kill web                     # SIGKILL immediately
docker kill -s HUP web              # send a specific signal
docker restart web
docker pause web / docker unpause web   # freeze and resume with the cgroup freezer
docker rename web web-old
docker update --memory 512m web     # change resource limits in place
docker rm web                       # delete a stopped container
docker rm -f web                    # delete a running or paused container
docker rm -v web                    # also delete its anonymous volumes
docker wait web                     # block until it exits, print the exit code
```

### Can a paused container be removed?

Not with a plain `docker rm`: it refuses and tells you to unpause first. Either
unpause and stop it, or use `docker rm -f`, which kills the container and then
removes it. The same applies to a running container.

### Inspecting containers

```bash
docker ps                           # running containers
docker ps -a                        # all containers, including exited
docker logs -f --tail 100 web       # container stdout/stderr
docker inspect web                  # full JSON: mounts, networks, IP, exit code
docker top web                      # processes inside the container
docker stats                        # live CPU, memory, network, block I/O
docker stats --all                  # include non-running containers
docker diff web                     # files changed in the writable layer
docker port web                     # published port mappings
docker events                       # daemon event stream
docker cp myfile.txt web:/usr/share # host to container
docker cp web:/var/log/app.log ./   # container to host
```

`docker inspect -f '{{.State.ExitCode}}' web` and
`docker inspect -f '{{.State.OOMKilled}}' web` are the two fastest checks after
an unexpected exit.

## attach vs exec

`docker attach` connects your terminal to the container's existing PID 1 streams.
`docker exec` starts a new process inside the running container.

| | `docker attach` | `docker exec` |
| :--- | :--- | :--- |
| Target | The existing main process | A new process |
| Multiple sessions | Yes, all see the same stream | Yes, independent |
| Requires the container to be running | Yes | Yes |
| Survives container restart | No | No, the exec process is not restarted |

- `docker exec -it web sh` is what you want almost always. `attach` is only for
  watching or driving the main process, for example an interactive shell that
  is itself PID 1.
- On an attached session, `Ctrl-C` sends `SIGINT` to the main process, which
  usually stops the container. Detach without stopping it using
  `Ctrl-P` then `Ctrl-Q`, or attach with `--sig-proxy=false`.
- `docker exec` cannot be used on a stopped container. To inspect one, either
  `docker cp` the files out, or `docker commit` it to an image and run a shell
  on that image.

## Networking

### Drivers

| Driver | Use it when |
| :--- | :--- |
| `bridge` | Default. Containers on one host that need to talk to each other and to be reachable through published ports. |
| `host` | The container should use the host network stack directly, for example for high packet rates or when it must bind the host's own ports. No network isolation, no port publishing. |
| `overlay` | Containers on different hosts must communicate, for example Swarm services. Traffic is encapsulated between daemons, so no manual routing is needed. |
| `macvlan` | The container needs its own MAC and IP on the physical LAN, so it appears as a separate host. Typical for legacy apps and for migrating from VMs. |
| `ipvlan` | Like `macvlan` but shares the host MAC, which suits switches that limit MACs per port. |
| `none` | No network at all beyond loopback. Used for batch jobs that must not reach the network. |

`docker run --network=none nginx` gives the container only its loopback
interface, so no inbound or outbound traffic is possible. The process still
starts; it just cannot be reached and cannot reach anything.

### Default bridge vs user-defined bridge

Always create a user-defined bridge for multi-container applications.

| | Default `bridge` | User-defined bridge |
| :--- | :--- | :--- |
| Service discovery by name | No | Yes, via the embedded DNS resolver at 127.0.0.11 |
| Container isolation | All containers share one network | Only attached containers can reach each other |
| Attach/detach while running | No | Yes |
| Configurable subnet and gateway | Limited | Yes |

The default bridge is `docker0`. Its default subnet is `172.17.0.0/16` and the
gateway address, which is the host as seen from containers, is `172.17.0.1`.
That subnet is the bridge network, not "the IP address of the Docker host"; the
host's own address on your LAN is unrelated and configurable via the daemon's
`default-address-pools`.

```bash
docker network ls
docker network create --driver bridge app-net
docker network create --subnet 203.0.113.0/24 --gateway 203.0.113.254 iptastic
docker network inspect app-net             # subnet, gateway, attached containers
docker network connect app-net web         # attach a running container
docker network disconnect app-net web
docker run -d --name db --network app-net postgres:16
docker run -it --network app-net alpine ping db   # resolves by container name
docker run --rm -it --network iptastic --ip 203.0.113.2 nginx
```

### Publishing ports

`EXPOSE` in a Dockerfile is documentation only. Traffic reaches a container
because you published a port at run time.

```bash
docker run -p 8080:80 nginx          # host 8080 to container 80, all host interfaces
docker run -p 127.0.0.1:8080:80 nginx # bind only to loopback on the host
docker run -P nginx                   # publish every EXPOSEd port to a random host port
```

In Compose, `expose` only records the port for other containers on the same
network, while `ports` actually maps it onto the host. The repository file
`docker-compose-diff-expose_&_ports.yaml` in the parent directory demonstrates
the difference.

Containers on the same user-defined network reach each other on the container
port directly by name, so `ports` is only needed for traffic entering from
outside Docker.

## Storage

A container's writable layer is copy-on-write and disappears with the
container. Anything that must survive has to be on a mount.

| Type | Managed by | Lives at | Use for |
| :--- | :--- | :--- | :--- |
| Volume | Docker | `/var/lib/docker/volumes/<name>/_data` on Linux | Database files and any container-produced state |
| Bind mount | You | Any host path you choose | Source code in development, host config and logs |
| tmpfs mount | Docker | Host memory only | Secrets and scratch data that must never hit disk |

### Volumes

```bash
docker volume create pgdata
docker volume ls
docker volume inspect pgdata
docker volume rm pgdata
docker volume prune                  # remove unused volumes

docker run -d --name db -v pgdata:/var/lib/postgresql/data postgres:16
docker run -d --name db --mount source=pgdata,target=/var/lib/postgresql/data postgres:16
docker run --rm --volumes-from db alpine tar cf - /var/lib/postgresql/data > backup.tar
```

Practical detail:

- Named volumes are created on first use and are **not** deleted with the
  container. `docker rm -v` removes anonymous volumes only, which is how
  orphaned volumes accumulate; check with `docker volume ls -f dangling=true`.
- The host path above is owned by root and is Docker's internal layout. It is
  readable on a Linux host, but you should treat it as private and go through
  `docker run`, `docker cp`, or a helper container instead of editing it. On
  Docker Desktop the path is inside the Linux VM, not on macOS or Windows.
- Volumes work across containers: `--volumes-from` and mounting the same named
  volume in several containers are the standard backup and sidecar patterns.
- Network volume drivers (NFS, EBS, Portworx) let a volume follow a container to
  another host, which is what local volumes cannot do.

### Bind mounts

`-v /host/path:/container/path` maps a host directory into the container. The
long form is clearer and fails loudly on a typo:
`--mount type=bind,source=/host/path,target=/container/path,readonly`.

The short `-v` form creates a missing host directory silently, while
`--mount type=bind` errors out. Bind mounts also expose the host filesystem and
carry host UID/GID semantics, so mounting `/var/run/docker.sock` or a host
config directory read-write is a privilege escalation risk.

### Storage driver and the writable layer

`overlay2` is the default storage driver on modern Linux. Reads come from the
image layers; the first write to a file copies it up into the container's
writable layer, so write-heavy workloads on the writable layer are slower and
grow disk usage per container. That is the technical reason databases belong on
volumes, which bypass the union filesystem.

```bash
docker info | grep -i 'storage driver'
docker system df                     # space used by images, containers, volumes, cache
docker system df -v                  # per-object breakdown
```

## Resource limits

By default a container can use all host CPU and memory. Set limits explicitly.

```bash
docker run -it --cpus=1.5 --memory=512m --memory-swap=512m myapp
docker run -it --cpuset-cpus=0,4,6 myapp     # pin to specific cores
docker run -it --cpu-shares=512 myapp        # relative weight under contention
docker run -it --pids-limit=200 myapp        # cap process count
docker update --cpus=2 --memory=1g myapp     # adjust a running container
```

Practical detail:

- `--cpus` is the option to use. `--cpus=1.5` means one and a half cores worth
  of CPU time per period, enforced as a hard cap.
- `--cpu-shares` is only a **relative weight** among competing containers, with
  1024 as the default. It does nothing when the host is idle, so `--cpu-shares=512`
  does not mean "50% of the CPU". Treat it as a priority, not a limit.
- `--memory` is a hard limit. Exceeding it means the kernel OOM-kills the
  process, the container exits with code 137, and
  `docker inspect -f '{{.State.OOMKilled}}'` reports `true`. Set
  `--memory-swap` equal to `--memory` to forbid swap use.
- Inside the container, tools such as `free`, `nproc`, and `/proc/cpuinfo` still
  report host-wide values unless the runtime virtualises them. Runtimes that
  size thread pools from `nproc` will over-allocate; pass the limit explicitly
  through configuration.

## Logging

Docker logging happens at two levels: the daemon and the container.

**Daemon logs** record the engine's own behaviour and are the place to look for
pull failures, storage driver errors, and networking problems. Verbosity is set
with `--log-level` or `"log-level"` in `/etc/docker/daemon.json`, with the
levels `debug`, `info` (default), `warn`, `error`, and `fatal`. Read them with
`journalctl -u docker.service` on systemd hosts.

**Container logs** are whatever the main process writes to stdout and stderr,
captured by the container's log driver.

```bash
docker logs web
docker logs -f --since 10m --timestamps web
docker logs --tail 100 web
```

Practical detail:

- Applications in containers should log to stdout/stderr, not to files inside
  the container. A file in the writable layer is invisible to `docker logs` and
  is lost with the container.
- The default driver is `json-file`, which writes to
  `/var/lib/docker/containers/<id>/<id>-json.log` and **does not rotate** unless
  configured. Unbounded container logs filling the disk is a routine incident;
  set `max-size` and `max-file` in `daemon.json`.
- `docker logs` works with `json-file`, `local`, and `journald`. With a shipping
  driver such as `awslogs`, `fluentd`, `gelf`, or `splunk`, `docker logs`
  returns nothing and you read logs in the destination system.

## Registries and image transfer

A **repository** is a named collection of tagged images, for example
`library/nginx`. A **registry** is the server hosting repositories and serving
the HTTP API, for example Docker Hub, Amazon ECR, or a self-hosted Harbor.

```bash
docker login registry.example.com
docker logout registry.example.com
docker pull nginx:1.27-alpine
docker tag myapp:1.4.0 registry.example.com/team/myapp:1.4.0
docker push registry.example.com/team/myapp:1.4.0
docker rmi myapp:1.4.0
```

Reference images from a public registry by digest (`nginx@sha256:...`) or at
least by an immutable tag when supply-chain integrity matters; a mutable tag can
be repointed at different content. Scan images before promotion and mirror
critical bases into your own registry.

### save/load vs export/import

`save` and `load` work on **images** and keep layers, tags, and history.
`export` and `import` work on a **container's filesystem** and keep neither
history nor configuration.

```bash
docker save my_image:my_tag | gzip > my_image.tar.gz   # image, with all layers
docker load < my_image.tar.gz                          # restore that image

docker export my_container | gzip > my_container.tar.gz  # flat filesystem snapshot
cat my_container.tar.gz | docker import - my_image:my_tag
```

Use `save`/`load` to move a real image between hosts without a registry, for
example into an air-gapped environment. `export`/`import` produces a single
flattened layer with no `ENTRYPOINT`, `CMD`, or `ENV`, so the resulting image
usually needs those supplied again. It is useful for inspecting a filesystem or
squashing a base layer, not for shipping applications.

## Docker Compose

Compose describes a multi-container application declaratively in a YAML file:
services, images or build contexts, environment, networks, volumes, and
dependencies. One command brings the whole set up with a shared default
network.

```bash
docker compose up -d
docker compose ps
docker compose logs -f api
docker compose exec api sh
docker compose config          # render and validate the merged configuration
docker compose down            # stop and remove containers and networks
docker compose down -v         # also remove named volumes, destroys data
```

Practical detail:

- Compose creates a default network for the project, so services reach each
  other by service name. Explicit `links` are obsolete.
- `depends_on` waits for the container to start, not for the application to be
  ready. Pair it with `condition: service_healthy` and a `HEALTHCHECK`.
- Compose is for local development and single-host deployments. Multi-host
  production belongs on an orchestrator.

## Cleanup

Inspect the candidates and reclaimable space before deleting anything:

```bash
docker system df -v
docker ps -a --filter status=exited
docker image ls --filter dangling=true
docker volume ls --filter dangling=true
docker network ls --filter type=custom
docker builder du
```

Then apply the narrowest cleanup that removes only reviewed objects:

```bash
docker system prune              # stopped containers, unused networks, dangling images, build cache
docker system prune -a --volumes # also unused images and volumes, destructive
docker container prune
docker image prune -a
docker network prune
docker volume prune
docker builder prune             # build cache only
```

Blunt reset of a disposable development host, only after reviewing the lists
above:

```bash
docker ps -aq                            # inspect every affected container ID
docker volume ls -q                      # inspect every affected volume name
docker stop $(docker ps -aq)
docker rm -f $(docker ps -aq)
docker volume rm $(docker volume ls -q)
```

Never run these on a shared or production host: they delete data volumes and
every container without confirmation. In production, prune specific object types
on a schedule with filters such as `--filter "until=168h"`.

## Security practices

- Run as a non-root user. Add a `USER` instruction, and enforce it at run time
  with `--user 1000:1000` where the image cannot be changed.
- Drop capabilities and privileges: `--cap-drop=ALL` then add back only what is
  needed, `--security-opt=no-new-privileges`, and a read-only root filesystem
  (`--read-only`) with a tmpfs for scratch space.
- Never use `--privileged` or mount `/var/run/docker.sock` into a container
  unless you accept that the container is equivalent to host root.
- Keep secrets out of images. Environment variables and labels persist in image
  configuration and appear in `docker inspect`; build arguments can leak
  through provenance, commands, logs, cache, or generated files even though an
  unused `ARG` is not a runtime environment variable. Use a secrets manager, a
  mounted file, or BuildKit secret mounts.
- Use minimal bases such as `alpine` or distroless to cut the vulnerability
  surface, pin versions, and rebuild regularly to pick up base image patches.
- Scan images in the pipeline and fail the build on fixable high-severity
  findings.

## Docker in CI/CD

**Continuous integration** means every change is merged into the mainline
frequently and validated automatically by a build and test run, so integration
problems surface in minutes rather than at release time.

**Continuous delivery** means every change that passes the pipeline is
automatically packaged and kept releasable, with the actual push to production
being a deliberate decision.

**Continuous deployment** goes one step further: any change that passes every
stage is released to production automatically, with no manual approval.

Docker's role is to make the build output an immutable artifact that every
stage shares.

Typical pipeline:

1. **Build** the image once, tagged with the commit SHA. Never rebuild per
   environment; a rebuild is a different artifact.
2. **Unit tests** run against the code or inside the built image.
3. **Image scan** and policy checks (no root user, no critical CVEs, size
   budget).
4. **Push** to the registry.
5. **Deploy to staging** using that exact image digest.
6. **Smoke test** as the gate: a small, fast, always-automated set of checks
   that the deployment is fundamentally alive, for example the process is
   serving, health endpoint returns 200, login works, a core page renders. It
   runs in minutes and its only job is a go/no-go decision. If it fails, stop
   the pipeline immediately instead of spending an hour on deeper suites.
7. **Regression suite** after the smoke gate passes: the broad set that
   verifies existing behaviour still works after the change, covering edge
   cases and previously fixed bugs. It is slower and is what gives you the
   confidence to refactor or bump base images.
8. **Promote** the same image to production, then verify with the same health
   checks and keep the previous tag available for rollback.

Pipeline practices:

- Cache layers between runs (registry cache or BuildKit cache mounts) and keep
  the dependency layer stable to keep builds fast.
- Build with BuildKit for parallel stages, secret mounts, and cache mounts.
- Tag with the SHA and add human-friendly tags as aliases; never deploy
  `latest`, since it makes the running version unknowable.
- Prefer rootless builders or BuildKit over mounting the Docker socket into
  build jobs.

## Troubleshooting scenarios

Realistic failures, how to diagnose them, and what stops them recurring. Each
scenario follows the pattern **symptom -> evidence -> cause -> fix ->
prevention** and links back to the concept section it depends on.

Collect evidence before restarting anything. A `docker restart` destroys the
writable layer state and the process list you needed, and often makes the
failure unreproducible.

### First-response triage

```bash
docker ps -a                                   # is it running, exited, or restarting?
docker inspect -f '{{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}} restarts={{.RestartCount}}' <c>
docker logs --tail 200 --timestamps <c>        # what the process said before it stopped
docker inspect -f '{{json .Config.Entrypoint}} {{json .Config.Cmd}}' <c>
docker stats --no-stream                       # CPU, memory against limits
docker system df                               # host disk pressure
docker events --since 30m                      # daemon view: kills, OOM, health status
journalctl -u docker.service --since '30 min ago'   # daemon-side errors
```

Exit codes worth memorising:

| Exit code | Meaning |
| :--- | :--- |
| 0 | The main process finished normally, so the container has nothing left to run |
| 1 / 2 | Application error or shell usage error; read the logs |
| 125 | The Docker daemon itself rejected the run command |
| 126 | The command was found but is not executable |
| 127 | The command was not found in the image |
| 137 | `SIGKILL`: OOM-killed by the kernel, or `docker kill`, or a stop that timed out |
| 139 | `SIGSEGV`: segmentation fault inside the container |
| 143 | `SIGTERM`: graceful stop, and the process honoured it |

### 1. Container exits immediately with code 0

**Symptom:** `docker run -d` returns an ID, but `docker ps` is empty and
`docker ps -a` shows `Exited (0)` a second later.

**Cause:** the container's main process finished, and a container lives exactly
as long as PID 1. Common variants: the image's `CMD` is a one-shot command, the
entrypoint script ends instead of `exec`ing the server, the service was started
with a flag that daemonises it into the background, or an interactive shell was
started without `-it` so it read EOF on stdin and exited.

**Diagnose:**

```bash
docker logs <c>
docker inspect -f '{{json .Config.Entrypoint}} {{json .Config.Cmd}}' <c>
docker run --rm -it <image> sh    # start a shell and run the command by hand
```

**Fix:** run the process in the foreground. For Nginx that is
`nginx -g 'daemon off;'`, for Apache `httpd-foreground`. In an entrypoint
script, finish with `exec "$@"` or `exec /usr/bin/myapp` so the real process
becomes PID 1 rather than a child of a script that then exits. The forms are
compared in [CMD vs ENTRYPOINT](#cmd-vs-entrypoint).

**Prevent:** treat exit 0 as a design signal, not a bug: if the workload really
is one-shot, run it as a job (`docker run --rm`) instead of `-d`, and do not
attach a restart policy to it.

### 2. Container killed with exit code 137

**Symptom:** the container disappears under load. `docker inspect` shows
`ExitCode: 137`. The application log ends mid-request with no error.

**Cause:** almost always the kernel OOM killer enforcing `--memory`, described
in [Resource limits](#resource-limits). The two other sources of 137 are an
explicit `docker kill` and a `docker stop` where the process ignored `SIGTERM`
and was killed after the grace period.

**Diagnose:**

```bash
docker inspect -f '{{.State.OOMKilled}}' <c>      # true means memory limit
docker inspect -f '{{.HostConfig.Memory}}' <c>    # the limit in bytes, 0 means unlimited
docker stats --no-stream <c>                      # usage against limit
dmesg -T | grep -i -E 'killed process|oom'        # host kernel confirmation
```

**Fix:** raise `--memory` if the limit is simply too low, or fix the memory
consumption. For JVM and Node workloads, also set the runtime's own heap limit:
a JVM without `-XX:MaxRAMPercentage` or `-Xmx` may size its heap from host
memory and get killed long before it thinks it is full.

**Prevent:** set both a container limit and a matching in-process limit, alert
on `container_memory_working_set_bytes` approaching the limit rather than on
restarts, and load-test at the configured limit instead of unlimited.

### 3. Container in a restart loop

**Symptom:** `docker ps` shows the status flipping between `Up 2 seconds` and
`Restarting (1)`, and `RestartCount` climbs.

**Cause:** the process crashes at startup and `--restart=always` keeps
relaunching it. Typical roots are a missing environment variable, an
unreachable dependency (database not up yet), a bad config file mount, or a port
conflict inside the container.

**Diagnose:**

```bash
docker inspect -f '{{.RestartCount}} {{.State.Error}}' <c>
docker logs <c> 2>&1 | head -50           # the first failure is the informative one
docker run --rm -it --entrypoint sh <image>   # inspect the image without the app
```

**Fix:** correct the configuration. To debug interactively, stop the restart
loop by starting the container with `--restart=no --entrypoint sh -it`, then run
the real command by hand and read the error.

**Prevent:** use `--restart=on-failure:5` rather than `always` so a permanently
broken container stops instead of hiding the failure, add a `HEALTHCHECK`, and
make the application retry dependencies with backoff instead of exiting on the
first connection refusal.

### 4. Port is already allocated

**Symptom:** `docker run -p 8080:80` fails with
`Bind for 0.0.0.0:8080 failed: port is already allocated` and exit code 125.

**Cause:** another container already publishes that host port, or a host process
outside Docker is listening on it. A stopped-but-not-removed container can also
hold the mapping if it is restarting.

**Diagnose:**

```bash
docker ps -a --format '{{.Names}}\t{{.Status}}\t{{.Ports}}' | grep 8080
sudo ss -ltnp | grep :8080         # host process holding the port
```

**Fix:** remove or re-map the conflicting container, or choose another host
port. Publishing to a specific interface (`-p 127.0.0.1:8080:80`) also avoids
clashing with a service bound to a different address.

**Prevent:** in Compose, avoid fixed host ports for services that do not need
host access; rely on the project network and the container port instead, as
described in [Publishing ports](#publishing-ports).

### 5. Published port is open but connections are refused

**Symptom:** `docker ps` shows `0.0.0.0:8080->80/tcp`, but `curl localhost:8080`
returns "connection reset" or "empty reply".

**Cause:** the application inside the container listens on `127.0.0.1` instead
of `0.0.0.0`. Traffic arrives in the container's network namespace, but nothing
is listening on the container's external interface. The other common cause is a
mapping to the wrong container port.

**Diagnose:**

```bash
docker exec <c> ss -ltn                     # what address is it bound to?
docker exec <c> curl -sv localhost:80       # does it answer from inside?
docker port <c>                             # what did Docker actually map?
```

**Fix:** configure the application to bind `0.0.0.0` (or `::`) inside the
container. Binding to loopback is correct on a VM and wrong in a container.

**Prevent:** make the bind address a configuration value with `0.0.0.0` as the
container default, and add a smoke test in the pipeline that curls the published
port after start.

### 6. One container cannot resolve another by name

**Symptom:** the API container fails with "could not resolve host: db", while
both containers are running on the same host.

**Cause:** they are on the **default** `bridge` network, which has no embedded
DNS for container names; see
[Default bridge vs user-defined bridge](#default-bridge-vs-user-defined-bridge).
Other variants: the containers are on two different user-defined networks, or
the code uses the Compose service name while the container was started with
`docker run` outside the project network.

**Diagnose:**

```bash
docker inspect -f '{{json .NetworkSettings.Networks}}' api
docker inspect -f '{{json .NetworkSettings.Networks}}' db     # same network?
docker exec api getent hosts db
docker exec api cat /etc/resolv.conf                          # expect nameserver 127.0.0.11
docker network inspect app-net
```

**Fix:**

```bash
docker network create app-net
docker network connect app-net db
docker network connect app-net api
docker exec api ping -c1 db
```

**Prevent:** never rely on the default bridge for multi-container work. Define
an explicit network in Compose, and address services by service name rather
than by IP, since container IPs change on every recreate.

### 7. Container has no internet or DNS access

**Symptom:** `docker exec <c> ping 8.8.8.8` works but
`docker exec <c> ping example.com` fails, or neither works.

**Cause:** if IP works and names do not, it is DNS: the container inherited a
host resolver it cannot reach, or the daemon has no usable upstream DNS. If
neither works, it is routing or NAT: IP forwarding disabled on the host,
missing masquerade rules after an iptables or firewalld reload, or the
container is on a `none` network.

**Diagnose:**

```bash
docker exec <c> cat /etc/resolv.conf
docker exec <c> nslookup example.com 8.8.8.8
sysctl net.ipv4.ip_forward                       # must be 1
sudo iptables -t nat -L DOCKER -n                # masquerade rules present?
docker inspect -f '{{json .NetworkSettings.Networks}}' <c>
```

**Fix:** set working resolvers for the daemon in `/etc/docker/daemon.json`
(`{"dns": ["10.0.0.2", "1.1.1.1"]}`) and restart the daemon; or enable
forwarding with `sysctl -w net.ipv4.ip_forward=1`. Restarting the Docker daemon
recreates its iptables chains after a firewall reload wiped them, but it also
restarts every container without a restart policy, so treat it as a change with
downtime rather than a quick retry.

**Prevent:** persist the sysctl setting, and restart Docker as part of any
firewall management change. On corporate networks, pin the daemon DNS instead of
inheriting a VPN-specific resolver that disappears.

### 8. No space left on device on the host

**Symptom:** builds fail, containers cannot start, and the application logs I/O
errors, while the application data itself is small.

**Cause:** `/var/lib/docker` filled up. In order of likelihood: unrotated
`json-file` container logs, accumulated build cache, dangling images from
repeated CI builds, and orphaned volumes.

**Diagnose:**

```bash
docker system df -v                        # reclaimable space per category
du -sh /var/lib/docker/*
du -sh /var/lib/docker/containers/*/*-json.log | sort -h | tail
docker volume ls -f dangling=true
df -h /var/lib/docker && df -i /var/lib/docker    # also check inodes
```

**Fix:** reclaim in the order of least risk, reviewing each list before pruning.
Filtered prunes are safer than a blanket `docker system prune -a --volumes`,
which also removes images and data volumes still in use elsewhere:

```bash
docker builder prune --filter 'until=168h'
docker image prune -a --filter 'until=168h'
docker container prune --filter 'until=24h'
docker volume ls -f dangling=true          # review, then remove named volumes individually
```

Truncate a runaway log with `truncate -s 0 <logfile>` rather than deleting it,
because deleting the open file frees nothing until the container restarts.

**Prevent:** configure log rotation once, globally, in
`/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" }
}
```

Then put `/var/lib/docker` on its own volume, run a scheduled filtered prune as
described in [Cleanup](#cleanup), and alert on disk usage rather than reacting
to a full disk.

### 9. Every build rebuilds everything

**Symptom:** a one-line source change triggers a full dependency install, and
builds take minutes in CI that took seconds locally.

**Cause:** the layer that installs dependencies sits after the `COPY` of the
whole source tree, so any source change invalidates it and every layer below.
In CI there is an additional cause: a fresh runner has no local layer cache at
all.

**Diagnose:**

```bash
docker history <image>                     # size and instruction per layer
DOCKER_BUILDKIT=1 docker build --progress=plain .   # shows CACHED lines
```

**Fix:** copy manifests first, install, then copy the source, following
[Build practices that matter](#build-practices-that-matter):

```dockerfile
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

In CI, import and export cache explicitly:

```bash
docker buildx build \
  --cache-from type=registry,ref=registry.example.com/app:buildcache \
  --cache-to   type=registry,ref=registry.example.com/app:buildcache,mode=max \
  -t registry.example.com/app:$GIT_SHA --push .
```

**Prevent:** add a `.dockerignore` so `.git`, `node_modules`, and test output
never enter the context and never invalidate a layer, and keep the base image
tag pinned so an upstream push does not invalidate the whole chain.

### 10. Build succeeds but the file is missing at runtime

**Symptom:** `COPY config/ /app/config/` builds fine, but the application
reports the config file is not found; or the build fails with
"COPY failed: file not found in build context".

**Cause:** the path is relative to the **build context**, not to the Dockerfile,
so `docker build -f docker/Dockerfile .` and `cd docker && docker build .` see
different trees. Or `.dockerignore` excludes the path. Or a later `COPY` into
the same directory, a `VOLUME` declaration, or a run-time mount shadows it.

**Diagnose:**

```bash
docker build --progress=plain .            # confirm which files were transferred
cat .dockerignore
docker run --rm <image> ls -la /app/config
docker inspect -f '{{json .Mounts}}' <c>   # is a mount hiding the image content?
```

**Fix:** make the context explicit and consistent
(`docker build -f docker/Dockerfile .` from the repository root), correct the
ignore rules, and remove the mount that shadows the baked-in path.

**Prevent:** verify contents in the build itself with a `RUN ls -la` during
development, and remember that a volume mounted over a directory hides
everything the image put there.

### 11. Permission denied on a mounted volume

**Symptom:** the container cannot write to a bind-mounted host directory, or a
database container fails at initialisation with a permissions error on its data
directory.

**Cause:** UID and GID are numeric and are not translated across the boundary.
The container process runs as, say, UID 1000 or the `postgres` user, while the
host directory is owned by a different UID. On SELinux hosts (RHEL, Fedora), the
mount also needs the right label.

**Diagnose:**

```bash
docker exec <c> id                          # UID/GID inside
ls -ln /host/path                           # numeric owner outside
docker inspect -f '{{json .Mounts}}' <c>
getenforce                                  # SELinux enforcing?
```

**Fix:** align ownership rather than using `chmod 777`, which grants every local
user write access to the data. Either `sudo chown -R 1000:1000 /host/path` to
match the container UID, or run the container as the host owner with
`--user "$(id -u):$(id -g)"`. Check the target path before any recursive
`chown`. On SELinux hosts add `:z` (shared) or `:Z` (private) to the mount, for
example `-v /host/path:/data:Z`; `:Z` relabels the host directory, so never
apply it to a shared system path.

**Prevent:** prefer named volumes for service state, since Docker initialises
their ownership from the image, and reserve bind mounts for development source
and read-only config (`--mount type=bind,...,readonly`). See
[Bind mounts](#bind-mounts).

### 12. Data disappeared after redeploy

**Symptom:** a database container is recreated during a deploy and comes back
empty.

**Cause:** the data lived in the container's writable layer or in an anonymous
volume. The writable layer is deleted with the container; an anonymous volume
survives, but the new container gets a new one, so the old data is orphaned
rather than destroyed.

**Diagnose:**

```bash
docker volume ls                                  # any unnamed hex-ID volumes?
docker inspect -f '{{json .Mounts}}' <old-c>      # Name empty means anonymous
docker volume inspect <hex-id>                    # Mountpoint on the host
```

**Fix:** the old data may still be recoverable. Locate the orphaned volume,
mount it into a temporary container, and copy the data into a properly named
volume. Do not prune volumes until the copy is verified:

```bash
docker run --rm -v <hex-id>:/from -v pgdata:/to alpine \
  sh -c 'cd /from && cp -a . /to'
```

**Prevent:** always mount a **named** volume for state
(`-v pgdata:/var/lib/postgresql/data`), as in [Volumes](#volumes), never rely on
`docker rm -v` semantics, and take backups from the volume rather than assuming
the volume is the backup. Treat `docker compose down -v` as a destructive
command.

### 13. `docker stop` always takes ten seconds

**Symptom:** every stop and every deploy pauses for the full grace period, and
the container ends with exit code 137 rather than 143. In-flight requests are
dropped.

**Cause:** PID 1 is not receiving or not handling `SIGTERM`, the shell-form
problem described in [CMD vs ENTRYPOINT](#cmd-vs-entrypoint). Alternatively, the
application has no `SIGTERM` handler and only responds to `SIGINT` or `SIGQUIT`.

**Diagnose:**

```bash
docker exec <c> ps -o pid,comm            # is PID 1 sh, or your process?
docker inspect -f '{{json .Config.Cmd}} {{json .Config.Entrypoint}}' <c>
time docker stop <c>
docker inspect -f '{{.State.ExitCode}}' <c>    # 143 good, 137 means it was killed
```

**Fix:** use exec form so the real binary is PID 1:
`CMD ["nginx", "-g", "daemon off;"]`. If a wrapper script is required, end it
with `exec "$@"`. Where the process expects a different signal, declare it with
`STOPSIGNAL SIGQUIT`.

**Prevent:** exec form everywhere, implement a `SIGTERM` handler that drains
connections, and set `--stop-timeout` slightly above the real drain time.

### 14. Zombie processes accumulate inside a container

**Symptom:** `docker exec <c> ps aux` shows a growing list of `<defunct>`
entries; eventually the container hits its PID limit or the process table
fills.

**Cause:** the container's PID 1 is an application that does not reap orphaned
children. On a normal system `init` adopts and reaps them, but inside a PID
namespace that responsibility falls to PID 1.

**Diagnose:**

```bash
docker exec <c> ps -eo pid,ppid,stat,comm | awk '$3 ~ /Z/'
docker exec <c> sh -c 'ls /proc | grep -c "^[0-9]"'
docker inspect -f '{{.HostConfig.PidsLimit}}' <c>
```

**Fix:** run with `docker run --init`, which inserts a minimal init process as
PID 1 that reaps children and forwards signals. `tini` inside the image does
the same job.

**Prevent:** use `--init` for any image whose main process spawns subprocesses,
particularly shell-wrapped and CI-agent style workloads, and set `--pids-limit`
so a fork bomb cannot take the host down.

### 15. Application is slow inside the container but fast on the host

**Symptom:** the same binary is several times slower in a container, with CPU
usage capped below the host's capacity and latency spikes at regular intervals.

**Cause:** CPU quota throttling from `--cpus`, which enforces a quota per
scheduling period and stalls threads once it is spent. A second cause is a
runtime that sizes its thread or connection pools from `nproc`, which reports
**host** cores rather than the quota, so the container creates far more threads
than its quota can run.

**Diagnose:**

```bash
docker stats --no-stream <c>
docker inspect -f '{{.HostConfig.NanoCpus}} {{.HostConfig.CpuShares}}' <c>
docker exec <c> cat /sys/fs/cgroup/cpu.stat        # nr_throttled and throttled_usec rising
docker exec <c> nproc                              # what the runtime will believe
```

**Fix:** raise `--cpus` to match real demand, and pass the effective CPU count
explicitly to the runtime (`GOMAXPROCS`, `-XX:ActiveProcessorCount`,
`UV_THREADPOOL_SIZE`, worker counts). Reserve `--cpu-shares` for relative
priority; it is not a limit and does nothing on an idle host.

**Prevent:** size limits from measured load, alert on cgroup throttling rather
than on CPU percentage, and keep write-heavy paths on volumes so the
copy-on-write layer is not in the hot path.

### 16. Works on my machine, fails on the server

**Symptom:** the image runs locally but on the server fails with "exec format
error", or a different application version starts.

**Cause:** architecture mismatch, typically an `arm64` image built on an Apple
Silicon laptop deployed to `amd64` servers. Or tag drift: both machines pulled
`myapp:latest` at different times and got different content.

**Diagnose:**

```bash
docker image inspect <image> -f '{{.Os}}/{{.Architecture}}'
docker manifest inspect <image> | grep architecture
docker inspect -f '{{.Image}}' <c>                 # the digest actually running
uname -m                                            # on the server
```

**Fix:** build for the target platform, or publish a multi-architecture image:

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t registry.example.com/app:1.4.0 --push .
```

**Prevent:** tag every image with the commit SHA, deploy by digest, never deploy
`latest`, and build release images in CI on the target platform rather than on a
developer laptop.

### 17. `docker logs` returns nothing

**Symptom:** the application is clearly working, but `docker logs <c>` is empty.

**Cause:** either the application writes to a log file inside the container
instead of stdout and stderr, or the container uses a shipping log driver for
which `docker logs` is unsupported. Both cases are covered in
[Logging](#logging).

**Diagnose:**

```bash
docker inspect -f '{{.HostConfig.LogConfig.Type}}' <c>
docker exec <c> ls -la /var/log/                   # log files inside?
docker exec <c> ls -l /proc/1/fd/1 /proc/1/fd/2    # where PID 1's streams point
```

**Fix:** configure the application to log to stdout, or symlink its log file to
`/dev/stdout` as official images do. With a shipping driver, read the logs in
the destination system.

**Prevent:** make "log to stdout, one event per line, structured" an image
requirement. A log file in the writable layer is invisible to the platform and
is deleted with the container.

### 18. A secret was baked into an image

**Symptom:** a scan or a code review finds an API key inside a published image,
even though a later Dockerfile line deletes the file.

**Cause:** layers are additive, so a `COPY` in one layer and an `rm` in a later
layer leaves the original content in the earlier layer. The image configuration
and build metadata are the second exposure route, described under
[Build practices that matter](#build-practices-that-matter).

**Diagnose:**

```bash
docker history --no-trunc <image>          # build args and commands
docker image inspect <image> -f '{{json .Config.Env}}'
docker image inspect <image> -f '{{json .Config.Labels}}'
docker save <image> -o out.tar && tar -tf out.tar   # unpack layers and grep
```

**Fix:** rotate the credential first; the image is already published and must be
assumed compromised. Then remove the affected tags from the registry and rebuild
without the secret.

**Prevent:** inject secrets at run time from a secrets manager, use BuildKit
secret mounts (`RUN --mount=type=secret,id=npmrc ...`) for build-time
credentials, keep credentials out of the build context with `.dockerignore`, and
run a secret scanner in the pipeline. See
[Security practices](#security-practices).

### 19. Cannot debug a distroless or scratch container

**Symptom:** `docker exec -it <c> sh` fails with "executable file not found",
and the container has no shell, no `ps`, and no `curl`.

**Cause:** minimal images intentionally contain only the application binary.
That is the security benefit and the debugging cost. A stopped container cannot
be `exec`ed into at all, whatever the image, as noted in
[attach vs exec](#attach-vs-exec).

**Diagnose and fix:** attach a debug container that shares the target's
namespaces, so your tools see its processes, network, and filesystem:

```bash
docker run -it --rm --pid=container:<c> --network=container:<c> \
  --cap-add=SYS_PTRACE nicolaka/netshoot
```

`--cap-add=SYS_PTRACE` lets the debug container inspect the target's memory and
system calls, so use it only while investigating and prefer a dedicated debug
image over adding the capability to the workload itself.

For a container that has already exited, extract state instead:

```bash
docker logs <c>
docker cp <c>:/path/to/file ./
docker commit <c> debug-image && docker run --rm -it --entrypoint sh debug-image
docker diff <c>                            # what the container wrote
```

**Prevent:** keep minimal runtime images and standardise on a sidecar debug
image, so nobody is tempted to add a shell and a package manager to production
images.

### 20. Container clock or timezone is wrong

**Symptom:** log timestamps are hours off, TLS certificate validation fails, or
scheduled jobs fire at the wrong local time.

**Cause:** containers use the host clock, so real drift is a host NTP problem,
not a container problem. A wrong local time is almost always a missing timezone:
minimal images default to UTC and may not even ship the tzdata database.

**Diagnose:**

```bash
docker exec <c> date
date                                   # compare to the host
docker exec <c> cat /etc/timezone       # if present
timedatectl status                      # host NTP synchronisation
```

**Fix:** fix host time synchronisation for actual drift. For local time, install
`tzdata` in the image and set `ENV TZ=Asia/Kolkata`, or pass `-e TZ=...`.

**Prevent:** run every service in UTC and convert only at presentation time, and
monitor host clock offset. Never try to set the container clock directly; that
requires `SYS_TIME` and would change the host clock.

### 21. Cannot connect to the Docker daemon

**Symptom:** `docker ps` fails with "Cannot connect to the Docker daemon at
unix:///var/run/docker.sock. Is the docker daemon running?"

**Cause:** the daemon is not running, the user is not in the `docker` group, or
`DOCKER_HOST` points somewhere unreachable such as a stale remote context.

**Diagnose:**

```bash
systemctl status docker
id -nG "$USER" | tr ' ' '\n' | grep -x docker
echo "$DOCKER_HOST"; docker context ls
ls -l /var/run/docker.sock
journalctl -u docker.service -n 50
```

**Fix:** start the service, add the user to the `docker` group and start a new
login session, or select the right context with `docker context use default`.

**Prevent:** remember that `docker` group membership is equivalent to root on
the host, since the socket can mount any host path into a privileged container,
as noted in [Components](#components). Grant it deliberately, and prefer
rootless Docker or a remote builder for untrusted users.

## Examples in this repository

- `NginxDockerfile` in the parent directory: minimal Nginx image.
- `docker-compose-diff-expose_&_ports.yaml` in the parent directory: `expose`
  versus `ports`.

### Running MinIO locally

```bash
docker run -d --name minio \
  -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=<access-key>" \
  -e "MINIO_ROOT_PASSWORD=<secret-key>" \
  -v minio-data:/data \
  minio/minio server /data --console-address ":9001"

mc alias set local http://localhost:9000 <access-key> <secret-key> --api S3v4
mc mb local/test
mc find local/test --newer-than 2d0h0m --ignore '*.html'
```

Pass credentials from your shell environment or a secrets file rather than
literal values, so they do not end up in shell history or in
`docker inspect` output that others can read.

## Reference

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Storage overview](https://docs.docker.com/engine/storage/)
- [Networking overview](https://docs.docker.com/engine/network/)
