# CKA Lab Recipes

These commands are practice patterns. Confirm names, namespaces, Kubernetes
version, runtime, and paths in the exam or target cluster before running them.

## Fast discovery and output

```bash
kubectl get pods -A -o wide
kubectl get pods --show-labels
kubectl get pods -A --sort-by=.spec.nodeName
kubectl get pods -A \
  -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,IMAGE:.spec.containers[*].image
kubectl get nodes \
  -o custom-columns=NAME:.metadata.name,VERSION:.status.nodeInfo.kubeletVersion
kubectl get nodes \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.osImage}{"\n"}{end}'
kubectl get nodes \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.podCIDR}{"\n"}{end}'
kubectl get nodes \
  -o jsonpath='{range .items[*].status.addresses[?(@.type=="InternalIP")]}{.address}{"\n"}{end}'
kubectl top pods -A --sort-by=cpu
kubectl get pv --sort-by=.spec.capacity.storage
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

`kubectl top` requires the Metrics Server to be installed and healthy.

## Labels, selectors, and node placement

```bash
kubectl label node node01 disktype=ssd
kubectl get pods -n production -l app=foo
kubectl get pods -n production -l app=foo > /root/foo-pods.txt
kubectl taint node node01 dedicated=payments:NoSchedule
kubectl taint node node01 dedicated=payments:NoSchedule-
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-ssd
spec:
  nodeSelector:
    disktype: ssd
  tolerations:
    - key: dedicated
      operator: Equal
      value: payments
      effect: NoSchedule
  containers:
    - name: nginx
      image: nginx:stable
```

The toleration permits the taint; the selector attracts the Pod to matching
nodes.

## Create and manage workloads

```bash
kubectl run web --image=nginx:alpine --restart=Never
kubectl create deployment web --image=nginx:1.26 --replicas=2
kubectl expose deployment web --type=NodePort --port=80 --name=web
kubectl scale deployment/web --replicas=5
kubectl set image deployment/web nginx=nginx:1.27
kubectl rollout status deployment/web
kubectl rollout history deployment/web
kubectl rollout undo deployment/web
```

`--record` is no longer available. To record a change cause:

```bash
kubectl annotate deployment/web \
  kubernetes.io/change-cause='Upgrade nginx to 1.27'
```

### DaemonSet

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-web
spec:
  selector:
    matchLabels:
      app: node-web
  template:
    metadata:
      labels:
        app: node-web
    spec:
      containers:
        - name: nginx
          image: nginx:stable
```

### Init container sharing a volume

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-demo
spec:
  initContainers:
    - name: prepare
      image: busybox:1.36
      command: [sh, -c, 'echo "Hello" > /work/index.html']
      volumeMounts:
        - name: work
          mountPath: /work
  containers:
    - name: web
      image: nginx:stable
      volumeMounts:
        - name: work
          mountPath: /usr/share/nginx/html
  volumes:
    - name: work
      emptyDir: {}
```

### Static Pod

On a kubeadm control-plane node, static manifests are commonly under
`/etc/kubernetes/manifests`, but verify kubelet's
`staticPodPath` first.

```bash
kubectl run static-busybox --image=busybox:1.36 --restart=Never \
  --dry-run=client -o yaml --command -- sleep 1000 \
  > /etc/kubernetes/manifests/static-busybox.yaml
```

## Logs and exec

```bash
kubectl logs web -n default
kubectl logs web -n default --previous
kubectl exec web -n default -- cat /log/app.log
kubectl describe pod web -n default
```

Redirecting `kubectl exec` writes command output on the client:

```bash
kubectl exec hr -n default -- nslookup mysql.payroll \
  > /root/nslookup.out
```

For images without a shell, or Pods that crash before exec is possible, use
`kubectl debug` with an ephemeral container as described in
[kubernetes-interview-guide.md](kubernetes-interview-guide.md#debugging-with-ephemeral-containers).

## ConfigMap

```bash
kubectl create configmap web-config \
  --from-literal=APP_COLOR=darkblue \
  --from-literal=APP_NAME=demo
kubectl create configmap file-config --from-file=app.conf
kubectl create configmap file-config --from-file=application=app.conf
```

Secret-specific exercises are in [kubernetes-secrets-recipes.md](kubernetes-secrets-recipes.md).

## Storage

### Ephemeral shared volume

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cache
spec:
  containers:
    - name: app
      image: redis:7
      volumeMounts:
        - name: data
          mountPath: /data/redis
  volumes:
    - name: data
      emptyDir: {}
```

