<details>
<summary> 🌐  Networking Fundamentals: Core Protocols.</code></summary><br><b>

## 🏗️ 1. TCP (Transmission Control Protocol)
TCP is a **connection-oriented** protocol that ensures the **reliable**, ordered, and error-checked delivery of a stream of data.

*   **Mechanism:** Uses the **Three-Way Handshake** (SYN, SYN-ACK, ACK) to establish a session.
*   **Key Features:**
    *   **Reliability:** Retransmits lost packets.
    *   **Flow Control:** Ensures the sender doesn't overwhelm the receiver.
    *   **Ordering:** Packets are reassembled in the correct sequence.
*   **Best For:** Web browsing (HTTP/S), File transfers (FTP), SSH, and Database connections.

## 🚀 2. UDP (User Datagram Protocol)
UDP is a **connectionless**, "fire-and-forget" protocol. It sends data without establishing a formal connection.

*   **Mechanism:** No handshaking; it simply pours data onto the network.
*   **Key Features:**
    *   **Low Latency:** No overhead for retransmissions or acknowledgments.
    *   **Speed:** Extremely fast compared to TCP.
    *   **Unreliable:** If a packet is lost, it stays lost.
*   **Best For:** Video streaming (YouTube/Netflix), VoIP (Zoom/Teams), Online Gaming, and **DNS** (Port 53).

## 📧 3. SMTP (Simple Mail Transfer Protocol)
SMTP is the industry standard protocol for **sending** email messages across IP networks.

*   **Mechanism:** Operates at the **Application Layer (Layer 7)** over TCP ports 25, 465, or 587.
*   **Key Features:**
    *   **Push Protocol:** Used only to "push" mail from a client to a server or between servers.
    *   **Authentication:** Modern SMTP uses TLS to secure the transmission of credentials.
*   **Best For:** Outbound email communication (Note: POP3 or IMAP are used for *receiving*).

## 🔒 4. HTTPS (Hypertext Transfer Protocol Secure)
HTTPS is the secure version of HTTP. It uses **TLS (Transport Layer Security)** to encrypt communication.

*   **Mechanism:** Operates over **TCP Port 443**.
*   **Key Features:**
    *   **Encryption:** Protects data from eavesdropping.
    *   **Data Integrity:** Prevents data from being tampered with during transit.
    *   **Authentication:** Uses SSL/TLS Certificates to verify the server's identity.
*   **Best For:** Any modern web application, API communication, and E-commerce.


## 📁 5. FTP (File Transfer Protocol)
FTP is a standard network protocol used to transfer files between a client and a server.

*   **Mechanism:** Uses a **dual-channel** approach:
    *   **Port 21 (Command):** For sending commands (login, list, delete).
    *   **Port 20 (Data):** For the actual transfer of file data.
*   **Key Features:**
    *   **Stateful:** Maintains a session state.
    *   **Modes:** Supports **Active** and **Passive** modes (Passive is preferred in modern cloud environments to avoid firewall issues).
*   **Best For:** Bulk file uploads and website maintenance.
*   **Note:** Standard FTP is **unsecured** (plaintext). In production, **SFTP** (FTP over SSH) or **FTPS** (FTP over SSL) is mandated.

## 📊 Summary Comparison Matrix

| Protocol | OSI Layer | Port | Reliability | Primary Strength |
| :--- | :---: | :---: | :--- | :--- |
| **TCP** | 4 (Transport) | Variable | **High** | Guaranteed Delivery |
| **UDP** | 4 (Transport) | Variable | **Low** | Speed & Low Latency |
| **SMTP** | 7 (Application) | 25/587 | **High** | Email Transmission |
| **HTTPS** | 7 (Application) | 443 | **High** | Secure Communication |
| **FTP** | 7 | 20 / 21 | **High** | File Transfers |


## 💡

