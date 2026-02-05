# Kubernetes Stateful Workloads & Storage

<details>
<summary>When to Use Which - ConfigMaps vs Secrets?.</summary><br><b>

| Feature | ConfigMap | Secret |
|---------|----------|-------|
| Use Case | Non-sensitive configuration | Sensitive data (passwords, tokens, keys) |
| Storage | Plaintext in etcd | Base64-encoded in etcd |
| Consumption | Environment variables, volumes, command args | Environment variables, volumes, command args |
| Example | `APP_MODE=prod`, `LOG_LEVEL=debug` | DB password, TLS certs, API keys |

💡 Use ConfigMaps for general config, Secrets for anything sensitive. Always enable **encryption at rest** for Secrets in production.
</b></details>

<details>
<summary>How Are Secrets Stored in etcd?.</summary><br><b>

- Secrets are stored **base64-encoded** by default (not encrypted).
- Base64 is **not secure** — anyone with etcd access can decode.
- Best practice:
  - Enable **encryption at rest** for Secrets in etcd (`--encryption-provider-config`).
  - Limit access to API Server and etcd.

💡Secrets = base64 by default, encrypt at rest for production.
</b></details>

<details>
<summary>How Do StatefulSets Work Internally?.</summary><br><b>

- Designed for **stateful workloads** requiring stable identity.
- Key features:
  1. **Stable network identity**: Pods get predictable names (`<statefulset-name>-0`, `<statefulset-name>-1`, …).
  2. **Stable storage**: Each Pod can attach a unique PersistentVolume.
  3. **Ordered deployment & scaling**: Pods are created, updated, and deleted sequentially.
- Use cases: Databases, Kafka, Zookeeper, etc.

💡StatefulSets give Pods stable identity and persistent storage with ordered lifecycle management.
</b></details>

<details>
<summary>Headless Services — Why and When?.</summary><br><b>

- Created by setting `clusterIP: None`.
- No ClusterIP is assigned; DNS returns Pod IPs directly.
- Use cases:
  - StatefulSets needing direct Pod-to-Pod communication
  - Service discovery for clustered applications
  - Avoiding load balancing (each Pod is addressed individually)

💡Headless Services give **direct Pod access** without load balancing.
</b></details>

<details>
<summary>How Do PVCs, PVs, and StorageClasses Work Together?.</summary><br><b>

| Component | Role |
|-----------|------|
| **PersistentVolume (PV)** | Storage resource in cluster (NFS, EBS, GCE Persistent Disk) |
| **PersistentVolumeClaim (PVC)** | Request for storage by a Pod |
| **StorageClass** | Defines storage type, provisioner, parameters, and reclaim policy |

**Workflow:**
1. Developer creates PVC
2. StorageClass provisions a PV dynamically
3. Pod mounts the PV via PVC
4. Reclaim policy determines what happens after Pod deletion (`Retain`, `Delete`, `Recycle`)

💡PVC requests storage, PV provides it, StorageClass defines how it’s provisioned.
</b></details>

<details>
<summary>How Do You Handle Database Workloads in Kubernetes?.</summary><br><b>

- Use **StatefulSets** for stable identity
- Use **PersistentVolumes** with proper storage class (fast SSD for DBs)
- Avoid using ephemeral storage (`emptyDir`) for DBs
- Configure **readiness probes** to prevent traffic to uninitialized Pods
- Consider **Backup & Restore** solutions
- For HA, use **multi-zone deployments** or managed operators (Postgres Operator, MySQL Operator)
- Prefer **separate node pools** for database workloads to avoid noisy neighbors
  
💡Databases in Kubernetes = StatefulSets + PersistentVolumes + careful HA, backup, and performance tuning.
</b></details>

🧠 Quick Summary

- ConfigMaps = non-sensitive config.
- Secrets = sensitive. Secrets must be **encrypted at rest**
- StatefulSets provide stable identity and storage
- Headless Services allow **direct Pod DNS resolution**
- PVC + PV + StorageClass = request → storage → provision
- DB workloads need **stateful, HA-aware, properly backed storage**

