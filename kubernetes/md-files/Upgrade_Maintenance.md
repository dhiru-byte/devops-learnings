# Kubernetes Cluster Upgrades – Interview Guide

This document covers **safe cluster upgrades, control plane vs worker node upgrades, cordon/drain, and zero-downtime strategies**.

---

## 1. How Do You Safely Upgrade a Kubernetes Cluster?

**Step-by-Step Process:**
1. **Backup critical data**:
   - etcd snapshots
   - Cluster manifests
   - Custom resources
2. **Check cluster health**:
   - `kubectl get nodes`
   - `kubectl get pods --all-namespaces`
3. **Plan the upgrade path**:
   - Follow supported version skew (`master -> worker` difference)
   - Read release notes for deprecated APIs
4. **Upgrade control plane first**, then worker nodes.
5. **Verify workloads** after each step:
   - Pods running
   - Services reachable
   - Node status healthy

**Interview Tip:**  
> Always backup etcd, upgrade control plane first, then nodes, verifying cluster health after each step.

---

## 2. Control Plane vs Worker Node Upgrade Strategy

| Component | Upgrade Strategy | Notes |
|-----------|-----------------|------|
| **Control Plane** | Upgrade first | Ensure API Server, Controller Manager, Scheduler, etcd are upgraded sequentially |
| **Worker Nodes** | Upgrade later, one node at a time | Cordon and drain node, upgrade kubelet & container runtime, uncordon, move to next node |
| **Key Principle** | Maintain cluster availability | Don’t upgrade all nodes at once to avoid downtime |

**Interview One-liner:**  
> Upgrade control plane first, then workers sequentially with cordon/drain.

---

## 3. What is Cordon and Drain?

- **Cordon**
  - Marks a node as **unschedulable**
  - New Pods will **not be scheduled** on this node
  - Command:  
    ```bash
    kubectl cordon <node-name>
    ```
- **Drain**
  - Safely **evicts all Pods** from a node
  - Respects **PodDisruptionBudgets**
  - Prepares node for maintenance or upgrade
  - Command:  
    ```bash
    kubectl drain <node-name> --ignore-daemonsets
    ```

**Interview One-liner:**  
> Cordon = prevent new Pods, Drain = safely evict existing Pods.

---

## 4. How Do You Perform Zero-Downtime Upgrades?

**Key Strategies:**
1. **Upgrade one component at a time**:
   - Control plane nodes sequentially
   - Worker nodes one by one
2. **Use cordon & drain**:
   - Prevent scheduling and move workloads off the node
3. **Respect PodDisruptionBudgets**:
   - Ensure minimum replicas remain running
4. **Verify workloads** after each step:
   - Services reachable
   - Stateful applications are stable
5. **Rolling updates**:
   - Deploy updates without stopping entire service
6. **Monitor cluster health** throughout

**Interview One-liner:**  
> Zero-downtime upgrades = sequential upgrades + cordon/drain + PodDisruptionBudgets + careful monitoring.

---

## 🧠 Quick Interview Summary

| Concept | Key Point |
|---------|----------|
| Safe Upgrade | Backup etcd, upgrade control plane first, then workers |
| Control Plane Upgrade | Sequential, maintain API availability |
| Worker Node Upgrade | Cordon → drain → upgrade → uncordon |
| Cordon | Node unschedulable |
| Drain | Evict all Pods safely |
| Zero-Downtime | Sequential upgrades + PDB + monitoring |