*   **TCP vs. UDP:** "I use **TCP** when every single bit of data is critical, like a database transaction. I use **UDP** when a few dropped frames don't matter as much as real-time speed, like in a Zoom call."
*   **On HTTPS:** "HTTPS is mandatory in modern DevOps; it provides the **Encryption** and **Trust** (via Certificates) necessary to protect user data from Man-in-the-Middle (MitM) attacks."
*   **DNS & UDP:** "DNS traditionally uses UDP because it's fast. If a DNS query fails, the application just retries, which is more efficient than the overhead of a full TCP handshake."
*   **On FTP Security:** "Standard FTP sends credentials in **plaintext**. In a secure DevOps pipeline, I would always advocate for **SFTP** to ensure data is encrypted via the SSH tunnel."
*   **Passive vs. Active FTP:** "In AWS/Cloud environments, we use **Passive FTP** because it allows the client to initiate the data connection, which is more compatible with Security Groups and Firewalls."

</b></details>

<details>
<summary> How many Subnets can you have per VPC?.</code></summary><br><b>

`200 Subnets per VPC`
</b></details>

<details>
<summary> ☁️ Cloud Service Models: IaaS vs. PaaS vs. SaaS.</code></summary><br><b>

📊 The "Pizza as a Service" Analogy
To simplify the management levels, think of making a pizza:
*   **IaaS (Infrastructure):** You buy the ingredients (flour, cheese, toppings). You have to bake it at home in your own oven.
*   **PaaS (Platform):** You order a pizza for delivery. The shop prepares and bakes it; you just provide the table and eat it.
*   **SaaS (Software):** You go to a restaurant. Everything is managed for you; you simply consume the meal.

⚖️ Comparison Table

| Feature | **IaaS** (Infrastructure As A Service) | **PaaS** (Platform As A Service) | **SaaS** (Software As A Service) |
| :--- | :--- | :--- | :--- |
| **You Manage** | OS, Middleware, Data, Apps | **Code** and **Data** only | Nothing (User access only) |
| **AWS Manages** | Virtualization, Servers, Disk | Runtime, OS, Hardware | The entire stack |
| **Flexibility** | Highest | Moderate | Lowest |
| **Complexity** | High (Maintenance heavy) | Low (Developer focused) | Zero (Consumer focused) |

