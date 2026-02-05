# Kubernetes Scheduler & Autoscaling

<details>
<summary>How the Scheduler Decides Where to Place a Pod?.</summary><br><b>

The Kubernetes scheduler uses a **two-step process: filtering and scoring**.

* **Filtering (Predicates):**   Removes nodes that cannot run the Pod:
  * Insufficient CPU or memory.
  * NodeSelector / NodeAffinity mismatch.
  * Taints not tolerated.
  * Volume or port conflicts.

* **Scoring (Priorities):**    Scores remaining nodes based on:
  * Resource availability.
  * Pod affinity / anti-affinity.
  * Topology spread constraints.
  * Balanced resource usage.

* **Binding:**
  * Highest-scoring node is selected.
  * Scheduler binds Pod to that node

**One-liner:**  Filters out invalid nodes, scores the rest, and picks the best fit.
</b></details>

<details>
<summary>Node Resource Handling: CPU & Memory.</summary><br><b>

* **CPU Exhaustion:**
  * CPU is compressible.
  * Pods are throttled but not killed.
  * Performance degrades.

* **Memory Exhaustion:**
  * Memory is not compressible.
  * Pods exceeding limits are OOMKilled.
  * Node enters `MemoryPressure` state.

* **Kubernetes Reaction:**
  * Kubelet evicts Pods based on:
  * QoS class (BestEffort → Burstable → Guaranteed).
  * Pod priority

**One-liner:**  CPU starvation throttles Pods; memory starvation kills them.
</b></details>

<details>
<summary>Requests, Limits, and QoS.</summary><br><b>

* **Requests:**
  * Used by the **scheduler**.
  * Determines where a Pod can be placed.
  * Reserved on the node.
 
* **Limits:**
  * Enforced by **kubelet**.
  * Maximum resources a Pod can consume.
  * Exceeding memory limit → OOMKill
  
**One-liner:**  Requests decide placement; limits decide enforcement.

* ** QoS Classes:**  QoS is a mechanism Kubernetes uses to decide which Pods to prioritize and which to **evict** when a Node runs out of resources (Memory or CPU).
  * Guaranteed
  * Burstable
  * BestEffort

Kubernetes assigns these automatically based on the `requests` and `limits` defined in the Pod spec.

🥇Guaranteed: Every container in the Pod must have both CPU and Memory **requests and limits** defined, and they must be **equal**. "The VIP."
*   **Eviction Priority:** Lowest. These are the last to be killed.
*   **Example Spec:**
    ```yaml
    resources:
      requests:
        cpu: "500m"
        memory: "1Gi"
      limits:
        cpu: "500m"
        memory: "1Gi"
    ```

🥈Burstable: The Pod has `requests` defined, but they are **less than** the `limits`, or one container doesn't have a limit.   "The Average Worker."
*   **Eviction Priority:** Medium. These are killed only if no `BestEffort` pods remain and they exceed their requested resources.
*   **Example Spec:**
    ```yaml
    resources:
      requests:
        memory: "512Mi"
      limits:
        memory: "1Gi"
    ```

🥉BestEffort: No `requests` or `limits` are defined for any container.
*   **Analogy:** "The Hitchhiker."
*   **Eviction Priority:** **Highest**. These are the first to be killed when the node feels any pressure.
*   **Example Spec:**
    ```yaml
    resources: {} # Empty
    ```

📊 2. Eviction Priority Matrix (The OOM Score)

When a node runs out of memory, the **OOM Killer** uses the [OOM Score](https://kubernetes.io) to decide who dies first:

| QoS Class | Scheduling | Eviction Order |
| :--- | :--- | :--- |
| **Guaranteed** | Resources are reserved 100%. | **Last** |
| **Burstable** | Guaranteed up to `request`. | **Second** |
| **BestEffort** | Uses whatever is left. | **First** |

🎯 3. Interview "Pro-Tips"

1.  **The "Request" is for Scheduling:** "I explain to the interviewer that the `request` is used by the **Scheduler** to find a node, while the `limit` is used by the **Kubelet** to manage the container at runtime."
2.  **Avoid BestEffort in Production:** "In a production environment, I always ensure critical microservices are **Guaranteed** or **Burstable** with high requests to prevent random evictions during minor traffic spikes."
3.  **CPU vs. Memory:** "I highlight that **CPU is a compressible resource**. If you hit a CPU limit, you are throttled (slowed down). **Memory is non-compressible**. If you hit a memory limit, you are OOMKilled (terminated)."
</b></details>

<details>
<summary>HPA vs VPA.</summary><br><b>

**HPA (Horizontal Pod Autoscaler)**
- Scales **number of Pods**
- Metrics: CPU, memory, custom metrics
- Best for **stateless workloads**

### VPA (Vertical Pod Autoscaler)
- Adjusts **CPU/memory requests**
- Pod restart required
- Best for **right-sizing workloads**

**Key Rule:**  
❌ Do not use HPA and VPA on the same resource simultaneously.
* Use HPA to scale out, VPA to size right.
</b></details>

<details>
<summary>Cluster Autoscaler.</summary><br><b>
  
Cluster Autoscaler adjusts **number of nodes**, not Pods.

**Scale Up**
- Trigger: Pods Pending due to resource shortage
- Adds a node to the node group
- Scheduler places Pods on new node

**Scale Down**
- Trigger: Nodes underutilized
- Pods can safely move elsewhere
- Node removed safely

**Safeguards**
- Respects PodDisruptionBudgets
- Avoids critical system Pods

**Key Point:**  Reacts to unschedulable Pods, not CPU usage.
</b></details>

> Kubernetes schedules Pods by filtering out incompatible nodes and scoring the rest. Requests determine placement while limits enforce runtime behavior. CPU pressure throttles Pods, memory pressure kills them. HPA scales the number of Pods, VPA adjusts resource sizes, and Cluster Autoscaler adds or removes nodes when Pods cannot be scheduled.

## Quick Reference Table

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
