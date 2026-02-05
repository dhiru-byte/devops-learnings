# Kubernetes Security & RBAC – Interview Guide

## 1. How Does Kubernetes RBAC Work?

- **RBAC (Role-Based Access Control)** manages **who can do what** in the cluster.
- Core components:
  1. **Role** / **ClusterRole**: Define permissions (verbs like get, list, create) on resources.
  2. **RoleBinding** / **ClusterRoleBinding**: Assign a Role/ClusterRole to a user, group, or ServiceAccount.
- RBAC enforcement happens at the **API Server**.
- Example: Limit a user to only view Pods in `dev` namespace.

💡RBAC is a way to enforce fine-grained access control in Kubernetes.

## 2. Role vs ClusterRole — Real-World Use Cases

| Component | Scope | Use Case |
|-----------|-------|---------|
| **Role** | Namespace-level | Allow `dev` team to manage Pods in `dev` namespace only |
| **ClusterRole** | Cluster-wide | Admins managing nodes or monitoring cluster resources across all namespaces |
| **RoleBinding** | Namespace-level | Assign a Role to a user/serviceaccount in that namespace |
| **ClusterRoleBinding** | Cluster-wide | Grant cluster-level permissions to a user/serviceaccount |

💡Roles = limited scope, ClusterRoles = global scope.

## 3. How Do ServiceAccounts Work?

- **ServiceAccounts** provide an **identity to Pods**.
- Automatically created in every namespace (`default` ServiceAccount).
- Used for **API authentication** (tokens mounted in Pods at `/var/run/secrets/kubernetes.io/serviceaccount/`).
- RBAC can bind **Roles/ClusterRoles** to ServiceAccounts.

💡ServiceAccounts give Pods a secure identity to access the API.

## 4. How Do You Secure etcd?

- etcd stores the **cluster state**, including Secrets — highly sensitive.
- Security measures:
  - Enable **TLS for client/server communication**
  - Enable **TLS peer-to-peer encryption** for etcd cluster nodes
  - Enable **etcd encryption at rest** for Secrets
  - Limit access to **API Server** and cluster admins
  - Backup regularly
  - Isolate etcd nodes on dedicated machines or VMs

💡Secure etcd with encryption, TLS, and limited access — it’s the heart of your cluster.

## 5. How Do Network Policies Work?

- Network Policies control **Pod-to-Pod communication**.
- Define **ingress and egress rules** using labels.
- Only enforced if **CNI plugin supports it** (e.g., Calico, Cilium).
- Example:
  - Allow only frontend Pods to reach backend Pods
  - Block all other traffic

💡Network Policies implement Kubernetes firewall rules at the Pod level.

## 6. How Do You Prevent Containers from Running as Root?

- SecurityContext controls Pod/Container privileges.
- Key fields:
  ```yaml
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    allowPrivilegeEscalation: false
