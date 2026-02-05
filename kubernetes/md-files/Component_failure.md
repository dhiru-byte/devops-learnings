# Kubernetes Master Components Failure Scenario

<details>
<summary>  Kube-apiserver crashes or becomes unreachable. </summary><br><b>
   
*   **Impact:** **Total Management Blackout.** 
    * `kubectl` commands hang or fail.
    * Deployments do not scale.
    * New Resources are not created.
    * Worker nodes cannot report status.
    * Controllers stop reconciling.

*   **Existing Workloads:**  Existing Pods continue running. Node-level workloads stay alive. Service traffic continues.

*   **Root Causes**
    * CPU / memory exhaustion.
    * Expired TLS certificates.
    * etcd connectivity issues.
    *  Load balancer misconfiguration.

*  **Solution**
   * Restart API Server.
   * Check certificates and rotate if expired.
   * Validate etcd health.
   * Ensure load balancer health checks are correct.

*  **Prevention**
   * Run multiple API servers behind a load balancer.
   * Monitor API latency and error rates.
   * Enable audit and health endpoints.
</b></details>  

<details>
<summary>  etcd Failures, loses quorum or data corruption occurs.</summary><br><b>

*   **Impact:** **Cluster State Paralysis.**
    * The API Server becomes read-only, fails or unresponsive.
    * Writes to cluster state fail. No changes can be saved.
    * Pods cannot be created or updated.
      
*   **Existing Workloads:** Continue to run but cannot scale or self-heal.
 
*   **Root Causes**
    *  Loss of majority etcd nodes.
    *  Disk latency or disk full.
    *  Network partition between etcd members.
    *  Improper snapshot restore.

