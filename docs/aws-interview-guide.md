# AWS

Interview notes on AWS services, VPC networking, and reliability practice.
Protocol and OS fundamentals (OSI, TCP handshake, DNS resolution, CIDR
arithmetic, HTTP status codes) are in
[Linux interview guide](linux-interview-guide.md#networking-fundamentals) rather
than repeated here. Machine learning certification material is in the
[AWS Machine Learning Associate study guide](aws-ml-associate-study-guide.md).

## Contents

- [Global infrastructure](#global-infrastructure)
- [Cloud service models](#cloud-service-models)
- [Serverless](#serverless)
- [VPC networking](#vpc-networking)
- [Security groups vs network ACLs](#security-groups-vs-network-acls)
- [NAT gateway vs NAT instance](#nat-gateway-vs-nat-instance)
- [VPC peering](#vpc-peering)
- [VPC endpoints](#vpc-endpoints)
- [Elastic Load Balancing](#elastic-load-balancing)
- [EC2](#ec2)
- [EBS vs EFS vs instance store](#ebs-vs-efs-vs-instance-store)
- [Auto Scaling and launch templates](#auto-scaling-and-launch-templates)
- [ECS vs EKS](#ecs-vs-eks)
- [S3](#s3)
- [SQS vs SNS vs EventBridge](#sqs-vs-sns-vs-eventbridge)
- [CloudWatch](#cloudwatch)
- [Route 53](#route-53)
- [KMS](#kms)
- [WAF vs Shield](#waf-vs-shield)
- [RDS](#rds)
- [Lambda](#lambda)
- [Identity](#identity)
- [Reliability and disaster recovery](#reliability-and-disaster-recovery)
- [CI/CD on AWS](#cicd-on-aws)

## Global infrastructure

A **Region** is a separate geographic area, for example `eu-west-1`. Regions are
fully isolated from each other: nothing replicates between them unless you
configure it, which is both the blast-radius boundary and the reason
multi-region designs are expensive.

An **Availability Zone** is one or more discrete data centres inside a Region
with independent power, cooling, and networking, connected to the other zones by
low-latency private links. Zones fail independently, so spreading instances
across at least two is the baseline for high availability. Zone names are
per-account aliases, so `us-east-1a` in two accounts is not necessarily the same
physical zone; compare AZ IDs such as `use1-az1` instead.

**Edge locations** are the CloudFront points of presence, far more numerous than
Regions, used for caching and for terminating connections close to users.

### Quotas worth knowing

| Quota | Default | Adjustable |
| :--- | :--- | :--- |
| VPCs per Region | 5 | Yes |
| Subnets per VPC | 200 | Yes |
| IPv4 CIDR blocks per VPC | 5 | Yes, up to 50 |
| VPC CIDR size | `/16` to `/28` | No |
| Route tables per VPC | 200 | Yes |
| Routes per route table | 50 | Yes, up to 1000 |
| Security groups per network interface | 5 | Yes, up to 16 |
| Rules per security group | 60 inbound, 60 outbound | Yes |
| Elastic IPs per Region | 5 | Yes |

State whether a quota is a soft limit. "200 subnets per VPC" is a default that
support can raise; "`/28` is the smallest subnet" is a hard protocol and
platform constraint.

## Cloud service models

Think about how much of the stack you keep responsibility for.

| | IaaS | PaaS | SaaS |
| :--- | :--- | :--- | :--- |
| You manage | OS, runtime, middleware, app, data | App code and data | Your data and users only |
| AWS manages | Hardware, virtualisation, network | Everything below your code | The entire stack |
| Flexibility | Highest | Moderate | Lowest |
| Operational overhead | High | Low | None |
| AWS examples | EC2, EBS, VPC | Elastic Beanstalk, App Runner, Lambda, RDS | Amazon Chime, Amazon WorkMail |

The pizza analogy: IaaS is buying ingredients and baking at home, PaaS is
delivery where someone else bakes and you supply the table, SaaS is eating at a
restaurant.

How to choose:

- **IaaS** when you need a specific OS build, kernel modules, licensed software,
  or a legacy application that managed platforms will not host.
- **PaaS** for new services, so the team spends its time on business logic
  rather than OS patching and capacity planning.
- **SaaS** for anything that is not a differentiator, such as email and chat, to
  cut total cost of ownership.

Note that responsibility never fully disappears. Under the shared
responsibility model AWS secures the cloud and you secure what you put in it:
your data, your IAM policies, your patching where you own the OS, and your
network configuration.

## Serverless

Serverless means you deploy code or configuration and the provider handles
provisioning, scaling, and patching of the compute underneath. Servers still
exist; you no longer manage them.

Characteristics: event-driven invocation, automatic scaling to demand, and
billing by request and duration, so an idle function costs nothing. Examples are
Lambda, Fargate, API Gateway, DynamoDB on-demand, SQS, SNS, EventBridge, and
Step Functions.

Trade-offs to raise in an interview: cold-start latency, per-invocation limits
such as Lambda's 15-minute maximum, weaker local development and debugging
story, potential vendor lock-in in the event and integration model, and cost
that is excellent at spiky load but can exceed a reserved instance at high
steady throughput.

## VPC networking

A **VPC** is a logically isolated network in one Region with a CIDR block you
choose. Everything else hangs off it.

| Component | Role |
| :--- | :--- |
| Subnet | A CIDR range inside the VPC, bound to exactly one Availability Zone |
| Route table | Decides where traffic leaving a subnet goes; a subnet has exactly one |
| Internet gateway (IGW) | Region-level, highly available door to the internet for IPv4 and IPv6 |
| Egress-only internet gateway | Outbound-only internet access for IPv6 |
| NAT gateway | Lets private subnets reach the internet outbound over IPv4 |
| Security group | Stateful firewall attached to network interfaces |
| Network ACL | Stateless firewall attached to subnets |
| VPC endpoint | Private access to AWS services without traversing the internet |
| Virtual private gateway / Transit Gateway | Connectivity to on-premises networks and between VPCs at scale |

A **public subnet** is simply a subnet whose route table has a `0.0.0.0/0` route
to an internet gateway, and whose instances have public or Elastic IP addresses.
A **private subnet** has no route to the IGW; its `0.0.0.0/0` route points at a
NAT gateway, or it has no default route at all.

Standard three-tier layout, repeated in each of at least two Availability Zones:

- Public subnet: load balancer, NAT gateway, and a bastion if you use one.
- Private application subnet: EC2 instances, containers, Lambda ENIs.
- Private data subnet: RDS and ElastiCache, with no default route to the
  internet at all.

Every subnet loses five addresses to AWS: the network address, the VPC router
(`.1`), the DNS server (`.2`), one reserved for future use (`.3`), and the
broadcast address. So a `/28` gives 11 usable addresses, not 14. Prefix
arithmetic is in
[Linux interview guide](linux-interview-guide.md#ip-addressing-and-cidr).

Plan CIDRs so nothing overlaps across VPCs, accounts, or on-premises ranges.
Overlapping ranges make peering, VPN, and Transit Gateway attachment impossible
and can only be fixed by renumbering, which is why this is the one design
decision to get right at the start.

## Security groups vs network ACLs

Both filter traffic, at different layers and with different semantics. The
difference interviewers look for is **stateful versus stateless**.

| | Security group | Network ACL |
| :--- | :--- | :--- |
| Attaches to | Elastic network interfaces, so effectively instances | Subnets |
| State | Stateful: return traffic is automatically allowed | Stateless: return traffic needs its own rule |
| Rule types | Allow only | Allow and deny |
| Evaluation | All rules are evaluated; any match allows | Rules in ascending number order, first match wins |
| Default behaviour | Deny all inbound, allow all outbound | Default NACL allows everything; a custom NACL denies everything until you add rules |
| Rule sources | CIDR, prefix list, or another security group | CIDR only |
| Scope | Only the interfaces it is attached to | Every resource in the subnet, with no exceptions |
| Typical use | The primary control, per application tier | Coarse subnet-level guardrail, for example blocking an IP range |

Consequences that matter in practice:

- Because a security group is **stateful**, allowing inbound 443 is enough; the
  response leaves regardless of outbound rules.
- Because a NACL is **stateless**, allowing inbound 443 is not enough. The
  response leaves from an ephemeral source port, so the outbound rules must
  allow `1024-65535`. Forgetting this is the classic "the security group is open
  but nothing works" incident.
- Security groups can reference **other security groups**, which is how you
  express "the database accepts connections from the application tier" without
  hardcoding IP addresses that change on every scale event. Do this rather than
  allowing a CIDR.
- A NACL applies to the whole subnet, including traffic between instances in it,
  and cannot be overridden per instance. Keep NACL rules simple; complex NACLs
  are difficult to debug because the first matching rule wins and denies are
  silent.
- Neither logs by itself. Enable **VPC Flow Logs** to see accepted and rejected
  flows, and use **Reachability Analyzer** to find which hop drops a packet.

Order of evaluation for inbound traffic: NACL inbound rules, then security group
inbound rules, then the instance's own host firewall. Outbound is the reverse.

## NAT gateway vs NAT instance

Network address translation lets instances in a private subnet start outbound
IPv4 connections to the internet while remaining unreachable from it. A **NAT
gateway** is the managed AWS service; a **NAT instance** is an EC2 instance you
configure to do the same job.

| | NAT gateway | NAT instance |
| :--- | :--- | :--- |
| Managed by | AWS | You: AMI, patching, monitoring |
| Bandwidth | Starts at 5 Gbps, scales automatically to 100 Gbps | Bounded by the instance type |
| Availability | Redundant within its Availability Zone | Single instance; you build failover yourself |
| Security groups | Not supported; filter with NACLs and the source security groups | Supported |
| Port forwarding, bastion use, custom software | Not possible | Possible |
| Source/destination check | Not applicable | Must be disabled on the ENI |
| Cost | Hourly charge plus per-GB data processing | Instance and data transfer cost only |
| Maintenance | None | Yours |

Use a NAT gateway by default. A NAT instance is justified only when you need
something a NAT gateway cannot do, such as port forwarding or acting as a
bastion at the same time, or on a development account where a `t4g.nano` is
cheaper than the gateway's hourly charge.

### How the traffic actually flows

1. An instance in a private subnet sends a packet to a public address. Its
   subnet's route table has `0.0.0.0/0` pointing at the NAT gateway.
2. The NAT gateway lives in a **public** subnet whose route table has
   `0.0.0.0/0` pointing at the internet gateway. This placement is the part
   people get wrong: a NAT gateway in a private subnet cannot work.
3. The NAT gateway rewrites the packet's source to its own Elastic IP, records
   the translation, and forwards it out through the internet gateway.
4. The response arrives addressed to the Elastic IP. The gateway looks up the
   translation entry and forwards the packet back to the private instance.

What this means:

- NAT is **outbound-initiated only**. Because a translation entry exists only
  after an outbound packet, an unsolicited inbound connection has nothing to
  match and is dropped. Inbound traffic needs a load balancer, or an instance in
  a public subnet with a public IP.
- Ordinary NAT gateway egress translates private **IPv4 to public IPv4**.
  Native IPv6 does not need address translation; use an **egress-only internet
  gateway** when IPv6 workloads need outbound-only access to IPv6 destinations.
  A NAT gateway also has built-in **NAT64** for an IPv6-only client reaching an
  IPv4-only destination. Enable DNS64 on the workload subnet so Route 53
  Resolver synthesises an address under `64:ff9b::/96`, and route that prefix to
  the NAT gateway. NAT64 is automatically available on the gateway; it is not a
  feature you enable there.
- Deploy **one NAT gateway per Availability Zone** and point each zone's private
  route table at the gateway in its own zone. A single shared gateway both adds
  cross-AZ data transfer charges and makes one zone's failure take down every
  zone's egress.
- NAT gateways charge per gigabyte processed. Traffic to S3, DynamoDB, ECR, and
  other AWS services should go through **VPC endpoints** so it never touches the
  NAT gateway. Pulling container images through NAT on every scale-out is a
  common source of surprising bills.
- A NAT gateway has no security group, so filtering has to happen on the source
  instances or with subnet NACLs.
- Typical failure signatures: instances have no internet access because the
  private route table is missing the NAT route, or because the NAT gateway
  itself sits in a subnet with no IGW route; and
  `ErrorPortAllocation`/`IdleTimeoutCount` metrics rising, which means port
  exhaustion from too many concurrent connections to a single destination.

## VPC peering

A VPC peering connection is a private, one-to-one network link between two VPCs.
Traffic stays on the AWS backbone, never traverses the internet, and needs no
gateway, VPN, or physical hardware. It works across accounts and across Regions.

Setting one up takes three steps that all have to be done:

1. Requester creates the peering connection; the accepter accepts it.
2. **Both** VPCs add routes to the other VPC's CIDR with the peering connection
   as the target.
3. Security groups on both sides allow the other side's CIDR or, within a
   Region, the other side's security group ID.

Constraints that are usually the point of the question:

- **CIDRs must not overlap.** There is no NAT in a peering connection, so
  overlapping ranges make the connection impossible.
- **Peering is not transitive.** If A peers with B and B peers with C, A cannot
  reach C. You need a direct A-to-C peering.
- **No edge-to-edge routing.** You cannot use a peer's internet gateway, NAT
  gateway, VPN connection, Direct Connect, or gateway VPC endpoint. Each VPC
  provides its own egress.
- **It does not scale.** Full mesh across n VPCs needs n(n-1)/2 connections and
  a route entry per peer in every route table. Beyond a handful of VPCs, use a
  **Transit Gateway**, which is a hub-and-spoke router that supports transitive
  routing, route tables per attachment, and on-premises attachment through VPN
  or Direct Connect.
- **DNS resolution of private hostnames** across the peering is off by default;
  enable it on both sides if you want private DNS names to resolve.
- Same-Region peering has no per-GB charge for the peering itself, though
  cross-AZ data transfer still applies. Inter-Region peering charges for data
  transfer and is encrypted in transit by AWS.

Choose peering for a small number of stable, point-to-point relationships.
Choose Transit Gateway for a hub topology or once transitivity is needed. Choose
**PrivateLink** when you only need to expose a single service to a consumer
rather than connect two networks, since it avoids sharing routable address space
altogether and works with overlapping CIDRs.

## VPC endpoints

Endpoints give resources in a VPC private access to AWS services without an
internet gateway or NAT gateway.

| | Gateway endpoint | Interface endpoint (PrivateLink) |
| :--- | :--- | :--- |
| Supported services | S3 and DynamoDB only | Most AWS services, plus partner and your own services |
| Mechanism | A route table entry with a prefix list | An ENI with a private IP in your subnet |
| Cost | Free | Hourly per ENI plus per-GB |
| Security control | Endpoint policy and route table | Endpoint policy and a security group |
| Cross-Region or on-premises access | No | Yes, through VPN or Direct Connect |

Two reasons to use them: cost, because traffic bypasses NAT gateway data
processing charges, and security, because an endpoint policy plus an
`aws:SourceVpce` condition on the bucket policy lets you enforce that a bucket
is reachable only from your VPC.

## Elastic Load Balancing

| | Application Load Balancer | Network Load Balancer | Gateway Load Balancer |
| :--- | :--- | :--- | :--- |
| Layer | 7 | 4 | 3 gateway plus GENEVE on port 6081 |
| Protocols | HTTP, HTTPS, gRPC | TCP, TLS, UDP, TCP_UDP | IP packets |
| Routing | Host, path, headers, query, method, weighted target groups | Destination port and connection flow | Routes all packets through virtual appliances |
| Targets | Instances, IPs, Lambda | Instances, IPs, ALBs | Firewall and inspection appliances |
| Client IP | In `X-Forwarded-For` | Preserved to the target | Preserved through encapsulation |
| Static IP | No; use its DNS name | One static IP per AZ; Elastic IP supported | Endpoint service, reached through GWLB endpoints |
| Choose it for | Web apps, APIs, redirects, authentication, content routing | Very high throughput, low latency, non-HTTP traffic, static allow-listed IPs | Transparent third-party firewalls, IDS/IPS, deep packet inspection |

**ALB** understands requests, terminates TLS, can authenticate through
OIDC/Cognito, and is the normal choice for HTTP services. **NLB** understands
connections rather than URLs; choose it for databases, MQTT, UDP, source-IP
preservation, or a fixed IP. **GWLB** is not an application frontend: it inserts
a fleet of network appliances into a route path and scales them transparently.

All are Regional and should have subnets in at least two Availability Zones.
Cross-zone load balancing is always enabled for ALB and configurable for NLB
and GWLB. Health checks decide whether new traffic reaches a target, so a
shallow process-only check can send users to an application that cannot reach
its database.

## EC2

### Instance families

| Family | Prefix | Optimised for | Typical workload |
| :--- | :---: | :--- | :--- |
| General purpose | `M` | Balanced CPU, memory, network | Application servers, small databases |
| General purpose | `T` | Burstable, credit-based | Dev/test, low-traffic web |
| Compute optimised | `C` | High CPU per unit of memory | Batch processing, encoding, high-performance web |
| Memory optimised | `R` | High memory per vCPU | In-memory caches, Redis, analytics |
| Memory optimised | `X`, `U` | Extreme memory | SAP HANA, large in-memory databases |
| Storage optimised | `I` | Local NVMe IOPS | NoSQL, low-latency data stores |
| Storage optimised | `D`, `H` | Dense HDD throughput | Hadoop, log and data warehouse processing |
| Accelerated | `P` | GPU for training | Machine learning training, HPC |
| Accelerated | `G` | GPU for inference and graphics | Inference, video encoding, 3D rendering |
| Accelerated | `F` | FPGA | Hardware acceleration, genomics |
| Accelerated | `Inf`, `Trn` | AWS custom silicon | Inference and training at lower cost |

Suffix letters carry information: `g` means an AWS Graviton (ARM) processor,
which offers materially better price-performance but requires ARM-compatible
builds and images; `a` means AMD; `i` means Intel; `d` means local NVMe storage;
`n` means enhanced network bandwidth.

`T` instances earn and spend CPU credits. Once credits run out, performance
drops to a low baseline, which appears in monitoring as unexplained latency.
Either use `unlimited` mode and accept the surcharge, or pick `M` or `C` for
production.

### Pricing models

| Model | Saving | Commitment | Use for |
| :--- | :--- | :--- | :--- |
| On-Demand | Baseline | None | Short-lived, unpredictable workloads |
| Savings Plans | Up to 72% | 1 or 3 years of hourly spend | Steady compute spend, flexible across family and Region |
| Reserved Instances | Up to 72% | 1 or 3 years on specific attributes | Steady-state workloads, especially RDS |
| Spot | Up to 90% | None; AWS can reclaim with 2 minutes' notice | Fault-tolerant, stateless, interruptible batch work |
| Dedicated Hosts | Varies | Per host | Licensing that is bound to physical cores |

Prefer Savings Plans over Reserved Instances for EC2 now, because they apply
across instance families and Regions. Spot works well for Kubernetes worker
nodes when you run the AWS Node Termination Handler, which catches the
interruption notice and drains pods before the node disappears; mix Spot with an
On-Demand or Savings Plan baseline so a capacity event cannot take out the whole
fleet.

### What an AMI contains

- A template for the root volume: the OS, and any pre-installed software and
  configuration.
- Launch permissions controlling which AWS accounts may launch from it.
- A block device mapping specifying the volumes attached at launch, their sizes,
  types, and delete-on-termination behaviour.

AMIs are Region-scoped, so a multi-Region deployment needs the AMI copied to
each Region. Baking configuration into an AMI (with Packer or EC2 Image Builder)
gives faster, more predictable launches than configuring at boot with user data,
which is the "golden AMI" pattern.

## EBS vs EFS vs instance store

| | EBS | EFS | Instance store |
| :--- | :--- | :--- | :--- |
| Model | Network block device | Managed NFS file system | Local NVMe/SATA block device |
| Scope | One Availability Zone | Regional, mounted from many AZs | One physical EC2 host |
| Attachment | Normally one instance; supported volumes can use Multi-Attach | Many Linux clients concurrently | Only its owning instance |
| Persistence | Survives stop and, unless configured otherwise, termination | Persists independently of clients | Data is lost on stop, terminate, or host failure |
| Performance | Provisioned volume type, IOPS, and throughput | Elastic shared throughput with network latency | Lowest latency and highest local IOPS |
| Best use | Boot volumes, databases, single-node durable state | Shared content, home directories, multi-instance file access | Cache, buffers, scratch, replicated data |

An EBS volume and its instance must be in the same AZ; snapshots are
incremental backups stored by AWS and can create volumes in another AZ or
Region. EFS removes the single-writer/AZ restriction but is a filesystem, not a
drop-in replacement for a database block device. Instance store is safe only
when the application can recreate or replicate every byte elsewhere.

## Auto Scaling and launch templates

An **EC2 Auto Scaling group (ASG)** maintains a desired instance count between
minimum and maximum bounds, replaces unhealthy instances, and distributes them
across Availability Zones. It is not the load balancer: the ASG controls
capacity and lifecycle, while an ALB or NLB distributes traffic.

A **launch template** is the versioned instance recipe used by the ASG: AMI,
instance type, security groups, IAM instance profile, storage, metadata options,
and user data. Prefer it over legacy launch configurations, which cannot be
edited or versioned and do not support current features such as mixed instance
policies.

Scaling policies:

- **Target tracking:** maintain a target such as 50% average CPU or a custom
  requests-per-target metric; the default answer for ordinary workloads.
- **Step scaling:** add different amounts of capacity at different alarm
  thresholds.
- **Scheduled scaling:** prepare for a predictable event before it begins.
- **Predictive scaling:** forecast recurring demand and launch ahead of it.

Scale-in is riskier than scale-out. Use instance warm-up so new instances do not
distort metrics, a lifecycle hook to drain work or upload logs before
termination, and termination protection for irreplaceable work. Feed ALB health
checks into the ASG so a process that is alive but cannot serve is replaced.

## ECS vs EKS

| | ECS | EKS |
| :--- | :--- | :--- |
| Orchestrator | AWS-native | Managed Kubernetes control plane |
| Workload object | Task definition, task, service | Pod, Deployment, StatefulSet, Service |
| Learning and operations | Simpler, fewer components | Higher complexity; Kubernetes skills required |
| Portability | AWS-specific API | Kubernetes API works across clouds and on-premises |
| Compute | EC2 or Fargate | EC2 managed node groups, self-managed nodes, or Fargate |
| Ecosystem | Tight AWS integration | Broad Kubernetes controllers, operators, Helm, service meshes |
| Choose it for | AWS-only teams wanting the least operational overhead | Existing Kubernetes investment, portability, or ecosystem requirements |

**Fargate is a compute option, not an orchestrator**: both ECS and EKS can use
it to run Pods or tasks without managing nodes. With EC2 capacity you manage
node patching and utilisation but gain daemon workloads, GPUs, and more control.
For either service, give workloads task or Pod roles rather than the broad node
role, publish images to ECR, and spread replicas across AZs.

## S3

### Storage classes

| Class | Durability | Availability zones | Minimum duration | Use for |
| :--- | :--- | :--- | :--- | :--- |
| Standard | 11 nines | 3 or more | None | Active, frequently accessed data |
| Intelligent-Tiering | 11 nines | 3 or more | None | Unknown or changing access patterns |
| Standard-IA | 11 nines | 3 or more | 30 days | Long-lived, infrequently accessed, needs immediate retrieval |
| One Zone-IA | 11 nines in one zone | 1 | 30 days | Reproducible data where losing a zone is acceptable |
| Express One Zone | 11 nines in one zone | 1 | 1 hour | Single-digit-millisecond latency, high request rates |
| Glacier Instant Retrieval | 11 nines | 3 or more | 90 days | Archive that still needs millisecond access |
| Glacier Flexible Retrieval | 11 nines | 3 or more | 90 days | Archive with minutes-to-hours retrieval |
| Glacier Deep Archive | 11 nines | 3 or more | 180 days | Compliance archive, 12-hour retrieval, lowest cost |
| S3 on Outposts | - | On-premises Outpost | None | Data that must stay on your own hardware, same S3 API |

Minimum duration is billed whether or not the object still exists, so moving
small short-lived objects to Glacier costs more than leaving them in Standard.
Retrieval and per-object overhead charges make lifecycle transitions of millions
of tiny objects a frequent cost mistake; use Intelligent-Tiering when the
pattern is genuinely unknown.

Reference: [S3 storage classes](https://aws.amazon.com/s3/storage-classes/)

### Accidental deletion

With **versioning** enabled, a delete only writes a delete marker. Remove the
marker to restore the object. Without versioning the object is gone.

Prevention: enable versioning before you need it, add **MFA Delete** so
permanent deletion of a version requires a token, use **Object Lock** in
compliance mode for data with a retention requirement, and replicate to a bucket
in another account so a compromised account cannot destroy both copies.

### Cost growth on large datasets

- Run **Storage Class Analysis** or S3 Storage Lens to see what is actually
  being read.
- Add **lifecycle policies** to transition and expire objects on age.
- Use **Intelligent-Tiering** where access is unpredictable.
- Expire incomplete multipart uploads with a lifecycle rule; abandoned parts are
  invisible in the console but billed.
- Check whether old **noncurrent versions** are the real cost, and expire them
  too.

### 503 Slow Down under high request rates

S3 scales to about 3,500 write and 5,500 read requests per second **per
prefix**, and partitions split automatically as load grows, but the split takes
time. A sudden ramp against one prefix produces `503 Slow Down`.

Fixes: spread keys across multiple prefixes so the load lands on more
partitions, ramp traffic gradually rather than instantly, retry with exponential
backoff and jitter (the SDKs do this by default), put CloudFront in front of read
traffic, and use multipart upload plus Transfer Acceleration for large objects.

### Cross-account access

An application in account A writes to a bucket in account B:

1. A bucket policy in B allows `s3:PutObject` for the IAM role in A.
2. Set `BucketOwnerEnforced` object ownership on the bucket, which disables ACLs
   and makes B the owner of everything uploaded. On older buckets that still use
   ACLs, A must upload with `bucket-owner-full-control`, otherwise B cannot read
   its own bucket's objects.
3. Use **S3 Access Points** to give each consumer its own named endpoint and
   policy instead of growing one bucket policy past readability.

### Preventing public exposure

- Enable **Block Public Access at the account level**, which overrides
  individual bucket settings.
- Require encryption and private access in bucket policies with `Condition`
  keys, for example `aws:SecureTransport` and `aws:SourceVpce`.
- Use **IAM Access Analyzer** to find buckets reachable from outside the account,
  and **Amazon Macie** to discover sensitive data at scale.
- Serve public content through CloudFront with Origin Access Control rather than
  by making the bucket public.

## SQS vs SNS vs EventBridge

| | SQS | SNS | EventBridge |
| :--- | :--- | :--- | :--- |
| Pattern | Queue: pull and buffer | Topic: push and fan out | Event bus: route matching events |
| Consumers | One consumer processes each message; competing consumers scale work | Every subscription receives a copy | Every matching rule can send a copy to one or more targets |
| Retention | Up to 14 days | No retention after delivery | Optional archive and replay; otherwise routes immediately |
| Filtering | Consumer decides; limited queue-side controls | Subscription filter policies | Rich rules over event structure and content |
| Ordering | Standard is best effort; FIFO preserves per-group order | Standard or FIFO topic | Best effort; no strict global order |
| Typical use | Decouple and absorb bursts, work queues, retries and DLQs | Notifications and simple fan-out to SQS, Lambda, HTTP, email | Domain events, AWS service events, SaaS integration, schedules |

Choose **SQS** when work must wait safely until a consumer is ready. Choose
**SNS** when one publisher must immediately notify many known subscribers.
Choose **EventBridge** when producers and consumers should be loosely coupled by
event schema and routing rules. A common reliable fan-out is SNS or EventBridge
to one SQS queue per consumer, so each subscriber gets independent buffering,
retries, and a dead-letter queue.

All three can deliver more than once, so consumers must be idempotent. SQS
visibility timeout hides a message while it is being processed; if the consumer
does not delete it before the timeout, another consumer receives it. Set the
timeout longer than normal processing and use a DLQ with a finite redrive count.

## CloudWatch

CloudWatch is AWS's native observability service:

- **Metrics** are time-series numbers. AWS service metrics arrive by default;
  application and OS metrics require custom publication or the CloudWatch
  agent. Choose dimensions carefully because every unique dimension set is a
  separate custom metric and cost.
- **Logs** stores log groups and streams, supports Logs Insights queries,
  subscription filters to Lambda, Firehose, or OpenSearch, and metric filters.
  Set retention explicitly; the default is never expire.
- **Alarms** evaluate a metric or metric-math expression and can notify SNS,
  invoke Auto Scaling actions, or drive rollback. A composite alarm reduces
  noise by combining several symptoms.
- **Container Insights and Application Signals** add curated workload metrics,
  traces, and service-level views. **X-Ray** supplies distributed traces.
- **EventBridge** is the service for event routing; the old CloudWatch Events
  product was renamed and expanded into EventBridge.

Monitor user-facing symptoms first: availability, latency, error rate, and
traffic, then resource saturation. Alarm on sustained periods and configure
missing-data treatment deliberately; `notBreaching` can hide a dead metric
publisher, while `breaching` can page during a planned shutdown.

## Route 53

Route 53 provides authoritative DNS, domain registration, health checks, and
Resolver for VPC and hybrid DNS. An **alias record** is AWS-specific: it can be
used at the zone apex, points to supported AWS resources such as ALB,
CloudFront, API Gateway, and S3 websites, and does not add a DNS query charge
for the alias lookup. A `CNAME` cannot exist at the apex.

| Routing policy | Choose it for |
| :--- | :--- |
| Simple | One endpoint or several unordered answers |
| Weighted | Canary releases, A/B tests, or controlled traffic migration |
| Latency | Send users to the AWS Region with the lowest measured latency |
| Failover | Active/passive service using Route 53 health checks |
| Geolocation | Route by the user's geographic origin for localisation or compliance |
| Geoproximity | Route by resource location with optional traffic bias |
| Multi-value answer | Up to eight healthy records returned; lightweight distribution, not a load balancer |
| IP-based | Route known client CIDR ranges to selected endpoints |

DNS failover is not instant: recursive resolvers cache answers until TTL expiry,
and clients may cache longer. Lower the TTL before a planned migration, but use
an ALB/NLB health check for fast target removal inside one Region.

## KMS

AWS KMS creates and controls encryption keys and performs cryptographic
operations; services such as S3, EBS, RDS, and Secrets Manager use it for
envelope encryption. KMS encrypts the small **data key**; the service encrypts
bulk data locally with that data key and stores the encrypted data key beside
the ciphertext. KMS does not receive the bulk payload.

- An **AWS owned key** is invisible and fully managed by the service. An **AWS
  managed key** is visible but has a fixed policy. A **customer managed key**
  gives you policy, grants, aliases, rotation, cross-account use, and disable or
  deletion control, with a monthly cost.
- Both the caller's IAM policy **and** the KMS key policy must permit use. An S3
  `AccessDenied` on an SSE-KMS object often means `kms:Decrypt` or the key policy,
  not the bucket policy.
- Automatic rotation for symmetric customer managed keys is configurable;
  rotation changes backing key material but the key ARN stays stable. Imported
  material and asymmetric keys require manual rotation to a new key.
- Deletion has a mandatory 7-to-30-day waiting period because deleting a key
  makes every remaining ciphertext permanently unrecoverable. Disable first,
  observe for use, then schedule deletion.
- Use a multi-Region key only when an application must decrypt the same
  ciphertext in another Region; ordinary KMS keys are Regional.

Do not confuse KMS with Secrets Manager: KMS protects cryptographic keys;
Secrets Manager stores and rotates credentials, using KMS underneath.

## WAF vs Shield

| | AWS WAF | AWS Shield Standard | AWS Shield Advanced |
| :--- | :--- | :--- | :--- |
| Protects against | Layer 7 request attacks: SQL injection, XSS, bad bots, abusive rates | Common layer 3/4 DDoS attacks | Larger and sophisticated layer 3/4 and layer 7 DDoS attacks |
| Control | Web ACL rules, managed rule groups, IP/reputation lists, rate rules | Automatic, no rules to manage | Automatic detection plus advanced visibility and response |
| Attach to | CloudFront, ALB, API Gateway, AppSync, Cognito and supported resources | Included automatically for AWS resources | Enrolled resources such as CloudFront, Route 53, ALB/NLB, EIP |
| Cost | Per Web ACL, rule, and request | Included | Subscription plus data-processing charges |

Use **WAF** to inspect HTTP requests and block application-layer patterns.
**Shield Standard** is already active and handles routine infrastructure DDoS
events. **Shield Advanced** adds the DDoS Response Team, cost-protection
credits, richer diagnostics, and application-layer automatic mitigation with
WAF. They complement rather than replace security groups, which filter ports
and sources but do not understand HTTP payloads.

## RDS

### Connection timeouts

The application cannot reach the database and the error is a timeout rather than
a refusal.

Causes: the DB security group has no inbound rule for the database port (3306
MySQL, 5432 PostgreSQL); the application is in another VPC with no peering,
Transit Gateway, or PrivateLink path; a subnet NACL blocks the ephemeral return
ports because NACLs are stateless; or the instance is not publicly accessible
while the client is outside AWS.

Fixes: allow the application's **security group ID** rather than an IP range,
verify the NACL allows `1024-65535` outbound, and use
[VPC Reachability Analyzer](https://aws.amazon.com/vpc/) to identify the exact
hop that drops the packet. A timeout means the packet never arrived; "connection
refused" means it arrived and nothing was listening, which is a different
problem.

### Sustained 100% CPU

Causes: expensive queries doing full table scans because an index is missing, a
sudden connection surge, or an under-provisioned instance class.

Fixes: open **Performance Insights** to identify the SQL contributing most to
database load, kill a runaway query (`CALL mysql.rds_kill(<id>)` on MySQL,
`SELECT pg_terminate_backend(<pid>)` on PostgreSQL), then add the missing index
or rewrite the query. Scale the instance class only after you know it is a
capacity problem, and put a connection pooler such as RDS Proxy in front if
connection churn is the driver.

### Storage full

The instance status becomes `storage-full` and all writes fail.

Causes: data growth past `AllocatedStorage`, unbounded log growth from general
or slow query logs, or a large temporary table or long-running transaction
retaining space.

Fixes: modify the instance to increase storage, which can be done online but
affects performance while it runs; then enable **storage autoscaling** so AWS
grows the volume automatically, reduce log retention in the parameter group, and
alarm on `FreeStorageSpace` well before exhaustion. Note that storage can be
increased but never decreased, so oversizing to fix an incident is permanent.

### Replication lag

Read replicas fall behind the primary, so users see stale data.

Causes: replica apply is largely single-threaded while the primary accepts
parallel writes, a replica smaller than the primary, large bulk operations, or a
long-running query on the replica blocking apply.

Fixes: alarm on the `ReplicaLag` CloudWatch metric, size replicas at least as
large as the primary, break bulk writes into batches, and route only queries
that tolerate staleness to replicas. Where zero lag is required, use Aurora,
whose shared storage layer keeps replica lag in the low milliseconds.

### Backup and replication impact on the source

| Operation | Single-AZ | Multi-AZ |
| :--- | :--- | :--- |
| Automated backup | Brief I/O suspension, seconds to minutes | No impact; the snapshot is taken from the standby |
| Creating a read replica | Brief I/O suspension for the initial snapshot | No impact; taken from the standby |
| Ongoing replica replication | Asynchronous, no blocking of the source | Asynchronous, no blocking of the source |
| Standby replication | Not applicable | Synchronous, adds a small write latency |
| Failover | Not applicable, no standby | 60 to 120 seconds of unavailability during DNS retargeting |
| OS or engine patching | Full downtime for the whole patch | Limited to a failover window |

**Synchronous versus asynchronous** is the key distinction: a Multi-AZ standby
acknowledges every write before the primary confirms it, which gives an RPO of
zero at the cost of write latency. A read replica is asynchronous, so the source
is never blocked, but the replica can lag and is not a zero-data-loss target.

Multi-AZ is a **high availability** feature, not a read-scaling feature: the
standby serves no traffic. Read replicas scale reads but are not automatic
failover, though a replica can be promoted manually.

Practices: enable Multi-AZ for production so backups and patching stop causing
downtime, set Single-AZ backup windows to the quietest hours, test failover with
**reboot with failover** so you know the application's connection pool actually
re-resolves the endpoint, and always connect by DNS endpoint rather than IP.

### Point-in-time recovery

PITR restores to any second within the retention window (1 to 35 days). It is
the defence against human error such as a `DELETE` with no `WHERE` clause.

It works from two pieces: automated daily snapshots, and transaction logs
uploaded to S3 roughly every five minutes. A restore takes the latest snapshot
before the target time and replays logs up to the requested second.

Recovery of a table wiped at 14:05:10 UTC: choose **Actions**, then **Restore to
point in time**, set a custom time of 14:05:00, and give a new instance
identifier. RDS always restores into a **new instance** and never overwrites the
existing one, so recovery means restoring alongside, copying or verifying the
data, and then repointing the application. Build that repointing step into the
runbook, because the restore itself can take a long time on a large database and
is what dominates your RTO.

Quick reference:

```bash
aws rds describe-db-instances --db-instance-identifier <name>
aws rds reboot-db-instance --db-instance-identifier <name> --force-failover
aws rds create-db-snapshot --db-instance-identifier <name> --db-snapshot-identifier <backup>
aws rds describe-events --source-identifier <name> --source-type db-instance
```

## Lambda

### Cold starts

The first request after idle time is slow because AWS must create an execution
environment, load the runtime, and run your initialisation code.

Fixes: **Provisioned Concurrency** keeps a set number of environments warm, which
is the answer for latency-sensitive APIs; **SnapStart** snapshots an initialised
JVM or .NET environment; and code-level work, meaning a smaller deployment
package, lazy-loaded dependencies, clients created outside the handler, and a
lightweight runtime. Note that attaching a Lambda to a VPC no longer adds
significant cold-start time, since ENIs are now shared, so old advice about
avoiding VPCs for this reason is out of date.

### Throttling with 429

You have hit the account's regional concurrency limit, 1,000 by default.

Fixes: set **Reserved Concurrency** on critical functions so they cannot be
starved by noisy neighbours in the same account, request a quota increase, and
buffer bursts through **SQS** so Lambda consumes at a controlled rate instead of
rejecting requests. Watch the `Throttles` and `ConcurrentExecutions` metrics.

### Timeouts and sizing

Causes: exceeding the configured timeout, which is 15 minutes maximum, or
running out of memory.

Fixes: memory and CPU are allocated together in Lambda, so raising memory also
raises CPU and often reduces both duration and cost. Use Lambda Power Tuning to
find the optimum rather than guessing. If the work genuinely needs more than 15
minutes, orchestrate it with **Step Functions** or move it to Fargate or a
container. API Gateway's default integration timeout is 29 seconds. For
**Regional and private REST APIs**, that maximum can be raised through a quota
request, potentially in exchange for a lower regional throttle quota.
**Edge-optimised REST APIs** remain capped at 29 seconds, and **HTTP APIs** have
a hard 30-second integration limit. A long-running Lambda still needs an
asynchronous pattern such as returning a job ID and polling or publishing the
result, rather than holding the client connection open.

### Errors and retries

An SQS-triggered function fails, and the same message is redelivered
indefinitely, blocking the queue. This is the poison-pill problem.

Fixes: configure a **dead-letter queue** so a message that fails the maximum
receive count is moved aside for inspection; use
`ReportBatchItemFailures` so only the failed message IDs are retried and
successful ones are deleted; and make handlers **idempotent**, because Lambda
guarantees at-least-once delivery, so the same event can arrive twice.

### VPC attachment and internet access

A Lambda attached to a VPC has no default internet access, so a function that
needs both a private RDS instance and a public third-party API fails on the
public call.

Fixes: route outbound traffic through a **NAT gateway** in a public subnet, and
use **VPC endpoints** for AWS services such as S3, DynamoDB, and Secrets Manager
so that traffic stays inside AWS and avoids NAT charges. Apply a security group
to the function's ENI and reference it from the database's security group.

### Symptom to action

| Symptom | First action | Metric |
| :--- | :--- | :--- |
| High latency on first request | Provisioned Concurrency | `InitDuration` |
| `429` throttling | Reserved Concurrency or quota increase | `Throttles` |
| Killed on memory | Raise memory allocation | `MaxMemoryUsed` in logs |
| Timeouts on long work | Step Functions or Fargate | `Duration` |
| Cannot reach the internet | NAT gateway or VPC endpoint | Error logs from the SDK |
| Queue stuck on one message | Dead-letter queue, batch item failures | `ApproximateAgeOfOldestMessage` |

## Identity

Prefer temporary, role-based credentials over long-lived keys everywhere.

- **IAM user with access keys:** long-lived credentials. Avoid for workloads;
  keys leak and are rarely rotated. Human access should go through IAM Identity
  Center with federated single sign-on.
- **IAM role:** a set of permissions with no permanent credentials, assumed to
  get short-lived STS credentials. This is the default answer for almost every
  "how should this authenticate" question.
- **Instance profile:** how an EC2 instance assumes a role, with credentials
  delivered through the instance metadata service. Enforce IMDSv2, since IMDSv1
  is vulnerable to server-side request forgery.
- **IRSA / EKS Pod Identity:** how a Kubernetes pod assumes a role, so
  permissions are scoped per service account rather than per node.
- **Resource-based policy:** attached to the resource, for example an S3 bucket
  policy or SQS queue policy, and the mechanism for cross-account access.

### Equivalents in Azure

Interviews often ask for the mapping, because the concepts have different names.

| Concept | AWS | Azure |
| :--- | :--- | :--- |
| Identity for an application, created and managed by you | IAM role plus an IAM user or external identity provider | Service principal |
| Identity attached automatically to a platform resource | IAM role via instance profile, IRSA, or task role | Managed identity (system-assigned or user-assigned) |
| Credential material | Assumed-role STS tokens, short-lived | Client secret or certificate for a service principal; none for a managed identity |
| Scoping | Trust policy plus permission policy | Role assignment at a resource scope |

An **Azure service principal** is created explicitly through the portal, CLI, or
SDK, and authenticates with a client secret or certificate that you have to store
and rotate. A **managed identity** is created on the Azure resource itself, and
Azure handles the credential lifecycle entirely, so nothing is stored in code or
configuration. Managed identity is tied to the resource it belongs to; a service
principal can be used from anywhere.

The AWS parallel is direct: an IAM role assumed through an instance profile or
IRSA is the managed-identity pattern, and an IAM user with access keys is the
service-principal-with-secret pattern. In both clouds, prefer the platform-managed
option and reserve explicit credentials for systems outside the cloud, ideally
through OIDC federation so even those need no stored secret.

### Diagnosing an unexpected `AccessDenied`

Start by proving which identity made the request; do not assume the workload is
using the role you intended:

```bash
aws sts get-caller-identity
```

For a Pod, run that command inside the affected container and verify its
ServiceAccount annotation or EKS Pod Identity association. For EC2, verify the
instance profile and IMDS credentials. Then:

1. capture the exact denied action, resource ARN, Region, and request time;
2. use CloudTrail to find the event and confirm the principal;
3. evaluate identity policies, permission boundaries, session policies, service
   control policies, and the resource policy;
4. check explicit denies first because they override every allow;
5. inspect KMS key policies when an encrypted S3 object or secret is involved;
6. test the smallest policy correction, then deploy it through code review.

A role trust policy controls who may assume the role; its permission policy
controls what the assumed role may do. IRSA failures commonly come from an OIDC
issuer or `sub`/`aud` condition mismatch, not from the S3 policy itself.

Prevent recurrence with least-privilege roles per workload, short-lived
credentials, policy validation in CI, CloudTrail alerts for critical denied
operations, and change history for IAM and Organizations policies.

## Reliability and disaster recovery

### High availability, fault tolerance, and disaster recovery

- **High availability** minimises downtime through redundancy and fast failover.
  Some interruption is accepted, for example a 60-second RDS Multi-AZ failover.
- **Fault tolerance** keeps the system fully working through a component
  failure, with no visible interruption. It is stricter and costs more, for
  example an Auto Scaling group behind a load balancer across three zones with
  capacity to spare.
- **Disaster recovery** is what you do after damage beyond repair: recover data
  and bring the system back, usually elsewhere, accepting measured data loss and
  downtime.

The distinction to state: high availability and fault tolerance prevent an
outage, disaster recovery recovers from one, and you need both because
redundancy does not protect against deletion, corruption, a bad deployment, or a
compromised account.

Reference:
[disaster recovery, high availability, and fault tolerance](https://www.nakivo.com/blog/disaster-recovery-vs-high-availability-vs-fault-tolerance/)

### RPO and RTO

**RPO (Recovery Point Objective)** answers "how much data can we afford to
lose". It is a measure of data, set by backup and replication frequency. With an
RPO of 4 hours and a backup at 12:00, a failure at 15:59 is within target and a
failure at 17:00 is not.

**RTO (Recovery Time Objective)** answers "how quickly must we be back". It is a
measure of clock time, driven by how automated recovery is. An RTO of one hour
means the system is serving traffic again within 60 minutes of the outage
starting.

| | RPO | RTO |
| :--- | :--- | :--- |
| Question | How much data loss is acceptable? | How long may we be down? |
| Unit | Data, expressed as time since the last recoverable point | Elapsed time to restore service |
| Lever | Backup and replication frequency | Automation, warm capacity, runbooks |
| Cost driver | Storage and replication bandwidth | Standby infrastructure |

Mapped to AWS DR strategies, cheapest to most expensive:

| Strategy | RPO | RTO | What runs in the second Region |
| :--- | :--- | :--- | :--- |
| Backup and restore | Hours | Hours to a day | Nothing; restore from snapshots and S3 |
| Pilot light | Minutes | Tens of minutes | Data replicated, core services off |
| Warm standby | Seconds to minutes | Minutes | A scaled-down but working copy |
| Multi-Region active-active | Near zero | Near zero | Full capacity serving traffic |

Worked examples: a trading platform needs RPO near zero and RTO under 30
seconds, so active-active with synchronous or near-synchronous replication. An
internal reporting tool can take RPO 24 hours and RTO 8 hours, so daily
snapshots and a documented restore are sufficient and far cheaper.

Points worth making:

- Cost rises steeply as both targets approach zero, so agree them with the
  business rather than assuming the strictest.
- RPO of zero across long distances is limited by physics and by the CAP
  theorem: synchronous replication across Regions adds the round-trip latency to
  every write.
- RTO is met by automation. Infrastructure as code plus tested failover
  automation is the difference between a documented RTO and a real one, and an
  untested DR plan should be assumed not to work.

### SLI, SLO, and SLA

| Term | Meaning | Analogy | Audience |
| :--- | :--- | :--- | :--- |
| SLI, Service Level Indicator | A measured metric of service behaviour | Speedometer | Engineers |
| SLO, Service Level Objective | The internal target for an SLI | Speed limit | Engineers and product |
| SLA, Service Level Agreement | A contractual commitment with consequences | Speeding fine | Business and customers |

An **SLI** is the raw measurement: request latency, error rate, availability,
throughput, usually as `successful events / total events`.

An **SLO** is the target, for example "99.9% of requests complete in under 200 ms
over a rolling 30 days". The useful mechanism attached to it is the **error
budget**: the 0.1% you are allowed to fail. While budget remains you can ship;
when it is exhausted, reliability work takes priority over features.

An **SLA** is the external promise, for example "if monthly availability falls
below 99.5%, we credit 10% of the bill". Keep the SLO stricter than the SLA, so
you detect and respond before you owe anyone money.

## CI/CD on AWS

A typical AWS-native pipeline, and the equivalent choices if you use GitHub
Actions or GitLab instead.

| Stage | AWS service | Purpose |
| :--- | :--- | :--- |
| Source | CodeCommit, or GitHub/GitLab via connection | Trigger on push, pull request, or tag |
| Build and test | CodeBuild | Compile, run tests, build the container image |
| Artifact store | ECR for images, S3 for archives | Immutable versioned artifacts |
| Orchestration | CodePipeline or Step Functions | Stage ordering, approvals, rollback |
| Deploy | CodeDeploy, ECS/EKS rolling update, CloudFormation, Terraform | Apply the change |
| Verify | CloudWatch alarms, synthetic canaries | Automatic rollback on regression |

Practices that come up in interviews:

- **Build once, promote the artifact.** Build the image in the pipeline, tag it
  with the commit SHA, and deploy that exact digest to every environment. A
  rebuild per environment means you are not shipping what you tested.
- **No long-lived credentials in the pipeline.** Use OIDC federation from GitHub
  Actions or GitLab into an IAM role, so the pipeline gets short-lived STS
  credentials and there is no access key to leak or rotate.
- **Least privilege per stage.** The build role can push to ECR but not deploy;
  the deploy role can update the service but not read production data.
- **Deployment strategy chosen for the blast radius:** rolling update for
  ordinary changes; blue/green through CodeDeploy or two target groups when you
  need instant rollback; canary with a weighted listener rule or ALB weighted
  target groups when you want to expose a small percentage first.
- **Automated rollback.** Wire CodeDeploy or the deployment controller to
  CloudWatch alarms on error rate and latency so a bad release reverts without a
  human deciding.
- **Infrastructure through the same pipeline.** Terraform or CloudFormation
  changes should be planned, reviewed, and applied by the pipeline, with drift
  detection, rather than changed in the console.
- **Environment isolation by account.** Separate AWS accounts for development,
  staging, and production under Organizations, with the pipeline assuming a role
  into each. This is the strongest available blast-radius boundary.

## Reference

- [AWS S3 storage classes](https://aws.amazon.com/s3/storage-classes/)
- [EC2 instance types](https://aws.amazon.com/ec2/instance-types/)
- [VPC documentation](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
