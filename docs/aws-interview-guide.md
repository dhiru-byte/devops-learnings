# AWS

- Pointer-style format: decision tables, one-line answers, commands, and failure
  signatures.
- Each section links to an official AWS User Guide and whitepaper.
- Protocol and OS fundamentals (OSI, TCP handshake, DNS, CIDR, HTTP status):
  [Linux interview guide](linux-interview-guide.md#networking-fundamentals).
- ML material: [AWS ML Associate guide](aws-ml-associate-study-guide.md).

- **Safety:** every `aws` command here is read-only unless marked `DESTRUCTIVE`.
- **Before a destructive operation:** use an approved change, name the non-production target, and confirm the account with `aws sts get-caller-identity`.

## Contents

**Foundations:** [Global infrastructure](#global-infrastructure) · [Cloud models and serverless](#cloud-models-and-serverless)

**Networking:** [VPC](#vpc-networking) · [SG vs NACL](#security-groups-vs-network-acls) · [NAT](#nat-gateway-vs-nat-instance) · [Peering](#vpc-peering) · [Endpoints](#vpc-endpoints) · [ELB](#elastic-load-balancing)

**Compute:** [EC2](#ec2) · [Storage](#ebs-vs-efs-vs-instance-store) · [Auto Scaling](#auto-scaling-and-launch-templates) · [ECS vs EKS](#ecs-vs-eks)

**Application services:** [S3](#s3) · [RDS](#rds) · [Lambda](#lambda) · [Messaging](#sqs-vs-sns-vs-eventbridge)

**Operations and security:** [CloudWatch](#cloudwatch) · [Route 53](#route-53) · [KMS](#kms) · [WAF vs Shield](#waf-vs-shield) · [Identity](#identity)

**Practice:** [Reliability and DR](#reliability-and-disaster-recovery) · [CI/CD](#cicd-on-aws)

## Global infrastructure

Docs: [Regions and Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) · Whitepaper: [Overview of Amazon Web Services](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)

| Term | One-liner |
| :--- | :--- |
| Region | Isolated geography (`eu-west-1`); nothing replicates out unless configured |
| Availability Zone | Discrete data centres, independent power/cooling/network, low-latency links |
| AZ ID | `use1-az1` is the physical zone; AZ *names* are per-account aliases, so `us-east-1a` differs across accounts |
| Edge location | CloudFront PoP for caching and connection termination |

Baseline HA is two or more AZs; multi-Region is a cost step change justified by
RPO/RTO. Say whether a limit is soft or hard: "200 subnets" is raiseable,
"`/28` minimum subnet" is not.

| Quota | Default | Adjustable |
| :--- | :--- | :--- |
| VPCs per Region | 5 | Yes |
| Subnets per VPC | 200 | Yes |
| VPC CIDR size | `/16` to `/28` | **No, hard limit** |
| Routes per route table | 50 | Yes, to 1000 |
| Security groups per ENI | 5 | Yes, to 16 |
| Lambda concurrency per Region | 1000 | Yes |

## Cloud models and serverless

Docs: [Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) · [Security Pillar: shared responsibility](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html) · Whitepapers: [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) · [Serverless Applications Lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html)

| | IaaS | PaaS | SaaS |
| :--- | :--- | :--- | :--- |
| You manage | OS, runtime, app, data | App code and data | Data and users only |
| AWS manages | Hardware, virtualisation, network | Everything under your code | Whole stack |
| Overhead | High | Low | None |
| Examples | EC2, EBS, VPC | Beanstalk, App Runner, Lambda, RDS | Chime, WorkMail |

- IaaS for a specific kernel, licensed software, or a legacy app; PaaS for new
  services so time goes on business logic; SaaS for non-differentiators.
- Shared responsibility: AWS secures *of* the cloud, you secure *in* it — data,
  IAM policies, guest OS patching, network configuration.
- **Serverless** means you deploy code or configuration and the provider
  provisions, scales, and patches the compute: event-driven, scaling to demand,
  billed per request and duration, idle costs nothing. Lambda, Fargate, API
  Gateway, DynamoDB on-demand, SQS, SNS, EventBridge, Step Functions.
- Serverless trade-offs: cold starts, Lambda's 15-minute ceiling, weaker local
  debugging, coupling to the event model, cost that wins at spiky load and loses
  against reserved capacity at high steady throughput.

## VPC networking

Docs: [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) · Whitepaper: [Building a Scalable and Secure Multi-VPC AWS Network Infrastructure](https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/welcome.html)

| Component | Role |
| :--- | :--- |
| VPC | Isolated network in one Region with a CIDR you choose |
| Subnet | CIDR inside the VPC, bound to exactly one AZ |
| Route table | Where traffic leaving a subnet goes; a subnet has exactly one |
| Internet gateway | Region-level, HA door to the internet; egress-only IGW for IPv6 |
| NAT gateway | Outbound IPv4 internet access for private subnets |
| Security group / NACL | Stateful firewall on ENIs / stateless firewall on subnets |
| VPC endpoint | Private access to AWS services without internet |
| VGW / Transit Gateway | On-premises connectivity, VPC-to-VPC at scale |

- **Public subnet** = route table has `0.0.0.0/0` → IGW and instances hold
  public or Elastic IPs. **Private subnet** = no IGW route; the default route
  points at a NAT gateway or does not exist.
- Three-tier layout per AZ: public (ALB, NAT, bastion), private app (EC2,
  containers, Lambda ENIs), private data (RDS, ElastiCache, no default route).
- Five addresses reserved per subnet — network, router `.1`, DNS `.2`, future
  `.3`, broadcast — so a `/28` yields 11 usable, not 14. Prefix arithmetic:
  [Linux interview guide](linux-interview-guide.md#ip-addressing-and-cidr).
- **Gotcha:** overlapping CIDRs across VPCs, accounts, or on-premises make
  peering, VPN, and Transit Gateway attachment impossible and can only be fixed
  by renumbering, so plan address space first.

## Security groups vs network ACLs

Docs: [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html) · [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html) · Whitepaper: [Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)

The answer interviewers want: **stateful versus stateless**.

| | Security group | Network ACL |
| :--- | :--- | :--- |
| Attaches to | ENIs, so effectively instances | Subnets |
| State | Stateful; return traffic auto-allowed | Stateless; return needs its own rule |
| Rules | Allow only | Allow and deny |
| Evaluation | All rules; any match allows | Ascending number, first match wins |
| Default | Deny inbound, allow outbound | Default NACL allows all; custom denies all |
| Sources | CIDR, prefix list, another security group | CIDR only |
| Scope | Only attached interfaces | Every resource in the subnet, no exceptions |
| Use for | Primary per-tier control | Coarse subnet guardrail, e.g. block an IP range |

- **Gotcha:** a stateless NACL needs outbound `1024-65535` for ephemeral return
  ports, so inbound 443 alone is not enough — the classic "the security group is
  open but nothing works" incident.
- A stateful SG still needs an **outbound allow** for traffic it initiates.
  Return traffic for allowed inbound is implicit; initiated egress is not.
- Reference **security group IDs**, not CIDRs, for tier-to-tier rules so scale
  events do not break connectivity.
- NACLs cover intra-subnet traffic and cannot be overridden per instance. Keep
  them simple: denies are silent and first match wins.
- Neither logs by itself. Enable **VPC Flow Logs** and use **Reachability
  Analyzer** to find the dropping hop.
- Inbound order: NACL in → security group in → host firewall. Outbound reverse.

## NAT gateway vs NAT instance

Docs: [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) · Whitepaper: [Amazon VPC Connectivity Options](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/welcome.html)

| | NAT gateway | NAT instance |
| :--- | :--- | :--- |
| Managed by | AWS | You: AMI, patching, monitoring |
| Bandwidth | 5 Gbps, scales to 100 Gbps | Bounded by instance type |
| Availability | Redundant within its AZ | Single instance; you build failover |
| Security groups | Not supported; filter at source or NACL | Supported |
| Port forwarding / bastion | Not possible | Possible |
| Source/dest check | N/A | Must be disabled on the ENI |
| Cost | Hourly plus per-GB processed | Instance plus data transfer |

- Default: NAT gateway. Use a NAT instance only for port forwarding, a
  dual-purpose bastion, or lower-cost dev usage.
- Flow: private route `0.0.0.0/0` → NAT gateway in a **public** subnet → IGW.
  The gateway rewrites the source to its Elastic IP and tracks the return flow.

- **Outbound-initiated only:** unsolicited inbound has no translation entry and
  is dropped; inbound needs a load balancer or a public IP in a public subnet.
- IPv6 needs no translation — use an **egress-only internet gateway**. For an
  IPv6-only client reaching IPv4 the gateway provides **NAT64** automatically:
  enable DNS64 on the subnet and route `64:ff9b::/96` to the gateway.
- **One NAT gateway per AZ**, each AZ's private route table pointing at its own;
  a shared gateway adds cross-AZ cost and makes one AZ failure kill all egress.
- Route S3, DynamoDB, and ECR traffic through **VPC endpoints** — pulling
  container images through NAT on every scale-out is a classic surprise bill.

| Symptom | Likely cause |
| :--- | :--- |
| No internet from private subnet | Private route table missing the NAT route |
| NAT gateway itself has no egress | Its subnet has no `0.0.0.0/0` → IGW |
| `ErrorPortAllocation` rising | Port exhaustion to a single destination |
| `IdleTimeoutCount` rising | Long-idle connections dropped at 350 s |
| Unexpected NAT data cost | AWS-service traffic not on VPC endpoints |

## VPC peering

Docs: [VPC Peering Guide](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) · [Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html)

- Private one-to-one VPC link on the AWS backbone; supports cross-account and
  cross-Region connectivity without a gateway or hardware.
- Setup requires all three: requester creates and accepter accepts; **both**
  VPCs add routes to the peer CIDR; both sides permit traffic in security groups
  by peer CIDR, or by peer security group ID within one Region.

- **CIDRs must not overlap** — there is no NAT in a peering connection — and
  peering is **not transitive**: A↔B and B↔C does not give A↔C.
- **No edge-to-edge routing:** you cannot use a peer's IGW, NAT gateway, VPN,
  Direct Connect, or gateway endpoint.
- **Does not scale.** Full mesh is n(n-1)/2 connections plus a route per peer;
  past a handful of VPCs use **Transit Gateway** (hub-and-spoke, transitive,
  route tables per attachment, VPN/DX attachment).
- Private DNS resolution across the peering is **off by default**. Same-Region
  peering has no per-GB peering charge (cross-AZ transfer still applies);
  inter-Region charges for transfer and is encrypted by AWS.
- Use **PrivateLink** to expose one service rather than join networks; it works
  with overlapping CIDRs.

## VPC endpoints

Docs: [AWS PrivateLink and VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) · Whitepaper: [Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)

| | Gateway endpoint | Interface endpoint (PrivateLink) |
| :--- | :--- | :--- |
| Services | S3 and DynamoDB only | Most AWS services, partner and your own |
| Mechanism | Route table entry with a prefix list | ENI with a private IP in your subnet |
| Cost | Free | Hourly per ENI plus per-GB |
| Control | Endpoint policy plus route table | Endpoint policy plus security group |
| Cross-Region / on-premises | No | Yes, via VPN or Direct Connect |

Two reasons to use them: cost, because traffic bypasses NAT data processing, and
security, because an endpoint policy plus an `aws:SourceVpce` bucket-policy
condition pins a bucket to your VPC.

## Elastic Load Balancing

Docs: [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) · [Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html) · Whitepaper: [Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)

| | ALB | NLB | GWLB |
| :--- | :--- | :--- | :--- |
| Layer | 7 | 4 | 3 plus GENEVE port 6081 |
| Protocols | HTTP, HTTPS, gRPC | TCP, TLS, UDP, TCP_UDP | IP packets |
| Routing | Host, path, header, query, method, weighted target groups | Destination port and flow | All packets through appliances |
| Targets | Instances, IPs, Lambda | Instances, IPs, ALBs | Firewall, IDS/IPS appliances |
| Client IP | `X-Forwarded-For` | Preserved to target | Preserved via encapsulation |
| Static IP | No, use the DNS name | One per AZ, EIP supported | Via GWLB endpoints |
| Choose for | Web apps, APIs, auth, content routing | High throughput, low latency, non-HTTP, fixed IPs | Transparent inspection appliances |

- ALB terminates TLS and can authenticate through OIDC/Cognito. NLB understands
  connections: databases, MQTT, UDP, source-IP preservation, allow-listed IPs.
  GWLB is not a frontend; it inserts an appliance fleet into a route path.
- All are Regional; use subnets in at least two AZs. Cross-zone is always on for
  ALB, configurable for NLB and GWLB.
- **Gotcha:** a shallow process-only health check sends users to an app that
  cannot reach its database, so health-check a dependency-aware endpoint —
  `aws elbv2 describe-target-health --target-group-arn <arn>`.

## EC2

Docs: [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) · [Instance types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html) · Whitepaper: [Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)

| Family | Prefix | Optimised for | Workload |
| :--- | :---: | :--- | :--- |
| General purpose | `M` | Balanced CPU/memory/network | App servers, small databases |
| Burstable | `T` | CPU credits | Dev/test, low-traffic web |
| Compute | `C` | High CPU per unit memory | Batch, encoding, HPC web |
| Memory | `R`, `X`, `U` | High to extreme memory | Caches, analytics, SAP HANA |
| Storage | `I`, `D`, `H` | Local NVMe IOPS, dense HDD | NoSQL, Hadoop, log processing |
| Accelerated | `P`, `G`, `F` | GPU training, inference, FPGA | ML, video, genomics |
| Accelerated | `Inf`, `Trn` | AWS custom silicon | Cheaper inference and training |

Suffixes: `g` Graviton/ARM (best price-performance, needs ARM builds), `a` AMD,
`i` Intel, `d` local NVMe, `n` enhanced network. **Gotcha:** exhausted `T` CPU
credits drop to a low baseline that reads as unexplained latency.

| Pricing model | Saving | Commitment | Use for |
| :--- | :--- | :--- | :--- |
| On-Demand | Baseline | None | Short-lived, unpredictable |
| Savings Plans | Up to 72% | 1 or 3 yr hourly spend | Steady spend, family/Region flexible |
| Reserved Instances | Up to 72% | 1 or 3 yr on attributes | Steady state, especially RDS |
| Spot | Up to 90% | None; 2-minute reclaim notice | Fault-tolerant, stateless batch |
| Dedicated Hosts | Varies | Per host | Core-bound licensing |

- Prefer Savings Plans over EC2 RIs. Spot suits Kubernetes workers running the
  AWS Node Termination Handler to drain pods; keep an On-Demand baseline so one
  capacity event cannot take the whole fleet.
- An **AMI** holds the root volume template, launch permissions, and the block
  device mapping, and is Region-scoped. Bake with Packer or EC2 Image Builder
  ("golden AMI") for faster launches than configuring at boot with user data.

## EBS vs EFS vs instance store

Docs: [Amazon EBS](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html) · [Amazon EFS](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html) · Whitepaper: [Performance Efficiency Pillar](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html)

| | EBS | EFS | Instance store |
| :--- | :--- | :--- | :--- |
| Model | Network block device | Managed NFS | Local NVMe/SATA |
| Scope | One AZ | Regional, many AZs | One physical host |
| Attachment | One instance, or Multi-Attach on supported types | Many Linux clients | Owning instance only |
| Persistence | Survives stop, and termination unless configured otherwise | Independent of clients | Lost on stop, terminate, host failure |
| Performance | Provisioned type, IOPS, throughput | Elastic shared throughput, network latency | Lowest latency, highest local IOPS |
| Use for | Boot volumes, databases, single-node state | Shared content, home directories | Cache, scratch, replicated data |

- EBS volume and instance must share an AZ; incremental snapshots can create
  volumes in another AZ or Region. EFS removes the single-writer restriction but
  is a filesystem, not a database block device.
- **Gotcha:** instance store data is unrecoverable after a stop or host failure,
  so use it only when the app can recreate or replicate every byte.

## Auto Scaling and launch templates

Docs: [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html) · Whitepaper: [Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)

- **ASG** holds desired capacity between min and max, replaces unhealthy
  instances, spreads across AZs. It is not the load balancer: the ASG owns
  capacity and lifecycle, the ALB/NLB owns traffic distribution.
- **Launch template** is the versioned recipe: AMI, type, security groups,
  instance profile, storage, metadata options, user data. Prefer it over launch
  configurations, which cannot be versioned and lack mixed instance policies.

| Policy | Use for |
| :--- | :--- |
| Target tracking | Default: hold 50% CPU or a requests-per-target target |
| Step scaling | Different capacity increments per alarm threshold |
| Scheduled | Known event at a known time |
| Predictive | Forecast recurring demand and pre-launch |

- **Scale-in risk:** use instance warm-up so new instances do not skew metrics.
- **Safe termination:** use lifecycle hooks to drain work and ship logs.
- **Health:** feed ALB checks into the ASG so it replaces an alive-but-not-serving process.

## ECS vs EKS

Docs: [Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html) · [Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html) · Whitepaper: [Implementing Microservices on AWS](https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices-on-aws.html)

| | ECS | EKS |
| :--- | :--- | :--- |
| Orchestrator | AWS-native | Managed Kubernetes control plane |
| Objects | Task definition, task, service | Pod, Deployment, StatefulSet, Service |
| Complexity | Lower, fewer components | Higher; Kubernetes skills required |
| Portability | AWS-specific API | Kubernetes API, portable |
| Compute | EC2 or Fargate | Managed node groups, self-managed nodes, Fargate |
| Choose for | AWS-only teams, least overhead | Kubernetes investment, portability, ecosystem |

- **Fargate is a compute option, not an orchestrator**: both ECS and EKS use it
  to run tasks or Pods without nodes; EC2 capacity costs patching and
  bin-packing but gives daemons, GPUs, and control.
- Give workloads task roles or IRSA/Pod Identity, never the broad node role, and
  spread replicas across AZs.

## S3

Docs: [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) · [Storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) · [S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

| Class | AZs | Minimum duration | Use for |
| :--- | :--- | :--- | :--- |
| Standard | 3+ | None | Active, frequent access |
| Intelligent-Tiering | 3+ | None | Unknown or changing patterns |
| Standard-IA | 3+ | 30 days | Infrequent, immediate retrieval |
| One Zone-IA | 1 | 30 days | Reproducible data, AZ loss acceptable |
| Express One Zone | 1 | 1 hour | Single-digit-ms latency, high request rate |
| Glacier Instant Retrieval | 3+ | 90 days | Archive with millisecond access |
| Glacier Flexible Retrieval | 3+ | 90 days | Archive, minutes to hours |
| Glacier Deep Archive | 3+ | 180 days | Compliance archive, 12 h, cheapest |

- All classes provide 11 nines of durability; One Zone variants store data within one AZ.
- **Gotcha:** minimum duration remains billable after deletion.
- **Cost check:** per-object transition overhead and retrieval fees can make Standard cheaper for millions of small objects.

- **Cost growth:** Storage Class Analysis or Storage Lens for what is really
  read, lifecycle rules to transition and expire, expiry of incomplete multipart
  uploads (invisible but billed), and **noncurrent versions** as a hidden cost.
- **Accidental deletion:** with versioning a delete only writes a delete marker,
  so removing it restores the object; without versioning it is gone.
  **DESTRUCTIVE caveat:** `s3 rm --recursive` and expiry rules on a
  non-versioned bucket are unrecoverable.
  - Enable versioning *before* it is needed and add **MFA Delete**.
  - Use **Object Lock** in compliance mode where retention is required.
  - Replicate cross-account so one compromised account cannot destroy both copies.
- **`503 Slow Down`:** ~3,500 write and ~5,500 read requests per second **per
  prefix**; partitions split automatically but not instantly. Spread keys across
  prefixes, ramp gradually, retry with backoff and jitter (SDK default), front
  reads with CloudFront, use multipart upload for large objects.
- **Cross-account writes:** bucket policy in B allows `s3:PutObject` for A's
  role; set `BucketOwnerEnforced` so ACLs are off and B owns uploads (legacy ACL
  buckets need `bucket-owner-full-control`); give consumers **Access Points**.
- **Preventing public exposure:** **Block Public Access at the account level**
  overrides bucket settings; require `aws:SecureTransport` and `aws:SourceVpce`;
  run **IAM Access Analyzer** and **Macie**; serve public content via CloudFront
  with Origin Access Control.

```bash
aws s3api get-bucket-versioning --bucket <bucket>
aws s3api get-public-access-block --bucket <bucket>
aws s3api list-object-versions --bucket <bucket> --prefix <key>
```

## RDS

Docs: [Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) · [Point-in-time recovery](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html) · Whitepaper: [Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)

| Symptom | Likely cause | First action |
| :--- | :--- | :--- |
| Connection **timeout** | SG missing inbound 3306/5432; cross-VPC with no path; stateless NACL blocking ephemeral return; not publicly accessible | Allow the app's **SG ID**, check NACL `1024-65535`, run Reachability Analyzer |
| Connection **refused** | Packet arrived, nothing listening | Wrong port or engine down — a different problem from timeout |
| Sustained 100% CPU | Missing index and full scans, connection surge, undersized class | Performance Insights → top SQL, then index or pool |
| `storage-full` | Data growth, unbounded logs, long transaction holding space | Increase storage, enable autoscaling, trim log retention |
| Replica lag | Single-threaded apply, undersized replica, bulk writes, blocking query | Alarm `ReplicaLag`, size replicas ≥ primary, batch writes |
| Stale reads | Async replica routing | Route only staleness-tolerant queries; Aurora for low-ms lag |

- Kill a runaway query with `CALL mysql.rds_kill(<id>)` or
  `SELECT pg_terminate_backend(<pid>)`. **DESTRUCTIVE:** rolls back in-flight
  work. Use **RDS Proxy** when connection churn, not query cost, is the driver.
- **DESTRUCTIVE caveat:** storage can be increased but **never decreased**, so
  oversizing to end an incident is permanent cost.

| Operation | Single-AZ | Multi-AZ |
| :--- | :--- | :--- |
| Automated backup | Brief I/O suspension | No impact; taken from standby |
| Create read replica | Brief I/O suspension for initial snapshot | No impact; from standby |
| Replica replication | Asynchronous, non-blocking | Asynchronous, non-blocking |
| Standby replication | N/A | Synchronous, small write latency |
| Failover | N/A | 60–120 s unavailable during DNS retargeting |
| Patching | Full downtime | Limited to a failover window |

- **Synchronous vs asynchronous** is the point: a Multi-AZ standby acknowledges
  every write before the primary confirms, giving RPO 0 at a write-latency cost;
  a read replica is async, never blocks the source, can lag, and is not a
  zero-data-loss target.
- Multi-AZ is **high availability, not read scaling** — the standby serves no
  traffic; replicas scale reads, do not fail over automatically, and can be
  promoted. Connect by DNS endpoint, never IP, and test failover.
- **PITR** restores to any second in the 1–35 day window from daily snapshots
  plus logs shipped every ~5 minutes, the defence against a `DELETE` with no
  `WHERE`. **Caveat:** it always restores into a **new instance**, so put
  verify-and-repoint in the runbook; restore time dominates RTO.

```bash
aws rds describe-db-instances --db-instance-identifier <name>
aws rds describe-events --source-identifier <name> --source-type db-instance
# DESTRUCTIVE: causes 60-120 s of downtime
aws rds reboot-db-instance --db-instance-identifier <name> --force-failover
```

## Lambda

Docs: [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) · [Lambda with VPC](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)

| Symptom | First action | Metric |
| :--- | :--- | :--- |
| Slow first request | Provisioned Concurrency, SnapStart | `InitDuration` |
| `429` throttling | Reserved Concurrency or quota increase | `Throttles` |
| Killed on memory | Raise memory, which raises CPU too | `MaxMemoryUsed` in logs |
| Timeout on long work | Step Functions or Fargate | `Duration` |
| No internet access | NAT gateway or VPC endpoint | SDK error logs |
| Queue stuck on one message | DLQ plus `ReportBatchItemFailures` | `ApproximateAgeOfOldestMessage` |

- **Cold starts:** Provisioned Concurrency for latency-sensitive APIs, SnapStart
  for JVM/.NET, smaller packages, lazy imports, clients built outside the
  handler. **Out of date:** VPC attachment no longer adds cold-start time.
- **Throttling:** 1,000 concurrent executions per Region by default. Reserved
  Concurrency protects critical functions from noisy neighbours; SQS buffers
  bursts so Lambda consumes at a controlled rate.
- **Sizing:** memory and CPU scale together, so more memory often cuts duration
  and cost. Use Lambda Power Tuning rather than guessing.
- **Timeouts:** 15 minutes maximum. API Gateway integration timeout defaults to
  29 s; Regional and private REST APIs can raise it by quota request, possibly
  trading regional throttle quota, edge-optimised REST stays at 29 s, HTTP APIs
  cap hard at 30 s. Long work needs an async pattern: return a job ID and poll.
- **Retries:** Lambda is at-least-once, so handlers must be **idempotent**. Use
  a DLQ past the max receive count and `ReportBatchItemFailures` so only failed
  message IDs are retried.
- **VPC:** an attached function has no default internet route, so route egress
  via a NAT gateway and use VPC endpoints for S3, DynamoDB, and Secrets Manager.

```bash
aws lambda get-function-configuration --function-name <name>
aws logs tail /aws/lambda/<name> --since 15m
```

## SQS vs SNS vs EventBridge

Docs: [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) · [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) · [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)

| | SQS | SNS | EventBridge |
| :--- | :--- | :--- | :--- |
| Pattern | Queue: pull and buffer | Topic: push and fan out | Bus: route matching events |
| Consumers | One per message; competing consumers scale | Every subscription gets a copy | Every matching rule fans to targets |
| Retention | Up to 14 days | None after delivery | Optional archive and replay |
| Filtering | Consumer-side | Subscription filter policies | Rich content-based rules |
| Ordering | Standard best effort; FIFO per group | Standard or FIFO topic | Best effort |
| Use for | Work queues, burst absorption, retries, DLQs | Notifications, fan-out to SQS/Lambda/HTTP/email | Domain and AWS service events, SaaS, schedules |

- SQS when work must wait safely for a consumer; SNS when one publisher
  notifies many known subscribers; EventBridge when producers and consumers
  should couple only on event schema.
- Reliable fan-out: SNS or EventBridge → one SQS queue per consumer, so each
  subscriber gets independent buffering, retries, and a DLQ.
- **Gotcha:** all three can deliver more than once, so consumers must be
  idempotent. Set the SQS visibility timeout longer than normal processing or
  another consumer picks the message up mid-flight; pair with a DLQ and a finite
  redrive count.

## CloudWatch

Docs: [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) · Whitepaper: [Operational Excellence Pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)

- **Metrics:** AWS service metrics arrive by default; application and OS metrics
  need the CloudWatch agent or custom publication. Every unique dimension set is
  a separate billable custom metric, so choose dimensions deliberately.
- **Logs:** log groups and streams, Logs Insights, subscription filters to
  Lambda/Firehose/OpenSearch, metric filters. **Gotcha:** default retention is
  never expire; set it explicitly.
- **Alarms:** evaluate a metric or metric-math expression, then notify SNS,
  drive Auto Scaling, or trigger rollback. Composite alarms cut noise.
- **Container Insights** and **Application Signals** add workload metrics and
  service views, **X-Ray** distributed traces; CloudWatch Events is EventBridge.
- Alarm on user-facing symptoms first — availability, latency, errors, traffic —
  then saturation. **Gotcha:** missing-data treatment, where `notBreaching`
  hides a dead metric publisher and `breaching` pages during planned shutdowns.

```bash
aws cloudwatch describe-alarms --state-value ALARM
aws logs describe-log-groups --query 'logGroups[].[logGroupName,retentionInDays]'
```

## Route 53

Docs: [Route 53 Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html) · [Routing policies](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html) · Whitepaper: [Hybrid Cloud DNS Options for Amazon VPC](https://docs.aws.amazon.com/whitepapers/latest/hybrid-cloud-dns-options-for-vpc/welcome.html)

- Route 53 provides authoritative DNS, registration, health checks, and Resolver
  for hybrid DNS; record types: [Linux interview guide](linux-interview-guide.md#dns).
- An AWS **alias record** works at the zone apex, targets ALB, CloudFront, API
  Gateway, or S3 websites, and adds no lookup charge.
- A `CNAME` cannot exist at the zone apex.

| Routing policy | Choose for |
| :--- | :--- |
| Simple | One endpoint, or several unordered answers |
| Weighted | Canary releases, A/B tests, controlled migration |
| Latency | Lowest measured latency Region |
| Failover | Active/passive with health checks |
| Geolocation | Route by user origin for localisation or compliance |
| Geoproximity | Route by resource location with traffic bias |
| Multi-value answer | Up to 8 healthy records; distribution, not load balancing |
| IP-based | Known client CIDRs to selected endpoints |

**Gotcha:** DNS failover is not instant — resolvers cache to TTL and clients
cache longer. Lower TTL before a planned migration and rely on ALB/NLB health
checks for fast in-Region target removal.

## KMS

Docs: [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) · [Key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html) · Whitepaper: [AWS KMS Cryptographic Details](https://docs.aws.amazon.com/kms/latest/cryptographic-details/intro.html)

Envelope encryption: KMS encrypts the small **data key**, the service encrypts
bulk data locally with it and stores that key beside the ciphertext, so KMS
never sees the payload.

| Key type | Control you get |
| :--- | :--- |
| AWS owned | Invisible, fully service-managed |
| AWS managed | Visible, fixed policy |
| Customer managed | Policy, grants, aliases, rotation, cross-account, disable and delete; monthly cost |

- **Both** the caller's IAM policy and the KMS key policy must allow the call.
  An S3 `AccessDenied` on an SSE-KMS object is usually `kms:Decrypt` or the key
  policy, not the bucket policy.
- Automatic rotation of symmetric CMKs changes backing material while the key
  ARN stays stable; imported and asymmetric keys need manual rotation.
- **DESTRUCTIVE caveat:** key deletion has a mandatory 7–30 day waiting period
  because it makes every remaining ciphertext permanently unrecoverable, so
  disable and observe for use first — never schedule deletion first.
- Multi-Region keys only when the same ciphertext must decrypt elsewhere;
  ordinary keys are Regional. KMS protects keys, while **Secrets Manager**
  stores and rotates credentials using KMS underneath — do not conflate them.

## WAF vs Shield

Docs: [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html) · Whitepaper: [AWS Best Practices for DDoS Resiliency](https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/welcome.html)

| | AWS WAF | Shield Standard | Shield Advanced |
| :--- | :--- | :--- | :--- |
| Blocks | L7: SQLi, XSS, bad bots, abusive rates | Common L3/L4 DDoS | Large or sophisticated L3/L4 and L7 DDoS |
| Control | Web ACLs, managed rule groups, IP lists, rate rules | Automatic, no rules | Automatic detection plus response support |
| Attach to | CloudFront, ALB, API Gateway, AppSync, Cognito | Automatic for AWS resources | Enrolled CloudFront, Route 53, ALB/NLB, EIP |
| Cost | Per Web ACL, rule, request | Included | Subscription plus data processing |

Shield Standard is already on; Shield Advanced adds the DDoS Response Team,
cost-protection credits, and automatic L7 mitigation with WAF. Neither replaces
security groups, which filter ports and sources but do not inspect HTTP.

## Identity

Docs: [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) · [Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) · Whitepaper: [Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)

| Mechanism | One-liner |
| :--- | :--- |
| IAM user plus access keys | Long-lived credentials; avoid for workloads, they leak and rarely rotate |
| IAM role | Permissions with no permanent credentials, assumed for short-lived STS tokens — the default answer |
| Instance profile | How EC2 assumes a role, delivered via IMDS. **Enforce IMDSv2**; IMDSv1 is SSRF-exploitable |
| IRSA / EKS Pod Identity | How a Pod assumes a role, scoped per ServiceAccount rather than per node |
| Resource-based policy | Attached to a bucket or queue; the mechanism for cross-account access |
| IAM Identity Center | Federated SSO for humans, replacing IAM users |

| Concept | AWS | Azure |
| :--- | :--- | :--- |
| App identity you create | IAM role plus IAM user or external IdP | Service principal |
| Identity attached by the platform | IAM role via instance profile, IRSA, task role | Managed identity |
| Credential material | Short-lived STS tokens | Client secret or certificate; none for managed identity |
| Scoping | Trust policy plus permission policy | Role assignment at a resource scope |

A role assumed via instance profile or IRSA is the managed-identity pattern; an
IAM user with access keys is the service-principal-with-secret pattern. Prefer
the platform-managed option, with OIDC federation for outside systems.

### Diagnosing `AccessDenied`

Prove which identity made the call first — in a Pod check the ServiceAccount
annotation or Pod Identity association, on EC2 the instance profile and IMDS.

```bash
aws sts get-caller-identity
aws iam simulate-principal-policy --policy-source-arn <role-arn> \
  --action-names s3:GetObject --resource-arns <resource-arn>
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=<Action>
```

1. Capture the denied action, resource ARN, Region, and request time, then find
   the CloudTrail event and confirm the principal.
2. Evaluate identity policies, permission boundaries, session policies, SCPs,
   and the resource policy. **Check explicit denies first** — they override
   every allow.
3. Inspect KMS key policies when an encrypted object or secret is involved.
4. Test the smallest correction, then ship it through code review.

- Trust policy: **who may assume** the role; permission policy: **what it may do**.
- IRSA failures usually come from an OIDC issuer or `sub`/`aud` mismatch, not
  the S3 policy.
- Prevention: least-privilege roles per workload, policy validation in CI, and
  CloudTrail alerts on denies.

## Reliability and disaster recovery

Docs: [AWS Resilience Hub](https://docs.aws.amazon.com/resilience-hub/latest/userguide/what-is.html) · Whitepapers: [Disaster Recovery of Workloads on AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html) · [Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)

| Term | One-liner |
| :--- | :--- |
| High availability | Minimise downtime through redundancy and fast failover; brief interruption accepted, e.g. a 60 s RDS failover |
| Fault tolerance | Keep working through a component failure with no visible interruption; stricter and costlier |
| Disaster recovery | Recover data and service after damage beyond repair, usually elsewhere, with measured loss and downtime |

HA and FT prevent an outage, DR recovers from one, and you need both: redundancy
does not protect against deletion, corruption, a bad deploy, or a compromise.

| | RPO | RTO |
| :--- | :--- | :--- |
| Question | How much data loss is acceptable? | How long may we be down? |
| Unit | Data, as time since the last recoverable point | Elapsed time to restore service |
| Lever | Backup and replication frequency | Automation, warm capacity, runbooks |
| Cost driver | Storage and replication bandwidth | Standby infrastructure |

RPO 4 h with a 12:00 backup: a 15:59 failure is within target, 17:00 is not.
RTO 1 h means serving traffic again within 60 minutes of the outage starting.

| Strategy | RPO | RTO | Second Region runs |
| :--- | :--- | :--- | :--- |
| Backup and restore | Hours | Hours to a day | Nothing; restore from snapshots and S3 |
| Pilot light | Minutes | Tens of minutes | Data replicated, core services off |
| Warm standby | Seconds to minutes | Minutes | Scaled-down working copy |
| Multi-Region active-active | Near zero | Near zero | Full capacity serving traffic |

- Trading platform: RPO ≈ 0, RTO < 30 s → active-active. Internal reporting:
  RPO 24 h, RTO 8 h → daily snapshots and a documented restore, far cheaper.
- Cost rises steeply as targets approach zero, so agree them with the business.
  RPO 0 over distance is limited by physics and CAP: synchronous cross-Region
  replication adds round-trip latency to every write.
- RTO is met by automation; IaC plus tested failover separates a documented RTO
  from a real one, so **assume an untested DR plan does not work**.

| Term | Meaning | Audience |
| :--- | :--- | :--- |
| SLI | Measured metric of behaviour, usually `good events / total events` | Engineers |
| SLO | Internal target for an SLI | Engineers and product |
| SLA | Contractual commitment with financial consequences | Business and customers |

- SLI: request latency, error rate, availability, throughput.
- SLO: "99.9% of requests under 200 ms over a rolling 30 days". Its mechanism is
  the **error budget**, the 0.1% you may fail: while budget remains you ship,
  when exhausted reliability work takes priority.
- SLA: "below 99.5% monthly availability, credit 10% of the bill". Keep the SLO
  stricter than the SLA so you react before you owe money.

## CI/CD on AWS

Docs: [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html) · [AWS CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html) · Whitepaper: [Practicing CI/CD on AWS](https://docs.aws.amazon.com/whitepapers/latest/practicing-continuous-integration-continuous-delivery/welcome.html)

| Stage | AWS service | Purpose |
| :--- | :--- | :--- |
| Source | GitHub/GitLab via CodeConnections, or CodeCommit | Trigger on push, PR, or tag |
| Build and test | CodeBuild | Compile, test, build the image |
| Artifacts | ECR for images, S3 for archives | Immutable versioned artifacts |
| Orchestration | CodePipeline or Step Functions | Stage order, approvals, rollback |
| Deploy | CodeDeploy, ECS/EKS rolling update, CloudFormation, Terraform | Apply the change |
| Verify | CloudWatch alarms, synthetic canaries | Automatic rollback on regression |

- **Build once, promote the artifact.** Tag with the commit SHA and deploy that
  exact digest everywhere; a per-environment rebuild means you are not shipping
  what you tested.
- **No long-lived credentials.** OIDC federation from GitHub Actions or GitLab
  into an IAM role gives short-lived STS credentials and no key to leak.
- **Least privilege per stage.** The build role pushes to ECR but cannot deploy;
  the deploy role updates the service but cannot read production data.
- **Strategy by blast radius:** rolling for ordinary changes, blue/green via
  CodeDeploy for instant rollback, canary with weighted target groups first, all
  wired to CloudWatch alarms on error rate and latency for automated rollback.
- **Infrastructure through the same pipeline** — Terraform or CloudFormation
  planned, reviewed, and applied with drift detection, never in the console.
- **Environment isolation by account** under
  [Organizations](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html),
  the pipeline assuming a role into each: the strongest blast-radius boundary.
- **DESTRUCTIVE caveat:** `terraform apply` and `cloudformation delete-stack`
  can remove stateful resources. Require a reviewed plan, enable deletion
  protection on databases and buckets, and never grant the deploy role
  `*:Delete*` on data stores.
