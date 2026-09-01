# CKA Lab Recipes

- **Card format:** task, minimal command or manifest, gotcha, and official docs.
- **Guides:** [concepts](kubernetes-interview-guide.md) · [Secrets](kubernetes-secrets-recipes.md).
- **Before running:** confirm names, namespaces, version, runtime, and paths.

**Cards:** [Exam scope](#exam-scope) · [Discovery and imperative creation](#discovery-and-imperative-creation) · [Placement](#placement-labels-taints-tolerations) · [Rollouts](#deployments-and-rollouts) · [Autoscaling](#autoscaling-workloads) · [DaemonSet and init containers](#daemonset-and-init-containers) · [Static Pods](#static-pods) · [Logs, exec, triage](#logs-exec-and-triage) · [ConfigMap](#configmap) · [Helm and Kustomize](#helm-and-kustomize) · [Storage](#volumes-pv-and-pvc) · [Dynamic provisioning](#dynamic-provisioning-with-storageclass) · [Services and Ingress](#services-and-ingress) · [Gateway API](#gateway-api) · [Networking](#networkpolicy-and-cluster-networking) · [RBAC](#rbac) · [Security context](#security-context-and-capabilities) · [Node maintenance](#node-maintenance) · [etcd](#etcd-snapshot-and-restore) · [CSR](#certificatesigningrequest) · [kubeadm](#kubeadm-cluster-and-certificates)

## Exam scope

- **Format:** Kubernetes v1.35, 2 hours, performance-based tasks on live clusters.
- **Weights:** Troubleshooting 30% · Cluster architecture, installation, configuration 25% · Services and networking 20% · Workloads and scheduling 15% · Storage 10%.
- **Official:** [CKA certification page](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/) · [CNCF curriculum repository](https://github.com/cncf/curriculum) · [Exam tips and permitted resources](https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad).
- **Gotcha:** the curriculum is versioned; re-check version and domains before scheduling.

## Discovery and imperative creation

Extract the exact field a task asks for; generate YAML rather than typing it. Docs:
[kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/) · [JSONPath](https://kubernetes.io/docs/reference/kubectl/jsonpath/) · [kubectl create](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#create)

```bash
kubectl get pods -A -o wide --sort-by=.spec.nodeName
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,IMAGE:.spec.containers[*].image
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.osImage}{"\n"}{end}'
kubectl get clusterroles --no-headers | wc -l   # kubectl JSONPath has no len()
kubectl explain deployment.spec.strategy --recursive

kubectl run web --image=nginx:alpine --restart=Never --dry-run=client -o yaml > pod.yaml
kubectl create deployment web --image=nginx:1.26 --replicas=2 --dry-run=client -o yaml
kubectl create cronjob nightly --image=busybox:1.36 --schedule='0 2 * * *' -- /bin/sh -c date
```

- `kubectl` flags must precede `--`; everything after it is the container command.
  `kubectl top` fails until Metrics Server is installed — an add-on problem.
- **Gotcha:** answers must be written client-side (`kubectl get ... > /root/out.txt`);
  a redirect placed after `kubectl exec --` writes inside the container instead.
- **Gotcha:** `apply` on an object made with `create`/`run` can conflict on managed
  fields, and immutable fields never update — use `kubectl replace --force` when a
  task requires changing one. [Job and CronJob fields](kubernetes-interview-guide.md#job-and-cronjob-fields).
- **Safety:** `kubectl replace --force` deletes and recreates the object instead of
  patching it: downtime, a new Pod UID and IP, loss of `emptyDir` and other
  container-local data, and no rollback. On a live workload prefer `kubectl edit`,
  `kubectl patch`, or a Deployment rollout.

## Placement: labels, taints, tolerations

Attract a Pod to a class of node and keep other Pods off it. Docs:
[Assigning Pods to nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) · [Taints and tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)

```bash
kubectl label node node01 disktype=ssd
kubectl taint node node01 dedicated=payments:NoSchedule    # trailing dash removes
```

```yaml
spec:
  nodeSelector: { disktype: ssd }
  tolerations:
    - { key: dedicated, operator: Equal, value: payments, effect: NoSchedule }
```

- **Gotcha:** a toleration only permits placement, it never attracts. A Pod
  carrying only the toleration can still land on any untainted node; pair it with
  `nodeSelector` or affinity when the task says "must run on". Effects and
  eviction: [Scheduling cycle and placement](kubernetes-interview-guide.md#scheduling-cycle-and-placement).

## Deployments and rollouts

Scale, update, watch, and roll back. Docs: [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

```bash
kubectl scale deployment/web --replicas=5
kubectl set image deployment/web nginx=nginx:1.27
kubectl rollout status deployment/web
kubectl rollout undo deployment/web --to-revision=2
kubectl annotate deployment/web kubernetes.io/change-cause='Upgrade nginx to 1.27'
```

- **Gotcha:** `--record` was removed; set `kubernetes.io/change-cause` yourself or
  `rollout history` shows `<none>`. `rollout undo` restores the Pod template only —
  ConfigMap, Secret, and Service changes made alongside it stay.

## Autoscaling workloads

Scale replicas from metrics. Docs: [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) · [HPA walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)

```bash
kubectl autoscale deployment web --cpu-percent=70 --min=2 --max=10
kubectl get hpa web -o wide && kubectl describe hpa web
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: web }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: web }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - { type: Resource, resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } } }
```

- **Gotcha:** utilization is a percentage of the container **request**, so a target
  with no CPU request reports `<unknown>` and never scales; Metrics Server must run.
- **Gotcha:** stop managing `replicas` in the manifest once an HPA owns it.
  Types: [Autoscalers](kubernetes-interview-guide.md#autoscalers) · [Requests, limits, and QoS](kubernetes-interview-guide.md#requests-limits-and-qos).

## DaemonSet and init containers

One Pod on every eligible node, typically a node agent. Docs:
[DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata: { name: node-web }
spec:
  selector: { matchLabels: { app: node-web } }
  template:
    metadata: { labels: { app: node-web } }
    spec: { containers: [{ name: nginx, image: "nginx:stable" }] }
```

- No generator exists: create Deployment YAML with `--dry-run=client -o yaml`,
  change `kind`, and delete `replicas`, `strategy`, and `status`.
- **Gotcha:** "every node" is not guaranteed — control-plane taints, selectors,
  and affinity still exclude nodes unless tolerated.

Init containers prepare data before the app container starts, through an
`emptyDir` both mount. Docs: [Init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)

```yaml
spec:
  initContainers:
    - { name: prepare, image: "busybox:1.36", volumeMounts: [{ name: work, mountPath: /work }],
        command: [sh, -c, 'echo Hello > /work/index.html'] }
  containers:
    - { name: web, image: "nginx:stable",
        volumeMounts: [{ name: work, mountPath: /usr/share/nginx/html }] }
  volumes: [{ name: work, emptyDir: {} }]
```

- Init containers run in order and must exit 0; a failing one holds the Pod in
  `Init:Error` or `Init:CrashLoopBackOff`.
- **Gotcha:** `emptyDir` dies with the Pod and is local to its node — scratch and
  container sharing only.

## Static Pods

A Pod the kubelet runs from a file on the node, which is how kubeadm runs the
control plane. Verify the directory first — `/etc/kubernetes/manifests` is a
convention. Docs: [Static Pods](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/)

```bash
sudo grep staticPodPath /var/lib/kubelet/config.yaml
systemctl cat kubelet | grep -i -- --pod-manifest-path

kubectl run static-busybox --image=busybox:1.36 --restart=Never \
  --dry-run=client -o yaml --command -- sleep 1000 \
  | sudo tee /etc/kubernetes/manifests/static-busybox.yaml
```

- The kubelet names the mirror Pod `<pod>-<node>`; delete the file, not the Pod.
- **Gotcha:** a manifest in the wrong path is silently ignored and an invalid one never
  reaches the API — read `journalctl -u kubelet` when it does not appear.

## Logs, exec, and triage

Read what a container did, and work outward on "fix the broken cluster" tasks.
Docs: [Debug running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)

```bash
kubectl logs web -n default --previous        # the instance that crashed
kubectl exec hr -n default -- nslookup mysql.payroll > /root/nslookup.out
kubectl describe pod web -n default
kubectl get events -n default --sort-by=.metadata.creationTimestamp
sudo journalctl -u kubelet -n 100 --no-pager && sudo crictl ps -a
```

- **Gotcha:** `--previous` is the only way to see why a `CrashLoopBackOff` container
  died; the current log belongs to the fresh instance. Events expire, so collect
  them first, and static Pod faults never surface as API errors.
- Distroless images and crash-before-exec Pods need ephemeral containers: [Investigation and live debugging](kubernetes-interview-guide.md#investigation-and-live-debugging) · [Symptom tables](kubernetes-interview-guide.md#symptom-tables).

## ConfigMap

Non-sensitive configuration from literals or files. Docs: [Configure a Pod to use a ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)

```bash
kubectl create configmap web-config --from-literal=APP_COLOR=darkblue
kubectl create configmap file-config --from-file=application=app.conf   # rename key
```

- **Gotcha:** plain `--from-file=app.conf` uses the file name as the key; use
  `key=path` when the task dictates it. Env values never change in a running process
  and `subPath` mounts never update:
  [Configuration and storage](kubernetes-interview-guide.md#configuration-and-storage).

## Helm and Kustomize

Install packaged charts, and layer overlays without templating. Docs:
[Using Helm](https://helm.sh/docs/intro/using_helm/) · [Kustomization](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)

```bash
helm template web ./charts/nginx -n web           # render a provided local chart
helm upgrade --install web ./charts/nginx -n web --create-namespace -f values.yaml
helm history web -n web && helm rollback web 1 -n web
kubectl kustomize ./overlays/prod                 # render
kubectl apply -k ./overlays/prod                  # apply
kubectl diff -k ./overlays/prod                   # preview against live state
```

- `helm upgrade --install` is idempotent; `--dry-run` validates against the cluster.
- **Gotcha:** `-k` needs a `kustomization.yaml` in that directory, and generated
  ConfigMap or Secret names carry a content hash that changes on every edit.
  Values: [Chart layout and values](kubernetes-interview-guide.md#chart-layout-and-values) · [Commands, rendering, and diff](kubernetes-interview-guide.md#commands-rendering-and-diff).

## Volumes, PV, and PVC

Bind a claim to one specific volume instead of the default StorageClass. Docs:
[Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) · [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata: { name: pv-log }
spec: { capacity: { storage: 100Mi }, accessModes: [ReadWriteOnce], storageClassName: "",
        persistentVolumeReclaimPolicy: Retain, hostPath: { path: /pv/log } }
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: log-claim }
spec: { accessModes: [ReadWriteOnce], volumeMode: Filesystem, storageClassName: "",
        resources: { requests: { storage: 50Mi } } }
```

- Binding needs compatible access mode, capacity, volume mode, and `storageClassName`;
  `storageClassName: ""` on both stops the default class provisioning.
- **Gotcha:** a `hostPath` volume is one directory on one node, so `ReadWriteOnce` is
  the honest access mode; `ReadWriteMany` may bind, but Pods on other nodes then see
  different local directories instead of shared data.
- **Gotcha:** it pins the Pod to that node and is a privilege-escalation vector; use
  a network or CSI volume for anything real.
- `Pending` with no events usually means a missing StorageClass, `Terminating` the
  in-use finalizer: [PV, PVC, StorageClass, CSI](kubernetes-interview-guide.md#pv-pvc-storageclass-csi).

## Dynamic provisioning with StorageClass

Let the provisioner create the PV when the claim appears. Docs: [Storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) · [Dynamic provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)

```bash
kubectl get storageclass && kubectl describe pvc data   # (default) marks the default class
```

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: { name: fast }
provisioner: rancher.io/local-path      # use the provisioner the cluster runs
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: data }
spec: { storageClassName: fast, accessModes: [ReadWriteOnce],
        resources: { requests: { storage: 1Gi } } }
```

- **Gotcha:** with `WaitForFirstConsumer` the PVC stays `Pending` until a Pod consumes
  it — expected, and it keeps the volume in a zone the Pod can reach.
- **Gotcha:** `provisioner`, `parameters`, and `reclaimPolicy` are immutable, so
  create a replacement class instead of editing one. Defaults come from the
  `storageclass.kubernetes.io/is-default-class` annotation.
  Static binding: [Volumes, PV, and PVC](#volumes-pv-and-pvc) · [PV, PVC, StorageClass, CSI](kubernetes-interview-guide.md#pv-pvc-storageclass-csi).

## Services and Ingress

Expose a workload internally and route external HTTP paths to it. Docs:
[Service](https://kubernetes.io/docs/concepts/services-networking/service/) · [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)

```bash
kubectl expose deployment web --port=80 --target-port=8080 --name=web
kubectl expose deployment web --type=NodePort --port=80 --name=web-np
kubectl get endpointslices -n default -l kubernetes.io/service-name=web
kubectl create ingress pong -n ing-internal --class=nginx \
  --rule='/hello*=hello:5678'   # the * suffix means pathType: Prefix
```

- **Gotcha:** an empty EndpointSlice means the selector matches nothing or the Pods
  are unready, while the Service itself still looks healthy.
- **Gotcha:** in hand-written Ingress YAML (`networking.k8s.io/v1`) `pathType` is
  mandatory, and `ingressClassName` must name an installed controller or the
  object is accepted but never programmed.

## Gateway API

Route ingress traffic with the Ingress successor. Docs: [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) · [HTTP routing guide](https://gateway-api.sigs.k8s.io/guides/http-routing/)

```bash
kubectl get crd | grep gateway.networking      # CRDs are not installed by default
kubectl get gatewayclass,gateway,httproute -A  # then inspect with describe
```

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: { name: web, namespace: infra }
spec:
  gatewayClassName: example                 # must match an installed GatewayClass
  listeners:
    - { name: http, protocol: HTTP, port: 80, allowedRoutes: { namespaces: { from: Same } } }
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: { name: hello, namespace: infra }
spec:
  parentRefs: [{ name: web }]
  rules:
    - matches: [{ path: { type: PathPrefix, value: /hello } }]
      backendRefs: [{ name: hello, port: 5678 }]
```

- **Roles:** GatewayClass is the cluster-scoped controller, Gateway the listener
  instance, HTTPRoute the namespaced rule attached through `parentRefs`.
- **Gotcha:** both apply cleanly even when no controller serves them — check the
  Gateway `Programmed` and HTTPRoute `Accepted` conditions.
- **Gotcha:** a route in another namespace attaches only if `allowedRoutes` permits
  it; cross-namespace backends need a ReferenceGrant. Ingress: [Exposure and traffic policy](kubernetes-interview-guide.md#exposure-and-traffic-policy).

## NetworkPolicy and cluster networking

Identify the CNI and Pod CIDR, then restrict who may reach a workload. Docs:
[Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) · [Cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) · [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.podCIDR}{"\n"}{end}'
kubectl get configmap kube-proxy -n kube-system -o yaml   # cluster CIDR, mode
ls /etc/cni/net.d/ && ip route && ip -brief address       # never assume ens3 or Weave
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: internal-client, namespace: default }
spec:
  podSelector: { matchLabels: { app: internal } }
  policyTypes: [Ingress, Egress]
  ingress:
    - from: [{ podSelector: { matchLabels: { app: frontend } } }]
      ports: [{ protocol: TCP, port: 8080 }]
  egress:
    - to: [{ podSelector: { matchLabels: { app: mysql } } }]
      ports: [{ protocol: TCP, port: 3306 }]
    - to:                                   # DNS, or everything appears broken
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
          podSelector: { matchLabels: { k8s-app: kube-dns } }
      ports: [{ protocol: UDP, port: 53 }, { protocol: TCP, port: 53 }]
```

- **Gotcha:** omitting the DNS egress rule is the usual reason a default-deny
  namespace seems to break every application — resolution fails first and looks
  like an application bug. Confirm the label: some installs use `k8s-app: coredns`.
- **Gotcha:** `ingress: [{}]` allows every source and destroys the isolation the
  policy exists to create. A default-deny namespace is `podSelector: {}` plus
  `policyTypes: [Ingress, Egress]` with the `ingress` and `egress` keys omitted
  entirely.
- `namespaceSelector` and `podSelector` in the **same** list item are ANDed; as
  two items they are ORed, a far wider rule. Enforcement caveats:
  [NetworkPolicy](kubernetes-interview-guide.md#networkpolicy).

## RBAC

Grant a subject specific verbs and prove the result. Docs:
[Using RBAC authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

```bash
kubectl create role pod-editor -n default --verb=get,list,watch,create --resource=pods
kubectl create rolebinding dev-pod-editor -n default --role=pod-editor --user=developer
kubectl create clusterrole node-reader --verb=get,list,watch --resource=nodes
kubectl create clusterrolebinding user-node-reader --clusterrole=node-reader --user=new-user
kubectl auth can-i list nodes --as=new-user   # or: --list -n dev --as=system:serviceaccount:dev:app
```

- **Gotcha:** a `RoleBinding` that references a `ClusterRole` grants only inside its
  own namespace, and users and groups are not objects, so a misspelled subject
  binds successfully and fails silently — only `auth can-i` reveals it.
  Subresources need their own entry, such as `--resource=pods/exec`.

## Security context and capabilities

Run a container with the smallest privilege set the task allows. Docs:
[Set the security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

```yaml
spec:
  containers:
    - name: sleeper
      image: ubuntu:24.04
      command: [sleep, "4800"]
      securityContext:
        runAsUser: 0
        allowPrivilegeEscalation: false
        capabilities: { drop: [ALL], add: [SYS_TIME] }
```

- **Gotcha:** `SYS_TIME` is highly privileged and normally disallowed. Unless the
  runtime supplies a separate time namespace, the container changes the **node's**
  clock, breaking certificates, logs, and etcd leases for every workload on it.
- Use it only when a lab demands it. Container-level `securityContext` overrides
  the Pod-level one. Baseline:
  [Pod Security Standards and hardening](kubernetes-interview-guide.md#pod-security-standards-and-hardening).

## Node maintenance

Take a node out of service safely and return it. Docs:
[Safely drain a node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)

```bash
kubectl cordon node02
kubectl drain node02 --ignore-daemonsets --timeout=5m
kubectl uncordon node02   # after the repair, and after kubelet and runtime are healthy
```

- `--ignore-daemonsets` is required on any real cluster: DaemonSet Pods are never evicted.
- **Safety:** add destructive flags only after reading the stall message.

| Flag | Safety cost |
| :--- | :--- |
| `--delete-emptydir-data` | Permanently destroys that scratch data |
| `--force` | Deletes Pods with no controller; nothing recreates them |
| `--disable-eviction` | Bypasses PodDisruptionBudgets; emergencies only |

- A blocked drain is usually correct feedback: a PDB with no spare replica, or an
  unowned Pod. Trade-offs: [Cordon, drain, and uncordon](kubernetes-interview-guide.md#cordon-drain-and-uncordon).

## etcd snapshot and restore

Back up cluster state and recover it on a kubeadm control-plane node. Docs:
[Operating etcd clusters](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)

> **Single-member example**, the usual lab and exam topology. Restoring a
> multi-member cluster this way corrupts it: members restored independently form
> divergent clusters. For three or five members, stop etcd everywhere, restore
> the same snapshot separately on each member with that member's own `--name`
> and `--initial-advertise-peer-urls` plus the identical full `--initial-cluster`
> list, then start them together.

**1. Read the configuration and save a snapshot.** Take certificate paths, data
directory, and peer URLs from the live manifest. A save talks to a running etcd
and needs certificates; a restore is offline.

```bash
sudo grep -E 'data-dir|cert-file|key-file|advertise' /etc/kubernetes/manifests/etcd.yaml
etcdctl version && etcdutl version   # etcdutl is absent before etcd 3.5

ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key snapshot save /opt/etcd-backup.db

etcdutl snapshot status /opt/etcd-backup.db --write-out=table
```

**2. Restore into a new directory.** Use `etcdutl` on etcd 3.5 and later;
`etcdctl snapshot restore` is deprecated there and removed in 3.6.

```bash
sudo etcdutl snapshot restore /opt/etcd-backup.db \
  --name=controlplane --data-dir=/var/lib/etcd-from-backup \
  --initial-cluster=controlplane=https://127.0.0.1:2380 \
  --initial-advertise-peer-urls=https://127.0.0.1:2380 \
  --initial-cluster-token=etcd-restore
```

- **Gotcha:** `--name` must match the member name in the manifest and the target
  directory must not exist; restoring into the live data directory corrupts it.

**3. Point the static Pod at the restored data.** In
`/etc/kubernetes/manifests/etcd.yaml`, repoint the host side of the `etcd-data`
volume and leave `--data-dir` and `mountPath` untouched:

```yaml
  volumes:
    - { name: etcd-data,
        hostPath: { path: /var/lib/etcd-from-backup, type: DirectoryOrCreate } }  # was /var/lib/etcd
```

- **Gotcha:** the container flag, volume mount, and hostPath must stay consistent.
  Changing `--data-dir` without `mountPath` starts etcd on an empty directory and
  the cluster appears to have lost every object.

**4. Verify** with `sudo crictl ps | grep etcd` and `kubectl get nodes`. Saving the
manifest makes the kubelet recreate the Pod; if it does not restart, move the
manifest out, wait for the container to disappear, and move it back.

- Expect API errors for a minute while the control plane restarts. Port `2379` is
  client traffic, `2380` peer replication. Quorum: [etcd, quorum, and HA design](kubernetes-interview-guide.md#etcd-quorum-and-ha-design).

## CertificateSigningRequest

Issue a client certificate for a new user through the cluster CA. Docs:
[Certificate signing requests](https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/)

```bash
openssl genrsa -out john.key 2048
openssl req -new -key john.key -out john.csr -subj '/CN=john/O=developers'
base64 < john.csr | tr -d '\n'   # paste into spec.request below
```

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata: { name: john }
spec:
  request: REPLACE_WITH_BASE64_CSR
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages: [client auth]
```

```bash
kubectl apply -f john-csr.yaml && kubectl certificate approve john
kubectl get csr john -o jsonpath='{.status.certificate}' | base64 --decode > john.crt
```

- The common name becomes the username and each `O` a group; match them to the
  RBAC bindings you intend to create.
- **Gotcha:** base64 the CSR without line wrapping or it is rejected as malformed,
  and approval is authentication only — bind a Role separately.

## kubeadm cluster and certificates

Bootstrap a cluster and keep control-plane certificates valid. Docs:
[Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) · [kubeadm certs](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/) · [kubeadm upgrade](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)

```bash
sudo kubeadm certs check-expiration
sudo cp -a /etc/kubernetes/pki "/root/pki-backup-$(date +%F)"
sudo kubeadm certs renew apiserver
```

- Install a CNI whose supported range matches the cluster version and whose config
  matches the Pod CIDR passed to `kubeadm init`.
- **Gotcha:** renewal rewrites files but reloads nothing — certificates take effect
  only after the control-plane static Pods restart, and `kubeadm certs renew all`
  rewrites the client certificate in `admin.conf`, so redistribute kubeconfigs.
- Cautions and skew: [Control-plane certificates](kubernetes-interview-guide.md#control-plane-certificates) · [Upgrades and maintenance](kubernetes-interview-guide.md#upgrades-and-maintenance).