**IaaS: [Amazon EC2](https://aws.amazon.com)**
*   **Context:** You get a virtual machine. You are responsible for patching the Linux/Windows OS, installing the web server, and managing the security of the instance.
*   **Other Examples:** [Amazon VPC](https://aws.amazon.com), [Amazon EBS](https://aws.amazon.com).

**PaaS: [AWS Elastic Beanstalk](https://aws.amazon.com)**
*   **Context:** You upload your code (`.zip` or `.jar`). AWS handles the deployment, capacity provisioning, load balancing, and auto-scaling automatically.
*   **Other Examples:** [AWS Lambda](https://aws.amazon.com) (Serverless PaaS), [Amazon RDS](https://aws.amazon.com).

**SaaS: [Gmail](https://www.gmail.com)**
*   **Context:** Ready-to-use application for video conferencing. You don't manage any servers or code; you just manage your user account.
*   **External Examples:** AWS Chime, Slack, Salesforce, Microsoft 365.

💡
When choosing between models, I consider the **Operational Overhead**. 

I recommend **IaaS (EC2)** when the application requires a specific custom OS configuration or legacy software that isn't supported on managed platforms. 

I prefer **PaaS (Lambda/App Runner)** for new microservices because it allows the team to focus on **Business Logic** rather than OS patching and infrastructure maintenance. 

**SaaS** is my choice for non-core business functions like email or chat to reduce the total cost of ownership."
</b></details>


<details>
<summary> ☁️ AWS RDS Troubleshooting Guide.</code></summary><br><b>

🚀 Scenario 1: Connection Timeout (Network/Security)
*   **The Problem:** The application returns "Connection Timeout" or "Host is unreachable."
*   **Root Causes:** 
    *   Missing **Security Group** inbound rules for the DB port (e.g., 3306 for MySQL, 5432 for Postgres).
    *   The DB is in a private subnet while the app is in a different VPC without **VPC Peering**.
    *   DB is not "Publicly Accessible" while the app is trying to connect from outside AWS.
*   **The Solution:**
    1.  **Trace Network:** Use the [VPC Reachability Analyzer](https://aws.amazon.com) to identify where the packet is dropped.
    2.  **Verify SGs:** Ensure the DB Security Group allows traffic from the **Application's Security Group ID** (best practice) rather than a fixed IP.
    3.  **Check NACLs:** Ensure Network ACLs for the subnet allow traffic on ephemeral ports.

📈 Scenario 2: 100% CPU Utilization
*   **The Problem:** The database becomes unresponsive; CloudWatch alarms trigger for sustained high CPU.
*   **Root Causes:** 
    *   **Expensive Queries:** Large table scans due to missing indexes.
    *   **Connection Bursts:** A sudden surge in application traffic.
*   **The Solution:**
    1.  **Analyze SQL:** Open [RDS Performance Insights](https://aws.amazon.com) to find the specific SQL queries contributing to the "Database Load."
    2.  **Emergency Kill:** Identify the process ID and run `CALL mysql.rds_kill(process_id)` or the Postgres equivalent to stop runaway queries.
    3.  **Optimization:** Add indexes or upgrade the [RDS Instance Class](https://aws.amazon.com) to a larger size.

💾 Scenario 3: "Storage Full" (Instance in Read-Only)
*   **The Problem:** The RDS instance status changes to `storage-full`. All write operations fail.
*   **Root Causes:** 
    *   Unexpected log file growth (General/Slow Query logs).
    *   Application data growth exceeding the provisioned `AllocatedStorage`.
*   **The Solution:**
    1.  **Immediate Fix:** Modify the instance to increase storage (e.g., from 100GB to 120GB). Note: This may impact performance during the modification.
    2.  **Proactive Fix:** Enable [RDS Storage Autoscaling](https://docs.aws.amazon.com) to let AWS increase space automatically.
    3.  **Cleanup:** Use `rds_modify_db_parameter_group` to reduce log retention periods.

🔄 Scenario 4: High Replication Lag
*   **The Problem:** Read Replicas are not in sync with the Primary, causing users to see stale data.
*   **Root Causes:** 
    *   Single-threaded replication on the replica cannot keep up with heavy multi-threaded writes on the primary.
    *   The Read Replica instance size is smaller than the Primary instance size.
*   **The Solution:**
    1.  **Monitor Metric:** Track the `ReplicaLag` metric in [Amazon CloudWatch](https://aws.amazon.com).
    2.  **Balance Sizing:** Ensure the Read Replica has the same CPU/RAM as the Primary.
    3.  **Optimize Writes:** Break down massive bulk updates/inserts into smaller batches to allow the replica to keep up.

🛠️ Quick Reference for RDS Administrators
| Task | AWS CLI Command / Action |
| :--- | :--- |
| **Check Status** | `aws rds describe-db-instances --db-instance-identifier <name>` |
| **Reboot Instance** | `aws rds reboot-db-instance --db-instance-identifier <name>` |
| **Create Snapshot** | `aws rds create-db-snapshot --db-instance-identifier <name> --db-snapshot-identifier <backup-name>` |
| **Modify Instance** | Use [RDS Console](https://console.aws.amazon.com) to change Instance Class/Storage |

</b></details>

<details>
<summary> ☁️ Impact of backups and replication on source RDS availability.</code></summary><br><b>

📊 Quick Impact Matrix

| Feature | Single-AZ Impact | Multi-AZ Impact |
| :--- | :--- | :--- |
| **Automated Backups** | Brief I/O suspension (seconds to minutes). | **No impact.** Backups are taken from the standby instance. |
| **Read Replica Creation** | Brief I/O suspension (~1 min) for the initial snapshot. | **No impact.** Initial snapshot is taken from the standby. |
| **Ongoing Replication** | N/A (Asynchronous). | **Minimal.** Synchronous replication adds slight write latency. |
| **Failover Events** | N/A (No standby exists). | **Brief Unavailability** (60–120s) during DNS retargeting. |
| **Maintenance/Patches** | **Full Downtime.** Instance is unavailable during update. | **Minimal.** Limited to the duration of the failover. |

🔍 Detailed Operational States

**I/O Suspension**
In **Single-AZ deployments**, RDS briefly freezes I/O to take a storage-level snapshot. While the instance status remains `Available` in the [Amazon RDS Console](https://console.aws.amazon.com), your application may experience connection timeouts or increased latency during this window.

**Synchronous vs. Asynchronous Replication**
*   **Multi-AZ Deployment:** Uses **synchronous replication** to ensure zero data loss. The primary instance waits for the standby to acknowledge writes before confirming to the application.
*   **Read Replicas:** Use **asynchronous replication**. The source database is never blocked waiting for the replica, but this can lead to [Replica Lag](https://docs.aws.amazon.com).

**Maintenance Windows**
During scheduled maintenance (e.g., OS patching):
*   **Multi-AZ:** AWS patches the standby instance first, performs a failover, and then patches the old primary. This limits unavailability to the failover window (~60-120s).
*   **Single-AZ:** The instance remains unavailable for the entire duration of the patching process.

💡 Best Practices for High Availability
1.  **Production Multi-AZ:** Always enable [Multi-AZ Deployments](https://aws.amazon.com) for production workloads to offload backup I/O and minimize maintenance downtime.
2.  **Monitor Replica Lag:** Use [Amazon CloudWatch](https://aws.amazon.com) to track the `ReplicaLag` metric. Significant lag can indicate that the replica instance is underpowered compared to the primary.
3.  **Optimize Backup Windows:** For Single-AZ instances, set the **Backup Window** to the lowest-traffic hours of the day to mitigate the impact of I/O suspension.
4.  **Test Failovers:** Periodically use the [Reboot with Failover](https://docs.aws.amazon.com) feature to ensure your application's connection logic (e.g., connection pooling) handles DNS changes correctly.
</b></details>

<details>
<summary> 🕒 Amazon RDS: Point-In-Time Recovery (PITR).</code></summary><br><b>

PITR allows you to restore a database instance to any specific second within your retention period. This is the primary defense against **human error** (e.g., accidental `DROP TABLE` or `DELETE` without a `WHERE` clause).

⚙️ 1. How PITR Works
PITR relies on two critical components:
1.  **Daily Snapshots:** Automated full backups of the entire DB instance.
2.  **Transaction Logs (Binary Logs):** RDS uploads your transaction logs to S3 every 5 minutes.

When you trigger a PITR, AWS identifies the **latest snapshot** before your requested time and then **replays the transaction logs** up to the exact second you specified.

🛠️ 2. Step-by-Step Recovery Scenario
*   **The Incident:** A developer accidentally ran a cleanup script that wiped the `users` table at **14:05:10 UTC**.
*   **The Goal:** Restore the database to its state at **14:05:00 UTC**.

Execution via [AWS Console](https://console.aws.amazon.com):
1.  In the RDS dashboard, select the database.
2.  Choose **Actions** -> **Restore to point in time**.
3.  Select **Latest restorable time** or **Custom** (Set to 14:05:00).
4.  Specify a **new DB instance identifier** (RDS always restores to a *new* instance; it never overwrites the existing one).
</b></details>

<details>
<summary>  📉 RPO vs. RTO: Business Side of Disaster Recovery.</code></summary><br><b>

In production environments, we measure the success of a Disaster Recovery (DR) strategy using two key metrics: **RPO** and **RTO**.

**RPO (Recovery Point Objective)** — "How much data can we afford to lose?"
*   **Definition:** The maximum targeted period in which data might be lost from an IT service due to a major incident.
*   **Focus:** Data Loss and Backup Frequency.
*   **Example:** If your RPO is **4 hours** and your last backup was at 12:00 PM, a crash at 3:59 PM is acceptable. A crash at 5:00 PM is a failure of the RPO.

**RTO (Recovery Time Objective)** — "How quickly must we be back online?"
*   **Definition:** The targeted duration of time and a service level within which a business process must be restored after a disaster.
*   **Focus:** Downtime and Recovery Speed.
*   **Example:** If your RTO is **1 hour**, your engineers must have the system fully operational within 60 minutes of the initial outage.

📊 Comparison Table
| Feature | RPO (Recovery Point Objective) | RTO (Recovery Time Objective) |
| :--- | :--- | :--- |
| **Question** | "When was the last backup?" | "How long until we are back?" |
| **Metric** | Amount of **Data/Time** | Amount of **Real-time/Clock** |
| **Optimization** | Increase backup frequency (Snapshots/Logs) | Automate recovery (Failover/IaC) |
| **Cost Factor** | More frequent backups = Higher Storage costs | Faster recovery = Higher Infrastructure costs |

🛠️ Real-World Application

**Scenario A: High-Frequency Trading (Critical)**
*   **Goal:** Zero data loss, near-instant recovery.
*   **Metrics:** RPO = 0 seconds | RTO = < 30 seconds.
*   **Solution:** [Multi-Region Active-Active](https://aws.amazon.com) architecture with synchronous data replication.

**Scenario B: Internal Reporting Tool (Non-Critical)**
*   **Goal:** Cost-effective recovery.
*   **Metrics:** RPO = 24 hours | RTO = 8 hours.
*   **Solution:** Daily [RDS Snapshots](https://docs.aws.amazon.com) and a standard restore process from S3.

💡
1.  **The Cost Trade-off:**  "The lower the RPO and RTO, the higher the cost. As a DevOps engineer, I work with stakeholders to find the balance between 'Five Nines' availability and budget constraints."
2.  **RPO is limited by Physics:** "In globally distributed systems, RPO is often limited by network latency. Synchronous replication (RPO=0) can slow down application performance due to the [CAP Theorem](https://en.wikipedia.org)."
3.  **Automation is Key for RTO:** "To meet strict RTOs, I use Infrastructure as Code (Terraform) and automated failover scripts to ensure we aren't manually configuring servers during an outage."</b></details>
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
<summary> AWS S3 Troubleshooting ?.</code></summary><br><b>

# 🪣 AWS S3: Troubleshooting & Design

### 1️⃣ Accidental Data Deletion
*   **The Scenario:** A critical production folder was accidentally deleted from an S3 bucket.
*   **Immediate Fix:** If [S3 Versioning](https://docs.aws.amazon.com) was enabled, simply remove the **Delete Marker** to restore the previous version.
*   **Production Prevention:** 
    1.  Enable **MFA Delete** to require a hardware token for permanent deletions.
    2.  Implement **S3 Object Lock** (WORM model) for compliance data to prevent any deletion for a fixed duration.

### 2️⃣ Cost Optimization (Massive Datasets)
*   **The Scenario:** Monthly S3 storage costs have spiked. You have 100TB+ of data with varying access patterns.
*   **The Solution:** 
    1.  **S3 Storage Class Analysis:** Use this to identify objects that aren't being accessed.
    2.  **S3 Lifecycle Policies:** Automate transitions (e.g., move to **S3 Glacier Deep Archive** after 90 days).
    3.  **S3 Intelligent-Tiering:** Use this for data with unknown or changing access patterns to automatically save costs.

### 3️⃣ Performance Bottlenecks (503 Slow Down)
*   **The Scenario:** Your application is making 10,000+ requests per second and receiving `503 Slow Down` errors.
*   **The Issue:** You have hit the partition limit (3,500 PUT/5,500 GET requests per second per prefix).
*   **Production Solutions:**
    1.  **Prefix Randomization:** Distribute high-volume traffic across multiple prefixes (folders).
    2.  **S3 Transfer Acceleration:** Use AWS edge locations for faster global uploads.
    3.  **CloudFront Integration:** Use [Amazon CloudFront](https://aws.amazon.com) to cache GET requests and reduce the direct load on the bucket.

### 4️⃣ Secure Cross-Account Access
*   **The Scenario:** An application in **Account A** needs to upload logs to a central bucket in **Account B**.
*   **The Solution:** 
    1.  **Bucket Policy:** Add a policy in Account B allowing `s3:PutObject` for the IAM Role in Account A.
    2.  **Ownership:** Ensure Account A uploads with the `bucket-owner-full-control` ACL so Account B can actually manage the objects.
    3.  **Access Points:** Use [S3 Access Points](https://aws.amazon.com) to simplify permissions for different cross-account teams.

### 5️⃣ Public Access Prevention
*   **The Scenario:** A security audit warns that several buckets might be accidentally exposed to the public.
*   **The Solution:**
    1.  **Block Public Access (BPA):** Enable this at the **Account Level** to override any individual bucket settings.
    2.  **IAM Policies:** Use `Condition` keys to enforce that only traffic from your **VPC Endpoint** can access the bucket.
    3.  **Amazon Macie:** Deploy [Amazon Macie](https://aws.amazon.com) to automatically discover and protect sensitive data (PII) at scale.

## 📊 S3 Storage Class Quick-Reference

| Storage Class | Durability | Min Duration | Ideal Use Case |
| :--- | :--- | :--- | :--- |
| **Standard** | 11 9s | None | Active, frequently accessed data. |
| **Intelligent-Tiering** | 11 9s | None | Changing or unknown access patterns. |
| **Standard-IA** | 11 9s | 30 Days | Long-lived, infrequently accessed data. |
| **Glacier Instant** | 11 9s | 90 Days | Archived data needing millisecond access. |
| **Glacier Deep Archive** | 11 9s | 180 Days | 12-hour retrieval (Lowest cost/Compliance). |

## 💡
*   **On Data Protection:** "I always implement **Replication (CRR/SRR)** across accounts to protect against regional disasters or account compromises."
*   **On Performance:** "S3 is horizontally scalable, but performance tuning starts with **Prefix Design** and **Multipart Uploads** for large files."
*   **On Security:** "I prefer **S3 Access Points** over massive Bucket Policies to keep permissions manageable and auditable."
</b></details>



<details>
<summary>  Diff types of EC2 instances ?.</code></summary><br><b>

* `General Purpose`: The most popular; used for web servers, development environments, etc.
* `Compute Optimized`: Good for compute-intensive applications such as some scientific modeling or high-performance web servers.
* `Memory Optimized`: Used for anything that needs memory-intensive applications, such as real-time big data analytics, or running Hadoop or Spark.
* `Accelerated Computing`: Include additional hardware (GPUs, FPGAs) to provide massive amounts of parallel processing for tasks such as graphics processing.
* `Storage Optimized`: Ideal for tasks that require huge amounts of storage, specifically with sequential read-writes, such as log processing.

📊 Instance Family Quick-Reference
Use the mnemonic **"FIGHT DR MCP X"** to remember the different families.

| Family | Prefix | Definition | Memory Hook | Ideal Workload |
| :--- | :---: | :--- | :--- | :--- |
| **General Purpose** | **M** | Main / Balanced | "M" for **M**id-range | Small/Med Databases, App Servers. |
| **General Purpose** | **T** | Turbo / Burstable | "T" for **T**iny / **T**emporary | Dev/Test, Low-traffic Web. |
| **Compute Optimized** | **C** | Compute | "C" for **C**PU | Batch Processing, High-perf Web. |
| **Memory Optimized** | **R** | RAM | "R" for **R**AM | In-memory DBs (Redis/SAP HANA). |
| **Memory Optimized** | **X** | Xtreme RAM | "X" for **X**tra Large Memory | Massive Enterprise DBs. |
| **Storage Optimized** | **I** | I/O Speed | "I" for **I**/O (NVMe) | NoSQL, Data Warehousing. |
| **Storage Optimized** | **D** | Density | "D" for **D**ense HDD | Hadoop, Log Processing. |
| **Accelerated** | **P** | Pictures (GPU) | "P" for **P**ixels / **P**ower | Machine Learning, AI Training. |
| **Accelerated** | **G** | Graphics | "G" for **G**raphics | Video Encoding, 3D Rendering. |
| **Accelerated** | **F** | FPGA | "F" for **F**ield Programmable | Hardware Acceleration, Genomics. |

💰 EC2 Pricing Models

| Model | Cost Savings | Use Case | Commitment |
| :--- | :--- | :--- | :--- |
| **On-Demand** | 0% (Base) | Short-term, unpredictable workloads. | None. |
| **Reserved (RI)** | Up to 72% | Steady-state, predictable workloads. | 1 or 3 Years. |
| **Spot Instances** | **Up to 90%** | Fault-tolerant, stateless batch jobs. | None (AWS can reclaim). |

💡Pro-Tip

**The "g" Suffix (Graviton)**
Mention that instances with a `g` (e.g., `M6g`) use [AWS Graviton Processors](https://aws.amazon.com). They offer up to **40% better price-performance** compared to Intel/AMD counterparts. This shows you are cost-conscious.

**CPU Credits (T-Series)**
Explain that `T` instances use a "credit" system. For production, you prefer `M` or `C` series because if a `T` instance runs out of [CPU Credits](https://docs.aws.amazon.com), its performance is throttled to a baseline, causing application latency.

**Spot Termination Handling**
When using **Spot Instances** for Kubernetes nodes, always mention using the [AWS Node Termination Handler](https://github.com). It catches the 2-minute interruption notice and gracefully drains pods before the node is reclaimed.

[EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
</b></details>

<details>
<summary> Reliability Metrics: SLI vs. SLO vs. SLA?.</code></summary><br><b>

| Metric | Full Name | Definition | Analogy | Who cares? |
| :--- | :--- | :--- | :--- | :--- |
| **SLI** | **Service Level Indicator** | specific metric used to measure performance | **Speedometer** | Engineers/SREs |
| **SLO** | **Service Level Objective** | target value or range for an SLI | **Speed Limit** | Engineers + Product |
| **SLA** | **Service Level Agreement** | legal contract with consequences for missing SLOs | **Traffic Fine** | Business + Customers |

### 🔍 Deep Dive with Examples
**SLI (Measurement)**
The actual "raw data" you are tracking.
*   **Examples:** Request Latency, Error Rate, System Throughput, Availability (Uptime).
*   **Formula:** `(Successful Events / Total Events) * 100`

**SLO (Internal Goal)**
The target your team agrees to meet to keep users happy.
*   **Example:** "99.9% of requests should have a latency < 200ms over a 30-day window."
*   **Pro-Tip:** If you meet your SLO, your users are happy. If you miss it, you stop new feature work to fix reliability (the **Error Budget**).

**SLA (External Promise)**
The commitment made to customers.
*   **Example:** "If availability drops below 99.5%, we will refund 10% of your monthly bill."
*   **Rule of Thumb:** Your **SLO** should always be stricter than your **SLA**. (e.g., Internal SLO 99.9%, External SLA 99.5%).
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


<details>
<summary> ⚡ AWS Lambda: Production Troubleshooting & Design.</code></summary><br><b>

Managing Lambda in production requires a deep understanding of concurrency, cold starts, and asynchronous event processing.

1️⃣ Addressing High Latency (Cold Starts)
*   **The Scenario:** Users report that the first request after a period of inactivity is significantly slower than subsequent ones.
*   **The Issue:** A **Cold Start** occurs when AWS must initialize a new execution environment (load runtime, load code) because no "warm" environments are available.
*   **Production Solutions:**
    1.  **Provisioned Concurrency:** Pre-warms a specified number of environments to ensure immediate response (best for latency-sensitive APIs).
    2.  **SnapStart (Java):** Specifically for Java runtimes, it snapshots the initialized environment to reduce startup time by up to 10x.
    3.  **Code Optimization:** Reduce package size, lazy-load dependencies, and choose lightweight runtimes like **Go, Python, or Node.js**.

2️⃣ Handling Throttling (429 Too Many Requests)
*   **The Scenario:** During a traffic spike, Lambda stops executing and returns `429` errors.
*   **The Issue:** You have hit the **Regional Concurrency Limit** (default 1,000).
*   **Production Solutions:**
    1.  **Reserved Concurrency:** Dedicate a specific portion of your limit to critical functions so they aren't starved by other functions in the account.
    2.  **Quota Increase:** Request a service quota increase from AWS Support for your region.
    3.  **Upstream Buffering:** Use **Amazon SQS** to buffer incoming requests and process them at a controlled rate via Lambda triggers.

3️⃣ Timeouts & Resource Optimization
*   **The Scenario:** A function processing S3 files or large datasets fails intermittently with "Task timed out."
*   **The Issue:** The function exceeds its maximum configured **Timeout** (max 15 mins) or runs out of **Memory**.
*   **Production Solutions:**
    1.  **Power Tuning:** Use [AWS Lambda Power Tuning](https://github.com) to find the "sweet spot" where memory and cost are balanced (more memory = more CPU).
    2.  **Orchestration:** If a task takes >15 mins, use [AWS Step Functions](https://aws.amazon.com) to break the process into smaller, stateful steps.
    3.  **API Gateway Limits:** Remember that API Gateway has a **29-second** timeout limit, even if the Lambda is configured for longer.

4️⃣ Error Handling & Retries
*   **The Scenario:** An SQS-triggered Lambda fails, and the same message keeps retrying, blocking the queue (Poison Pill).
*   **The Issue:** Unhandled exceptions lead to infinite loops or wasted execution time.
*   **Production Solutions:**
    1.  **Dead Letter Queues (DLQ):** Route failed events to an SQS queue or SNS topic after `X` retries for manual debugging.
    2.  **Report Batch Item Failures:** For SQS, return only the IDs of failed messages so that successful ones are deleted and only failed ones are retried.
    3.  **Idempotency:** Ensure code can run multiple times with the same input without side effects (crucial because Lambda guarantees *at-least-once* delivery).

5️⃣ VPC Networking & Internet Access
*   **The Scenario:** Your Lambda needs to access a private RDS database *and* a public 3rd party API (like Stripe).
*   **The Issue:** When a Lambda is attached to a **VPC**, it loses default internet access.
*   **Production Solutions:**
    1.  **NAT Gateway:** Route outbound traffic through a NAT Gateway in a public subnet.
    2.  **VPC Endpoints:** Use **PrivateLink** for AWS services (S3, DynamoDB, Secrets Manager) to keep traffic inside the AWS network and save NAT costs.
    3.  **Security Groups:** Apply strict Inbound/Outbound rules to the Lambda's ENI (Elastic Network Interface).

📊 Summary Cheat Sheet

| Symptom | Primary Solution | CloudWatch Metric |
| :--- | :--- | :--- |
| **High Initial Latency** | Provisioned Concurrency | `ProvisionedConcurrencySpilloverInvocations` |
| **Throttling (429)** | Reserved Concurrency / Quota Increase | `Throttles` |
| **Out of Memory** | Increase RAM (Scale vertically) | `Errors` |
| **Slow Integration** | SQS Buffering / Step Functions | `Duration` |
| **Connectivity Issues** | NAT Gateway / VPC Endpoints | `NetworkInterface` metrics |
</b></details>

