# Kubernetes Operators & Advanced Scheduling – Interview Guide

This document covers **Operators, CRDs, webhooks, taints/tolerations, and affinity rules** for Kubernetes.

---

## 1. What Are Kubernetes Operators?

- Operators are **extensions of Kubernetes** that encode **domain-specific operational knowledge**.
- Automate tasks that humans normally do manually:
  - Deploying applications
  - Upgrading databases
  - Backups, scaling, failover
- Built using **Custom Resource Definitions (CRDs)** and **controllers**.
- Example: Postgres Operator, Prometheus Operator, Kafka Operator

**Interview One-liner:**  
> Operators make Kubernetes “smarter” by automating application-specific operations.

---

## 2. CRDs vs Controllers — How Do They Work Together?

| Component | Role |
|-----------|------|
| **CRD (CustomResourceDefinition)** | Extends the Kubernetes API with new resource types |
| **Controller** | Watches CRDs and reconciles the actual state with the desired state |

**Workflow Example:**
1. Define a **CRD** for `PostgresCluster`.
2. Deploy a **controller/operator** to watch `PostgresCluster` objects.
3. Operator ensures Pods, StatefulSets, services, backups match the desired spec.

**Interview One-liner:**  
> CRDs define new resource types; controllers/operators make them “live” and self-healing.

---

## 3. What Is a Mutating vs Validating Webhook?

| Webhook Type | Purpose | When to Use |
|--------------|--------|------------|
| **Mutating** | Can **modify** objects on creation/update | Add default labels, sidecars (e.g., Istio injection) |
| **Validating** | Can **accept/reject** objects based on rules | Enforce security policies, validate resource limits |

**Key Points:**
- Both are **admission controllers**
- Executed **before object is persisted** in etcd

**Interview One-liner:**  
> Mutating = modifies resources; Validating = approves or rejects resources.

---

## 4. Taints and Tolerations — Real Production Use Cases

- **Taints**: Mark nodes to repel certain Pods
- **Tolerations**: Allow Pods to schedule on tainted nodes
- Common use cases:
  - Reserve GPU nodes for GPU workloads only
  - Isolate critical workloads on dedicated nodes
  - Prevent scheduling on nodes under maintenance
- Example YAML:
  ```yaml
  spec:
    tolerations:
      - key: "gpu"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"

# Kubernetes GitOps & Deployment Strategies – Interview Guide

This document covers **GitOps concepts, Argo CD vs Flux, deployment sync, blue-green/canary deployments, and rollback strategies**.

---

## 1. What is GitOps in Kubernetes?

- GitOps is a **declarative approach** to cluster management.
- The **desired state of the cluster is stored in Git**.
- Changes to Git are automatically **applied to the cluster** via controllers.
- Benefits:
  - Version-controlled deployments
  - Auditability
  - Rollback via Git history
  - Reduced manual intervention

**Interview One-liner:**  
> GitOps = Kubernetes state stored in Git + automated synchronization.

---

## 2. Argo CD vs Flux — Which One and Why?

| Feature | Argo CD | Flux |
|---------|---------|------|
| Approach | Pull-based GitOps | Pull-based GitOps |
| UI | Web UI with dashboards | Minimal/no UI |
| Sync | Manual or automated | Automated |
| Multi-cluster | Built-in support | Multi-cluster via GitOps Toolkit |
| Popular Use Case | Teams that want visual deployment insights | Lightweight automation for infra-as-code |

**Interview Tip:**  
> Use **Argo CD** for visual control and multi-app GitOps dashboards; **Flux** for simple, automated GitOps pipelines.

---

## 3. How Does Argo CD Sync State With the Cluster?

- Argo CD monitors **Git repositories** containing manifests (YAML/Helm/Kustomize).
- It compares the **desired state (Git)** with the **actual state (cluster)**.
- Performs actions:
  - Apply missing resources
  - Update outdated resources
  - Delete drifted resources (if configured)
- Can operate in **manual** or **auto-sync** mode.

**Interview One-liner:**  
> Argo CD continuously ensures the cluster matches the Git repository state.

---

## 4. How Do You Implement Blue-Green or Canary Deployments in Kubernetes?

### Blue-Green Deployment
- Two identical environments: **blue (current)** and **green (new)**.
- Switch traffic from blue → green once new version is ready.
- Implement via:
  - Services (ClusterIP / LoadBalancer) pointing to the desired Deployment
  - Argo CD or manual rollout

### Canary Deployment
- Gradually roll out new version to a **subset of Pods**.
- Monitor metrics before full rollout.
- Implement via:
  - Kubernetes Deployment with `maxSurge`/`maxUnavailable`
  - Service routing (Istio, Linkerd, or Flagger)
  - Argo Rollouts

**Interview One-liner:**  
> Blue-Green = switch traffic between environments; Canary = gradual rollout with monitoring.

---

## 5. How Do You Rollback a Failed Deployment?

- Kubernetes tracks deployment history.
- Commands:
  ```bash
  # Rollback to previous revision
  kubectl rollout undo deployment <deployment-name>

  # Check rollout status
  kubectl rollout status deployment <deployment-name>
