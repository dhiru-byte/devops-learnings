# Kubernetes Scheduler & Autoscaling – Interview Guide

## 1. How the Scheduler Decides Where to Place a Pod

The Kubernetes scheduler uses a **two-step process: filtering and scoring**.

### Filtering (Predicates)
Removes nodes that cannot run the Pod:
- Insufficient CPU or memory
- NodeSelector / NodeAffinity mismatch
- Taints not tolerated
- Volume or port conflicts

### Scoring (Priorities)
Scores remaining nodes based on:
- Resource availability
- Pod affinity / anti-affinity
- Topology spread constraints
- Balanced resource usage

### Binding
- Highest-scoring node is selected
- Scheduler binds Pod to that node

**One-liner:**  
> Filters out invalid nodes, scores the rest, and picks the best fit.

---

## 2. Node Resource Handling: CPU & Memory

### CPU Exhaustion
- CPU is compressible
- Pods are throttled but not killed
- Performance degrades

### Memory Exhaustion
- Memory is not compressible
- Pods exceeding limits are OOMKilled
- Node enters `MemoryPressure` state

### Kubernetes Reaction
- Kubelet evicts Pods based on:
  - QoS class (BestEffort → Burstable → Guaranteed)
  - Pod priority

**One-liner:**  
> CPU starvation throttles Pods; memory starvation kills them.

---

## 3. Requests, Limits, and QoS

### Requests
- Used by the **scheduler**
- Determines where a Pod can be placed
- Reserved on the node

### Limits
- Enforced by **kubelet**
- Maximum resources a Pod can consume
- Exceeding memory limit → OOMKill

### QoS Classes
| Requests | Limits | QoS |
|----------|--------|-----|
| None     | None   | BestEffort |
| Set      | Not equal | Burstable |
| Equal    | Equal  | Guaranteed |

**One-liner:**  
> Requests decide placement; limits decide enforcement.

---

## 4. HPA vs VPA

### HPA (Horizontal Pod Autoscaler)
- Scales **number of Pods**
- Metrics: CPU, memory, custom metrics
- Best for **stateless workloads**

### VPA (Vertical Pod Autoscaler)
- Adjusts **CPU/memory requests**
- Pod restart required
- Best for **right-sizing workloads**

**Key Rule:**  
❌ Do not use HPA and VPA on the same resource simultaneously

**Interview Summary:**  
> Use HPA to scale out, VPA to size right.

---

## 5. Cluster Autoscaler

### How It Works
Cluster Autoscaler adjusts **number of nodes**, not Pods.

### Scale Up
- Trigger: Pods Pending due to resource shortage
- Adds a node to the node group
- Scheduler places Pods on new node

### Scale Down
- Trigger: Nodes underutilized
- Pods can safely move elsewhere
- Node removed safely

### Safeguards
- Respects PodDisruptionBudgets
- Avoids critical system Pods

**Key Point:**  
> Reacts to unschedulable Pods, not CPU usage.

---

## 6. 30-Second Interview Answer

> Kubernetes schedules Pods by filtering out incompatible nodes and scoring the rest. Requests determine placement while limits enforce runtime behavior. CPU pressure throttles Pods, memory pressure kills them. HPA scales the number of Pods, VPA adjusts resource sizes, and Cluster Autoscaler adds or removes nodes when Pods cannot be scheduled.

---

## 7. Quick Reference Table

| Topic | Key Insight |
|-------|-------------|
| Scheduler | Filter → Score → Bind |
| CPU Exhaustion | Throttling |
| Memory Exhaustion | OOMKill |
| Requests | Scheduling |
| Limits | Enforcement |
| HPA | Scale Pods |
| VPA | Resize Pods |
| Cluster Autoscaler | Scale Nodes |
