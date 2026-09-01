# Kubernetes Interview Study Guide

This file holds the core interview explanations for Kubernetes. Procedural lab
recipes are kept in separate files so that conceptual answers and hands-on
command sequences do not drift apart or contradict each other.

## Contents

- [Architecture](#architecture): control-plane flow, etcd quorum, HA design, and
  cluster interfaces.
- [Component failures and troubleshooting](#component-failures-and-troubleshooting):
  failure impact, diagnosis, certificate expiry, live debugging, and recovery.
- [Scheduling and autoscaling](#scheduling-and-autoscaling): placement, taints,
  resources, QoS, quotas, eviction, and autoscalers.
- [Networking](#networking): Pod networking, Services, traffic policies, DNS,
  exposure, and NetworkPolicy.
- [Configuration and storage](#configuration-and-storage): ConfigMaps, PV/PVC,
  StorageClasses, StatefulSets, and databases.
- [Security](#security): API access, Pod hardening, Secrets, supply chain,
  nodes, and audit.
- [Upgrades and maintenance](#upgrades-and-maintenance): version planning,
  drain, disruption budgets, control-plane certificates, and node operations.
- [Workloads and extensibility](#workloads-and-extensibility): controllers,
  Jobs, lifecycle, probes, APIs, operators, admission, GitOps, and rollouts.
- [Helm](#helm): charts, values, release operations, validation, CRDs, and hooks.
- [Companion files](#companion-files): procedural material kept separate.
- [Recommended interview-answer structure](#recommended-interview-answer-structure).

## Architecture

### How does the control plane work?

Kubernetes is a declarative, reconciliation-based system:

1. A client sends a request to `kube-apiserver`.
2. The API server authenticates, authorizes, validates, and admits the request.
3. The API server persists desired state in etcd.
4. Controllers compare desired and observed state and create corrective changes.
5. The scheduler assigns unscheduled Pods to suitable nodes.
6. Each node's kubelet asks the container runtime to run assigned containers.

The API server is the control plane's front door and the only core component
that directly accesses etcd. Components watch the API instead of calling each
other directly.

**Practical significance:** Creating a Deployment does not directly create
containers. Controllers create a ReplicaSet and Pods, the scheduler binds the
Pods, and kubelets run them.

### Core components

| Location | Component | Responsibility |
| --- | --- | --- |
| Control plane | `kube-apiserver` | Serves the API and enforces API policy |
| Control plane | etcd | Stores durable cluster state |
| Control plane | `kube-scheduler` | Selects nodes for unscheduled Pods |
| Control plane | `kube-controller-manager` | Runs core reconciliation controllers |
| Control plane | `cloud-controller-manager` | Integrates supported cloud APIs |
| Every node | kubelet | Reconciles assigned Pod specs with containers |
| Every node | container runtime | Manages images and containers through CRI |
| Commonly every node | `kube-proxy` or replacement | Implements Service forwarding |
| Cluster add-on | CNI plugin | Configures Pod networking |
| Cluster add-on | CoreDNS | Provides cluster DNS and service discovery |

### How does etcd provide consistency?

etcd uses Raft consensus and requires a majority quorum:

`quorum = floor(N / 2) + 1`

| Members | Quorum | Failures tolerated |
| ---: | ---: | ---: |
| 1 | 1 | 0 |
| 3 | 2 | 1 |
| 5 | 3 | 2 |

An odd member count normally provides the best fault tolerance for the cost.
Losing quorum prevents normal writes and linearizable reads. Existing workloads
may continue, but the control plane cannot reliably change state. Quorum does
not replace regular, tested snapshots.

### How do you design a highly available cluster?

- Put multiple API servers behind a health-checked load balancer.
- Run three or five etcd members on fast, low-latency, durable storage.
- Run multiple schedulers and controller managers with leader election.
- Spread control-plane and worker nodes across failure domains.
- Keep spare capacity and multiple replicas of critical workloads.
- Use topology spread constraints, zone-aware storage, and multi-zone traffic.
- Back up etcd and test restoration.

A common three-zone design places one control-plane/etcd member in each zone.
It can survive one zone loss while retaining etcd quorum. Node distribution
alone is insufficient if every application replica or volume remains in one
zone.

### Single versus multiple control-plane nodes

| Design | Appropriate use | Main trade-off |
| --- | --- | --- |
| Single control plane | Learning and disposable development | Simple, but one host failure stops cluster management |
| Multiple control planes | Production and availability-sensitive systems | More complex, but removes a host-level control-plane SPOF |

Existing Pods do not need the API server to keep their processes running.
Scheduling, scaling, reconciliation, status updates, and API operations do.

### What are CSI, CRI, and CNI?

- **CSI (Container Storage Interface):** lets storage drivers implement volume
  provisioning, attachment, mounting, and snapshots.
- **CRI (Container Runtime Interface):** lets kubelet manage runtimes such as
  containerd and CRI-O.
- **CNI (Container Network Interface):** defines how plugins configure Pod
  interfaces, addresses, and routes.

A specification defines the contract; a plugin or driver implements it.

## Component failures and troubleshooting

Use the pattern **symptom -> scope -> evidence -> recovery -> prevention**.
Avoid restarting components before collecting logs and events unless service
restoration is more urgent than diagnosis.

### API server unavailable

**Impact:** `kubectl` and API requests fail; nodes cannot report status; new
objects, scheduling decisions, and controller updates cannot be persisted.
Existing containers and most data-plane forwarding usually continue.

**Check:** API load-balancer health, API server logs and health endpoints,
certificates, CPU/memory, and connectivity to etcd.

**Recover:** restore etcd connectivity or certificates, restart the failed
instance, and keep healthy API servers behind the load balancer.

### etcd loses quorum or data

**Impact:** cluster-state writes fail and the API server may return errors.
Existing workloads continue temporarily, but cannot be reliably changed or
self-healed.

**Check:** member health, endpoint status, disk latency/capacity, peer
connectivity, and alarms for corruption.

**Recover:** repair failed members while quorum exists. For corruption or total
loss, stop writes and restore a known-good snapshot using the procedure for the
installed etcd version. Do not independently restore members into one cluster.

**Prevent:** use an odd member count, dedicated low-latency storage, TLS,
monitoring, and tested snapshots.

### Scheduler unavailable

**Impact:** already-bound Pods and existing workloads are unaffected; new Pods
remain `Pending` with no `.spec.nodeName`.

**Check:** scheduler logs, leader election, API connectivity, RBAC, and scheduler
configuration.

**Recover:** restore the process or configuration. Run redundant instances with
leader election.

### Controller manager unavailable

**Impact:** existing processes run, but reconciliation stops. ReplicaSets stop
replacing Pods, Jobs and node lifecycle handling stall, and controller-driven
scaling stops.

**Check:** controller-manager logs, leader election, API connectivity, RBAC, and
work-queue/reconciliation metrics.

**Recover:** restore the process and verify controller queues converge. Run
redundant instances with leader election.

### Kubelet or node failure

**Impact:** the node becomes `NotReady`; its Pods may be unreachable. After node
lifecycle tolerations expire, controllers can replace managed Pods elsewhere.
Pods on the failed node are not live-migrated.

**Check:** node conditions and events, kubelet and runtime status, disk/memory
pressure, networking, and certificates.

**Recover:** repair kubelet/runtime/networking, or cordon, drain when possible,
and replace the node. A hard-failed node may require workload-specific fencing
before force deletion, especially with attached storage.

### CNI, Service forwarding, or DNS failure

| Symptom | Likely area | First checks |
| --- | --- | --- |
| Pod IPs cannot communicate | CNI/routes/policy | CNI Pods and logs, routes, NetworkPolicies |
| Service IP fails but Pod IP works | `kube-proxy` or eBPF Service implementation | EndpointSlices, node rules, agent logs |
| Names fail but direct IP works | CoreDNS | DNS Pods, Service/EndpointSlices, `resolv.conf`, upstream DNS |

Do not flush production iptables rules blindly: rules may belong to Kubernetes,
the CNI, firewalls, or other host services. The step-by-step network bisection
is in [Network troubleshooting](#network-troubleshooting).

### Common workload symptoms

| Symptom | Common causes | Useful evidence |
| --- | --- | --- |
| `CrashLoopBackOff` | App exits, failed liveness probe, bad config, OOM | `describe`, current and `--previous` logs |
| `Pending` | No fitting node, untolerated taint, unbound PVC | Pod events and scheduler messages |
| `OOMKilled` | Container exceeded cgroup memory limit | Last state, exit code 137, metrics |
| `ImagePullBackOff` | Bad image/tag, auth, DNS, or registry | Pod events and runtime logs |
| Service 503/no endpoints | Selector mismatch or Pods not ready | Service selector and EndpointSlices |
| `NodeNotReady` | Kubelet, runtime, network, or host pressure | Node conditions and system logs |

### Certificate expiry: which TLS is broken?

Two unrelated certificate systems are commonly confused. Identify which one is
failing before touching anything.

| Layer | Who it serves | Typical symptom | Where certificates live |
| --- | --- | --- | --- |
| Ingress or application TLS | External clients of an app | Browser warning, failed HTTPS handshake to the app hostname | Kubernetes TLS Secret, usually issued by cert-manager or a cloud load balancer |
| Cluster PKI | API server, kubelets, etcd, controllers | `kubectl` reports `x509: certificate has expired`, nodes go `NotReady` | Node filesystem under `/etc/kubernetes/pki` |

An expired Ingress certificate never breaks `kubectl`, and renewing an Ingress
Secret never fixes cluster PKI.

#### Ingress or application TLS

**Check:** confirm where TLS terminates, then inspect the served certificate and
the issuing resources:

```bash
openssl s_client -connect app.example.com:443 -servername app.example.com </dev/null \
  | openssl x509 -noout -subject -issuer -dates
kubectl describe ingress <name> -n <namespace>
kubectl describe certificate <name> -n <namespace>
kubectl get certificaterequest,order,challenge -n <namespace>
```

**Recover:** fix the failing ACME challenge, issuer configuration, DNS record, or
load-balancer certificate mapping. For an emergency replacement, update the TLS
Secret referenced by the Ingress and confirm the controller reloaded it.

**Prevent:** alert well before expiry, monitor `Certificate` readiness, and
re-test the challenge path after DNS, firewall, or Ingress changes.

#### Control-plane certificates on kubeadm clusters

**Impact:** API requests fail authentication, kubelets cannot report status, and
the cluster becomes unmanageable while containers keep running.

**Check:** run this on a control-plane node, because the API may be unreachable:

```bash
sudo kubeadm certs check-expiration
sudo openssl x509 -noout -subject -dates -in /etc/kubernetes/pki/apiserver.crt
```

**Recover:** back up `/etc/kubernetes/pki` and the kubeconfig files, renew with
`kubeadm certs renew`, restart the control-plane static Pods, and redistribute
regenerated kubeconfigs. The full procedure and its cautions are in
[Control-plane certificate maintenance](#control-plane-certificate-maintenance).

**Prevent:** upgrade at least annually so renewal happens during upgrades, and
alert on remaining certificate lifetime from each control-plane node.

### Investigation sequence

```bash
kubectl get pods -A -o wide
kubectl describe <kind> <name> -n <namespace>
kubectl logs <pod> -n <namespace> --all-containers
kubectl logs <pod> -n <namespace> --previous
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

Then inspect the owning controller, node conditions, EndpointSlices, storage,
and component logs. Events are transient, so collect them early.

### Debugging with ephemeral containers

When an image has no shell, or a Pod crashes before you can exec into it,
`kubectl debug` attaches tooling without rebuilding the image:

```bash
# Add an ephemeral container that shares the target container's process namespace.
kubectl debug -it pod/web -n default --image=busybox:1.36 --target=app

# Copy the Pod and override the entrypoint when the original crashes on startup.
kubectl debug pod/web -n default --copy-to=web-debug --container=app \
  --image=busybox:1.36 -it -- sh

# Open a shell on the node itself.
kubectl debug node/node01 -it --image=busybox:1.36
```

Ephemeral containers cannot be removed from a running Pod, are never restarted,
and cannot declare probes or resources. `--target` requires runtime support for
process-namespace sharing. Node debugging creates a highly privileged Pod with
host access, so restrict who may use it and treat the session as sensitive.

### Availability-zone loss

A sound design retains API and etcd quorum, has capacity in surviving zones,
spreads workload replicas, and uses storage that can recover or fail over.
PodDisruptionBudgets limit voluntary disruption; they do not guarantee
availability during involuntary zone failure.

## Scheduling and autoscaling

### How does the scheduler place a Pod?

1. **Filter:** remove nodes that violate resources, selectors/affinity, taints,
   topology, volume, or port constraints.
2. **Score:** rank feasible nodes using configured scoring plugins.
3. **Bind:** write the selected node to the Pod binding.

The scheduler uses resource **requests**, not current utilization, for normal
fit decisions. A `Pending` Pod's events usually identify the failed filters.

### Placement controls

| Mechanism | Meaning | Typical use |
| --- | --- | --- |
| `nodeSelector` | Required exact label matches | Simple hardware placement |
| Required node affinity | Expressive hard node constraint | Specific zones or architectures |
| Preferred node affinity | Weighted preference | Favor a node group with fallback |
| Pod affinity | Co-locate with matching Pods | Latency-sensitive peers |
| Pod anti-affinity | Separate from matching Pods | Replica fault isolation |
| Topology spread | Bound skew across domains | Even node/zone distribution |
| `nodeName` | Bypasses scheduler and targets one node | Exceptional low-level use |
| Taint/toleration | Node repels Pods lacking a match | Dedicated or impaired nodes |

A toleration only permits scheduling; it does not attract a Pod. For dedicated
nodes, combine a taint with node affinity or a selector.

### What are the taint effects?

| Effect | Existing Pods | New Pods without matching toleration |
| --- | --- | --- |
| `NoSchedule` | Remain running | Not scheduled |
| `PreferNoSchedule` | Remain running | Avoided when feasible; not guaranteed |
| `NoExecute` | Evicted unless tolerated | Not scheduled |

`tolerationSeconds` on a matching `NoExecute` toleration delays eviction. With
no value, the Pod tolerates the taint indefinitely. DaemonSet Pods receive some
system tolerations automatically, including for node readiness and
unreachability.

```bash
kubectl taint node node01 workload=gpu:NoSchedule
kubectl taint node node01 workload=gpu:NoSchedule-
```

### Requests, limits, and QoS

- A **request** informs scheduling and is the baseline used for resource
  accounting.
- A **limit** is runtime enforcement. CPU over a limit is throttled; memory over
  a limit can cause an OOM kill.
- Node memory or disk pressure can trigger kubelet eviction. Pod priority,
  requests relative to usage, and QoS influence eviction order; QoS alone does
  not fully determine it.

| QoS class | Conditions |
| --- | --- |
| Guaranteed | Every container has CPU and memory requests and limits, and each request equals its limit |
| Burstable | At least one request or limit exists, but Guaranteed conditions are not met |
| BestEffort | No container has CPU or memory requests or limits |

A frequently missed detail: if a container sets a limit but no request, the
request defaults to the limit. Specifying only CPU and memory limits therefore
produces a Guaranteed Pod that reserves the full limit for scheduling, which
consumes far more allocatable capacity than intended. A LimitRange can also
inject defaults, so confirm the effective values on a created Pod:

```bash
kubectl get pod web -o jsonpath='{.spec.containers[*].resources}{"\n"}'
kubectl get pod web -o jsonpath='{.status.qosClass}{"\n"}'
```

CPU is compressible: contention mainly causes throttling. Memory is not
compressible: pressure leads to reclaim, eviction, or OOM termination.

### ResourceQuota and LimitRange

A ResourceQuota caps aggregate consumption in a namespace. A LimitRange
constrains and defaults individual Pods and containers.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    pods: "100"
    persistentvolumeclaims: "20"
    requests.storage: 500Gi
---
apiVersion: v1
kind: LimitRange
metadata:
  name: container-defaults
  namespace: team-a
spec:
  limits:
    - type: Container
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      default:
        cpu: 500m
        memory: 512Mi
      max:
        cpu: "4"
        memory: 8Gi
```

Once a quota constrains a compute resource, every new Pod in that namespace must
declare the matching requests and limits or admission rejects it. Pairing the
quota with a LimitRange that supplies defaults prevents that failure for teams
that do not set resources explicitly.

Quotas apply at admission to new objects, so lowering a quota does not evict
existing workloads; it only blocks further growth. Inspect usage with:

```bash
kubectl describe resourcequota team-quota -n team-a
```

### Pod priority and preemption

A `PriorityClass` gives Pods an integer priority. If a high-priority Pod cannot
schedule, preemption may nominate a node and evict lower-priority Pods to make
room. Priority does not override hard constraints, and a PodDisruptionBudget is
considered on a best-effort basis during preemption.

### Eviction versus deletion

- **Kubelet eviction:** reacts to node pressure such as low memory or disk.
- **Node-controller eviction:** replaces managed workloads after a node remains
  unreachable and Pod tolerations expire.
- **API eviction:** used by `kubectl drain`; honors PodDisruptionBudgets.
- **Preemption:** scheduler removes lower-priority Pods for a higher-priority Pod.

Drain behavior and its opt-in flags are covered in
[Cordon, drain, and uncordon](#cordon-drain-and-uncordon).

### HPA, VPA, and node autoscaling

| Autoscaler | Changes | Trigger |
| --- | --- | --- |
| HPA | Replica count | Resource, custom, or external metrics |
| VPA | Resource requests, and optionally Pods | Historical/current usage |
| Cluster/node autoscaler | Node count | Unschedulable Pods and removable capacity |

HPA commonly suits scalable stateless workloads. VPA helps right-size requests
but some update modes restart Pods. Avoid having HPA and VPA both control CPU or
memory for the same workload; using HPA on custom metrics with VPA on resources
can be valid.

The node autoscaler reacts primarily to Pods that cannot schedule, not simply to
high node CPU. Scale-down considers whether Pods can move and whether disruption
constraints permit removal.

### Scheduling for high availability

Prefer topology spread constraints for balanced replicas across hosts and
zones. Use anti-affinity when replicas must not share a domain, while accounting
for the risk that strict rules can leave Pods pending. Ensure the topology label
exists on all candidate nodes and align storage topology with Pod placement.

## Networking

### What does the Kubernetes network model require?

Each Pod receives an IP. In the standard model, Pods can communicate with other
Pods across nodes without application-visible NAT, and agents on a node can
reach that node's Pods. A CNI implementation supplies interfaces, addresses,
routes or overlays, and often NetworkPolicy enforcement.

Common dataplanes use overlays such as VXLAN/Geneve, routed networking such as
BGP, or eBPF. CNI is the specification; Calico, Cilium, and Flannel are example
implementations with different capabilities.

### How do Services route traffic?

A Service provides a stable virtual IP and port over a changing set of ready
backends. Its selector normally produces EndpointSlices. On each node,
`kube-proxy` programs iptables, IPVS, or nftables rules; some CNIs replace this
with eBPF.

`kube-proxy` does not proxy every packet in user space. It installs forwarding
state. It is distinct from `kubectl proxy`, which runs for a client and exposes
an authenticated local HTTP proxy to the API server.

### iptables versus IPVS

| Mode | Strength | Trade-off |
| --- | --- | --- |
| iptables | Mature and broadly available | Large rule sets can be slower to update and inspect |
| IPVS | Efficient lookup and multiple balancing algorithms | Requires IPVS kernel support and still uses some iptables |

IPVS is not universally better. Current Kubernetes also offers an nftables mode,
and eBPF dataplanes can replace `kube-proxy` entirely. Choose based on the
supported platform, cluster scale, observability, and operational maturity.

### Service exposure

| API | Purpose |
| --- | --- |
| `ClusterIP` | Cluster-internal stable virtual IP |
| `NodePort` | Opens the same high port on node addresses |
| `LoadBalancer` | Asks an integration to provision or configure an external load balancer |
| `ExternalName` | Returns a CNAME to an external DNS name |
| Ingress | HTTP(S) host/path routing through an Ingress controller |
| Gateway API | Role-oriented, extensible L4/L7 routing APIs |

Ingress is not a Service type and does nothing without a controller. A
`LoadBalancer` Service often builds on NodePort, although implementations may
route directly to Pods.

An `ExternalName` Service has no selector, endpoints, or proxying:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: payments-api
spec:
  type: ExternalName
  externalName: payments.vendor.example.com
```

Because it works purely at DNS level, it cannot target an IP literal, does not
rewrite ports, and leaves TLS server-name validation against the external name.
To keep a stable in-cluster name in front of an IP address, create a selectorless
Service with a manually managed EndpointSlice instead.

### externalTrafficPolicy and internalTrafficPolicy

| Setting | Behavior | Trade-off |
| --- | --- | --- |
| `externalTrafficPolicy: Cluster` (default) | Any node forwards to endpoints on any node | Even spreading, but SNAT usually hides the client source IP |
| `externalTrafficPolicy: Local` | A node forwards only to its local endpoints | Preserves the client source IP, but traffic follows Pod distribution |
| `internalTrafficPolicy: Local` | In-cluster traffic uses same-node endpoints only | Lower cross-node traffic, but fails when no local endpoint exists |

With `Local`, nodes that have no ready endpoint fail the load-balancer health
check so external traffic stops being sent to them. Combine it with a DaemonSet
or topology spread so every eligible node has a backend, otherwise capacity
becomes uneven.

### NodeLocal DNSCache

NodeLocal DNSCache runs a DNS cache as a DaemonSet on every node. Pods query the
node-local cache, which answers hits directly and forwards misses to CoreDNS,
usually over TCP.

It reduces DNS latency, lowers CoreDNS load, and avoids UDP conntrack races that
cause intermittent resolution timeouts in large clusters. Deployment must match
the cluster DNS Service address and the local link address used by the manifest,
so treat it as a cluster-level rollout that is verified per node rather than a
per-application change.

### How does DNS service discovery work?

CoreDNS watches the Kubernetes API and serves records such as:

- Service: `<service>.<namespace>.svc.cluster.local`
- Short same-namespace name: `<service>`
- Cross-namespace name: `<service>.<namespace>`

A normal Service name resolves to its ClusterIP. A headless Service
(`clusterIP: None`) resolves to selected Pod addresses, enabling clients to
discover individual members. Named Service ports also receive SRV records.

Kubelet writes each Pod's `/etc/resolv.conf`. Important `dnsPolicy` values are:

- `ClusterFirst`: use cluster DNS, forwarding non-cluster queries upstream.
- `ClusterFirstWithHostNet`: cluster-first behavior for `hostNetwork` Pods.
- `Default`: inherit node resolver settings.
- `None`: use only explicit `dnsConfig`.

The API server is discoverable in-cluster through
`kubernetes.default.svc`. Its ClusterIP is installation-specific; query the
Service instead of assuming it is the first address in the Service CIDR:

```bash
kubectl get service kubernetes -n default
```

### What is a headless Service?

It has no virtual ClusterIP and no Service-level load balancing. DNS returns
backend addresses directly. StatefulSets often use one to give each Pod stable
DNS such as:

`web-0.nginx.default.svc.cluster.local`

Headless Services provide discovery, not persistence; StatefulSet identity and
PVCs provide stable workload identity and storage.

### NetworkPolicy

NetworkPolicy is additive and only works when the network plugin enforces it.
A Pod is non-isolated for a direction until selected by a policy for that
direction. Once isolated, traffic must be allowed by at least one applicable
policy. Selectors are combined as follows:

- entries in one `from` or `to` item are ANDed;
- separate list items are ORed;
- ingress rules govern incoming traffic and egress rules govern outgoing traffic.

An empty rule is not a deny rule. `ingress: [{}]` matches every source and
`egress: [{}]` matches every destination, so either one re-opens the direction
it appears in. To deny a direction, list it in `policyTypes` and provide no rule
for it.

Start with namespace-scoped default-deny ingress and egress, then explicitly
allow application flows, DNS, monitoring, and required external endpoints.
A worked policy is in [kubernetes-cka-labs.md](kubernetes-cka-labs.md). The wider isolation picture,
including what NetworkPolicy does not cover, is in
[Network isolation](#network-isolation).

### Session affinity and advanced routing

- A Service can use `sessionAffinity: ClientIP` for basic source-IP affinity.
  NAT or proxies can collapse many users onto one apparent IP.
- An Ingress controller may implement cookie affinity for HTTP applications.
- A service mesh or Gateway implementation can route by headers for canaries or
  user segments.

Prefer stateless applications and external session storage where practical;
stickiness can hide uneven load and complicate failover.

### Network troubleshooting

1. Test DNS name, Service IP, and Pod IP separately.
2. Verify selectors and EndpointSlices.
3. Check readiness; unready Pods are normally excluded from Service backends.
4. Inspect NetworkPolicies in both source and destination namespaces.
5. Inspect CNI and Service-dataplane agent logs and node routes/rules.
6. For external traffic, verify load-balancer health checks, Ingress/Gateway
   status, TLS, source-IP policy, and cloud firewall rules.

## Configuration and storage

### ConfigMap versus Secret

| Object | Intended data | Default API representation |
| --- | --- | --- |
| ConfigMap | Non-sensitive configuration | Plain strings or binary data |
| Secret | Credentials, keys, tokens, certificates | Base64-encoded values |

Base64 is encoding, not encryption. Protection controls are covered in
[Protecting Secrets and etcd](#protecting-secrets-and-etcd), and creation and
consumption recipes are in [kubernetes-secrets-recipes.md](kubernetes-secrets-recipes.md).

### How do applications consume configuration?

ConfigMaps and Secrets can be exposed as:

- environment variables;
- command arguments populated from environment variables;
- projected volume files;
- individual keys through `subPath` mounts.

Environment values do not update in a running process when the source changes.
Projected volume files update eventually, but an application must reload them.
`subPath` mounts do not receive updates. A common rollout pattern adds a
configuration checksum to the Pod template so a config change creates new Pods.

### PV, PVC, StorageClass, and CSI

| Object | Responsibility |
| --- | --- |
| PersistentVolume (PV) | Cluster storage resource and lifecycle record |
| PersistentVolumeClaim (PVC) | Namespaced request for storage |
| StorageClass | Provisioner, parameters, binding mode, and reclaim policy |
| CSI driver | Implements storage operations for a provider |

Typical dynamic provisioning flow:

1. A workload creates a PVC.
2. A matching StorageClass and CSI provisioner create a PV.
3. The PVC binds to the PV.
4. Kubelet and the CSI driver attach and mount it where required.

`WaitForFirstConsumer` delays provisioning/binding until scheduling so the
volume can be created in a compatible zone.

### What happens when a Pod or PVC is deleted?

A PVC normally outlives a Pod. Deleting a Pod does not delete its PVC.
StatefulSet `volumeClaimTemplates` also create PVCs with stable ordinal-based
names; retention behavior can be configured by the StatefulSet PVC retention
policy.

When a PVC is deleted:

- `Delete` reclaim policy normally deletes the PV and backing storage;
- `Retain` leaves the PV in `Released` for manual recovery and cleanup.

`Recycle` is deprecated and should not be used. PV/PVC protection finalizers
delay deletion while resources are in use; they do not change the reclaim
policy.

### Access modes and volume modes

- `ReadWriteOnce` (RWO): read-write by nodes on one node at a time; multiple Pods
  on that node may still mount it.
- `ReadOnlyMany` (ROX): read-only by many nodes.
- `ReadWriteMany` (RWX): read-write by many nodes.
- `ReadWriteOncePod` (RWOP): read-write by one Pod cluster-wide when supported.
- `Filesystem`: mounted filesystem.
- `Block`: raw block device.

Access modes describe requested/provider capability; they are not a general
authorization mechanism.

### StatefulSet internals

StatefulSets provide:

- stable ordinal names such as `db-0`;
- stable network identity, commonly through a headless Service;
- one PVC per ordinal when using `volumeClaimTemplates`;
- ordered rollout and scaling by default;
- optional parallel Pod management.

The Pods are replaceable, but their identities are not interchangeable. Use
StatefulSets for systems that depend on stable membership or storage, not merely
because an application writes files.

### Database workloads

- Confirm the database supports the storage latency, failure, and attachment
  semantics of the platform.
- Spread replicas across zones while keeping volumes schedulable.
- Use readiness and startup probes; avoid liveness probes that create unsafe
  restart loops.
- Define disruption budgets and graceful termination.
- Back up application-consistently and test restore and failover.
- Consider a mature operator or managed database when it reduces operational
  risk.

Persistent storage is not a backup, and multiple database Pods are not
automatically a consistent HA database.

### Ephemeral volumes

`emptyDir` exists for the lifetime of a Pod and is deleted when the Pod is
removed from its node. It is useful for scratch space or sharing files between
containers, but not durable application data. It can use node disk or memory
(`medium: Memory`) and counts toward relevant resource limits and pressure.

## Security

Think in layers: supply chain, API access, workload isolation, network, secrets,
node security, and audit/response. RBAC alone is not cluster security.

### Authentication, authorization, and admission

1. **Authentication** establishes identity, for example OIDC users,
   certificates, or ServiceAccount tokens.
2. **Authorization** decides whether that identity may perform the request.
   RBAC is the common authorizer.
3. **Admission** validates or mutates an authorized request before persistence.

TLS protects API traffic, but it does not grant permission.

### How does RBAC work?

- `Role`: permissions for namespaced resources within one namespace.
- `ClusterRole`: permissions for cluster-scoped resources or a reusable set of
  namespaced permissions.
- `RoleBinding`: grants a Role or ClusterRole within one namespace.
- `ClusterRoleBinding`: grants a ClusterRole cluster-wide.

Bindings target users, groups, or ServiceAccounts. RBAC permissions are
additive; there are no deny rules.

Apply least privilege: avoid wildcards, restrict Secret access and
`pods/exec`, separate human and workload identities, and periodically review
bindings. The ability to create or patch a Pod may allow an identity to use a
more privileged ServiceAccount or mount accessible Secrets, so evaluate
privilege-escalation paths rather than verbs in isolation.

```bash
kubectl auth can-i create deployments -n dev --as alice
kubectl auth can-i --list -n dev --as system:serviceaccount:dev:app
```

### ServiceAccounts

A ServiceAccount is a namespaced workload identity. Modern clusters inject a
short-lived, audience-bound projected token when needed. Set
`automountServiceAccountToken: false` for Pods that do not call the API, and
bind dedicated ServiceAccounts rather than using the namespace's `default`
account.

### Pod Security Standards and Admission

The standards are cumulative:

| Profile | Intent |
| --- | --- |
| Privileged | Unrestricted; suitable only for explicitly trusted system workloads |
| Baseline | Prevent known privilege escalations with broad compatibility |
| Restricted | Current hardening practices for ordinary workloads |

Pod Security Admission enforces these profiles through namespace labels in
`enforce`, `audit`, and `warn` modes. Roll out with audit/warn first and use
version-pinned labels where predictable upgrades matter. It does not provide
arbitrary policy logic; use a validating admission policy or policy engine for
organization-specific requirements. Webhook-based admission trade-offs are in
[Mutating and validating admission](#mutating-and-validating-admission).

### Workload hardening

```yaml
securityContext:
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault
containers:
  - name: app
    image: registry.example.com/app@sha256:replace-me
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
          - ALL
      readOnlyRootFilesystem: true
```

Also:

- avoid privileged containers, host namespaces, `hostPath`, and host ports;
- set a known non-root UID/GID when the image supports it;
- add only the specific Linux capability required;
- use read-only mounts and a writable `emptyDir` only where needed;
- set resource requests/limits to reduce noisy-neighbor and denial-of-service risk;
- use RuntimeClass sandboxing for higher-risk workloads where supported.

`runAsNonRoot` alone is incomplete if the image identity is ambiguous; test the
image and set `runAsUser` where appropriate.

### Network isolation

Use a CNI that enforces NetworkPolicy. Establish default-deny ingress and egress,
then allow only required service, DNS, monitoring, and external traffic; the rule
semantics are in [NetworkPolicy](#networkpolicy). NetworkPolicy is namespaced and
additive; it does not filter node-level traffic in every implementation and is not
a replacement for cloud firewalls.

### Protecting Secrets and etcd

- Enable Kubernetes encryption at rest with a KMS provider where possible and
  rotate/re-encrypt existing data.
- Use TLS for etcd client and peer traffic and restrict network access to etcd.
- Grant Secret `get`, `list`, and `watch` sparingly; list/watch can expose all
  values in scope.
- Prefer short-lived credentials and an external secret manager with workload
  identity.
- Back up etcd encrypted, restrict backup access, and test recovery.
- Protect API audit logs because requests and responses can contain sensitive data.

Encryption at rest protects storage media and backups; it does not protect a
Secret from an identity authorized to read it or from a compromised Pod that
receives it.

### Supply-chain and node security

- Use minimal maintained images, pin digests, scan continuously, and verify
  signatures/provenance at admission.
- Keep Kubernetes, the host OS, runtime, and CNI patched.
- Restrict registry access and image pull credentials.
- Harden kubelet access, disable anonymous access, and use authorization.
- Limit SSH, isolate control-plane/etcd hosts, and protect cloud instance metadata.
- Treat a compromised node as compromise of workloads and credentials on it;
  cordon, isolate, rotate credentials, rebuild, and investigate.

### Audit and detection

Enable an API audit policy that records security-relevant metadata without
unnecessarily logging Secret bodies. Monitor privileged Pod creation, RBAC
changes, exec/attach, Secret access, admission failures, unusual API clients,
and node/runtime alerts. Send logs to tamper-resistant remote storage and
practice credential rotation and incident recovery.

## Upgrades and maintenance

### How do you plan a safe upgrade?

1. Read release notes and the version-skew policy for the exact distribution.
2. Inventory deprecated APIs, admission integrations, CRDs, CNIs, CSIs,
   operators, and client tooling.
3. Confirm backups and perform a test restore, especially for etcd and
   application data.
4. Check control-plane, node, workload, storage, and network health.
5. Validate the target release in a representative non-production environment.
6. Upgrade one supported minor version at a time when required.
7. Upgrade control-plane instances first, then worker nodes in small batches.
8. Verify API health, controllers, nodes, DNS/networking, storage, and
   application service-level indicators after each batch.
9. Retain a tested rollback or recovery plan. An etcd restore is disaster
   recovery, not a routine downgrade mechanism.

Managed services and kubeadm differ, so use the vendor's procedure rather than
assuming component commands are portable.

### Control-plane and worker order

Maintain a supported skew among `kube-apiserver`, kubelet,
`kube-controller-manager`, `kube-scheduler`, and `kubectl`. The API server is
normally upgraded before kubelets. Upgrade redundant control-plane instances
sequentially to retain API availability, then rotate worker pools or upgrade
workers in controlled batches.

Do not manually upgrade etcd merely because Kubernetes is being upgraded. Use
the distribution's supported etcd version and process.

### Cordon, drain, and uncordon

- `cordon` marks a node unschedulable; existing Pods remain.
- `drain` uses the eviction API to remove evictable Pods and cordons the node.
- `uncordon` makes the node schedulable again.

Start with the safe form. `--ignore-daemonsets` is required on nearly every real
cluster because DaemonSet Pods are managed per node and are never evicted:

```bash
kubectl cordon node01
kubectl drain node01 --ignore-daemonsets --timeout=5m
# Perform maintenance and verify kubelet/runtime health.
kubectl uncordon node01
```

If the drain stalls, read the message before adding flags. Each override trades
away a protection:

| Flag | Effect | Risk accepted |
| --- | --- | --- |
| `--ignore-daemonsets` | Proceeds despite DaemonSet Pods, which stay running | None in normal use; node agents remain on the node |
| `--delete-emptydir-data` | Allows evicting Pods with `emptyDir` volumes | That scratch data is destroyed permanently |
| `--force` | Deletes Pods with no managing controller | Those Pods are not recreated anywhere |
| `--disable-eviction` | Deletes Pods directly, bypassing the eviction API | PodDisruptionBudgets are ignored; avoid outside emergencies |
| `--grace-period` | Overrides the Pod termination grace period | Shortening it can cut off shutdown and data flushing |

```bash
# Opt in only after confirming the affected data and Pods are expendable.
kubectl drain node01 \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --force \
  --timeout=10m
```

A blocked drain is usually correct feedback: a PodDisruptionBudget has no spare
replica, or a workload has no controller to recreate it. Fix the underlying
capacity or ownership problem rather than forcing the eviction.

### PodDisruptionBudgets

A PDB limits simultaneous **voluntary** disruptions by specifying
`minAvailable` or `maxUnavailable`. It does not protect against node crashes,
zone failures, direct Pod deletion, or all rollout behavior. A PDB with no spare
replicas can block maintenance indefinitely.

Design applications with:

- enough replicas and failure-domain spread;
- readiness probes that represent service capability;
- graceful termination and suitable termination grace periods;
- storage detach/failover behavior that fits drain timing;
- PDBs aligned with real availability requirements.

### Control-plane certificate maintenance

Cluster PKI is separate from application or Ingress TLS. kubeadm issues
control-plane client and serving certificates with a one-year lifetime, while
the cluster CA is long-lived. Telling the two layers apart during an incident is
covered in
[Certificate expiry: which TLS is broken?](#certificate-expiry-which-tls-is-broken).

`kubeadm upgrade` renews these certificates as part of the upgrade, so clusters
that are upgraded at least yearly rarely reach expiry. For a cluster that is not
being upgraded, renew explicitly:

```bash
# 1. Back up the PKI directory and the generated kubeconfig files first.
sudo cp -a /etc/kubernetes/pki "/root/pki-backup-$(date +%F)"
sudo cp -a /etc/kubernetes/*.conf "/root/kubeconfig-backup-$(date +%F)/"

# 2. Renew one certificate, or all kubeadm-managed certificates.
sudo kubeadm certs renew apiserver
sudo kubeadm certs renew all

# 3. Confirm the new dates.
sudo kubeadm certs check-expiration
```

Renewal writes new files but does not reload running components. Restart the
control-plane static Pods afterwards, commonly by moving the manifests out of
the static Pod directory and back, then verify API availability. Repeat the
process on every control-plane node.

Two cautions:

- `kubeadm certs renew all` also refreshes the embedded client certificates in
  files such as `admin.conf`, so redistribute updated kubeconfigs. A copy taken
  earlier keeps failing until it is replaced.
- Never run `kubeadm init phase certs` against a live cluster to fix expiry.
  Regenerating a CA invalidates every existing certificate and kubeconfig.

Kubelet client certificates rotate automatically when rotation is enabled;
kubelet serving certificates may require approval of the pending CSRs.

### Zero-downtime expectations

Cluster maintenance can be disruption-free only when workloads are designed
for it. Sequential node upgrades, spare capacity, topology distribution, PDBs,
and graceful shutdown reduce risk, but single-replica or non-failover stateful
applications still have downtime.

### Node maintenance checklist

1. Confirm cluster health and spare capacity.
2. Cordon and drain one node or a small safe batch.
3. Confirm replacement Pods are ready and service indicators are healthy.
4. Patch or replace the node, runtime, kubelet, and required agents.
5. Verify node conditions, versions, CNI/CSI/DaemonSets, and logs.
6. Uncordon and observe scheduling.
7. Continue only when the cluster has returned to steady state.

Replacing immutable worker nodes is often safer and more repeatable than
in-place upgrades.

## Workloads and extensibility

### Workload controllers

| Controller | Use |
| --- | --- |
| Deployment | Stateless replicas, rolling updates, and rollback |
| ReplicaSet | Maintains replica count; normally managed by a Deployment |
| StatefulSet | Stable ordinal identity, storage, and ordered lifecycle |
| DaemonSet | Runs a Pod on every eligible node |
| Job | Runs finite work to completion |
| CronJob | Creates Jobs on a schedule |

DaemonSet Pods receive several automatic tolerations so node-level agents such
as networking and logging can run where ordinary Pods may not. A DaemonSet does
not necessarily run on every node: selectors, affinity, and taints still matter.
StatefulSet storage and identity details are in
[StatefulSet internals](#statefulset-internals).

### Job and CronJob fields

| Job field | Effect |
| --- | --- |
| `completions` | Number of successful Pod completions required |
| `parallelism` | Maximum Pods running concurrently |
| `completionMode` | `NonIndexed` (default) or `Indexed` for per-index work |
| `backoffLimit` | Pod retries before the Job is marked `Failed` |
| `activeDeadlineSeconds` | Wall-clock limit; running Pods are terminated |
| `ttlSecondsAfterFinished` | Automatic cleanup after completion or failure |
| `podFailurePolicy` | Fail fast or ignore specific exit codes and conditions |
| `suspend` | Pauses or resumes Pod creation |

Job Pod templates must set `restartPolicy` to `OnFailure` or `Never`.
`backoffLimit` counts Pod failures, so a container that restarts in place under
`OnFailure` consumes retries differently than a Pod that is replaced.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: report
spec:
  completions: 5
  parallelism: 2
  backoffLimit: 3
  activeDeadlineSeconds: 1800
  ttlSecondsAfterFinished: 3600
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: report
          image: registry.example.com/report:1.4.0
```

| CronJob field | Effect |
| --- | --- |
| `schedule` | Cron expression for Job creation |
| `timeZone` | IANA zone name; otherwise the controller's time reference applies |
| `concurrencyPolicy` | `Allow`, `Forbid`, or `Replace` |
| `startingDeadlineSeconds` | How late a missed run may still start |
| `successfulJobsHistoryLimit` | Completed Jobs retained |
| `failedJobsHistoryLimit` | Failed Jobs retained |
| `suspend` | Stops creating new Jobs |

A CronJob guarantees neither exactly-once execution nor perfectly timed runs, so
Job workloads should be idempotent. If many scheduled runs are missed, the
controller stops attempting to catch up and reports the problem in events.

### Pod lifecycle

Pod phases are `Pending`, `Running`, `Succeeded`, `Failed`, and `Unknown`.
`Terminating` is a `kubectl` display state, not a Pod phase. Container states
are `Waiting`, `Running`, and `Terminated`.

The Pod `restartPolicy` is `Always`, `OnFailure`, or `Never` and applies to app
and regular init containers on the same node. Controllers replace Pods;
`restartPolicy` governs kubelet container restarts inside one Pod.

### Init containers and sidecars

Init containers run to successful completion before app containers. Use them
for bounded setup such as generating config or waiting for a dependency, not
for long-running services. They can share volumes with app containers.

Sidecar containers provide supporting behavior such as proxies or log
processing. Kubernetes supports sidecar-style init containers with
`restartPolicy: Always` on supported versions, providing lifecycle ordering.

### Probes

| Probe | Failure effect | Purpose |
| --- | --- | --- |
| Startup | Restarts container after threshold | Protect slow startup from liveness checks |
| Readiness | Removes Pod from ready endpoints | Decide whether to receive traffic |
| Liveness | Restarts container after threshold | Recover a process that cannot make progress |

Exec, HTTP, TCP, and gRPC handlers are available subject to version support.
Readiness failure does not restart a container. Poor liveness probes can amplify
an outage, so keep them independent of optional downstream dependencies.

### Lifecycle hooks and termination

`postStart` runs after container creation but is not guaranteed to run before
the entrypoint. `preStop` runs before normal Kubernetes-initiated termination
when the container is still running. The termination grace countdown begins
before `preStop`; hooks are not guaranteed during node loss, process crash, or
forced termination. Therefore, hooks must not be the only mechanism protecting
data correctness.

### Labels and annotations

Labels are indexed identifying metadata used by selectors. Annotations hold
non-identifying metadata for tools and controllers, and their values are always
strings.

| Annotation | Purpose |
| --- | --- |
| `kubernetes.io/description` | Human-readable description of the object |
| `kubernetes.io/change-cause` | Reason recorded in `kubectl rollout history` |
| `deployment.kubernetes.io/revision` | Revision tracked by the Deployment controller |
| `kubectl.kubernetes.io/default-container` | Default container for `logs` and `exec` |
| `cluster-autoscaler.kubernetes.io/safe-to-evict` | Allows or blocks autoscaler eviction |
| `helm.sh/hook` | Marks a resource as a Helm lifecycle hook |
| `helm.sh/resource-policy` | Set to `keep` to survive `helm uninstall` |

Prefer structured API fields over annotations where a field exists. Ingress
class belongs in `spec.ingressClassName`, and metrics scraping under the
Prometheus Operator belongs in `ServiceMonitor` or `PodMonitor` objects rather
than scrape annotations.

Controller-specific annotations are implementation behavior rather than portable
API guarantees, so verify them against the installed controller version.

### CRDs, controllers, and operators

A CustomResourceDefinition adds a resource type to the Kubernetes API. A
controller watches resources and reconciles desired state. An operator combines
CRDs and controllers to encode application-specific operations such as backup,
upgrade, and failover.

A CRD without a controller stores custom objects but performs no domain action.
Operators should expose status conditions, use finalizers carefully, be
idempotent, and handle upgrades and backup compatibility.

### Mutating and validating admission

- Mutating admission can default or modify an accepted request.
- Validating admission accepts or rejects the resulting object.

Use admission for guardrails such as image policy and security requirements.
Webhook outages can block API operations depending on `failurePolicy`; deploy
webhooks redundantly, scope them narrowly, set timeouts, and avoid intercepting
their own recovery resources.

### API versions

An API version is commonly `<group>/<version>`, for example `apps/v1`; core
resources use `v1`. Stability levels are:

- `v1alpha1`: experimental and may change or disappear without compatibility;
- `v1beta1`: approaching stability but still subject to incompatible change;
- `v1`: stable with strong compatibility expectations.

A resource's preferred served version is not necessarily its storage version,
which matters when planning CRD schema migrations.

### Apply and field ownership

Patch behavior depends on the operation and the schema: some list fields merge
by key while others are replaced wholesale. Client-side apply compares against a
last-applied annotation. Server-side apply records per-field ownership in
`managedFields` and reports conflicts between managers, which makes shared
ownership between CI, operators, and humans explicit.

### GitOps

GitOps stores declarative desired state in version control and uses an in-cluster
controller such as Argo CD or Flux to reconcile it. Benefits include review,
auditability, drift detection, and repeatable rollback. Git history alone does
not roll back external state or database changes.

Argo CD emphasizes application views and a UI; Flux emphasizes composable
controllers and toolkit APIs. Both support automated pull-based reconciliation.

### Deployment strategies

- **Rolling update:** incrementally replaces Pods using `maxSurge` and
  `maxUnavailable`.
- **Blue-green:** runs old and new environments, then switches traffic.
- **Canary:** sends a controlled traffic percentage or audience to a new
  version and promotes based on evidence.

A standard Deployment approximates replica-based canaries but does not provide
precise traffic weighting. Use a Gateway/service mesh or rollout controller
when weighted routing and automated analysis are required.

### Kompose

Kompose converts Compose definitions into starter Kubernetes manifests:

```bash
kompose convert
```

The result requires review for probes, resources, security, storage, Services,
and production architecture. Conversion is not production validation.

## Helm

### What is a Helm chart?

A chart is a versioned package of Kubernetes templates, default values, and
metadata. Helm renders the chart and tracks each installation as a release.

```text
my-chart/
├── Chart.yaml
├── values.yaml
├── values.schema.json
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   └── service.yaml
├── charts/
├── crds/
└── .helmignore
```

- `Chart.yaml`: chart metadata and dependencies.
- `values.yaml`: default user configuration.
- `values.schema.json`: optional validation for values.
- `templates/`: Go templates rendered into manifests.
- `charts/`: packaged dependencies.
- `crds/`: CRDs installed before templates, with special lifecycle behavior.

Charts make related resources reusable and configurable, but templates should
remain simple enough that rendered output can be reviewed.

### Values and precedence

Later, more specific values override earlier values. Common precedence from low
to high is:

1. chart `values.yaml`;
2. parent chart values for a subchart;
3. files passed with `-f`/`--values`, in command order;
4. `--set`, `--set-string`, `--set-file`, or `--set-json`.

Use version-controlled values files for repeatability. Use `--set` sparingly for
small automation overrides; shell escaping and type coercion make complex data
error-prone.

```bash
helm upgrade --install web ./chart \
  -f values-production.yaml \
  --set-string image.tag=1.2.3
```

#### Values on upgrade: reuse versus reset

`helm upgrade` decides what to do with the values a previous release already
carried, and the flags are a common source of surprise:

| Flag | Starting point | Typical failure mode |
| --- | --- | --- |
| `--reuse-values` | The previous release's values, then this command's overrides | Retired values persist and new chart defaults are not picked up |
| `--reset-values` | The chart's defaults, then this command's overrides | Overrides supplied in earlier upgrades are silently dropped |
| `--reset-then-reuse-values` | Chart defaults, then previously supplied values, then this command's overrides | Available only on newer Helm releases |

The reliable practice is to pass the complete set of values files on every
upgrade so the outcome does not depend on flag semantics or release history.
Confirm what the cluster actually holds before and after:

```bash
helm get values web            # user-supplied values only
helm get values web --all      # merged computed values
helm upgrade --help            # verify flag behavior for the installed version
```

### Core commands

```bash
helm install <release> <chart>
helm upgrade <release> <chart>
helm upgrade --install <release> <chart>
helm history <release>
helm rollback <release> <revision>
helm uninstall <release>
helm repo update
```

`install` creates a release. `upgrade` creates a new release revision from a
chart and values. `rollback` creates another revision based on an earlier one;
it does not reverse external side effects such as database migrations.
`repo update` refreshes local repository indexes and does not upgrade releases.

### Rendering and validation

```bash
helm lint ./chart
helm template web ./chart -f values-production.yaml
helm install web ./chart --dry-run
helm get manifest web
helm get values web --all
```

Rendering catches template problems but not every API, admission, runtime, or
controller error. Validate rendered manifests against the target Kubernetes
version and test an actual upgrade.

### Helm diff

The community `helm-diff` plugin previews rendered changes:

```bash
helm diff upgrade web ./chart -f values-production.yaml
helm diff revision web 2 3
```

It reduces surprise but does not predict all defaulting, mutation, immutable
field behavior, hooks, or external controller effects.

### Dependencies and CRDs

Declare dependencies in `Chart.yaml`, then run:

```bash
helm dependency update ./chart
```

Helm installs CRDs from `crds/` if absent, but does not template, upgrade, or
delete them automatically. Plan CRD schema and controller upgrades explicitly,
especially when stored custom resources may no longer match a new schema.

### Hooks and release safety

Hooks can run Jobs around install, upgrade, rollback, or delete events. They can
block a release and may not be managed like ordinary resources. Define deletion
policies and make hook Jobs idempotent.

For safer production upgrades, pin chart and image versions, inspect diffs,
validate schemas, set `--wait` and an appropriate `--timeout`, and understand
`--atomic`: it attempts rollback on failure but cannot undo external side
effects.

## Companion files

Procedural material stays outside this guide so that command sequences can be
practised without rereading the explanations:

- [Secret recipes](kubernetes-secrets-recipes.md): creating and consuming Secrets.
- [CKA labs](kubernetes-cka-labs.md): imperative commands, JSONPath, RBAC, networking,
  storage, workloads, node maintenance, and etcd exercises.

## Recommended interview-answer structure

1. Give a direct one- or two-sentence definition.
2. Explain the control flow or key distinction.
3. State practical significance or a production example.
4. Mention one important limitation or failure mode.

For troubleshooting questions, use:

1. symptom and blast radius;
2. evidence to collect;
3. most likely causes;
4. safe recovery;
5. prevention and monitoring.
