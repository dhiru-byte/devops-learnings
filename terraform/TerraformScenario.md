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
