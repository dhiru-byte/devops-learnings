# Docker

Pointer-style interview notes for Docker.

- **Owns:** the container runtime — images, layers, Dockerfiles, networking,
  storage, limits, logging, failure modes.
- **Elsewhere:** kernel primitives (namespaces, cgroups, OOM killer, TCP/IP, DNS)
  in the [Linux guide](linux-interview-guide.md); history and branch policy in
  the [Git guide](git-interview-guide.md).
- **Layout:** facts in tables, actions in command blocks, traps under **Gotchas**,
  failures in [scenarios](#troubleshooting-scenarios) as
  **Symptom -> Check -> Cause -> Fix -> Prevent**.
- **Safety:** destructive commands are marked; run the read-only form first.

## Contents

- **Build:** [Concepts](#concepts) · [Architecture and isolation](#architecture-and-isolation) ·
  [Images and layers](#images-and-layers) · [Dockerfile](#dockerfile) ·
  [COPY vs ADD](#copy-vs-add) · [CMD vs ENTRYPOINT](#cmd-vs-entrypoint)
- **Run:** [Container lifecycle](#container-lifecycle) · [attach vs exec](#attach-vs-exec) ·
  [Networking](#networking) · [Storage](#storage) · [Resource limits](#resource-limits) ·
  [Logging](#logging)
- **Ship:** [Registries and image transfer](#registries-and-image-transfer) ·
  [Docker Compose](#docker-compose) · [Cleanup](#cleanup) ·
  [Security practices](#security-practices) · [Docker in CI/CD](#docker-in-cicd)
- **Reference:** [Troubleshooting scenarios](#troubleshooting-scenarios)

- **Scenarios:**
  - [triage](#first-response-triage) · [1 exits with 0](#1-container-exits-immediately-with-code-0) · [2 exit 137](#2-container-killed-with-exit-code-137)
  - [3 restart loop](#3-container-in-a-restart-loop) · [4 port allocated](#4-port-is-already-allocated) · [5 connection refused](#5-published-port-is-open-but-connections-are-refused)
  - [6 DNS and egress](#6-container-cannot-resolve-another-container-or-has-no-internet) · [7 host disk full](#7-no-space-left-on-device-on-the-host)
  - [8 cache misses](#8-every-build-rebuilds-everything) · [9 missing file](#9-build-succeeds-but-the-file-is-missing-at-runtime)
  - [10 volume permissions](#10-permission-denied-on-a-mounted-volume) · [11 data lost](#11-data-disappeared-after-redeploy)
  - [12 slow stop](#12-docker-stop-always-takes-ten-seconds) · [13 zombies](#13-zombie-processes-accumulate-inside-a-container)
  - [14 CPU throttling](#14-slow-in-the-container-fast-on-the-host) · [15 wrong architecture](#15-works-on-my-machine-fails-on-the-server)
  - [16 no logs](#16-docker-logs-returns-nothing) · [17 baked-in secret](#17-a-secret-was-baked-into-an-image)
  - [18 no shell](#18-cannot-debug-a-distroless-or-scratch-container) · [19 daemon unreachable](#19-cannot-connect-to-the-docker-daemon)

## Concepts

**Docs:** [Docker overview](https://docs.docker.com/get-started/docker-overview/) ·
[What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)

Docker packages an application with its dependencies into an image and runs it
as an isolated process on a **shared host kernel**: a running process plus an
image filesystem, with its own view of the process tree, network, and mounts.

| Benefit | Why |
| :--- | :--- |
| Identical runtime everywhere | The image carries libraries, binaries, and configuration |
| Fast start, low overhead | A process with namespaces and cgroups applied, no guest OS |
| Immutable versioned artifacts | Content-addressed and tagged, so rollback is a tag change |
| Layer caching and density | Unchanged layers are reused across builds and pulls; many containers per host |

| | Virtual machine | Container |
| :--- | :--- | :--- |
| Abstracts | The machine | The application process |
| Kernel | Its own guest kernel | Shares the host kernel |
| Size / start time | Gigabytes / tens of seconds | Megabytes / milliseconds |
| Isolation | Hardware-level via hypervisor | Process-level via namespaces and cgroups |

- **Type 1** (bare-metal) hypervisor runs directly on hardware (ESXi, KVM);
  **type 2** (hosted) runs as an application (VirtualBox).
- Complementary: containers usually run inside cloud VMs, so the VM supplies the
  hard tenancy boundary and the container supplies packaging and density.

Where Docker alone falls short:

- No scheduling, rolling updates, or self-healing across hosts — that is Kubernetes.
- Local volumes are tied to one host: multi-host state needs a network volume
  driver or a managed database.
- A shared kernel cannot satisfy a different kernel or OS.
- Observability needs an external stack; image sprawl grows without registry
  lifecycle policies.

**Gotchas.** "Docker has no storage option" is wrong: volumes, bind mounts, and
tmpfs mounts are built in ([Storage](#storage)).

## Architecture and isolation

**Docs:** [Docker Engine](https://docs.docker.com/engine/) ·
[`dockerd` reference](https://docs.docker.com/reference/cli/dockerd/) ·
Linux primitives: [cgroups and namespaces](linux-interview-guide.md#cgroups-and-namespaces)

| Component | Role |
| :--- | :--- |
| `docker` client | Sends commands to the daemon over the REST API, by default via `/var/run/docker.sock` |
| `dockerd` | Builds images, manages networks and volumes, drives the container lifecycle |
| `containerd` | Runtime the daemon delegates to for image pull and container supervision |
| `runc` | Actually creates the container by applying namespaces and cgroups |
| Registry | Stores and serves images over HTTP (Docker Hub, GHCR, ECR, Harbor, Artifactory) |

- Namespaces give the container its own **view** (PID, mount, network, UTS, IPC,
  user, cgroup); cgroups **limit** what it consumes (CPU, memory, block I/O,
  process count). Both are Linux kernel features, not Docker features.
- Namespaces without cgroups lets one container starve the host; cgroups without
  namespaces gives no isolation.

**Gotchas**

- The daemon socket is **root-equivalent**: anyone in the `docker` group can mount any host path into a privileged container and become root.
- Treat that membership as administrator access; prefer rootless Docker for untrusted users.

## Images and layers

**Docs:** [Image layers](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/) ·
[`docker image`](https://docs.docker.com/reference/cli/docker/image/)

- **Image:** a read-only layered filesystem plus configuration metadata
  (entrypoint, command, environment, ports, user).
- **Layer:** the filesystem diff from one build instruction.
- **Container:** an image plus a thin writable layer.

| Fact | Detail |
| :--- | :--- |
| Which instructions create layers | Only `FROM`, `RUN`, `COPY`, `ADD` (`FROM` brings in the base image's layers); `ENV`, `WORKDIR`, `EXPOSE`, `LABEL`, `CMD` change metadata only |
| Sharing | Ten containers from one image share one copy of the image layers plus ten small writable layers |
| Additivity | Deleting a file in a later layer hides it but does not shrink the image |

```bash
docker images; docker images -a          # list; include intermediate layers
docker history <image>                   # per-layer size and instruction
docker image inspect <image>             # full configuration
docker commit <container> my-image:tag   # snapshot a running container
docker import archive.tar my-image:tag   # import a root filesystem tarball
```

| Gotcha | Detail |
| :--- | :--- |
| Deleting a secret in a later layer | `RUN rm secret.key` after `COPY secret.key` **still ships the secret** in the earlier layer; remove it in the same layer or use a multi-stage build |
| `commit` and `import` are not a build process | Debugging or migration tools only: the result is not reproducible, `commit` records no build context, `import` drops history and configuration such as `ENTRYPOINT` |
| Production images | Come from a Dockerfile in version control |

## Dockerfile

**Docs:** [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) ·
[Best practices](https://docs.docker.com/build/building/best-practices/) ·
[BuildKit secrets](https://docs.docker.com/build/building/secrets/)

The default filename is `Dockerfile`; use `-f <path>` for anything else.

| Instruction | Purpose |
| :--- | :--- |
| `FROM` | Base image; starts a build stage |
| `RUN` | Execute a command in a new layer |
| `COPY` / `ADD` | Copy from the build context / also remote URLs and archive extraction |
| `CMD` | Default command or default arguments, overridable at run time |
| `ENTRYPOINT` | The executable the container always runs |
| `ENV` / `ARG` | Runtime environment variable, persisted in the image / build-time variable |
| `WORKDIR` / `USER` | Working directory for later instructions and run time / UID and GID for them |
| `EXPOSE` | Documents the listening port; **does not publish it** |
| `VOLUME` | Declares a mount point that gets an anonymous volume if unmounted |
| `LABEL` | Metadata such as source commit and maintainer (`MAINTAINER` is deprecated) |
| `HEALTHCHECK` | Command that reports container health |
| `STOPSIGNAL` / `SHELL` | Stop signal (default `SIGTERM`) / shell for shell-form instructions |
| `ONBUILD` | Deferred instruction that runs when this image is used as a base |
| `.dockerignore` | Not an instruction: excludes paths from the build context |

### Build practices that matter

- **Order by change frequency:** copy dependency manifests and install before
  copying source, so a code change does not invalidate the dependency layer.
- **One logical step per `RUN`:** chain install and cleanup in a single `RUN` so
  the cleanup actually reduces image size.
- **Always write a `.dockerignore`.** Excluding `.git`, `node_modules`, and
  build output shrinks the context and keeps secrets out of it.
- **Pin base images** to a tag or digest; `FROM ubuntu:latest` is not
  reproducible.
- **Use multi-stage builds** so compilers stay out of the runtime image, and
  **run as non-root** with `USER`.

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

- Distro packages in one layer, so the cleanup counts: `RUN apt-get update &&
  apt-get install -y --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*`,
  with `ENV DEBIAN_FRONTEND=noninteractive` to stop apt prompting.
- A Dockerfile has **no end-of-line comments**: `#` is a comment only as the
  first non-whitespace character.

| Gotcha | Detail |
| :--- | :--- |
| **Never pass secrets through `ARG` or `ENV`** | `ENV` and `LABEL` are stored in the final image configuration and appear in `docker inspect` |
| `ARG` still leaks | Not automatically present at run time, but leaks through provenance, command history, build logs, cache metadata, or files a `RUN` creates; copying it into `ENV` or `LABEL` makes it persist explicitly |
| Do this instead | BuildKit secret mounts (`RUN --mount=type=secret,...`) or inject at run time |

## COPY vs ADD

**Docs:** [`COPY`](https://docs.docker.com/reference/dockerfile/#copy) ·
[`ADD`](https://docs.docker.com/reference/dockerfile/#add)

Use `COPY` unless you specifically need one of `ADD`'s extra behaviours.

| | `COPY` | `ADD` |
| :--- | :--- | :--- |
| Local files and directories | Yes | Yes |
| Remote URL / Git repository as source | No | Yes / yes, with the BuildKit frontend |
| Auto-extract local tar archive | No | Yes, for recognised compression |
| Behaviour predictable from the line alone | Yes | No |

```dockerfile
# Verifiable download instead of ADD https://..., and an explicit owner
RUN curl -fsSL <url> -o file && echo "<sha256>  file" | sha256sum -c
COPY --chown=app:app --chmod=0644 config/ /app/config/
```

**Gotchas**

- `ADD some.tar.gz /opt/` silently extracts while `ADD app.jar /opt/` silently
  copies; a reviewer cannot tell which happens without knowing the file type.
- `ADD https://...` has no checksum verification or retry control, and leaves
  the download in a layer even after later deletion.
- Without `--chown`, copied files are owned by root regardless of `USER`.
- Legitimate `ADD` use: unpacking a base root filesystem tarball, as official
  distro images do. Git URL sources need BuildKit; pin a commit or tag, and use
  `--keep-git-dir` only when the build truly needs `.git`.

## CMD vs ENTRYPOINT

**Docs:** [`ENTRYPOINT`](https://docs.docker.com/reference/dockerfile/#entrypoint) ·
[`CMD`](https://docs.docker.com/reference/dockerfile/#cmd)

`ENTRYPOINT` is the executable that always runs; `CMD` supplies default
arguments, and anything passed to `docker run` replaces `CMD`. Replacing
`ENTRYPOINT` requires `docker run --entrypoint`.

| | `ENTRYPOINT` | `CMD` |
| :--- | :--- | :--- |
| Role | Fixed executable | Default arguments or default command |
| Overridden by | `--entrypoint` only | Trailing arguments of `docker run` |
| Inherited from base | Yes | Yes, and reset to empty when `ENTRYPOINT` is set later |

| Pattern | Result |
| :--- | :--- |
| `ENTRYPOINT ["app"]` + `CMD ["--help"]` | `docker run img` runs `app --help`; `docker run img --port 80` runs `app --port 80` |
| `CMD ["app", "--help"]` only | `docker run img` runs `app --help`; `docker run img bash` runs `bash` |
| `ENTRYPOINT ["app"]` only | Arguments always append; the image cannot easily run a shell |

Exec form versus shell form matters more than the choice between the two
instructions:

```dockerfile
ENTRYPOINT ["nginx", "-g", "daemon off;"]   # exec form: nginx is PID 1
ENTRYPOINT nginx -g 'daemon off;'           # shell form: /bin/sh -c is PID 1
```

- Single-purpose image: set `ENTRYPOINT` to the binary and `CMD` to default flags.
- Image people need to poke at: use `CMD` alone, so `docker run img bash` works.
- An `ENTRYPOINT` script ending in `exec "$@"` does setup work and still hands
  PID 1 to the real process.

**Gotchas**

- With shell form the shell is PID 1, so `SIGTERM` from `docker stop` goes to the shell and is often not forwarded: the container ignores the graceful stop and is `SIGKILL`ed after the timeout.
- **Always use exec form** for the process that must receive signals; an `ENTRYPOINT` of `/bin/sh` turns every argument into a shell string and breaks signal handling.

## Container lifecycle

**Docs:** [`docker run`](https://docs.docker.com/reference/cli/docker/container/run/) ·
[`docker container`](https://docs.docker.com/reference/cli/docker/container/)

States: created, running, paused, restarting, exited, dead. `docker run` is
`docker create` plus `docker start`.

```bash
docker create --name web nginx      # create without starting
docker run -d --name web nginx      # create and start
docker run --rm -it alpine sh       # remove automatically on exit
docker stop web; docker stop -t 30 web   # SIGTERM then SIGKILL; longer grace
docker kill web; docker kill -s HUP web  # SIGKILL now; specific signal
docker restart web; docker pause web; docker unpause web
docker update --memory 512m web     # change resource limits in place
docker rm web; docker rm -f web     # stopped container; force running or paused
docker rm -v web                    # also delete its ANONYMOUS volumes
docker wait web                     # block until exit, print the exit code

docker ps; docker ps -a                   # running; including exited
docker logs -f --tail 100 web             # container stdout/stderr
docker inspect web                        # mounts, networks, IP, exit code
docker inspect -f '{{.State.ExitCode}} {{.State.OOMKilled}}' web
docker top web; docker stats; docker stats --no-stream
docker diff web                           # files changed in the writable layer
docker port web; docker events
docker cp myfile.txt web:/usr/share; docker cp web:/var/log/app.log ./
```

**Gotchas.** A plain `docker rm` refuses a paused or running container; `-f`
kills it first. The `ExitCode` and `OOMKilled` inspect fields are the fastest
checks after an unexpected exit.

## attach vs exec

**Docs:** [`docker exec`](https://docs.docker.com/reference/cli/docker/container/exec/) ·
[`docker attach`](https://docs.docker.com/reference/cli/docker/container/attach/)

| | `docker attach` | `docker exec` |
| :--- | :--- | :--- |
| Target | The existing main process (PID 1) streams | A new process |
| Multiple sessions | Yes, all see the same stream | Yes, independent |
| Needs the container running | Yes | Yes |
| Survives container restart | No | No |

`docker exec -it web sh` is what you want almost always; `attach` is only for
watching or driving a main process that is itself an interactive shell.

**Gotchas**

- On an attached session `Ctrl-C` sends `SIGINT` to the main process and usually stops the container — detach with `Ctrl-P` then `Ctrl-Q`, or attach with `--sig-proxy=false`.
- Neither command works on a **stopped** container: `docker cp` the files out, or `docker commit` it and run a shell on that image.

## Networking

**Docs:** [Networking overview](https://docs.docker.com/engine/network/) ·
[Bridge driver](https://docs.docker.com/engine/network/drivers/bridge/) ·
[Published ports](https://docs.docker.com/engine/network/#published-ports)

| Driver | Use it when |
| :--- | :--- |
| `bridge` | Default. Containers on one host talking to each other and reachable through published ports |
| `host` | The container should use the host network stack directly (high packet rates, binding host ports). No isolation, no port publishing |
| `overlay` | Containers on different hosts must communicate; traffic is encapsulated between daemons |
| `macvlan` / `ipvlan` | The container needs its own IP on the physical LAN, with its own MAC / sharing the host MAC |
| `none` | Loopback only; batch jobs that must not reach the network |

| | Default `bridge` | User-defined bridge |
| :--- | :--- | :--- |
| Service discovery by name | No | Yes, embedded DNS at `127.0.0.11` |
| Isolation | All containers share one network | Only attached containers can reach each other |
| Attach/detach while running | No | Yes |
| Configurable subnet and gateway | Limited | Yes |

- **Always create a user-defined bridge for multi-container applications.**
- The default bridge is `docker0`, subnet `172.17.0.0/16`, gateway `172.17.0.1` —
  the host *as seen from containers*, not "the IP of the Docker host"; the host's
  LAN address is unrelated, and the pool is set by `default-address-pools`.

```bash
docker network ls; docker network inspect app-net   # subnet, gateway, members
docker network create --driver bridge app-net
docker network create --subnet 203.0.113.0/24 --gateway 203.0.113.254 lab-net
docker network connect app-net web; docker network disconnect app-net web
docker run -d --name db --network app-net postgres:16
docker run -it --network app-net alpine ping db   # resolves by container name

docker run -p 8080:80 nginx           # host 8080 -> container 80, all interfaces
docker run -p 127.0.0.1:8080:80 nginx # bind only to host loopback
docker run -P nginx                   # publish every EXPOSEd port to a random port
```

**Gotchas**

- `EXPOSE` is documentation only; traffic reaches a container because a port was
  **published** at run time.
- In Compose, `expose` only records the port while `ports` maps it onto the
  host. Containers on the same user-defined network already reach each other on
  the container port by name, so `ports` is only for traffic from outside
  Docker.
- Address services by name, never by container IP: IPs change on every recreate.

## Storage

**Docs:** [Storage overview](https://docs.docker.com/engine/storage/) ·
[Volumes](https://docs.docker.com/engine/storage/volumes/) ·
[Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)

The writable layer is copy-on-write and disappears with the container, so
anything that must survive belongs on a mount.

| Type | Managed by | Lives at | Use for |
| :--- | :--- | :--- | :--- |
| Volume | Docker | `/var/lib/docker/volumes/<name>/_data` on Linux | Database files and any container-produced state |
| Bind mount | You | Any host path you choose | Source code in development, host config and logs |
| tmpfs mount | Docker | Host memory only | Secrets and scratch data that must never hit disk |

```bash
docker volume create pgdata; docker volume ls; docker volume inspect pgdata
docker volume ls -f dangling=true          # orphaned volumes
docker volume rm pgdata; docker volume prune   # prune: unused anonymous volumes

docker run -d --name db -v pgdata:/var/lib/postgresql/data postgres:16
docker run -d --name db --mount source=pgdata,target=/var/lib/postgresql/data postgres:16
docker run --rm --volumes-from db alpine tar cf - /var/lib/postgresql/data > backup.tar
docker run -v /host/path:/app --mount type=bind,source=/host/path,target=/app,readonly
docker info | grep -i 'storage driver'     # overlay2 on modern Linux
docker system df; docker system df -v      # space used, then per object
```

`overlay2` copies a file up into the writable layer on first write, so
write-heavy workloads there are slower and grow disk usage per container — the
technical reason databases belong on volumes, which bypass the union filesystem.

**Gotchas**

- Named volumes are created on first use and are **not** deleted with the
  container; `docker rm -v` removes anonymous volumes only, which is how
  orphaned volumes accumulate.
- Treat `/var/lib/docker/volumes` as private: go through `docker run`,
  `docker cp`, or a helper container. On Docker Desktop it is inside the Linux
  VM, not on the macOS or Windows filesystem.
- The short `-v` bind form **creates a missing host directory silently**, while
  `--mount type=bind` errors out. Prefer `--mount` and add `readonly`.
- Bind mounts expose the host filesystem with host UID/GID semantics; mounting
  `/var/run/docker.sock` or a host config directory read-write is a privilege
  escalation risk.
- Only network volume drivers (NFS, EBS, CSI) let a volume follow a container to
  another host.

## Resource limits

**Docs:** [Runtime resource constraints](https://docs.docker.com/engine/containers/resource_constraints/) ·
Kernel behaviour: [cgroups](linux-interview-guide.md#cgroups-and-namespaces),
[OOM killer](linux-interview-guide.md#memory)

By default a container can use all host CPU and memory. Set limits explicitly.

```bash
docker run -it --cpus=1.5 --memory=512m --memory-swap=512m myapp
docker run -it --cpuset-cpus=0,4,6 myapp     # pin to specific cores
docker run -it --cpu-shares=512 myapp        # relative weight under contention
docker run -it --pids-limit=200 myapp        # cap process count
docker update --cpus=2 --memory=1g myapp     # adjust a running container
```

| Flag | Semantics |
| :--- | :--- |
| `--cpus=1.5` | Hard cap: one and a half cores' worth of CPU time per period |
| `--cpu-shares=512` | **Relative weight only** (default 1024); does nothing on an idle host and is not "50% of the CPU" |
| `--memory` | Hard limit; exceeding it means a kernel OOM kill, exit code 137, and `OOMKilled: true` |
| `--memory-swap` / `--pids-limit` | Equal to `--memory` forbids swap / bounds runaway forking |

**Gotchas**

- Inside the container, `free`, `nproc`, and `/proc/cpuinfo` still report **host-wide** values unless the runtime virtualises them, so runtimes that size thread pools or heaps from them over-allocate.
- Pass the effective limit explicitly: `GOMAXPROCS`, `-XX:MaxRAMPercentage`, `UV_THREADPOOL_SIZE`.

## Logging

**Docs:** [Logging drivers](https://docs.docker.com/engine/logging/configure/) ·
[`json-file` driver](https://docs.docker.com/engine/logging/drivers/json-file/)

- **Daemon logs:** engine behaviour — pull failures, storage driver errors,
  networking problems. Verbosity is `"log-level"` in `/etc/docker/daemon.json`
  (`debug`, `info` default, `warn`, `error`, `fatal`); read with
  `journalctl -u docker.service`.
- **Container logs:** whatever the main process writes to stdout and stderr,
  captured by the log driver.

```bash
docker logs web; docker logs --tail 100 web
docker logs -f --since 10m --timestamps web
docker inspect -f '{{.HostConfig.LogConfig.Type}}' web
```

Set rotation globally in `/etc/docker/daemon.json`:
`{"log-driver": "json-file", "log-opts": {"max-size": "10m", "max-file": "3"}}`

**Gotchas**

- Applications should log to **stdout/stderr**, not to files inside the
  container: a file in the writable layer is invisible to `docker logs` and is
  lost with the container.
- The default `json-file` driver writes to
  `/var/lib/docker/containers/<id>/<id>-json.log` and **does not rotate** unless
  configured. Unbounded logs filling the disk is a routine incident.
- `docker logs` works with `json-file`, `local`, and `journald`. With a shipping
  driver (`awslogs`, `fluentd`, `gelf`, `splunk`) it returns nothing and you
  read logs in the destination system.

## Registries and image transfer

**Docs:** [`docker push`](https://docs.docker.com/reference/cli/docker/image/push/) ·
[`docker save`](https://docs.docker.com/reference/cli/docker/image/save/)

A **repository** is a named collection of tagged images (`library/nginx`); a
**registry** is the server hosting repositories (Docker Hub, ECR, Harbor).

```bash
docker login registry.example.com; docker logout registry.example.com
docker pull nginx:1.27-alpine; docker rmi myapp:1.4.0
docker tag myapp:1.4.0 registry.example.com/team/myapp:1.4.0
docker push registry.example.com/team/myapp:1.4.0
docker manifest inspect <image>            # platforms in a multi-arch image
```

| Pair | Works on | Preserves |
| :--- | :--- | :--- |
| `save` / `load` | **Images** | All layers, tags, and history |
| `export` / `import` | A **container's filesystem** | Neither history nor configuration |

```bash
docker save my_image:tag | gzip > my_image.tar.gz   # image, with all layers
docker load < my_image.tar.gz
docker export my_container | gzip > fs.tar.gz       # flat filesystem snapshot
cat fs.tar.gz | docker import - my_image:tag
```

| Gotcha | Detail |
| :--- | :--- |
| `save`/`load` | The way to move a real image between hosts without a registry, e.g. into an air-gapped environment |
| `export`/`import` | Produces one flattened layer with no `ENTRYPOINT`, `CMD`, or `ENV`: for inspecting a filesystem, not shipping applications |
| Pin by digest | Reference `nginx@sha256:...` when supply-chain integrity matters; a mutable tag can be repointed at different content |

## Docker Compose

**Docs:** [Compose overview](https://docs.docker.com/compose/) ·
[Compose file reference](https://docs.docker.com/reference/compose-file/)

- Compose declares a multi-container application in YAML: services, images or
  build contexts, environment, networks, volumes, dependencies.
- One command brings the set up on a shared default network, so services reach
  each other by name (explicit `links` are obsolete).

```bash
docker compose up -d; docker compose ps
docker compose logs -f api; docker compose exec api sh
docker compose config          # render and validate the merged configuration
docker compose down            # stop and remove containers and networks
docker compose down -v         # DESTRUCTIVE: also removes named volumes
```

**Gotchas**

- `depends_on` waits for the container to **start**, not for the application to be ready; pair it with `condition: service_healthy` and a `HEALTHCHECK`.
- Compose targets local development and single-host deployments; multi-host production belongs on an orchestrator. `down -v` is data loss.

## Cleanup

**Docs:** [Prune unused objects](https://docs.docker.com/engine/manage-resources/pruning/)

Inspect candidates and reclaimable space **before** deleting anything:

```bash
docker system df -v; docker builder du
docker ps -a --filter status=exited
docker image ls --filter dangling=true; docker volume ls --filter dangling=true
```

Then apply the narrowest cleanup that removes only reviewed objects. Every
`prune` deletes **unused** objects only, and prompts unless you pass `-f`:

```bash
docker container prune --filter 'until=24h'   # stopped containers only
docker network prune                          # networks with no container attached
docker image prune -a --filter 'until=168h'   # -a: all unused images, not just dangling
docker builder prune --filter 'until=168h'    # build cache only
docker volume prune                           # unused ANONYMOUS volumes
docker volume prune -a                        # DESTRUCTIVE: also unused NAMED volumes
docker system prune                           # stopped containers, unused networks, dangling images, cache
docker system prune -a --volumes -f           # DESTRUCTIVE: adds all unused images and anonymous volumes, no prompt
```

**Gotchas**

- "Unused" is the safety model: anything referenced by a running container is never pruned. Stopped containers and unreferenced volumes are fair game.
- `docker volume prune` removes unused **anonymous** volumes only; `-a` extends it to unused **named** volumes, which is where real data lives.
- `docker system prune --volumes` covers anonymous volumes only — named volumes need `docker volume prune -a`.
- The prompt is the last safeguard: `-f` removes it, so an unattended `-f` prune on a shared or production host is the risk, not the command itself.
- Prune specific object types on a schedule with `--filter "until="`.
- Blunt resets such as `docker rm -f $(docker ps -aq)` are for disposable development hosts only, and only after reviewing the object list first.

## Security practices

**Docs:** [Engine security](https://docs.docker.com/engine/security/) ·
[Rootless mode](https://docs.docker.com/engine/security/rootless/)

- Run as a non-root user: add `USER` to the image, and enforce
  `--user 1000:1000` at run time where the image cannot be changed.
- Drop privileges: `--cap-drop=ALL` then add back only what is needed,
  `--security-opt=no-new-privileges`, `--read-only` root filesystem with a tmpfs
  for scratch space.
- **Never** use `--privileged` or mount `/var/run/docker.sock` into a container
  unless you accept that the container is equivalent to host root.
- Keep secrets out of images: environment variables and labels persist in image
  configuration and appear in `docker inspect`, and build arguments can leak
  through provenance, commands, logs, cache, or generated files. Use a secrets
  manager, a mounted file, or BuildKit secret mounts.
- Never type a credential as a literal `docker run` argument: pass it from your
  shell environment or a secrets file, or it lands in shell history and
  `docker inspect` output.
- Use minimal bases (`alpine`, distroless), pin versions, rebuild regularly for
  base patches, and fail the pipeline on fixable high-severity scan findings.

## Docker in CI/CD

**Docs:** [Build cache](https://docs.docker.com/build/cache/) ·
[BuildKit](https://docs.docker.com/build/buildkit/) ·
[Multi-platform builds](https://docs.docker.com/build/building/multi-platform/)

- **Continuous integration:** merge every change into the mainline frequently and
  validate it automatically.
- **Continuous delivery:** keep every passing change packaged and releasable, the
  push to production a deliberate decision.
- **Continuous deployment:** release every passing change automatically.
- Docker's role is an immutable build artifact every stage shares; Git's role is
  in [Git in a CI/CD pipeline](git-interview-guide.md#git-in-a-cicd-pipeline).

| Stage | What it does |
| :--- | :--- |
| 1. Build | Build the image **once**, tagged with the commit SHA; a rebuild per environment is a different artifact |
| 2. Unit tests | Run against the code or inside the built image |
| 3. Image scan | CVE and policy checks: no root user, no critical CVEs, size budget |
| 4. Push | Publish to the registry |
| 5. Deploy to staging | Deploy that exact image digest |
| 6. Smoke test | Fast go/no-go gate: health endpoint 200, login works, core page renders. If it fails, stop immediately |
| 7. Regression suite | Broad set covering existing behaviour and previously fixed bugs; slower, and what makes refactors and base-image bumps safe |
| 8. Promote | Promote the same image to production, verify with the same health checks, keep the previous tag for rollback |

```bash
docker buildx build \
  --cache-from type=registry,ref=registry.example.com/app:buildcache \
  --cache-to   type=registry,ref=registry.example.com/app:buildcache,mode=max \
  --platform linux/amd64,linux/arm64 \
  -t registry.example.com/app:$GIT_SHA --push .
```

**Gotchas.** Never deploy `latest`: it makes the running version unknowable. Tag
with the SHA and add human-friendly aliases. Prefer rootless builders over
mounting the Docker socket into build jobs.

## Troubleshooting scenarios

Collect evidence **before** restarting anything: `docker restart` destroys the
process list you needed and often makes the failure unreproducible.

### First-response triage

```bash
docker ps -a                                   # running, exited, or restarting?
docker inspect -f '{{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}} restarts={{.RestartCount}}' <c>
docker logs --tail 200 --timestamps <c>        # what it said before it stopped
docker inspect -f '{{json .Config.Entrypoint}} {{json .Config.Cmd}}' <c>
docker stats --no-stream; docker system df     # limits; host disk pressure
docker events --since 30m                      # daemon view: kills, OOM, health
journalctl -u docker.service --since '30 min ago'   # daemon-side errors
```

| Exit code | Meaning |
| :---: | :--- |
| 0 | The main process finished normally, so the container has nothing left to run |
| 1 / 2 | Application error or shell usage error; read the logs |
| 125 / 126 / 127 | Daemon rejected the run command / command not executable / command not found |
| 137 | `SIGKILL`: OOM-killed, `docker kill`, or a stop that timed out |
| 139 / 143 | `SIGSEGV` inside the container / `SIGTERM` honoured (graceful stop) |

### 1. Container exits immediately with code 0

- **Symptom:** `docker run -d` returns an ID, `docker ps -a` shows `Exited (0)`.
- **Check:** `docker logs <c>`; `docker inspect -f '{{json .Config.Cmd}}' <c>`;
  `docker run --rm -it <image> sh` and run the command by hand.
- **Cause:** the main process finished and a container lives exactly as long as
  PID 1: one-shot `CMD`, an entrypoint script that ends instead of `exec`ing the
  server, a flag that daemonises, or a shell started without `-it` reading EOF.
- **Fix:** run in the foreground (`nginx -g 'daemon off;'`) and end entrypoint
  scripts with `exec "$@"`. See [CMD vs ENTRYPOINT](#cmd-vs-entrypoint).
- **Prevent:** if the workload really is one-shot, run it as a job
  (`docker run --rm`) with no restart policy.

### 2. Container killed with exit code 137

- **Symptom:** the container disappears under load; the log ends mid-request.
- **Check:** `docker inspect -f '{{.State.OOMKilled}}' <c>` (true = memory
  limit); `{{.HostConfig.Memory}}` (0 = unlimited); `docker stats --no-stream`;
  `dmesg -T | grep -i -E 'killed process|oom'`.
- **Cause:** almost always the kernel OOM killer enforcing `--memory`; the other
  sources of 137 are `docker kill` and a `docker stop` that timed out.
- **Fix:** raise `--memory` or reduce consumption, **and** set the runtime's own
  heap limit — a JVM without `-XX:MaxRAMPercentage` sizes its heap from **host**
  memory and dies long before it thinks it is full.
- **Prevent:** container limit plus matching in-process limit, alert on working
  set near the limit rather than on restarts, load-test at the configured limit.
  See [Resource limits](#resource-limits).

### 3. Container in a restart loop

- **Symptom:** status flips between `Up 2 seconds` and `Restarting (1)`.
- **Check:** `docker inspect -f '{{.RestartCount}} {{.State.Error}}' <c>`;
  `docker logs <c> 2>&1 | head -50` (the **first** failure is informative).
- **Cause:** the process crashes at startup and `--restart=always` relaunches
  it: missing environment variable, unreachable dependency, bad config mount, or
  an in-container port conflict.
- **Fix:** correct the configuration; to debug, break the loop with
  `--restart=no --entrypoint sh -it` and run the real command by hand.
- **Prevent:** `--restart=on-failure:5` rather than `always`, so a permanently
  broken container stops instead of hiding the failure; add a `HEALTHCHECK` and
  retry dependencies with backoff.

### 4. Port is already allocated

- **Symptom:** `Bind for 0.0.0.0:8080 failed: port is already allocated` (125).
- **Check:** `docker ps -a --format '{{.Names}}\t{{.Ports}}' | grep 8080`;
  `sudo ss -ltnp | grep :8080`.
- **Cause:** another container publishes that host port, a non-Docker process is
  listening, or a restarting container still holds the mapping.
- **Fix:** remove or re-map the conflicting container, choose another host port,
  or bind one interface (`-p 127.0.0.1:8080:80`).
- **Prevent:** in Compose, avoid fixed host ports for services that do not need
  host access; rely on the project network. See [Networking](#networking).

### 5. Published port is open but connections are refused

- **Symptom:** `docker ps` shows `0.0.0.0:8080->80/tcp`, but
  `curl localhost:8080` returns connection reset or an empty reply.
- **Check:** `docker exec <c> ss -ltn` (bound to which address?);
  `docker exec <c> curl -sv localhost:80`; `docker port <c>`.
- **Cause:** the application listens on `127.0.0.1` inside the container, so
  nothing is listening on its external interface; or the wrong container port.
- **Fix:** bind `0.0.0.0` (or `::`) inside the container — loopback is correct
  on a VM and wrong in a container.
- **Prevent:** make the bind address configurable with `0.0.0.0` as the
  container default, and smoke-test the published port after start.

### 6. Container cannot resolve another container, or has no internet

- **Symptom:** "could not resolve host: db" between running containers; or
  `ping 8.8.8.8` works while `ping example.com` fails; or neither works.
- **Check:** `docker inspect -f '{{json .NetworkSettings.Networks}}' api db`
  (same network?); `docker exec api getent hosts db`; `cat /etc/resolv.conf`
  (expect `nameserver 127.0.0.11`); `sysctl net.ipv4.ip_forward` (must be 1);
  `sudo iptables -t nat -L DOCKER -n`.
- **Cause:** name resolution fails on the **default** bridge, which has no
  embedded DNS, or across different networks. IP works but names fail = DNS
  (unreachable inherited resolver); neither works = routing or NAT (forwarding
  off, masquerade rules wiped by a firewall reload, or a `none` network).
- **Fix:** create a user-defined network and attach both containers; for egress
  set daemon resolvers in `/etc/docker/daemon.json` (`{"dns": ["1.1.1.1"]}`) or
  `sysctl -w net.ipv4.ip_forward=1`. Restarting the daemon recreates its
  iptables chains but also restarts every container without a restart policy —
  a change with downtime, not a quick retry.
- **Prevent:** never rely on the default bridge; define explicit networks in
  Compose, address services by name, persist the sysctl, and restart Docker as
  part of any firewall management change.

### 7. No space left on device on the host

- **Symptom:** builds fail and containers cannot start while application data
  itself is small.
- **Check:** `docker system df -v`; `du -sh /var/lib/docker/*`;
  `du -sh /var/lib/docker/containers/*/*-json.log | sort -h | tail`;
  `df -h /var/lib/docker && df -i /var/lib/docker`.
- **Cause:** `/var/lib/docker` filled up — most often unrotated `json-file`
  logs, build cache, dangling images from CI builds, and orphaned volumes.
- **Fix:** reclaim with filtered prunes ([Cleanup](#cleanup)), reviewing each
  list first; a blanket `docker system prune -a --volumes` also takes every
  unused image and anonymous volume, including data you meant to keep. Truncate a runaway
  log with `truncate -s 0 <logfile>` — deleting an open file frees nothing until
  the container restarts.
- **Prevent:** global log rotation in `daemon.json` ([Logging](#logging)),
  `/var/lib/docker` on its own volume, scheduled filtered prunes, disk alerts.

### 8. Every build rebuilds everything

- **Symptom:** a one-line source change triggers a full dependency install.
- **Check:** `docker history <image>`;
  `DOCKER_BUILDKIT=1 docker build --progress=plain .` and look for `CACHED`.
- **Cause:** the dependency install sits **after** the `COPY` of the whole
  source tree, so any source change invalidates it and everything below; in CI,
  a fresh runner also has no local layer cache at all.
- **Fix:** copy manifests first, install, then copy source (`COPY package*.json
  ./`, `RUN npm ci`, `COPY . .`), and import/export cache in CI with
  `buildx --cache-from/--cache-to` ([Docker in CI/CD](#docker-in-cicd)).
- **Prevent:** a `.dockerignore` that keeps `.git`, `node_modules`, and test
  output out of the context, and a pinned base image tag.

### 9. Build succeeds but the file is missing at runtime

- **Symptom:** `COPY config/ /app/config/` builds but the app cannot find the
  file; or the build fails with "file not found in build context".
- **Check:** `docker build --progress=plain .` (files transferred);
  `cat .dockerignore`; `docker run --rm <image> ls -la /app/config`;
  `docker inspect -f '{{json .Mounts}}' <c>`.
- **Cause:** paths are relative to the **build context**, not the Dockerfile, so
  `docker build -f docker/Dockerfile .` and `cd docker && docker build .` see
  different trees. Or `.dockerignore` excludes it. Or a later `COPY`, a `VOLUME`
  declaration, or a run-time mount shadows it.
- **Fix:** make the context explicit and consistent from the repository root,
  correct the ignore rules, remove the mount shadowing the baked-in path.
- **Prevent:** verify with `RUN ls -la` during development, and remember a
  volume mounted over a directory hides everything the image put there.

### 10. Permission denied on a mounted volume

- **Symptom:** the container cannot write to a bind-mounted host directory, or a
  database container fails initialising its data directory.
- **Check:** `docker exec <c> id`; `ls -ln /host/path` (numeric owner outside);
  `docker inspect -f '{{json .Mounts}}' <c>`; `getenforce`.
- **Cause:** UID and GID are numeric and are not translated across the boundary;
  on SELinux hosts the mount also needs the right label.
- **Fix:** align ownership instead of `chmod 777`, which grants every local user
  write access: `chown -R 1000:1000 /host/path` to match the container UID, or
  run with `--user "$(id -u):$(id -g)"`. Check the target path before any
  recursive `chown`. On SELinux add `:z` (shared) or `:Z` (private); `:Z`
  relabels the host directory, so **never** apply it to a shared system path.
- **Prevent:** named volumes for service state, since Docker initialises their
  ownership from the image; bind mounts only for development source and
  read-only config. See [Storage](#storage).

### 11. Data disappeared after redeploy

- **Symptom:** a database container is recreated and comes back empty.
- **Check:** `docker volume ls` (unnamed hex-ID volumes?);
  `docker inspect -f '{{json .Mounts}}' <old-c>` (empty `Name` = anonymous).
- **Cause:** the data lived in the writable layer (deleted with the container)
  or an **anonymous** volume, which survives but is not reattached, so the data
  is orphaned rather than destroyed.
- **Fix:** often recoverable — mount the orphaned volume into a temporary
  container and copy into a named one; do not prune until the copy is verified:
  `docker run --rm -v <hex-id>:/from -v pgdata:/to alpine cp -a /from/. /to/`
- **Prevent:** always mount a **named** volume for state, take backups from the
  volume rather than assuming the volume is the backup, and treat
  `docker compose down -v` as destructive.

### 12. `docker stop` always takes ten seconds

- **Symptom:** every stop pauses for the full grace period and the container
  ends with 137 rather than 143; in-flight requests are dropped.
- **Check:** `docker exec <c> ps -o pid,comm` (is PID 1 `sh` or your process?);
  `docker inspect -f '{{json .Config.Entrypoint}}' <c>`; `time docker stop <c>`.
- **Cause:** PID 1 is not receiving or not handling `SIGTERM` — the shell-form
  problem in [CMD vs ENTRYPOINT](#cmd-vs-entrypoint) — or the application only
  responds to `SIGINT` or `SIGQUIT`.
- **Fix:** exec form so the real binary is PID 1; end wrapper scripts with
  `exec "$@"`; declare another signal with `STOPSIGNAL SIGQUIT`.
- **Prevent:** exec form everywhere, a `SIGTERM` handler that drains
  connections, `--stop-timeout` slightly above the real drain time.

### 13. Zombie processes accumulate inside a container

- **Symptom:** `docker exec <c> ps aux` shows growing `<defunct>` entries;
  eventually the PID limit or process table fills.
- **Check:** `docker exec <c> ps -eo pid,ppid,stat,comm | awk '$3 ~ /Z/'`;
  `docker inspect -f '{{.HostConfig.PidsLimit}}' <c>`.
- **Cause:** PID 1 is an application that does not reap orphaned children;
  outside a container `init` does that job. See
  [Processes](linux-interview-guide.md#processes).
- **Fix:** `docker run --init` inserts a minimal init as PID 1 that reaps
  children and forwards signals; `tini` in the image does the same.
- **Prevent:** `--init` for any image whose main process spawns subprocesses,
  and `--pids-limit` so a fork bomb cannot take the host down.

### 14. Slow in the container, fast on the host

- **Symptom:** the same binary is several times slower in a container, with CPU
  capped below host capacity and periodic latency spikes.
- **Check:** `docker stats --no-stream <c>`;
  `docker inspect -f '{{.HostConfig.NanoCpus}}' <c>`;
  `docker exec <c> cat /sys/fs/cgroup/cpu.stat` (`nr_throttled` rising);
  `docker exec <c> nproc`.
- **Cause:** CPU quota throttling from `--cpus`, which stalls threads once the
  per-period quota is spent, plus runtimes sizing pools from `nproc`, which
  reports **host** cores rather than the quota.
- **Fix:** raise `--cpus` to match real demand and pass the effective CPU count
  to the runtime. `--cpu-shares` is relative priority, not a limit.
- **Prevent:** size limits from measured load, alert on cgroup throttling rather
  than CPU percentage, keep write-heavy paths on volumes.

### 15. Works on my machine, fails on the server

- **Symptom:** "exec format error" on the server, or a different version starts.
- **Check:** `docker image inspect <image> -f '{{.Os}}/{{.Architecture}}'`;
  `docker manifest inspect <image>`; `docker inspect -f '{{.Image}}' <c>` (the
  digest actually running); `uname -m` on the server.
- **Cause:** architecture mismatch, typically an `arm64` image built on Apple
  Silicon deployed to `amd64`; or tag drift, where both machines pulled
  `myapp:latest` at different times.
- **Fix:** build for the target platform or publish a multi-architecture image
  with `docker buildx build --platform linux/amd64,linux/arm64 ... --push .`
- **Prevent:** tag with the commit SHA, deploy by digest, never deploy `latest`,
  build release images in CI on the target platform.

### 16. `docker logs` returns nothing

- **Symptom:** the application is clearly working but `docker logs <c>` is
  empty.
- **Check:** `docker inspect -f '{{.HostConfig.LogConfig.Type}}' <c>`;
  `docker exec <c> ls -l /proc/1/fd/1 /proc/1/fd/2 /var/log/`.
- **Cause:** the application writes to a log file inside the container, or a
  shipping log driver is in use, for which `docker logs` is unsupported. Both
  are covered in [Logging](#logging).
- **Fix:** log to stdout, or symlink the file to `/dev/stdout` as official
  images do; with a shipping driver, read logs in the destination system.
- **Prevent:** make "log to stdout, one event per line, structured" an image
  requirement.

### 17. A secret was baked into an image

- **Symptom:** a scan finds an API key inside a published image even though a
  later Dockerfile line deletes the file.
- **Check:** `docker history --no-trunc <image>`;
  `docker image inspect <image> -f '{{json .Config.Env}}'`, same for
  `.Config.Labels`; `docker save <image> -o out.tar && tar -tf out.tar`.
- **Cause:** layers are additive, so a `COPY` in one layer and an `rm` in a
  later one leaves the content in the earlier layer; image configuration and
  build metadata are the second exposure route.
- **Fix:** **rotate the credential first** — the image is published and must be
  assumed compromised — then remove the affected tags from the registry and
  rebuild without the secret.
- **Prevent:** inject at run time from a secrets manager, use BuildKit secret
  mounts for build-time credentials, keep credentials out of the context with
  `.dockerignore`, run a secret scanner in the pipeline. See
  [Security practices](#security-practices).

### 18. Cannot debug a distroless or scratch container

- **Symptom:** `docker exec -it <c> sh` fails with "executable file not found";
  no shell, `ps`, or `curl` in the image.
- **Check:** confirm the image is minimal and the container is still running — a
  stopped container cannot be `exec`ed into whatever the image.
- **Cause:** minimal images contain only the application binary; that is the
  security benefit and the debugging cost.
- **Fix:** attach a debug container sharing the target's namespaces:
  `docker run -it --rm --pid=container:<c> --network=container:<c> --cap-add=SYS_PTRACE nicolaka/netshoot`.
  `SYS_PTRACE` lets it read the target's memory and system calls, so use it only
  while investigating and never add it to the workload itself. For an exited
  container extract state instead: `docker logs`, `docker cp <c>:/path ./`,
  `docker diff <c>`, or `docker commit <c> debug-image`.
- **Prevent:** keep minimal runtime images and standardise on a sidecar debug
  image, so nobody adds a shell and package manager to production images.

### 19. Cannot connect to the Docker daemon

- **Symptom:** `Cannot connect to the Docker daemon at
  unix:///var/run/docker.sock. Is the docker daemon running?`
- **Check:** `systemctl status docker`; `id -nG "$USER" | grep -w docker`;
  `echo "$DOCKER_HOST"; docker context ls`; `journalctl -u docker.service -n 50`.
- **Cause:** the daemon is not running, the user is not in the `docker` group,
  or `DOCKER_HOST` points at an unreachable or stale remote context.
- **Fix:** start the service, add the user to the `docker` group and start a new
  login session, or `docker context use default`.
- **Prevent:** grant `docker` group membership deliberately — it is equivalent
  to root on the host — and prefer rootless Docker or a remote builder for
  untrusted users. See [Architecture and isolation](#architecture-and-isolation).