### PersistentVolume and claim

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-log
spec:
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ""
  hostPath:
    path: /pv/log
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: log-claim
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  storageClassName: ""
  resources:
    requests:
      storage: 50Mi
```

A `hostPath` volume is a directory on one node, so `ReadWriteOnce` is the honest
access mode. Declaring `ReadWriteMany` makes the PVC bind, but Pods scheduled on
different nodes then see different local directories rather than shared data.
Use a real network or CSI volume when multiple nodes must write.

The claim binds only when the access mode, capacity, volume mode, and
`storageClassName` are all compatible. Setting `storageClassName: ""` on both
objects avoids the default StorageClass provisioning a different volume.

Inspect protection and binding with:

```bash
kubectl describe pvc log-claim
kubectl get pvc log-claim -o jsonpath='{.metadata.finalizers}{"\n"}'
```

## Network discovery

```bash
kubectl get pods -n kube-system
kubectl get configmap kube-proxy -n kube-system -o yaml
kubectl get endpointslices -A
```

To identify the CNI, inspect CNI Pods/DaemonSets and, on the node,
`/etc/cni/net.d/`. To determine a node network, inspect `ip address` and
`ip route`; do not assume an interface name such as `ens3` or `weave`.

### NetworkPolicy: restrict an internal app to two backends

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-client
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: internal
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: payroll
      ports:
        - protocol: TCP
          port: 8080
    - to:
        - podSelector:
            matchLabels:
              app: mysql
      ports:
        - protocol: TCP
          port: 3306
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

Writing `ingress: [{}]` would allow traffic from every source and defeat the
isolation this policy is meant to create. When a task asks to allow nothing
inbound, keep `Ingress` in `policyTypes` and omit the `ingress` key entirely:

```yaml
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

The `namespaceSelector` above relies on the automatic
`kubernetes.io/metadata.name` label. Confirm the DNS Pod label in the cluster,
since some installations use `k8s-app: coredns`. Omitting the DNS egress rule is
the usual reason a default-deny namespace appears to break every application.

### Current Ingress API

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: pong
  namespace: ing-internal
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          - path: /hello
            pathType: Prefix
            backend:
              service:
                name: hello
                port:
                  number: 5678
```

## RBAC

```bash
kubectl create role pod-editor -n default \
  --verb=get,list,watch,create \
  --resource=pods
kubectl create rolebinding developer-pod-editor -n default \
  --role=pod-editor \
  --user=developer
kubectl auth can-i create pods -n default --as=developer

kubectl create clusterrole node-reader \
  --verb=get,list,watch \
  --resource=nodes
kubectl create clusterrolebinding user-node-reader \
  --clusterrole=node-reader \
  --user=new-user
kubectl auth can-i list nodes --as=new-user
```

Count resources without parsing table output:

```bash
kubectl get clusterroles -o jsonpath='{len(.items)}{"\n"}'
kubectl get clusterrolebindings -o jsonpath='{len(.items)}{"\n"}'
```

## Security context and capabilities

Adding `SYS_TIME` is highly privileged and usually disallowed. For a lab that
explicitly requires it:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: time-lab
spec:
  containers:
    - name: sleeper
      image: ubuntu:24.04
      command: [sleep, "4800"]
      securityContext:
        runAsUser: 0
        allowPrivilegeEscalation: false
        capabilities:
          drop: [ALL]
          add: [SYS_TIME]
```

This changes the node's time namespace unless runtime isolation provides a
separate time namespace. Never use it as ordinary application configuration.

## Node maintenance

```bash
kubectl cordon node02
kubectl drain node02 --ignore-daemonsets --timeout=5m
# Repair or upgrade the node.
kubectl uncordon node02
```

`--ignore-daemonsets` is needed on essentially every real cluster, since
DaemonSet Pods are not evicted. Add the destructive flags only when the drain
message shows they are required and the consequence is acceptable:

```bash
kubectl drain node02 \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --force
```

