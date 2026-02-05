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
