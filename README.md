# DevOps Interview Study Guide

Curated notes, interview questions, troubleshooting scenarios, and hands-on
examples for DevOps and SRE preparation.

## Start here

1. Use the [interview checklist](Interview_Q_N_A.md) to identify weak areas.
2. Read the canonical topic guide linked from each question.
3. Practise explaining the answer in two minutes: definition, operation,
   production example, and one failure mode.
4. Work through the scenario guides without reading the solution first.
5. Use the labs and examples only after understanding the underlying concept.

## Core interview topics

### Linux and networking

- [Linux](linux/Linux.md): processes, memory, filesystems, permissions,
  networking, DNS, CIDR, HTTP, SSH, and a practical command reference

### Git and delivery

- [Git](git/git.md): merge, rebase, conflict resolution, recovery, hooks, tags,
  and CI usage

### Docker

- [Docker](docker/Docker.md): images, Dockerfiles, runtime isolation,
  networking, storage, security, CI/CD, and troubleshooting scenarios

### Kubernetes

- [Kubernetes](kubernetes/md-files/Kubernetes.md): architecture, failures,
  scheduling, networking, storage, security, upgrades, workloads, and Helm
- [Secret recipes](kubernetes/md-files/Secrets-Recipes.md)
- [CKA lab recipes](kubernetes/md-files/CKA-Labs.md)

### Terraform

- [Terraform](terraform/Terraform.md): interview concepts and operational
  troubleshooting scenarios
- [Terraform certification drills](terraform/Terraform-Certification.md):
  deduplicated multiple-choice practice grouped by objective

### AWS

- [AWS core guide](aws/AWS.md): VPC, security, compute, storage, databases,
  identity, serverless, reliability, and CI/CD

## Hands-on labs and examples

These resources support the core guides but are not the recommended starting
point.

- [Kubernetes example manifests](kubernetes/task-official-k8s/)
- [Python exercises](python-learning/)
- [Kubernetes cheat sheet](kubernetes/cheatsheet-kubernetes-A4.pdf)

## Supplemental material

- [AWS Machine Learning Associate notes](aws/AWS_MLCA-01.md)
- [Informatica IDMC notes](Informatica.md)

These are preserved for specialised preparation and are intentionally separate
from the core DevOps interview path.

## External practice

- [DevOps Exercises](https://github.com/bregman-arie/devops-exercises)
- [DevOps: The Hard Way on AWS](https://github.com/AdminTurnedDevOps/DevOps-The-Hard-Way-AWS)
- [Docker Labs](https://github.com/collabnix/dockerlabs)
- [Docker cheat sheet](https://github.com/wsargent/docker-cheat-sheet)
- [CKA exercises](https://github.com/walidshaari/Kubernetes-Certified-Administrator)
- [CKAD exercises](https://github.com/dgkanatsios/CKAD-exercises)
- [Jenkins pipeline examples](https://github.com/jenkinsci/pipeline-examples)

## Repository scope

Markdown files under the topic directories are study notes. YAML, JSON,
scripts, images, PDFs, and lab directories are runnable or reference artifacts;
review them before using them in a real environment because example values and
credentials are not production configuration.
