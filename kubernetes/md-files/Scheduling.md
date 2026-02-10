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
<summary>How to schedule pods across different nAcross Nodes & Zones?.</summary><br><b>

In production, how you distribute Pods determines your **High Availability (HA)** and **Resource Efficiency**. Kubernetes provides several mechanisms to attract or repel Pods from specific Nodes.

### 📊 Scheduling Strategies Comparison

| Strategy | Mechanism | Logic | Best Use Case |
| :--- | :--- | :--- | :--- |
| **Node Selector** | Direct Label Match | Binary (Yes/No) | Simple hardware needs (e.g., SSD vs HDD). |
| **Node Affinity** | Rules & Operators | Flexible/Soft | "Prefer ARM nodes, but fallback to Intel." |
| **Taints & Tolerations** | Repulsion | Exclusionary | Keeping generic pods off GPU or Master nodes. |
| **Pod Anti-Affinity** | Inter-Pod Interaction | Separation | **High Availability:** Spread replicas across Nodes/AZs. |
| **Topology Spread** | Skew Calculation | Balanced | Evenly distributing pods across 3+ Availability Zones. |

### 🏗️ 1. Node Selector (The Simple Approach)
`nodeSelector` is the most basic form of node constraint. It is a hard requirement; if no node matches the label, the Pod stays `Pending`.

### Step 1: Label the Node
```bash
kubectl label nodes worker-node-01 disktype=ssd
```
### Step 2: Define in Pod Spec

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-ssd
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disktype: ssd # Pod will ONLY land on nodes with this label
```
### 🚀 2. Node Affinity (The Advanced Approach)

Node Affinity expands on the basic `nodeSelector` by adding flexible logical operators (`In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt`) and the ability to define "Soft" vs "Hard" rules.

### Key Types:
*   **Required (Hard):** `requiredDuringSchedulingIgnoredDuringExecution` - The scheduler **must** find a matching node, or the Pod will remain in `Pending` state.
*   **Preferred (Soft):** `preferredDuringSchedulingIgnoredDuringExecution` - The scheduler will **try** to find a matching node, but will fallback to other nodes if necessary to ensure availability.

### Configuration Example (Hard Requirement):
This example ensures the Pod only lands in specific AWS Availability Zones.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: regional-affinity-pod
spec:
  containers:
  - name: app-container
    image: nginx
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-east-1a
            - us-east-1b
```
###🛡️ 3. Taints and Tolerations (The Isolation Approach)

Used to ensure Pods are not scheduled onto inappropriate nodes.
* **Taint:** Applied to a Node to repel Pods.
* **Toleration:** Applied to a Pod to allow it to "ignore" the taint.

```bash
# Taint a node to dedicate it to a specific team
kubectl taint nodes node1 team=payments:NoSchedule
```
```yaml
spec:
  tolerations:
  - key: "team"
    operator: "Equal"
    value: "payments"
    effect: "NoSchedule"
```

💡
>
* **On High Availability:** "I use Pod Anti-Affinity with topologyKey: kubernetes.io/hostname to ensure that no two replicas of a mission-critical microservice run on the same physical hardware."
* **On Resource Management:** "I use Node Selectors for specialized workloads like ML models that require GPU nodes, ensuring we don't waste expensive resources on generic web traffic."
* **On Dedicated Environments:** "I combine Taints and Node Affinity to create 'True Isolation'. The Taint keeps the general workloads out, and the Affinity pulls the specific team's workload in."
* **On Multi-AZ Resilience:** "For cloud-native apps, I prefer Topology Spread Constraints. It allows me to define a maxSkew, ensuring Pods are evenly balanced across Availability Zones even during scaling events."
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



