# Kubernetes Interview Guide

Pointer-style recall notes: one-line facts, decision tables, gotchas, and short
symptom/check/recover drills. Procedures live in the companion files; official docs are linked
beside each topic.

## Contents

[Architecture](#architecture) · [Failures and troubleshooting](#failures-and-troubleshooting) · [Scheduling and autoscaling](#scheduling-and-autoscaling) · [Networking](#networking) ·
[Configuration and storage](#configuration-and-storage) · [Security](#security) · [Upgrades and maintenance](#upgrades-and-maintenance) · [Workloads and extensibility](#workloads-and-extensibility) ·
[Helm](#helm) · [Companion files](#companion-files) · [Answer structure](#answer-structure)

## Architecture

Docs: [Architecture](https://kubernetes.io/docs/concepts/architecture/) · [Components](https://kubernetes.io/docs/concepts/overview/components/) · [etcd](https://etcd.io/docs/)

1. Request reaches `kube-apiserver`, which authenticates, authorizes, validates, admits.
2. Desired state is persisted in etcd; controllers reconcile observed toward desired state.
3. Scheduler binds unscheduled Pods; kubelet drives the runtime on the node.

- The API server is the only core component that talks to etcd directly, and components watch the API rather than calling each other.
- A Deployment creates no container directly: Deployment → ReplicaSet → Pod → bind → kubelet.
- Running Pods do not need the API server; scheduling, scaling, self-healing, and status do.

### Components and interfaces

| Location | Component | Responsibility |
| :--- | :--- | :--- |
| Control plane | `kube-apiserver` | Serves the API, enforces API policy |
| Control plane | etcd | Durable cluster state |
| Control plane | `kube-scheduler` | Picks nodes for unscheduled Pods |
| Control plane | `kube-controller-manager` | Core reconciliation loops |
| Control plane | `cloud-controller-manager` | Cloud provider integration |
| Node | kubelet | Reconciles assigned Pod specs with containers |
| Node | container runtime | Images and containers via CRI |
| Node | `kube-proxy` or replacement | Service forwarding |
| Add-on | CNI plugin | Pod networking |
| Add-on | CoreDNS | Cluster DNS and service discovery |

Docs: [CRI](https://kubernetes.io/docs/concepts/architecture/cri/) · [Network plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/) · [CSI](https://kubernetes.io/docs/concepts/storage/volumes/#csi)

- **CRI:** kubelet ↔ runtime (containerd, CRI-O). **CNI:** Pod interfaces, IPs, routes, usually policy. **CSI:** provisioning, attach, mount, snapshots.
- The spec is the contract; Calico, Cilium, Flannel, and each CSI driver implement it differently.

### etcd, quorum, and HA design

Docs: [etcd FAQ](https://etcd.io/docs/v3.5/faq/) · [Disaster recovery](https://etcd.io/docs/v3.5/op-guide/recovery/) · [HA topology](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)

- Raft consensus, `quorum = floor(N / 2) + 1`: 3 members tolerate 1 loss, 5 tolerate 2, odd counts give the best ratio.
- Quorum loss blocks writes and linearizable reads; running Pods serve but state cannot change.
- **Caveat:** repair members while quorum exists; on corruption or total loss stop writes and restore one known-good snapshot for the installed etcd version.
- **Caveat:** never restore members independently into one cluster — that is a split brain.
- **Caveat:** quorum is not a backup. Snapshot drills: [CKA labs](kubernetes-cka-labs.md).
- HA: several API servers behind a health-checked LB, 3 or 5 etcd members on low-latency disks, scheduler and controller-manager active/passive by leader election.
- One control-plane/etcd member per zone across three zones survives one zone loss; node spread is not HA if all replicas or volumes sit in one zone.
- A single control plane suits only disposable dev: one host failure ends cluster management.

## Failures and troubleshooting

Docs: [Debug clusters](https://kubernetes.io/docs/tasks/debug/debug-cluster/) · [Debug applications](https://kubernetes.io/docs/tasks/debug/debug-application/)

Pattern: **symptom → scope → evidence → recovery → prevention.** Collect logs and events before restarting anything, unless restoring service outranks diagnosis.

### Control-plane and node failure

| Down | Impact | Check | Recover |
| :--- | :--- | :--- | :--- |
| `kube-apiserver` | No API, nodes cannot report, no new state; containers keep running | LB health, API logs and health endpoints, certs, etcd reachability | Fix etcd or certs, restart instance, keep healthy replicas in the LB |
| etcd | Writes fail, API errors, no self-healing | Member health, endpoint status, disk latency, peers, corruption alarms | Repair with quorum, else restore a snapshot |
| `kube-scheduler` | New Pods stay `Pending` with no `.spec.nodeName` | Logs, leader election, API access, RBAC, config | Restore process or config, run replicas |
| `kube-controller-manager` | No Pod replacement, Job or node lifecycle progress | Logs, leader election, RBAC, work-queue metrics | Restore process, confirm queues drain |
| kubelet | Node `NotReady`, its Pods possibly unreachable | Node conditions and events, kubelet/runtime status, pressure, certs | Fix kubelet/runtime/network, or cordon, drain, replace |

- Pods on a dead node are never live-migrated; controllers recreate managed Pods after node-lifecycle tolerations expire.
- **Caveat:** a hard-failed node with attached storage may need workload-specific fencing before force deletion, or two writers touch one volume.
- **Caveat:** zone loss needs quorum, spare capacity, and spread replicas to survive; PodDisruptionBudgets bound voluntary disruption only and promise nothing during involuntary failure.

### Symptom tables

| Network symptom | Likely layer | Check |
| :--- | :--- | :--- |
| Pod IP → Pod IP fails | CNI, routes, policy | CNI Pods and logs, node routes, NetworkPolicies |
| Service IP fails, Pod IP works | `kube-proxy` or eBPF dataplane | EndpointSlices, node rules, agent logs |
| Name fails, IP works | CoreDNS | DNS Pods, Service/EndpointSlices, `resolv.conf`, upstream |

- **Caveat:** never blanket-flush iptables on a production node — rules belong to Kubernetes, the CNI, host firewalls, and other services. Use [Network bisection](#network-bisection).

| Workload symptom | Common causes | Evidence |
| :--- | :--- | :--- |
| `CrashLoopBackOff` | App exit, failing liveness probe, bad config, OOM | `describe`, current and `--previous` logs |
| `Pending` | No fitting node, untolerated taint, unbound PVC | Pod events, scheduler messages |
| `OOMKilled` | Exceeded cgroup memory limit | Last state, exit code 137, metrics |
| `ImagePullBackOff` | Bad tag, auth, DNS, registry | Pod events, runtime logs |
| Service 503, no endpoints | Selector mismatch, Pods not ready | Service selector, EndpointSlices |
| `NodeNotReady` | Kubelet, runtime, network, host pressure | Node conditions, system logs |
| `Terminating` forever | Finalizer or stuck volume detach | Object finalizers, CSI and kubelet logs |

### Certificate expiry: which TLS layer?

Docs: [kubeadm certs](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/) · [PKI certificates](https://kubernetes.io/docs/setup/best-practices/certificates/)

| Layer | Serves | Symptom | Location |
| :--- | :--- | :--- | :--- |
| Ingress / app TLS | External clients of an app | Browser warning, failed handshake to the app host | Kubernetes TLS Secret, cert-manager, or cloud LB |
| Cluster PKI | API server, kubelets, etcd, controllers | `x509: certificate has expired` from `kubectl`, nodes `NotReady` | Node filesystem, `/etc/kubernetes/pki` |

- **Caveat:** an expired Ingress cert never breaks `kubectl`, and renewing an Ingress Secret never fixes cluster PKI. Identify the layer first.

```bash
# App TLS: inspect what is actually served, then the issuing chain.
openssl s_client -connect app.example.com:443 -servername app.example.com </dev/null \
  | openssl x509 -noout -subject -issuer -dates
kubectl get certificate,certificaterequest,order,challenge -n <namespace>

# Cluster PKI: run on a control-plane node, the API may be unreachable.
sudo kubeadm certs check-expiration
```

- Renewal and its cautions: [Control-plane certificates](#control-plane-certificates).

### Investigation and live debugging

Docs: [kubectl reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/) · [Debug running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)

```bash
kubectl get pods -A -o wide
kubectl describe <kind> <name> -n <namespace>
kubectl logs <pod> -n <namespace> --all-containers
kubectl logs <pod> -n <namespace> --previous
kubectl get events -A --sort-by=.metadata.creationTimestamp
kubectl get endpointslices -n <namespace> -l kubernetes.io/service-name=<svc>

kubectl debug -it pod/web --image=busybox:1.36 --target=app
kubectl debug pod/web --copy-to=web-debug --container=app --image=busybox:1.36 -it -- sh
kubectl debug node/node01 -it --image=busybox:1.36
```

- Events expire, so collect them first, then walk the owning controller, node conditions, EndpointSlices, storage, and component logs.
- Ephemeral containers cannot be removed, never restart, take no probes or resources, and `--target` needs runtime support for process-namespace sharing.
- **Caveat:** `kubectl debug node/...` creates a highly privileged Pod with host access; restrict who may run it and treat the session as sensitive.

## Scheduling and autoscaling

Docs: [Scheduling and eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/) · [Assigning Pods](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)

### Scheduling cycle and placement

- **Filter** nodes failing resources, selectors/affinity, taints, topology, volume, or ports; **score** the survivors; **bind** the winner into the Pod.
- Fit uses **requests**, not live utilization, and a `Pending` Pod's events name the failed filter.

| Mechanism | Meaning | Use |
| :--- | :--- | :--- |
| `nodeSelector` | Required exact label match | Simple hardware targeting |
| Required node affinity | Expressive hard constraint | Specific zones, architectures |
| Preferred node affinity | Weighted preference | Favor a pool, allow fallback |
| Pod affinity | Co-locate with matching Pods | Latency-sensitive peers |
| Pod anti-affinity | Separate from matching Pods | Replica fault isolation |
| Topology spread | Bound skew across domains | Even node/zone distribution |
| Taint / toleration | Node repels non-tolerating Pods | Dedicated or impaired nodes |
| `nodeName` | Bypasses the scheduler | Exceptional low-level use |

- A toleration only permits placement, never attracts: for dedicated nodes pair a taint with node affinity or a selector.
- Strict anti-affinity can leave Pods `Pending`, and the topology label must exist on every candidate node.
- Prefer topology spread for balanced replicas; align storage topology with placement.

Docs: [Taints and tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)

| Effect | Existing Pods | New Pods without toleration |
| :--- | :--- | :--- |
| `NoSchedule` | Keep running | Not scheduled |
| `PreferNoSchedule` | Keep running | Avoided when feasible, not guaranteed |
| `NoExecute` | Evicted unless tolerated | Not scheduled |

- `tolerationSeconds` on a `NoExecute` toleration delays eviction; omitting it tolerates forever.
- DaemonSet Pods get some system tolerations automatically (not-ready, unreachable).
- `kubectl taint node node01 workload=gpu:NoSchedule` — a trailing `-` removes the taint.

### Requests, limits, and QoS

Docs: [Manage resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) · [Pod QoS](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)

- Request = scheduling and accounting baseline; limit = runtime enforcement.
- CPU is compressible (throttling); memory is not (reclaim, eviction, OOM kill).
- **Guaranteed:** *every* container sets CPU **and** memory requests **and** limits, with each request equal to its limit. **Burstable:** at least one request or limit set somewhere, but not Guaranteed. **BestEffort:** no container sets any request or limit.
- **Gotcha:** a limit with no request makes the request default to that limit. A limits-only spec is therefore Guaranteed **only when every container limits both CPU and memory** — limiting just one of the two leaves the Pod Burstable.
- **Gotcha:** either way the defaulted request reserves the full limit and burns allocatable capacity. LimitRange defaults do the same, so verify the created Pod:

```bash
kubectl get pod web -o jsonpath='{.spec.containers[*].resources}{"\n"}'
kubectl get pod web -o jsonpath='{.status.qosClass}{"\n"}'
```

### Quotas, priority, and eviction

Docs: [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) · [LimitRange](https://kubernetes.io/docs/concepts/policy/limit-range/) · [Priority and preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/) · [Node-pressure eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/)

- ResourceQuota caps namespace aggregates: `requests.cpu`, `requests.memory`, `limits.cpu`, `limits.memory`, `pods`, `persistentvolumeclaims`, `requests.storage`, object counts.
- LimitRange sets `defaultRequest`, `default`, `min`, and `max` per container.
- **Gotcha:** once a quota constrains a compute resource, every new Pod must declare the matching request and limit or admission rejects it — pair the quota with a LimitRange.
- Quotas apply at admission: lowering one blocks growth, it never evicts. Inspect with `kubectl describe resourcequota <name> -n <ns>`.

| Eviction path | Trigger | Notes |
| :--- | :--- | :--- |
| Kubelet eviction | Node memory or disk pressure | Priority, usage over requests, and QoS all matter |
| Node-controller eviction | Node unreachable past tolerations | Replaces managed workloads elsewhere |
| API eviction | `kubectl drain` | Honors PodDisruptionBudgets |
| Preemption | High-priority Pod cannot schedule | Evicts lower-priority Pods for room |

- `PriorityClass` sets an integer priority; it never overrides hard constraints, and PDBs are only best-effort during preemption. QoS alone does not set kubelet eviction order.
- Drain flag risks: [Cordon, drain, and uncordon](#cordon-drain-and-uncordon).

### Autoscalers

Docs: [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) · [Topology spread](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/)

| Autoscaler | Changes | Trigger |
| :--- | :--- | :--- |
| HPA | Replica count | Resource, custom, or external metrics |
| VPA | Requests, optionally recreating Pods | Historical and current usage |
| Cluster autoscaler | Node count | Unschedulable Pods, removable capacity |

- **Gotcha:** never let HPA and VPA both drive CPU or memory for one workload; HPA on custom metrics plus VPA on resources is fine.
- The cluster autoscaler reacts to unschedulable Pods, not high node CPU; scale-down weighs Pod movability and disruption constraints.

## Networking

Docs: [Cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) · [Services](https://kubernetes.io/docs/concepts/services-networking/service/) · [Virtual IPs](https://kubernetes.io/docs/reference/networking/virtual-ips/)

- Every Pod gets an IP; Pods reach Pods across nodes without app-visible NAT, and a node's agents reach that node's Pods.
- The CNI supplies interfaces, addresses, routes or overlays, and usually policy; dataplanes are overlay (VXLAN/Geneve), routed (BGP), or eBPF.
- A Service is a stable virtual IP/port over a changing set of **ready** backends; its selector produces EndpointSlices.
- `kube-proxy` installs forwarding state, it does not proxy packets in user space; some CNIs replace it with eBPF.
- **Do not confuse:** `kube-proxy` (Service dataplane) with `kubectl proxy` (local authenticated HTTP proxy to the API server).

| Mode | Strength | Trade-off |
| :--- | :--- | :--- |
| iptables | Mature, ubiquitous | Large rule sets update and inspect slowly |
| IPVS | Efficient lookup, multiple algorithms | Needs IPVS modules, still uses some iptables |
| nftables | Better scaling than iptables | Requires a recent cluster and kernel |
| eBPF (CNI-provided) | Replaces `kube-proxy`, high scale | Ties you to that CNI's tooling |

- IPVS is not universally better: choose on platform support, scale, observability, and operational familiarity.

### Exposure and traffic policy

Docs: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) · [Gateway API](https://gateway-api.sigs.k8s.io/)

| API | Purpose |
| :--- | :--- |
| `ClusterIP` | Internal stable virtual IP |
| `NodePort` | Same high port on every node address |
| `LoadBalancer` | Provisions or configures an external load balancer |
| `ExternalName` | Returns a CNAME to an external DNS name |
| Ingress | HTTP(S) host/path routing via a controller |
| Gateway API | Role-oriented, extensible L4/L7 routing |

- Ingress is **not** a Service type and does nothing without a controller; `LoadBalancer` usually builds on NodePort, though some implementations route straight to Pods.
- `ExternalName` is DNS-only: no selector, endpoints, or proxying, cannot target an IP literal or rewrite ports, and TLS SNI validates against the external name. To front a bare IP, use a selectorless Service with a manually managed EndpointSlice.

| Setting | Behavior | Trade-off |
| :--- | :--- | :--- |
| `externalTrafficPolicy: Cluster` (default) | Any node forwards to any endpoint | Even spread, SNAT hides client source IP |
| `externalTrafficPolicy: Local` | Node forwards only to local endpoints | Preserves source IP, capacity follows Pod placement |
| `internalTrafficPolicy: Local` | In-cluster traffic stays same-node | Less cross-node traffic, fails with no local endpoint |

- With `Local`, endpoint-less nodes fail the LB health check and stop receiving traffic — pair it with a DaemonSet or topology spread or capacity skews.
- `sessionAffinity: ClientIP` is crude because NAT collapses many clients to one IP; prefer stateless apps with external session storage.

### DNS

Docs: [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) · [NodeLocal DNSCache](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/)

- Records: `<service>.<namespace>.svc.cluster.local`, plus `<service>` in-namespace and `<service>.<namespace>` cross-namespace; named ports get SRV records.
- A normal Service name resolves to the ClusterIP; a headless Service (`clusterIP: None`) resolves to Pod addresses, giving names like `web-0.nginx.default.svc.cluster.local`.
- Headless Services give discovery only; StatefulSet identity and PVCs give stable storage.
- `dnsPolicy`: `ClusterFirst` (default), `ClusterFirstWithHostNet` (needed for `hostNetwork`), `Default` (node resolver), `None` (explicit `dnsConfig`).
- NodeLocal DNSCache is a per-node caching DaemonSet: lower latency, less CoreDNS load, and it avoids the UDP conntrack races behind intermittent timeouts; verify the rollout per node.
- **Gotcha:** the API server is `kubernetes.default.svc` but its ClusterIP is installation-specific — run `kubectl get service kubernetes -n default` rather than assuming the first address in the Service CIDR.

### NetworkPolicy

Docs: [Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

- Additive allow-list model with no deny rules, enforced only if the CNI implements it.
- A Pod is non-isolated for a direction until a policy selects it for that direction; once isolated, traffic needs a matching allow rule.
- Selector logic: entries inside one `from`/`to` item are ANDed, separate list items are ORed.
- **Caveat:** an empty rule is not a deny rule. `ingress: [{}]` matches every source and `egress: [{}]` matches every destination, re-opening that direction. To deny, name the direction in `policyTypes` and supply **no** rule for it.
- Start with namespace default-deny both ways, then allow app flows, DNS, monitoring, and required external endpoints. Worked policy: [CKA labs](kubernetes-cka-labs.md).
- Limits: namespaced, does not filter node-level traffic in every implementation, and never replaces cloud firewalls.

### Network bisection

1. Test DNS name, Service IP, and Pod IP separately; the first failing layer is the answer.
2. Verify selector labels, EndpointSlice contents, and readiness — unready Pods are excluded from Service backends.
3. Inspect NetworkPolicies in **both** source and destination namespaces.
4. Inspect CNI and dataplane agent logs, node routes, and rules.
5. External traffic: LB health checks, Ingress/Gateway status, TLS, source-IP policy, cloud firewall rules.

## Configuration and storage

Docs: [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) · [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) · [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

- ConfigMap holds non-sensitive config as plain strings or binary; Secret holds credentials, keys, tokens, and certs as base64-encoded values.
- **Caveat:** base64 is encoding, not encryption — see [Secrets and etcd protection](#secrets-and-etcd-protection). Recipes: [Secret recipes](kubernetes-secrets-recipes.md).
- Exposure paths: environment variables, args from env vars, projected volume files, single keys via `subPath`.
- Env values never update in a running process; projected files update eventually but the app must reload; `subPath` mounts never update.
- Standard trick: a config checksum annotation in the Pod template rolls new Pods on change.

### PV, PVC, StorageClass, CSI

Docs: [Storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)

- PV is the cluster storage resource, PVC the namespaced request, StorageClass the provisioner/parameters/binding mode/reclaim policy, CSI driver the implementation.
- Dynamic flow: PVC created → provisioner creates a PV → PVC binds → kubelet and CSI attach and mount.
- `volumeBindingMode: WaitForFirstConsumer` defers provisioning until scheduling so the volume lands in a compatible zone.
- A PVC outlives its Pod; deleting a Pod never deletes the PVC.
- On PVC deletion `Delete` removes PV and backing storage, `Retain` leaves the PV `Released` for manual recovery; `Recycle` is deprecated — do not use it.
- Protection finalizers delay deletion of in-use objects but never change the reclaim policy.

### StatefulSets and access modes

Docs: [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

- Access modes: `ReadWriteOnce` (one node at a time, several Pods on that node possible), `ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod` (exactly one Pod cluster-wide, where supported).
- Volume modes are `Filesystem` or raw `Block`; access modes express requested and provider capability, not authorization.
- StatefulSets give stable ordinal names (`db-0`), stable identity via a headless Service, one PVC per ordinal, ordered rollout and scaling by default, optional parallel management.
- `volumeClaimTemplates` create ordinal-named PVCs; retention is configurable via the PVC retention policy.
- Pods are replaceable but their identities are not interchangeable: use StatefulSets for stable membership or storage, not because an app happens to write files.

### Ephemeral volumes and databases

Docs: [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)

- `emptyDir` lives only while the Pod stays on the node: scratch and container sharing only, and `medium: Memory` counts against memory limits and pressure.
- **Caveat:** `hostPath` mounts node paths into a Pod. It breaks portability, pins data to one node, and is a privilege-escalation vector — writable host paths can expose the runtime socket, kubelet credentials, or host binaries. Prefer PVCs or CSI ephemeral volumes; if unavoidable, mount read-only from a narrow subdirectory and gate it with admission policy.
- Databases: match storage latency and attachment semantics, spread replicas while keeping volumes schedulable, use readiness and startup probes, avoid liveness probes that cause unsafe restart loops, set PDBs and graceful termination, back up application-consistently.
- Persistent storage is not a backup, and several database Pods are not automatically a consistent HA database; prefer a mature operator or managed service.

## Security

Docs: [Security concepts](https://kubernetes.io/docs/concepts/security/) · [Authentication](https://kubernetes.io/docs/reference/access-authn-authz/authentication/) · [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

Layers: supply chain, API access, workload isolation, network, secrets, node, audit. RBAC alone is not cluster security.

- **Authentication** establishes identity (OIDC, client certs, ServiceAccount tokens), **authorization** decides permission (usually RBAC), **admission** mutates or validates before persistence.
- TLS protects transport and grants no permission.
- `Role` covers namespaced resources in one namespace; `ClusterRole` covers cluster-scoped resources or a reusable namespaced set.
- `RoleBinding` grants either within one namespace; `ClusterRoleBinding` grants cluster-wide.
- Subjects are users, groups, or ServiceAccounts; permissions are additive with no deny rules.
- Avoid wildcards, restrict Secret access and `pods/exec`, separate human from workload identities, and review bindings.
- **Gotcha:** create or patch on Pods is an escalation path — the identity may attach a more privileged ServiceAccount or mount readable Secrets. Evaluate paths, not verbs in isolation.
- ServiceAccounts are namespaced workload identities with short-lived, audience-bound projected tokens; set `automountServiceAccountToken: false` for Pods that never call the API and bind dedicated accounts instead of `default`.

```bash
kubectl auth can-i create deployments -n dev --as alice
kubectl auth can-i --list -n dev --as system:serviceaccount:dev:app
```

### Pod Security Standards and hardening

Docs: [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) · [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) · [Security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

- **Privileged:** unrestricted, only for explicitly trusted system workloads. **Baseline:** blocks known escalations, broadly compatible. **Restricted:** current hardening practice.
- Pod Security Admission enforces a profile per namespace label in `enforce`, `audit`, and `warn` modes; roll out audit/warn first and pin versions for predictable upgrades.
- It cannot express arbitrary policy — use validating admission policy or a policy engine.

```yaml
securityContext:
  runAsNonRoot: true
  seccompProfile: { type: RuntimeDefault }
containers:
  - name: app
    image: registry.example.com/app@sha256:replace-me
    securityContext:
      allowPrivilegeEscalation: false
      capabilities: { drop: [ALL] }
      readOnlyRootFilesystem: true
```

- Avoid privileged containers, host namespaces, `hostPath`, and host ports.
- Set a known non-root UID/GID, add only the one capability needed, use read-only mounts with a writable `emptyDir` where required, and always set resources.
- Consider RuntimeClass sandboxing for higher-risk workloads.
- **Caveat:** `runAsNonRoot` alone is insufficient when the image identity is ambiguous — test the image and set `runAsUser`.

### Secrets and etcd protection

Docs: [Encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) · [etcd security](https://etcd.io/docs/v3.5/op-guide/security/)

- Enable encryption at rest, preferably KMS-backed, then re-encrypt existing objects.
- Use TLS for etcd client and peer traffic and restrict network access to etcd hosts.
- Grant Secret `get`/`list`/`watch` sparingly — list/watch exposes every value in scope.
- Prefer short-lived credentials and an external secret manager with workload identity.
- **Caveat:** an etcd snapshot is a full copy of cluster state including Secrets, so encrypt backups, restrict access to them, and test recovery.
- **Caveat:** encryption at rest protects media and backups only; it does not stop an authorized reader or a compromised Pod that already receives the Secret.

### Supply chain, nodes, and audit

Docs: [Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)

- Minimal maintained images, pinned digests, continuous scanning, signature and provenance verification at admission.
- Patch Kubernetes, host OS, runtime, and CNI; restrict registries and pull credentials.
- Harden kubelet (no anonymous auth, authorization on), limit SSH, isolate control-plane and etcd hosts, protect cloud instance metadata.
- Audit security-relevant metadata without logging Secret bodies; alert on privileged Pod creation, RBAC changes, exec/attach, Secret access, admission failures, unusual clients.
- **Caveat:** treat a compromised node as compromise of every workload and credential on it — cordon, isolate, rotate, rebuild, investigate.

## Upgrades and maintenance

Docs: [Cluster upgrade](https://kubernetes.io/docs/tasks/administer-cluster/cluster-upgrade/) · [Version skew](https://kubernetes.io/releases/version-skew-policy/) · [kubeadm upgrade](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)

1. Read release notes and the skew policy for the exact distribution.
2. Inventory deprecated APIs, admission integrations, CRDs, CNI/CSI, operators, client tools.
3. Confirm backups and perform a **test restore**, especially etcd and app data.
4. Check control-plane, node, workload, storage, and network health, then validate the release in a representative non-production cluster.
5. Move one minor version at a time where required: control-plane instances first and sequentially, then workers in small batches.
6. After each batch verify API, controllers, nodes, DNS, storage, and app SLIs.

- Maintain supported skew across `kube-apiserver`, kubelet, controller-manager, scheduler, and `kubectl`; the API server upgrades before kubelets.
- **Caveat:** keep a tested rollback path — an etcd restore is disaster recovery, not a routine downgrade.
- **Caveat:** do not hand-upgrade etcd just because Kubernetes is upgrading; use the distribution's supported etcd version and process.
- Managed services and kubeadm differ; follow the vendor procedure rather than assuming component commands are portable.

### Cordon, drain, and uncordon

Docs: [Safely drain a node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/) · [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

- `cordon` marks unschedulable and leaves Pods; `drain` evicts evictable Pods through the eviction API and cordons; `uncordon` restores scheduling.

```bash
kubectl cordon node01
kubectl drain node01 --ignore-daemonsets --timeout=5m
# maintenance, then verify kubelet and runtime health
kubectl uncordon node01
```

- `--ignore-daemonsets` is needed on nearly every real cluster because DaemonSet Pods are per-node and are never evicted.
- **Caveat:** read the stall message before adding flags — each override trades a protection.

| Flag | Effect | Risk accepted |
| :--- | :--- | :--- |
| `--ignore-daemonsets` | Proceeds despite DaemonSet Pods | None in normal use, node agents stay |
| `--delete-emptydir-data` | Evicts Pods with `emptyDir` | That scratch data is destroyed permanently |
| `--force` | Deletes Pods with no controller | Those Pods are recreated nowhere |
| `--disable-eviction` | Deletes Pods directly | Bypasses the eviction API and ignores PDBs, emergencies only |
| `--grace-period` | Overrides termination grace | Can cut off shutdown and data flushing |

- A blocked drain is usually correct feedback: a PDB has no spare replica, or a Pod has no owning controller. Fix capacity or ownership instead of forcing.
- A PDB bounds concurrent **voluntary** disruption via `minAvailable` or `maxUnavailable`.
- **Caveat:** a PDB does not protect against node crashes, zone failure, direct Pod deletion, or every rollout path, and one with no spare replica blocks maintenance indefinitely.
- Pair PDBs with enough replicas, failure-domain spread, meaningful readiness probes, graceful termination, and storage failover that fits drain timing.

Node maintenance loop:

1. Confirm cluster health and spare capacity, then cordon and drain one node or a small batch.
2. Confirm replacement Pods are ready and SLIs healthy.
3. Patch or replace node, runtime, kubelet, and agents.
4. Verify node conditions, versions, CNI/CSI DaemonSets, and logs.
5. Uncordon, watch scheduling, and continue only at steady state.

- Replacing immutable nodes is usually safer and more repeatable than in-place upgrades.
- Zero downtime needs workloads designed for it: single-replica or non-failover stateful apps still take an outage.

### Control-plane certificates

Docs: [kubeadm certificate management](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)

- kubeadm issues one-year control-plane client and serving certs; the CA is long-lived. Layer identification: [Certificate expiry](#certificate-expiry-which-tls-layer).
- `kubeadm upgrade` renews them, so yearly-upgraded clusters rarely expire.

```bash
sudo cp -a /etc/kubernetes/pki "/root/pki-backup-$(date +%F)"   # back up PKI and kubeconfigs first
sudo kubeadm certs renew all                                    # or one cert: renew apiserver
sudo kubeadm certs check-expiration                             # confirm new dates
```

- Renewal writes files but does not reload components: restart the control-plane static Pods (commonly by moving manifests out of the static Pod directory and back), verify API health, and repeat on every control-plane node.
- **Caveat:** `kubeadm certs renew all` refreshes embedded client certs in files such as `admin.conf`, so redistribute kubeconfigs — older copies keep failing.
- **Caveat:** never run `kubeadm init phase certs` on a live cluster to fix expiry. Regenerating a CA invalidates every existing certificate and kubeconfig.
- Kubelet client certs rotate automatically when enabled; serving certs may need CSR approval.

## Workloads and extensibility

Docs: [Workload controllers](https://kubernetes.io/docs/concepts/workloads/controllers/) · [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)

| Controller | Use |
| :--- | :--- |
| Deployment | Stateless replicas, rolling update, rollback |
| ReplicaSet | Maintains replica count, normally owned by a Deployment |
| StatefulSet | Stable identity, storage, ordered lifecycle |
| DaemonSet | One Pod per eligible node |
| Job | Finite work to completion |
| CronJob | Creates Jobs on a schedule |

- DaemonSet Pods get automatic tolerations so node agents run where ordinary Pods cannot, but selectors, affinity, and taints still apply — "every node" is not guaranteed.
- Identity and storage details: [StatefulSets and access modes](#statefulsets-and-access-modes).

### Job and CronJob fields

Docs: [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) · [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)

| Job field | Effect |
| :--- | :--- |
| `completions` / `parallelism` | Successful completions required / max concurrent Pods |
| `completionMode` | `NonIndexed` (default) or `Indexed` |
| `backoffLimit` | Pod retries before `Failed` |
| `activeDeadlineSeconds` | Wall-clock limit, running Pods terminated |
| `ttlSecondsAfterFinished` | Automatic cleanup after finish |
| `podFailurePolicy` | Fail fast or ignore specific exit codes and conditions |
| `suspend` | Pause or resume Pod creation |

| CronJob field | Effect |
| :--- | :--- |
| `schedule` / `timeZone` | Cron expression / IANA zone, else the controller's reference time |
| `concurrencyPolicy` | `Allow`, `Forbid`, or `Replace` |
| `startingDeadlineSeconds` | How late a missed run may still start |
| `successfulJobsHistoryLimit` / `failedJobsHistoryLimit` | Retained Jobs |
| `suspend` | Stops creating Jobs |

- Job templates must set `restartPolicy` to `OnFailure` or `Never`, and `backoffLimit` counts Pod failures, so in-place restarts consume retries differently from replaced Pods.
- **Gotcha:** no exactly-once and no precise timing, so make Job work idempotent. After many missed runs the controller stops catching up and reports it in events.

### Pod lifecycle, containers, and probes

Docs: [Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) · [Lifecycle hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/)

- Phases: `Pending`, `Running`, `Succeeded`, `Failed`, `Unknown`. `Terminating` is a `kubectl` display state, not a phase. Container states: `Waiting`, `Running`, `Terminated`.
- `restartPolicy` (`Always`, `OnFailure`, `Never`) governs kubelet container restarts inside one Pod on one node; controllers replace Pods.
- Init containers run to completion in order before app containers: bounded setup such as config generation or dependency waits, sharing volumes as needed.
- Sidecars provide proxies and log shipping; modern versions model them as init containers with `restartPolicy: Always`, giving startup and shutdown ordering.

| Probe | Failure effect | Purpose |
| :--- | :--- | :--- |
| Startup | Restarts container after threshold | Shields slow starts from liveness |
| Readiness | Removes Pod from ready endpoints | Should it receive traffic |
| Liveness | Restarts container after threshold | Recover a wedged process |

- Handlers are exec, HTTP, TCP, and gRPC subject to version support, and readiness failure never restarts a container.
- **Gotcha:** a liveness probe depending on an optional downstream turns a partial outage into a cluster-wide restart storm.
- `postStart` is not guaranteed to run before the entrypoint; `preStop` runs before Kubernetes-initiated termination while the container still runs.
- The grace countdown starts before `preStop`, and hooks do not run on node loss, process crash, or forced termination — never make them the only guard for data correctness.

### Labels and annotations

Docs: [Labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) · [Well-known annotations](https://kubernetes.io/docs/reference/labels-annotations-taints/)

- Labels are indexed identifying metadata for selectors; annotation values are always strings and never selectable.

| Annotation | Purpose |
| :--- | :--- |
| `kubernetes.io/change-cause` | Reason shown by `kubectl rollout history` |
| `deployment.kubernetes.io/revision` | Deployment revision tracking |
| `kubectl.kubernetes.io/default-container` | Default container for `logs` and `exec` |
| `cluster-autoscaler.kubernetes.io/safe-to-evict` | Allows or blocks autoscaler eviction |
| `helm.sh/hook` | Marks a Helm lifecycle hook |
| `helm.sh/resource-policy: keep` | Survives `helm uninstall` |

- Prefer real API fields where they exist: `spec.ingressClassName`, and `ServiceMonitor`/`PodMonitor` instead of scrape annotations.
- Controller-specific annotations are implementation behavior, not portable API guarantees.

### CRDs, operators, admission, and APIs

Docs: [Custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) · [Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) · [Dynamic admission](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) · [Server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/)

- A CRD adds a type, a controller reconciles it, an operator combines both to encode backup, upgrade, and failover. A CRD without a controller does nothing.
- Operators should publish status conditions, be idempotent, use finalizers carefully, and handle upgrade and backup compatibility.
- Mutating admission defaults or modifies; validating admission accepts or rejects.
- **Caveat:** a webhook outage can block API operations depending on `failurePolicy`. Deploy redundantly, scope narrowly, set timeouts, and never let a webhook intercept the resources needed to recover it.
- API versions are `<group>/<version>` such as `apps/v1`; core resources are just `v1`. `v1alpha1` may break or vanish, `v1beta1` may still change incompatibly, `v1` is stable.
- The preferred served version is not necessarily the storage version, which matters for CRD schema migrations.
- Patch semantics vary: some list fields merge by key, others are replaced wholesale.
- Client-side apply diffs a last-applied annotation; server-side apply records per-field ownership in `managedFields` and surfaces conflicts between CI, operators, and humans.

### GitOps and rollout strategies

- GitOps keeps declarative state in Git and lets an in-cluster controller (Argo CD, Flux) reconcile it: review, audit, drift detection, repeatable rollback.
- Git history cannot roll back external state or database migrations.
- Argo CD leans on application views and a UI, Flux on composable controllers and toolkit APIs; both reconcile pull-based.
- **Rolling update:** incremental replacement via `maxSurge`/`maxUnavailable`. **Blue-green:** parallel environments, then a traffic switch. **Canary:** small traffic share or audience, promoted on evidence.
- A plain Deployment only approximates canaries by replica ratio; weighted routing and automated analysis need a Gateway, mesh, or rollout controller.
- `kompose convert` produces starter manifests only — review probes, resources, security, storage, and Services before any real use.

## Helm

Docs: [Helm docs](https://helm.sh/docs/) · [Charts](https://helm.sh/docs/topics/charts/) · [Best practices](https://helm.sh/docs/chart_best_practices/)

### Chart layout and values

A chart is a versioned package of templates, default values, and metadata; each installation is tracked as a release.

```text
my-chart/
├── Chart.yaml            # metadata and dependencies
├── values.yaml           # default configuration
├── values.schema.json    # optional values validation
├── templates/            # Go templates rendered to manifests, plus _helpers.tpl
├── charts/               # packaged dependencies
├── crds/                 # installed before templates, special lifecycle
└── .helmignore
```

- Keep templates simple enough that rendered output stays reviewable.
- Value precedence low to high: chart `values.yaml` → parent values for a subchart → each `-f` file in command order → `--set`, `--set-string`, `--set-file`, `--set-json`.
- Keep values in version control; use `--set` sparingly because shell escaping and type coercion make complex data error-prone.

Docs: [helm upgrade](https://helm.sh/docs/helm/helm_upgrade/)

| Flag | Starting point | Failure mode |
| :--- | :--- | :--- |
| `--reuse-values` | Previous release's values, then this command's overrides | Retired values persist, new chart defaults ignored |
| `--reset-values` | Chart defaults, then this command's overrides | Earlier overrides silently dropped |
| `--reset-then-reuse-values` | Chart defaults, then prior values, then overrides | Newer Helm versions only |

- **Caveat:** pass the complete set of values files on every upgrade so the result never depends on flag semantics or release history.

### Commands, rendering, and diff

```bash
helm upgrade --install web ./chart -f values-production.yaml --set-string image.tag=1.2.3
helm history web && helm rollback web <revision>
helm get values web --all      # merged computed values; omit --all for user-supplied only
helm lint ./chart
helm template web ./chart -f values-production.yaml
helm get manifest web
helm diff upgrade web ./chart -f values-production.yaml   # helm-diff plugin
```

- `upgrade` creates a new revision; `rollback` creates yet another revision from an earlier one and cannot reverse external side effects such as database migrations.
- `helm repo update` refreshes local indexes only and upgrades nothing.
- Rendering catches template errors, not API, admission, runtime, or controller errors — validate against the target Kubernetes version and rehearse a real upgrade.
- `helm diff` cannot predict all defaulting, mutation, immutable-field rejection, hooks, or external controller effects.

### Dependencies, CRDs, and hooks

Docs: [CRD best practices](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/) · [Chart hooks](https://helm.sh/docs/topics/charts_hooks/)

- Declare dependencies in `Chart.yaml`, then run `helm dependency update ./chart`.
- **Caveat:** Helm installs `crds/` only when absent and never templates, upgrades, or deletes them. Plan CRD schema and controller upgrades explicitly because stored custom resources may no longer match a new schema.
- Hooks run Jobs around install, upgrade, rollback, and delete. They can block a release and are not managed like ordinary resources: set deletion policies and make hook Jobs idempotent.
- Safer production upgrades: pin chart and image versions, inspect diffs, validate schemas, set `--wait` with a real `--timeout`, and remember `--atomic` attempts rollback but cannot undo external side effects.

## Companion files

Procedures stay out of this guide so command sequences can be practised separately.

- [Secret recipes](kubernetes-secrets-recipes.md): creating and consuming Secrets.
- [CKA labs](kubernetes-cka-labs.md): imperative commands, JSONPath, RBAC, networking, storage, workloads, node maintenance, CSRs, and etcd snapshot/restore.
- [DevOps interview checklist](devops-interview-checklist.md): gap self-assessment.

## Answer structure

- **Concept:** definition in one or two sentences → control flow or key distinction → practical significance → one limitation or failure mode.
- **Troubleshooting:** symptom and blast radius → evidence to collect → likely causes → safe recovery → prevention and monitoring.
