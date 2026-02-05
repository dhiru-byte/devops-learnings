# Kubernetes Operators & Advanced Scheduling

## 1. What Are Kubernetes Operators?

- Operators are **extensions of Kubernetes** that encode **domain-specific operational knowledge**.
- Automate tasks that humans normally do manually:
  - Deploying applications
  - Upgrading databases
  - Backups, scaling, failover
- Built using **Custom Resource Definitions (CRDs)** and **controllers**.
- Example: Postgres Operator, Prometheus Operator, Kafka Operator

💡Operators make Kubernetes “smarter” by automating application-specific operations.

## 2. CRDs vs Controllers — How Do They Work Together?

| Component | Role |
|-----------|------|
| **CRD (CustomResourceDefinition)** | Extends the Kubernetes API with new resource types |
| **Controller** | Watches CRDs and reconciles the actual state with the desired state |

**Workflow Example:**
1. Define a **CRD** for `PostgresCluster`.
2. Deploy a **controller/operator** to watch `PostgresCluster` objects.
3. Operator ensures Pods, StatefulSets, services, backups match the desired spec.

💡CRDs define new resource types; controllers/operators make them “live” and self-healing.

## 3. What Is a Mutating vs Validating Webhook?

| Webhook Type | Purpose | When to Use |
|--------------|--------|------------|
| **Mutating** | Can **modify** objects on creation/update | Add default labels, sidecars (e.g., Istio injection) |
| **Validating** | Can **accept/reject** objects based on rules | Enforce security policies, validate resource limits |

**Key Points:**
- Both are **admission controllers**
- Executed **before object is persisted** in etcd

💡Mutating = modifies resources; Validating = approves or rejects resources.

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

## 1. What is GitOps in Kubernetes?

- GitOps is a **declarative approach** to cluster management.
- The **desired state of the cluster is stored in Git**.
- Changes to Git are automatically **applied to the cluster** via controllers.
- Benefits:
  - Version-controlled deployments
  - Auditability
  - Rollback via Git history
  - Reduced manual intervention

💡GitOps = Kubernetes state stored in Git + automated synchronization.

## 2. Argo CD vs Flux — Which One and Why?

| Feature | Argo CD | Flux |
|---------|---------|------|
| Approach | Pull-based GitOps | Pull-based GitOps |
| UI | Web UI with dashboards | Minimal/no UI |
| Sync | Manual or automated | Automated |
| Multi-cluster | Built-in support | Multi-cluster via GitOps Toolkit |
| Popular Use Case | Teams that want visual deployment insights | Lightweight automation for infra-as-code |

💡Use **Argo CD** for visual control and multi-app GitOps dashboards; **Flux** for simple, automated GitOps pipelines.

## 3. How Does Argo CD Sync State With the Cluster?

- Argo CD monitors **Git repositories** containing manifests (YAML/Helm/Kustomize).
- It compares the **desired state (Git)** with the **actual state (cluster)**.
- Performs actions:
  - Apply missing resources
  - Update outdated resources
  - Delete drifted resources (if configured)
- Can operate in **manual** or **auto-sync** mode.

💡Argo CD continuously ensures the cluster matches the Git repository state.

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

💡 Blue-Green = switch traffic between environments; Canary = gradual rollout with monitoring.

## 5. How Do You Rollback a Failed Deployment?

- Kubernetes tracks deployment history.
- Commands:
  ```bash
  # Rollback to previous revision
  kubectl rollout undo deployment <deployment-name>

  # Check rollout status
  kubectl rollout status deployment <deployment-name>

## 🏷️ Kubernetes Annotations: 
Annotations are key-value pairs used to attach non-identifying metadata to Kubernetes objects. While labels are used for selection and grouping, annotations are used by tools, libraries, and external controllers to modify behavior.
These annotations are often used for documentation or managed by the Kubernetes control plane.

| Annotation | Description |
| :--- | :--- |
| `kubernetes.io/description` | Provides a human-readable description of the resource. |
| `deployment.kubernetes.io/revision` | Tracks the specific rollout revision of a Deployment. |
| `kubernetes.io/change-cause` | Records the command or reason for a change (e.g., used by `kubectl rollout history`). |
| `a8r.io/owner` | Identifies the team or individual responsible for the service. |
| `a8r.io/runbook` | A direct link to the operational runbook for the application. |

## 🌐 2. Ingress & Networking (Nginx Ingress)
Used to configure behavior for the [NGINX Ingress Controller](https://kubernetes.github.io).

| Annotation | Description |
| :--- | :--- |
| `kubernetes.io/ingress.class` | Specifies which ingress controller should handle this resource (e.g., `nginx`). |
| `nginx.ingress.kubernetes.io/rewrite-target` | Rewrites the target URI for the backend service. |
| `nginx.ingress.kubernetes.io/ssl-redirect` | Enforces a 301 redirect from HTTP to HTTPS. |
| `nginx.ingress.kubernetes.io/proxy-body-size` | Sets the maximum allowed size of the client request body (e.g., `50m`). |
| `nginx.ingress.kubernetes.io/affinity` | Enables session affinity (sticky sessions) via cookies. |
| `nginx.ingress.kubernetes.io/whitelist-source-range` | Limits access to specific client IP ranges (CIDR). |


## ☁️ 3. AWS Load Balancer Controller (ALB/NLB)
Used to configure [AWS Application and Network Load Balancers](https://kubernetes-sigs.github.io).

| Annotation | Description |
| :--- | :--- |
| `alb.ingress.kubernetes.io/scheme` | Defines if the ALB is `internet-facing` or `internal`. |
| `alb.ingress.kubernetes.io/certificate-arn` | Specifies the ARN of the SSL certificate from AWS Certificate Manager (ACM). |
| `alb.ingress.kubernetes.io/listen-ports` | Defines which ports the ALB listens on (e.g., `'[{"HTTP": 80}, {"HTTPS": 443}]'`). |
| `alb.ingress.kubernetes.io/target-type` | Sets backend targets as `instance` (NodePort) or `ip` (Pod IP). |
| `service.beta.kubernetes.io/aws-load-balancer-type` | Specifies the NLB type, often set to `nlb-ip` or `external`. |

## 📊 4. Monitoring & Prometheus
The de-facto standard for [Prometheus discovery](https://prometheus.io).

| Annotation | Description |
| :--- | :--- |
| `prometheus.io/scrape` | Signals Prometheus whether to scrape this Pod (`"true"`). |
| `prometheus.io/path` | Overrides the default metrics path (defaults to `/metrics`). |
| `prometheus.io/port` | Specifies the container port to scrape. |
| `prometheus.io/scheme` | Defines the protocol (`http` or `https`). |

## ⚙️ 5. Scaling & Infrastructure
Common annotations for the [Cluster Autoscaler](https://github.com) and Helm.

| Annotation | Description |
| :--- | :--- |
| `cluster-autoscaler.kubernetes.io/safe-to-evict` | If `"false"`, prevents the autoscaler from terminating the Pod during node drain. |
| `helm.sh/hook` | Defines lifecycle hooks (e.g., `pre-install`, `post-upgrade`) for Helm. |
| `helm.sh/resource-policy` | If set to `keep`, Helm will not delete this resource during an uninstall. |

## 💡 Best Practices
* **Strings Only:** All annotation values must be **strings** (e.g., `"true"` instead of `true`).
* **Metadata Context:** Always define annotations under the `metadata` section of your YAML.
* **Size Limit:** Individual annotations can be up to **256KB**, far larger than labels.

  
