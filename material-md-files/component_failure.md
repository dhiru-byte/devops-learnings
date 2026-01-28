
# kube-apiserver Failures (L3)
kube-apiserver crashes or becomes unreachable.

## Symptoms
- `kubectl` commands hang or fail
- Deployments do not scale
- New Pods are not created
- Controllers stop reconciling

## What Still Works
- Existing Pods continue running
- Node-level workloads stay alive
- Service traffic continues

## Root Causes
- CPU / memory exhaustion
- Expired TLS certificates
- etcd connectivity issues
- Load balancer misconfiguration

## Fix
- Restart API Server
- Check certificates and rotate if expired
- Validate etcd health
- Ensure load balancer health checks are correct

## Prevention
- Run multiple API servers behind a load balancer
- Monitor API latency and error rates
- Enable audit and health endpoints

### Interview Line
> API Server failure blinds the control plane but does not immediately kill workloads.

# etcd Failures (L3)
etcd loses quorum or data corruption occurs.

## Symptoms
- API Server becomes read-only or fails
- Writes to cluster state fail
- Pods cannot be created or updated

## Root Causes
- Loss of majority etcd nodes
- Disk latency or disk full
- Network partition between etcd members
- Improper snapshot restore

## Fix
- Restore quorum by bringing nodes back
- Restore from snapshot if corruption occurs
- Fix disk and network issues

## Prevention
- Always use odd number of etcd nodes (3 or 5)
- Regular automated snapshots
- Dedicated disks for etcd
- Low-latency networking

### Interview Line
> etcd favors consistency over availability; without quorum, Kubernetes refuses to lie.


# Scheduler Failures (L3)
kube-scheduler crashes or is unavailable.

## Symptoms
- Pods remain in Pending state
- No node assignment in Pod spec
- Existing workloads unaffected

## Root Causes
- Scheduler process crash
- Resource starvation
- Leader election issues

## Fix
- Restart scheduler
- Check leader election lease
- Validate RBAC permissions

## Prevention
- Run multiple schedulers with leader election
- Monitor scheduling latency
- Ensure adequate CPU/memory

### Interview Line
> Scheduler failure stops future workloads, not current ones.


# Controller Manager Failures (L3)
Controller Manager crashes or reconciliation stops.

## Symptoms
- ReplicaSets stop healing Pods
- Jobs never complete
- Node failures not cleaned up

## Root Causes
- Controller crash
- API Server communication issues
- Leader election failure

## Fix
- Restart controller manager
- Validate API Server connectivity
- Check controller logs

## Prevention
- Multiple controller managers with leader election
- Alert on reconciliation lag

### Interview Line
> Without controllers, Kubernetes stops correcting reality.

# Node & Kubelet Failures (L3)
Kubelet crashes or node becomes unreachable.

## Symptoms
- Node shows NotReady
- Pods stop responding
- New Pods not scheduled on that node

## Root Causes
- OS-level issues
- Disk pressure
- Kubelet crash
- Network failure

## Fix
- Restart kubelet
- Drain and reboot node
- Replace node if unrecoverable

## Prevention
- Node auto-repair
- Health monitoring
- Pod disruption budgets

### Interview Line
> Kubelet failure removes a node from the cluster without killing the cluster.


# Networking & kube-proxy Failures (L3)
kube-proxy or CNI plugin misbehaves.

## Symptoms
- Services exist but traffic fails
- Pod-to-Pod communication breaks
- DNS resolution works but connections fail

## Root Causes
- iptables/ipvs corruption
- CNI misconfiguration
- Node networking issues

## Fix
- Restart kube-proxy
- Restart CNI pods
- Flush and rebuild iptables rules

## Prevention
- Monitor Service latency
- Use proven CNI plugins
- Limit custom iptables rules

### Interview Line
> Kubernetes networking failures are silent but deadly.


# Multi-AZ Failure Scenarios (L3)
Entire Availability Zone goes down.

## Symptoms
- Nodes in one AZ disappear
- Some Pods rescheduled
- Possible etcd quorum loss (bad design)

## Good Design Outcome
- Control plane survives
- etcd maintains quorum
- Traffic rerouted to healthy AZs

## Bad Design Outcome
- etcd loses quorum
- API Server becomes unavailable

## Fix
- Ensure control plane spread across AZs
- Use odd-numbered etcd members
- Rebalance workloads

## Prevention
- AZ-aware scheduling
- Pod anti-affinity
- Zone-spread node groups

### Interview Line
> Multi-AZ design is about surviving failure without losing quorum.


