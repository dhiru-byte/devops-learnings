# Kubernetes Cluster Architecture & Design (L2 Interview Guide)

This document covers **Level-2 Kubernetes architecture and design questions**, focusing on how the control plane works, high availability, and multi-AZ design.

---

## 1. How Does the Kubernetes Control Plane Actually Work?

The Kubernetes control plane is a **state-driven control system**.

### Flow (High Level)
1. User submits a request (`kubectl`, API, controller)
2. **kube-apiserver** validates and authenticates the request
3. Desired state is stored in **etcd**
4. Controllers detect state changes and reconcile
5. Scheduler assigns Pods to Nodes
6. Kubelets execute workloads on Nodes

### Key Idea
> Kubernetes does not “do” things directly — it **continuously reconciles desired state with current state**.

---

## 2. What Happens When kube-apiserver Goes Down?

### Impact
- `kubectl` stops working
- No scaling, scheduling, or deployments
- Controllers and schedulers cannot read/write state

### What Still Works
- Existing Pods keep running
- Node-level workloads continue
- Services still route traffic

### Interview Summary
> If the API Server is down, Kubernetes becomes **read-only and blind**, but **already-running workloads survive**.

---

## 3. How Does etcd Ensure Consistency and Quorum?

etcd uses the **Raft consensus algorithm**.

### Key Concepts
- Strong consistency (CP system)
- Leader-based writes
- Majority quorum required

### Quorum Rule
(N / 2) + 1

| etcd Nodes | Quorum Needed |
|----------|---------------|
| 1 | 1 |
| 3 | 2 |
| 5 | 3 |

### Failure Behavior
- Writes fail if quorum is lost
- Reads may still succeed (depending on config)

### Interview Gold Line
> etcd prioritizes **consistency over availability**, which protects cluster correctness.

---

## 4. How Do You Design a Highly Available Kubernetes Cluster?

### Control Plane HA Design
- Multiple **kube-apiserver** instances
- Load balancer in front of API servers
- Multi-node **etcd cluster** (odd number)
- Redundant controller managers and schedulers

### Best Practices
- Minimum **3 control plane nodes**
- Separate etcd from worker nodes (production)
- Regular etcd backups

### Architecture

---

## 5. Difference Between Single-Master and Multi-Master Clusters

| Feature | Single-Master | Multi-Master |
|------|--------------|--------------|
| Availability | Low | High |
| Fault Tolerance | None | Yes |
| Production Ready | ❌ | ✅ |
| Complexity | Simple | Moderate |
| Use Case | Dev / Test | Production |

### Interview Verdict
> Single-master is for learning. Multi-master is for real workloads.

---

## 6. How Do You Design Kubernetes Across Multiple AZs?

### Goals
- Survive AZ failures
- Maintain quorum
- Ensure traffic availability

### Control Plane Design
- Spread control plane nodes across AZs
- Place etcd nodes across AZs carefully
- Avoid even-numbered etcd nodes

### Worker Node Design
- Node groups per AZ
- Pod anti-affinity rules
- Zone-aware scheduling

### Networking
- Load balancer spans AZs
- CNI supports multi-AZ routing
- Service traffic is zone-aware

### Example (3 AZs)


# kube-apiserver Failures (L3)

## Failure
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

## Failure
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

## Failure
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

## Failure
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

## Failure
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

## Failure
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

## Failure
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


