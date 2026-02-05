# ☸️ Kubernetes Architecture & Design

This document covers Kubernetes architecture and design questions**, focusing on how the control plane works, high availability, and multi-AZ design.

<details>
<summary>  How Does the Kubernetes Control Plane Actually Work? </summary><br><b>

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

</b></details>

<details>
<summary>  What Happens When kube-apiserver Goes Down? </summary><br><b>
  
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

</b></details>

<details>
<summary>  How Does etcd Ensure Consistency and Quorum?. </summary><br><b>

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

</b></details>

<details>
<summary>  How Do You Design a Highly Available Kubernetes Cluster?. </summary><br><b>

### Control Plane HA Design
- Multiple **kube-apiserver** instances
- Load balancer in front of API servers
- Multi-node **etcd cluster** (odd number)
- Redundant controller managers and schedulers

### Best Practices
- Minimum **3 control plane nodes**
- Separate etcd from worker nodes (production)
- Regular etcd backups

</b></details>

<details>
<summary>  Difference Between Single-Master and Multi-Master Clusters. </summary><br><b>

| Feature | Single-Master | Multi-Master |
|------|--------------|--------------|
| Availability | Low | High |
| Fault Tolerance | None | Yes |
| Production Ready | ❌ | ✅ |
| Complexity | Simple | Moderate |
| Use Case | Dev / Test | Production |

### Interview Verdict
> Single-master is for learning. Multi-master is for real workloads.

</b></details>

<details>
<summary>  How Do You Design Kubernetes Across Multiple AZs? </summary><br><b>

**Goals**
- Survive AZ failures
- Maintain quorum
- Ensure traffic availability

**Control Plane Design**
- Spread control plane nodes across AZs
- Place etcd nodes across AZs carefully
- Avoid even-numbered etcd nodes

**Worker Node Design**
- Node groups per AZ
- Pod anti-affinity rules
- Zone-aware scheduling

**Networking**
- Load balancer spans AZs
- CNI supports multi-AZ routing
- Service traffic is zone-aware
</b></details>

## 🏗️The Request Flow
1. **Request:** A user or script sends a command via `kubectl`.
2. **Validate:** The `kube-apiserver` authenticates the user and validates the request.
3. **Persist:** The desired state is saved into **etcd**.
4. **Detect:** **Controllers** (e.g., Deployment Controller) notice the difference between etcd and reality.
5. **Schedule:** The **`kube-scheduler`** selects a healthy node with enough resources.
6. **Execute:** The **Kubelet** on the target node receives the instruction and starts the container.

## 📊 Quick Reference Table

| Category | Component / Concept | Interview-Ready Summary |
| :--- | :--- | :--- |
| **Source of Truth** | **etcd** | Distributed key-value store. If etcd is lost, the cluster state is lost. |
| **The Brain** | **API Server** | The only component that talks to etcd. If it’s down, the cluster is "blind." |
| **Consistency** | **Raft Quorum** | Rule: **$(N / 2) + 1$**. Always use odd numbers (3, 5) for etcd nodes. |
| **Resilience** | **HA Design** | Load Balancer ➡️ 3x API Servers ➡️ 3x etcd ➡️ Redundant Controllers. |
| **Multi-AZ** | **Zone Awareness** | Spread control plane nodes across AZs to survive a data centre outage. |
| **Scheduling** | **Anti-Affinity** | Use rules to ensure replicas of the same app aren't all in one AZ. |

💡 
*   **On etcd:** "etcd prioritizes **consistency over availability**; it would rather stop accepting writes than allow corrupted data."
*   **On Multi-AZ:** "Designing for Multi-AZ isn't just about nodes; it requires **topology-aware** routing and storage that understands zone boundaries."
*   **On systemd:** "The API server is the entry point, but `systemd` is often what keeps the `kubelet` itself running on the host."
