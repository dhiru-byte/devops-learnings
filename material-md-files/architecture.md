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

