# AWS 

<details>
<summary> How many Subnets can you have per VPC?.</code></summary><br><b>

`200 Subnets per VPC`
</b></details>

<details>
<summary> Relation between the Availability Zone and Region?.</code></summary><br><b>

Each Region is a separate geographic area. 

Availability Zones are multiple, isolated locations within each Region. 
</b></details>

<details>
<summary> What does AMI include?.</code></summary><br><b>

An AMI includes the following things:

* A template for the root volume for the instance.

* Launch permissions to decide which AWS accounts can avail the AMI to launch instances.

* A block device mapping that determines the volumes to attach to the instance when it is launched.
</b></details>

<details>
<summary> What does serverless mean to you ?.</code></summary><br><b>

Serverless is a cloud-native development model that allows developers to build and run applications without having to manage servers.

There are still servers in serverless, but they are abstracted away from app development. A cloud provider handles the routine work of provisioning, maintaining, and scaling the server infrastructure. Developers can simply package their code in containers for deployment.

Once deployed, serverless apps respond to demand and automatically scale up and down as needed. Serverless offerings from public cloud providers are usually metered on-demand through an event-driven execution model. As a result, when a serverless function is sitting idle, it doesn’t cost anything.
</b></details>

<details>
<summary> Different storage classes in AWS ?.</code></summary><br><b>

* `Amazon S3 Standard (S3 Standard)`
* `Amazon S3 Intelligent-Tiering (S3 Intelligent-Tiering)`
* `Amazon S3 Standard-Infrequent Access (S3 Standard-IA)`
* `Amazon S3 One Zone-Infrequent Access (S3 One Zone-IA)`
* `Amazon S3 Glacier (S3 Glacier)`
* `Amazon S3 Glacier Deep Archive (S3 Glacier Deep Archive)`
* `S3 Outposts storage class` : object storage to your on-premises AWS Outposts environment. Using the S3 APIs and features available in AWS Regions today, S3 on Outposts makes it easy to store and retrieve data on your Outpost, as well as secure the data, control access, tag, and report on it. S3 on Outposts provides a single Amazon S3 storage class, named S3 Outposts, which uses the S3 APIs, and is designed to durably and redundantly store data across multiple devices and servers on your Outposts.

