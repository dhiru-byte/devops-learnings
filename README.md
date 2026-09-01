# DevOps Interview Study Pointers

Compact interview facts, commands, gotchas, scenarios, and links to official
documentation. Start with the [interview checklist](docs/devops-interview-checklist.md).

## Core topics

| Topic | Local pointer guide | Official documentation |
| :--- | :--- | :--- |
| Linux and networking | [Linux](docs/linux-interview-guide.md) | [Linux man pages](https://man7.org/linux/man-pages/) · [Kernel docs](https://docs.kernel.org/) |
| Git and delivery | [Git](docs/git-interview-guide.md) | [Git documentation](https://git-scm.com/doc) |
| Containers | [Docker](docs/docker-interview-guide.md) | [Docker documentation](https://docs.docker.com/) |
| Orchestration | [Kubernetes](docs/kubernetes-interview-guide.md) | [Kubernetes documentation](https://kubernetes.io/docs/) · [Helm docs](https://helm.sh/docs/) |
| Infrastructure as code | [Terraform](docs/terraform-interview-guide.md) | [Terraform documentation](https://developer.hashicorp.com/terraform/docs) |
| Cloud platform | [AWS](docs/aws-interview-guide.md) | [AWS documentation](https://docs.aws.amazon.com/) · [Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) |

## Practice and certification

| Track | Use it for | Official documentation |
| :--- | :--- | :--- |
| [CKA lab pointers](docs/kubernetes-cka-labs.md) | `kubectl`, workloads, networking, RBAC, node and etcd tasks | [kubectl reference](https://kubernetes.io/docs/reference/kubectl/) |
| [Kubernetes Secret recipes](docs/kubernetes-secrets-recipes.md) | Create, mount, rotate, and verify Secrets | [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) |
| [Terraform Associate pointers](docs/terraform-certification-drills.md) | Exam domains, traps, commands, and recall scenarios | [Terraform Associate](https://developer.hashicorp.com/terraform/tutorials/certification-004) |
| [AWS ML Associate pointers](docs/aws-ml-associate-study-guide.md) | MLA-C01 services, algorithms, deployment, and exam traps | [Certification page](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) |

## Study loop

1. Pick unchecked items in the [interview checklist](docs/devops-interview-checklist.md).
2. Use the local guide for key facts, commands, and production gotchas.
3. Follow its official links for complete behavior and version-specific details.
4. Answer aloud: definition → decision → example → failure mode.
5. Practise scenarios as: symptom → evidence → fix → prevention.

## Community practice

- [DevOps Exercises](https://github.com/bregman-arie/devops-exercises)
- [DevOps: The Hard Way on AWS](https://github.com/AdminTurnedDevOps/DevOps-The-Hard-Way-AWS)
- [Docker Labs](https://github.com/collabnix/dockerlabs)
- [CKA exercises](https://github.com/walidshaari/Kubernetes-Certified-Administrator)
- [CKAD exercises](https://github.com/dgkanatsios/CKAD-exercises)

## Scope

- `docs/*.md`: curated study pointers; verify current details in linked official docs.
- Commands marked destructive require review before use.
- Community links are practice material, not authoritative documentation.