`--delete-emptydir-data` destroys `emptyDir` contents on that node, and
`--force` deletes Pods that have no controller, which means nothing recreates
them. `--disable-eviction` bypasses PodDisruptionBudgets and should stay out of
practice runs. The flag trade-offs are tabulated in
[kubernetes-interview-guide.md](kubernetes-interview-guide.md#cordon-drain-and-uncordon).

On the node:

```bash
sudo systemctl status kubelet
sudo journalctl -u kubelet
sudo systemctl restart kubelet
```

## etcd snapshot and restore

> **Single-member example.** Everything below assumes one etcd member on one
> control-plane node, which is the usual lab and exam topology. Restoring a
> multi-member cluster this way corrupts it: members restored independently form
> divergent clusters. For three or five members, stop etcd on every member,
> restore the same snapshot separately on each with that member's own `--name`
> and `--initial-advertise-peer-urls` plus the identical full `--initial-cluster`
> list, then start them together.

### 1. Read the running configuration

Never assume paths. Take the certificate paths, data directory, and peer URLs
from the live manifest, and check which tools this etcd version ships:

```bash
sudo grep -E 'data-dir|cert-file|key-file|trusted-ca-file|advertise' \
  /etc/kubernetes/manifests/etcd.yaml
kubectl -n kube-system get pod -l component=etcd \
  -o jsonpath='{.items[0].spec.containers[0].image}{"\n"}'
etcdctl version
etcdutl version   # absent on etcd releases older than 3.5
```

### 2. Save and verify a snapshot

```bash
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /opt/etcd-backup.db

etcdutl snapshot status /opt/etcd-backup.db --write-out=table
```

A snapshot save talks to a running etcd, so it needs endpoints and certificates.
A restore is an offline operation on the file and needs neither.

### 3. Restore into a new directory

Use `etcdutl` on etcd 3.5 and later; `etcdctl snapshot restore` is deprecated
there and removed in 3.6. On older releases, use
`ETCDCTL_API=3 etcdctl snapshot restore` with the same arguments.

```bash
sudo etcdutl snapshot restore /opt/etcd-backup.db \
  --name=controlplane \
  --data-dir=/var/lib/etcd-from-backup \
  --initial-cluster=controlplane=https://127.0.0.1:2380 \
  --initial-advertise-peer-urls=https://127.0.0.1:2380 \
  --initial-cluster-token=etcd-restore
```

`--name` must match the member name in the manifest, and the target directory
must not already exist. Restoring into the live data directory while etcd is
running will fail or corrupt the member.

### 4. Point the static Pod at the restored data

Edit `/etc/kubernetes/manifests/etcd.yaml`. The simplest correct change is to
repoint the host side of the `etcd-data` volume and leave the container's
`--data-dir` and `mountPath` untouched:

```yaml
  volumes:
    - name: etcd-data
      hostPath:
        path: /var/lib/etcd-from-backup   # was /var/lib/etcd
        type: DirectoryOrCreate
```

The container flag, the volume mount, and the hostPath must stay consistent. If
you instead change `--data-dir`, change `volumeMounts[].mountPath` to the same
value; a mismatch starts etcd on an empty directory and the cluster appears to
have lost all objects.

### 5. Verify

Saving the manifest makes kubelet recreate the etcd Pod. If it does not restart,
move the manifest out of the directory, wait for the container to disappear, and
move it back.

```bash
sudo crictl ps | grep etcd
kubectl -n kube-system get pods
kubectl get nodes
kubectl get deployments -A
```

The API server may return errors for a minute while etcd and the control-plane
Pods restart. Ports involved:

- `2379`: client traffic from the API server and administrative clients.
- `2380`: peer replication between etcd members.

## CertificateSigningRequest

Create a key and CSR, base64-encode the request without line wrapping, and use
the stable API:

```bash
openssl genrsa -out john.key 2048
openssl req -new -key john.key -out john.csr -subj '/CN=john/O=developers'
base64 < john.csr | tr -d '\n'   # paste this into spec.request
```

The common name becomes the username and each `O` becomes a group, so choose
them to match the RBAC bindings you intend to create.

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john
spec:
  request: REPLACE_WITH_BASE64_CSR
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages:
    - client auth
```

```bash
kubectl apply -f john-csr.yaml
kubectl certificate approve john
kubectl get csr john \
  -o jsonpath='{.status.certificate}' | base64 --decode > john.crt
```

Approval does not grant authorization; bind the resulting username through
RBAC separately.

## Kubeadm

Follow the documentation matching the intended Kubernetes minor version:
[Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/).
Install a maintained CNI whose supported version range matches the cluster and
whose configuration matches the Pod CIDR passed to `kubeadm init`.

### Control-plane certificates

```bash
sudo kubeadm certs check-expiration
sudo cp -a /etc/kubernetes/pki "/root/pki-backup-$(date +%F)"
sudo kubeadm certs renew apiserver
sudo kubeadm certs check-expiration
```

Renewal takes effect only after the control-plane static Pods restart, and
`kubeadm certs renew all` rewrites the client certificates embedded in
`admin.conf`. See
[kubernetes-interview-guide.md](kubernetes-interview-guide.md#control-plane-certificate-maintenance) for the
full procedure and its cautions.