[AWS S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
</b></details>

<details>
<summary>  Diff types of EC2 instances ?..</code></summary><br><b>

* `General Purpose`: The most popular; used for web servers, development environments, etc.
* `Compute Optimized`: Good for compute-intensive applications such as some scientific modeling or high-performance web servers.
* `Memory Optimized`: Used for anything that needs memory-intensive applications, such as real-time big data analytics, or running Hadoop or Spark.
* `Accelerated Computing`: Include additional hardware (GPUs, FPGAs) to provide massive amounts of parallel processing for tasks such as graphics processing.
* `Storage Optimized`: Ideal for tasks that require huge amounts of storage, specifically with sequential read-writes, such as log processing.

[EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
</b></details>

<details>
<summary>  Diff. between fault tolerance and Disaster recovery ?.</code></summary><br><b>

Fault tolerant design ensures that system is up and working even in faulty scenarios. When you app / business can afford some time otherwise High Availablity will be required if don’t want any downtime.

Disaster recovery ensures that in situation when there is damage beyond repair, system is able to preserve key data and bring up servers in same state. Disaster can be failure of components or entire physical infrastructure.

[fault tolerance and Disaster recovery](https://www.nakivo.com/blog/disaster-recovery-vs-high-availability-vs-fault-tolerance/)
</b></details>

<details>
<summary>  Diff. between Service Principal and Managed Identity ?.</code></summary><br><b>

Service principal is a security identity used by user-created apps, services, and automation tools to access specific Azure resources. 

- SP's are created manually by users/administrators through Azure portal, Azure CLI, PowerShell, or Azure SDKs.

- SP's are typically used in scenarios where an application needs to access Azure resources. They can be assigned roles and permissions, enabling applications to interact with Azure services securely.

- SP's are authenticated using either a client secret (a password) or a certificate. They can authenticate without the need for interactive sign-ins.

Managed identities for Azure resources, also known as Managed Service Identity (MSI), are a feature in Azure Active Directory that allow services to authenticate to cloud services (e.g., Azure Key Vault) without needing to insert credentials into the code.

- MI's are created directly on Azure resources (like Virtual Machines, App Services, Functions, etc.). There's no need for manual creation or management.

- MI's are used in scenarios where an Azure resource needs to access other Azure resources securely. The identity is automatically managed by Azure and doesn’t require explicit management by users.

- MI's use the Azure AD authentication flow. When enabled, Azure automatically handles the authentication process for the resource using the identity.

##Key Differences:

1.Creation and Management:
- Service Principal: Created manually and requires explicit management by the user.
- Managed Identity: Created directly on Azure resources, and Azure handles the management automatically.

2.Scope:
- Service Principal: Can be created for various scenarios and doesn’t have a specific scope in Azure.
- Managed Identity: Tied to a specific Azure resource and can only be used by that resource and its child resources.

3.Authentication:
- Service Principal: Requires manual configuration of authentication methods (client secret or certificate).
- Managed Identity: Authentication is automatically handled by Azure AD.

4.Use Cases:
- Service Principal: Typically used for broader scenarios where applications or services need to access various Azure resources.
- Managed Identity: Ideal for scenarios where a specific Azure resource (e.g., a VM or an App Service) needs secure access to other Azure resources.

[fault tolerance and Disaster recovery](https://www.nakivo.com/blog/disaster-recovery-vs-high-availability-vs-fault-tolerance/)
</b></details>

# ☁️ AWS RDS Production Troubleshooting Guide

This guide covers real-world failure scenarios for managed databases like Amazon RDS and Aurora. Use these structured answers to demonstrate your ability to handle database outages during SRE/DevOps interviews.

---

## 🚀 Scenario 1: Connection Timeout (Network/Security)
*   **The Problem:** The application returns "Connection Timeout" or "Host is unreachable."
*   **Root Causes:** 
    *   Missing **Security Group** inbound rules for the DB port (e.g., 3306 for MySQL, 5432 for Postgres).
    *   The DB is in a private subnet while the app is in a different VPC without **VPC Peering**.
    *   DB is not "Publicly Accessible" while the app is trying to connect from outside AWS.
*   **The Solution:**
    1.  **Trace Network:** Use the [VPC Reachability Analyzer](https://aws.amazon.com) to identify where the packet is dropped.
    2.  **Verify SGs:** Ensure the DB Security Group allows traffic from the **Application's Security Group ID** (best practice) rather than a fixed IP.
    3.  **Check NACLs:** Ensure Network ACLs for the subnet allow traffic on ephemeral ports.

## 📈 Scenario 2: 100% CPU Utilization
*   **The Problem:** The database becomes unresponsive; CloudWatch alarms trigger for sustained high CPU.
*   **Root Causes:** 
    *   **Expensive Queries:** Large table scans due to missing indexes.
    *   **Connection Bursts:** A sudden surge in application traffic.
*   **The Solution:**
    1.  **Analyze SQL:** Open [RDS Performance Insights](https://aws.amazon.com) to find the specific SQL queries contributing to the "Database Load."
    2.  **Emergency Kill:** Identify the process ID and run `CALL mysql.rds_kill(process_id)` or the Postgres equivalent to stop runaway queries.
    3.  **Optimization:** Add indexes or upgrade the [RDS Instance Class](https://aws.amazon.com) to a larger size.

## 💾 Scenario 3: "Storage Full" (Instance in Read-Only)
*   **The Problem:** The RDS instance status changes to `storage-full`. All write operations fail.
*   **Root Causes:** 
    *   Unexpected log file growth (General/Slow Query logs).
    *   Application data growth exceeding the provisioned `AllocatedStorage`.
*   **The Solution:**
    1.  **Immediate Fix:** Modify the instance to increase storage (e.g., from 100GB to 120GB). Note: This may impact performance during the modification.
    2.  **Proactive Fix:** Enable [RDS Storage Autoscaling](https://docs.aws.amazon.com) to let AWS increase space automatically.
    3.  **Cleanup:** Use `rds_modify_db_parameter_group` to reduce log retention periods.

## 🔄 Scenario 4: High Replication Lag
*   **The Problem:** Read Replicas are not in sync with the Primary, causing users to see stale data.
*   **Root Causes:** 
    *   Single-threaded replication on the replica cannot keep up with heavy multi-threaded writes on the primary.
    *   The Read Replica instance size is smaller than the Primary instance size.
*   **The Solution:**
    1.  **Monitor Metric:** Track the `ReplicaLag` metric in [Amazon CloudWatch](https://aws.amazon.com).
    2.  **Balance Sizing:** Ensure the Read Replica has the same CPU/RAM as the Primary.
    3.  **Optimize Writes:** Break down massive bulk updates/inserts into smaller batches to allow the replica to keep up.

---

## 🛠️ Quick Command Reference for RDS Administrators

| Task | AWS CLI Command / Action |
| :--- | :--- |
| **Check Status** | `aws rds describe-db-instances --db-instance-identifier <name>` |
| **Reboot Instance** | `aws rds reboot-db-instance --db-instance-identifier <name>` |
| **Create Snapshot** | `aws rds create-db-snapshot --db-instance-identifier <name> --db-snapshot-identifier <backup-name>` |
| **Modify Instance** | Use [RDS Console](https://console.aws.amazon.com) to change Instance Class/Storage |

---

**Next Interview Question:** Would you like to explore **Aurora Multi-Master** clusters or how to perform a **Point-In-Time Recovery (PITR)**?

