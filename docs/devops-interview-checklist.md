# DevOps Interview Checklist

Use this as a self-assessment, not as a second copy of the answers. Each group
links to the canonical study guide. Mark a question complete only when you can
answer it aloud with a practical example and one important limitation or
failure mode.

## Linux and networking

Read [Linux](linux-interview-guide.md), including its
[command reference](linux-interview-guide.md#command-reference).

- [ ] Explain process states, zombie processes, and orphan processes.
- [ ] Interpret load average on a multi-core host.
- [ ] Compare virtual memory, resident memory, and swap.
- [ ] Change a running process's CPU priority safely.
- [ ] Explain file permissions, ownership, and the setuid, setgid, and sticky bits.
- [ ] Compare a hard link with a symbolic link.
- [ ] Manage a service with systemd and investigate it with journald.
- [ ] Explain CIDR and calculate the usable range of a subnet.
- [ ] Describe DNS resolution from browser to authoritative server.
- [ ] Explain the TCP three-way handshake and when UDP is preferable.
- [ ] Diagnose a host that is reachable by IP but not by hostname.

## Git and CI/CD

Read [Git](git-interview-guide.md) and [Docker CI/CD](docker-interview-guide.md#docker-in-cicd).

- [ ] Compare merge and rebase, including the risk of rewriting shared history.
- [ ] Compare `reset`, `revert`, and `restore`.
- [ ] Recover a lost commit with the reflog.
- [ ] Resolve a merge conflict without discarding another person's changes.
- [ ] Explain client-side and server-side Git hooks, including what CI must still enforce.
- [ ] Explain continuous integration and the gates you would place before deployment.
- [ ] Design artifact promotion so production runs the same image tested in CI.
- [ ] Explain rollback, roll-forward, and how you would make either safe.

## Docker

Read [Docker](docker-interview-guide.md), then practise its
[troubleshooting scenarios](docker-interview-guide.md#troubleshooting-scenarios).

- [ ] Compare containers with virtual machines.
- [ ] Explain image layers and how Docker's build cache works.
- [ ] Compare `COPY` with `ADD`.
- [ ] Compare `CMD` with `ENTRYPOINT`, including how each is overridden.
- [ ] Describe a container's lifecycle and signal handling.
- [ ] Compare bridge, host, none, overlay, and macvlan networking.
- [ ] Explain what `docker run --network=none nginx` does.
- [ ] Compare volumes, bind mounts, and tmpfs mounts.
- [ ] Diagnose a container that exits immediately or cannot reach another service.
- [ ] Secure a Docker image and runtime for production.

## Kubernetes

Read the [Kubernetes interview guide](kubernetes-interview-guide.md).

### Architecture and workloads

- [ ] Explain the API server, etcd, scheduler, controller manager, kubelet, and kube-proxy.
- [ ] Explain what happens when two members of a three-member etcd cluster fail.
- [ ] Compare a Pod, ReplicaSet, Deployment, DaemonSet, Job, and StatefulSet.
- [ ] Explain Pod phases, restart policies, init containers, and sidecars.
- [ ] Compare liveness, readiness, and startup probes and their HTTP, TCP, exec, and gRPC mechanisms.
- [ ] Explain how a safe rolling update and rollback work.

### Scheduling, networking, and storage

- [ ] Place a Pod on a labelled node using node affinity or a node selector.
- [ ] Compare Pod affinity, anti-affinity, taints, and tolerations.
- [ ] Explain `NoSchedule`, `PreferNoSchedule`, and `NoExecute`.
- [ ] Compare resource requests, limits, QoS classes, and eviction.
- [ ] Distinguish scaling from autoscaling, then compare HPA, VPA, and node autoscaling.
- [ ] Restrict communication so only one selected workload can reach another.
- [ ] Explain Service discovery, kube-proxy, Ingress, and a headless Service.
- [ ] Compare ConfigMaps and Secrets, name common Secret types, and explain how Pods consume them.
- [ ] Compare a PersistentVolume, PersistentVolumeClaim, StorageClass, and CSI driver.
- [ ] Explain why editing an existing Pod has important limitations.

### Security and operations

- [ ] Explain authentication, authorization, admission control, and RBAC.
- [ ] Harden a workload so it cannot run as root or gain extra privileges.
- [ ] Explain why base64 is not encryption and how to protect Kubernetes Secrets.
- [ ] Upgrade and drain a node while respecting disruption budgets.
- [ ] Diagnose `CrashLoopBackOff`, `ImagePullBackOff`, `Pending`, and DNS failures.
- [ ] Explain what Helm adds and how values precedence works.

## Terraform

Read [Terraform](terraform-interview-guide.md), then use the
[certification drills](terraform-certification-drills.md) for recall practice.

- [ ] Explain what `terraform init`, `validate`, `plan`, and `apply` do.
- [ ] Explain why Terraform state exists and why it contains sensitive data.
- [ ] Describe remote state, locking, and safe stale-lock recovery.
- [ ] Compare `count` and `for_each`, including resource-address stability.
- [ ] Explain variables, locals, outputs, and expression interpolation.
- [ ] Compare providers, provisioners, resources, and data sources.
- [ ] Compare `terraform_data` with the legacy `null_resource` and explain when neither should be used.
- [ ] Explain how provider plugins and `.terraform.lock.hcl` work.
- [ ] Design a reusable module and pass values between parent and child modules.
- [ ] Import existing infrastructure without recreating it.
- [ ] Diagnose drift, a partial apply, or an unexpected replacement.

## AWS

Read the [AWS core guide](aws-interview-guide.md).

- [ ] Compare a security group with a network ACL.
- [ ] Compare a NAT gateway with a NAT instance.
- [ ] Explain the path of outbound traffic from a private subnet through NAT.
- [ ] Explain VPC peering and its non-transitive routing limitation.
- [ ] Choose between an internet gateway, NAT, VPC endpoint, and Transit Gateway.
- [ ] Compare ALB, NLB, and Gateway Load Balancer and choose one for a workload.
- [ ] Choose an EC2 instance family and pricing model for a workload.
- [ ] Compare the main S3 storage classes and lifecycle transitions.
- [ ] Explain IAM users, groups, roles, policies, and temporary credentials.
- [ ] Explain serverless computing without claiming that servers do not exist.
- [ ] Compare high availability, fault tolerance, and disaster recovery.
- [ ] Define RPO, RTO, SLI, SLO, and SLA.
- [ ] Diagnose an AWS `AccessDenied` failure from a workload.

## Troubleshooting and system design

For every scenario, state the blast radius, evidence to collect, safe recovery,
and prevention before proposing commands.

- [ ] A deployment succeeded, but the service is unavailable.
- [ ] A CI runner reports `no space left on device`.
- [ ] A production database is at 100% CPU.
- [ ] Terraform plans to replace a production database.
- [ ] A Kubernetes workload is healthy but receives no traffic.
- [ ] A container works locally but fails in CI.
- [ ] DNS is intermittently failing for one service.
- [ ] An application suddenly loses permission to read an S3 bucket.
- [ ] Design a highly available service across failure domains.
- [ ] Explain how you would observe and safely reduce deployment risk.

## Behavioural questions

Answer with **situation, task, action, and result (STAR)**. Use a real example,
state your personal contribution, quantify the result where possible, and say
what you learned.

- [ ] Tell me about a significant responsibility you took on outside your normal role.
- [ ] Describe a production incident you diagnosed under pressure.
- [ ] Describe a disagreement about technical risk and how you resolved it.
- [ ] Describe an automation that removed recurring manual work.
- [ ] Describe a mistake you made and the control you added afterward.