*  **Solution**
    *  Restore from snapshot if corruption occurs. Restore the state using `etcdctl snapshot restore`.
    *  Fix disk and network issues
    *  Maintain an odd number of members (3, 5, or 7) for [etcd clusters](https://kubernetes.io) and schedule frequent snapshots.

*  **Prevention**
   * Regular automated snapshots.
   * Dedicated disks for etcd.
   * Low-latency networking.
*  **Interview Line:**  etcd favors consistency over availability; without quorum, Kubernetes refuses to lie.
</b></details> 

<details>
<summary>  Kube-scheduler crashes or is unavailable. </summary><br><b>
  
*   **Impact:** **Scheduling Halt.** New pods remain in `Pending` state indefinitely.  No node assignment in Pod spec.
  
*   **Existing Workloads:** Unaffected.

*   **Root Causes**
    * Scheduler process crash.
    * Resource starvation.
    * Leader election issues.
  
*   **Solution:** 
    *   Check for leader election issues in logs.
    *   Validate RBAC permissions
    *   Verify the [Scheduler Configuration](https://kubernetes.io) for syntax errors.
    *   **Proactive Fix:** Run replicas with `--leader-elect=true`.

*  **Prevention**
   *  Run multiple schedulers with leader election.
   *  Monitor scheduling latency.
   *  Ensure adequate CPU/memory.
*  **Interview Line:**  Scheduler failure stops future workloads, not current ones.
</b></details>

<details>
<summary>  Controller Manager crashes or reconciliation stops.</summary><br><b>
  
*   **Impact:** **Loss of Self-Healing.** If a node fails, pods aren't rescheduled.  HPA stops working.
    * ReplicaSets stop healing Pods.
    * Jobs never complete.
    * Node failures not cleaned up.
   
*   **Existing Workloads:** Unaffected until a failure occurs.

*   **Root Causes**
    * Controller crash.
    * API Server communication issues.
    * Leader election failure.
   
*   **Solution:** 
    *   Check logs for RBAC/permission issues with the API server.
    *   Validate API Server connectivity.
    *   Restart controller manager.
    *   **Proactive Fix:** Ensure [High Availability](https://kubernetes.io) through leader election.

*  **Prevention**
   *  Multiple controller managers with leader election.
   * Alert on reconciliation lag.
*  **Interview Line:**  Without controllers, Kubernetes stops correcting reality.
</b></details>

<details>
<summary>  Node & Kubelet crashes or node becomes unreachable.</summary><br><b>

*   **Impact:**  Node shows NotReady.  Pods stop responding.  New Pods not scheduled on that node

*   **Root Causes**
    *   OS-level issues.
    *   Disk pressure.
    *    Kubelet crash.
    *    Network failure

*   **Solution:**
    * Restart kubelet.
    * Drain and reboot node.
    * Replace node if unrecoverable.

*  **Prevention**
   * Node auto-repair.
   * Health monitoring.
   * Pod disruption budgets
*  **Interview Line:** Kubelet failure removes a node from the cluster without killing the cluster.
</b></details>

<details>
<summary>  Networking & kube-proxy Failures, CNI plugin misbehaves.</summary><br><b>

*   **Impact:** Services exist but traffic fails.  Pod-to-Pod communication breaks.  DNS resolution works but connections fail.

*   **Root Causes**
    * iptables/ipvs corruption.
    * CNI misconfiguration.
    * Node networking issues.

*   **Solution:**
    * Restart kube-proxy.
    *  Restart CNI pods.
    *  Flush and rebuild iptables rules.

*  **Prevention**
   * Monitor Service latency.
   * Use proven CNI plugins.
   * Limit custom iptables rules
*  **Interview Line:**  Kubernetes networking failures are silent but deadly.
  
</b></details>

<details>
<summary>  Multi-AZ Failure, Entire Availability Zone goes down.</summary><br><b>
   
*   **Impact:**  Nodes in one AZ disappear.  Some Pods rescheduled.  Possible etcd quorum loss (bad design)

*   **Solution:**
    * Ensure control plane spread across AZs.
    * Use odd-numbered etcd members.
    * Rebalance workloads.

*  **Prevention**
   * AZ-aware scheduling.
   * Pod anti-affinity.
   * Zone-spread node groups
*  **Interview Line:**  Multi-AZ design is about surviving failure without losing quorum.
</b></details>

<details>
<summary>  Common Pod & Node Scenarios.</summary><br><b>
   
| Scenario | Symptom | Root Cause | Solution |
| :--- | :--- | :--- | :--- |
| **CrashLoopBackOff** | Pod restarts repeatedly | App bugs, missing env vars, or failed probes | Check `kubectl logs --previous` |
| **Pending Pod** | Pod never starts | Insufficient CPU/Mem or unbound PVC | Check `kubectl describe pod` events |
| **OOMKilled** | Exit Code 137 | Container hit memory `limit` | Increase [Resource Limits](https://kubernetes.io) |
| **503 Service** | App unreachable | Selector/Label mismatch or failing Readiness probe | Verify [Service Endpoints](https://kubernetes.io) |
| **Node NotReady** | Node goes offline | Kubelet crash or Disk/Memory pressure | Check `kubectl describe node` |

## 🔍 General Troubleshooting Workflow

1.  **Level 1:** `kubectl get pods -A` (Identify the failing resource)
2.  **Level 2:** `kubectl describe <resource> <name>` (Check Events and Status)
3.  **Level 3:** `kubectl logs <pod-name> [-p]` (Inspect application/component output)
4.  **Level 4:** `kubectl get events --sort-by=.metadata.creationTimestamp` (Timeline of cluster issues)
</b></details>

# ♾️ DevOps & Infrastructure Troubleshooting Guide

## 🛠️ Scenario 1: Terraform "State Lock" Failure
*   **The Problem:** During a deployment, Terraform fails with `Error acquiring the state lock`.
*   **Root Cause:** 
    *   A previous CI/CD job crashed before releasing the lock in the backend (e.g., AWS DynamoDB or Azure Blob).
    *   Concurrent runs by two different engineers or pipelines.
*   **The Solution:**
    1.  **Verify:** Ensure no other deployment is currently active to avoid state corruption.
    2.  **Identify:** Extract the `Lock ID` from the error message.
    3.  **Action:** Use the [Terraform Force-Unlock](https://developer.hashicorp.com) command: `terraform force-unlock <LOCK_ID>`.
    4.  **Prevention:** Implement pipeline locking or "concurrency" limits in GitHub Actions/GitLab CI.

## 🌐 Scenario 2: Cluster-Wide DNS Failures (CoreDNS)
*   **The Problem:** Microservices cannot communicate via Service names, but IP addresses work fine.
*   **Root Cause:** 
    *   CoreDNS pods are in `CrashLoopBackOff`.
    *   Upstream DNS servers are unreachable.
    *   Overloaded CoreDNS instances (CPU/Memory exhaustion).
*   **The Solution:**
    1.  **Check Logs:** Run `kubectl logs -n kube-system -l k8s-app=kube-dns`.
    2.  **Verify Endpoints:** Check `kubectl get ep kube-dns -n kube-system` to ensure the service is routing to active pods.
    3.  **Action:** Scale the [CoreDNS Deployment](https://kubernetes.io) or adjust resource limits. 
    4.  **Optimization:** Implement [NodeLocal DNSCache](https://kubernetes.io) to reduce the load on CoreDNS.

## 🔒 Scenario 3: SSL/TLS Certificate Expiry
*   **The Problem:** Users receive "Your connection is not private" errors. HTTPS traffic is blocked.
*   **Root Cause:** 
    *   `cert-manager` failed to complete the ACME challenge.
    *   Manual certificate secrets were not rotated.
    *   Cloud Load Balancer (ALB/GLB) certificate mapping is incorrect.
*   **The Solution:**
    1.  **Verify:** Use `openssl s_client -connect yourdomain.com:443` to check the expiry date.
    2.  **Debug Cert-Manager:** Check the status of the challenge: `kubectl get challenges`.
    3.  **Action:** Fix the ingress firewall rules if the [HTTP-01 challenge](https://cert-manager.io) is failing, or manually renew the secret as an emergency fix.

## 🏗️ Scenario 4: CI/CD Runner "No Space Left on Device"
*   **The Problem:** Pipelines fail during `docker build` or `npm install` steps due to disk exhaustion.
*   **Root Cause:** 
    *   Dangling Docker images and build caches accumulating on the self-hosted runner.
    *   Large log files or temporary build artifacts not being cleared.
*   **The Solution:**
    1.  **Cleanup:** Run `docker system prune -af` on the runner to clear unused data.
    2.  **Automate:** Implement a cronjob for [Docker Pruning](https://docs.docker.com) or use ephemeral runners (like Actions Runner Controller) that vanish after each job.
    3.  **Scale:** Increase the EBS volume size if the workload has permanently outgrown the runner size.

## 🔑 Scenario 5: IAM Permission "Silent Failure"
*   **The Problem:** An application that was working suddenly fails to access S3 buckets or Secrets Manager.
*   **Root Cause:** 
    *   The IAM Role/Policy was modified by another team.
    *   ServiceAccount tokens in Kubernetes failed to rotate (IRSA issues).
*   **The Solution:**
    1.  **Audit:** Check [AWS CloudTrail](https://aws.amazon.com) for `AccessDenied` events associated with the pod's role.
    2.  **Verify:** Use `aws sts get-caller-identity` from within the failing container to verify the active identity.
    3.  **Action:** Re-apply the [IAM Policy](https://docs.aws.amazon.com) with correct permissions and ensure the OIDC provider trust relationship is intact.

---

## 📊 Summary Table

| Issue | Primary Tool | Resolution |
| :--- | :--- | :--- |
| **State Lock** | Terraform CLI | `force-unlock` |
| **DNS Issues** | `nslookup` / `dig` | Scale CoreDNS / Check Endpoints |
| **Disk Full** | `df -h` / `docker` | `system prune` / Ephemeral Runners |
| **SSL Expired** | `cert-manager` | Check ACME Challenges / Fix Ingress |
| **IAM Denied** | CloudTrail | Fix IAM Policy / OIDC Trust |

---

**Follow-up:** Would you like to add a section on **Cost Optimization** troubleshooting, such as identifying "Orphaned Resources" (unattached EBS/EIPs)?



