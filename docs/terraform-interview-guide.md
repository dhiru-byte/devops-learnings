# Terraform

Interview guide for Terraform: language, state, providers, modules, and the
operational failures interviewers use to test judgement. Multiple-choice
certification drills are in [terraform-certification-drills.md](terraform-certification-drills.md).

Terraform Cloud was renamed **HCP Terraform** in 2024. Both names appear in older
documentation and in the certification exam; they refer to the same product.

Work troubleshooting questions as **symptom -> evidence -> cause -> fix ->
prevention**. Collect evidence before you touch state. Before any
`terraform state rm`, `mv` or `push`, confirm the selected workspace and backend,
stop concurrent runs, and save a restricted backup with
`(umask 077; terraform state pull > state-backup.json)`. Store that backup only
in an approved secure location and delete it when recovery is complete; it may
contain plaintext secrets.

The most useful habit in an interview answer: say what you would check *before*
changing anything, and say how you would make the fix reviewable rather than
applying it from your laptop.

## Contents

- [Fundamentals](#fundamentals)
- [Configuration language](#configuration-language)
- [Resources and meta-arguments](#resources-and-meta-arguments)
- [Providers](#providers)
- [Variables and outputs](#variables-and-outputs)
- [State](#state)
- [Provisioners](#provisioners)
- [Modules](#modules)
- [Operations and tooling](#operations-and-tooling)
- [Troubleshooting scenarios](#troubleshooting-scenarios)
  - [First-response triage](#first-response-triage)
  - [1. Error acquiring the state lock](#1-error-acquiring-the-state-lock)
  - [2. Plan wants to destroy and recreate a production database](#2-plan-wants-to-destroy-and-recreate-a-production-database)
  - [3. Someone changed infrastructure in the console (drift)](#3-someone-changed-infrastructure-in-the-console-drift)
  - [4. State file lost, corrupted, or partially deleted](#4-state-file-lost-corrupted-or-partially-deleted)
  - [5. Provider version drift between laptop and CI](#5-provider-version-drift-between-laptop-and-ci)
  - [6. Secrets found in plaintext in the state file](#6-secrets-found-in-plaintext-in-the-state-file)
  - [7. Cycle error, or resources created in the wrong order](#7-cycle-error-or-resources-created-in-the-wrong-order)
  - [8. Apply failed halfway and left partial infrastructure](#8-apply-failed-halfway-and-left-partial-infrastructure)
  - [9. Migrating count to for_each without destroying everything](#9-migrating-count-to-for_each-without-destroying-everything)
  - [10. Deploying to multiple regions or accounts in one configuration](#10-deploying-to-multiple-regions-or-accounts-in-one-configuration)

## Fundamentals

### What is Terraform and how does it work?

Terraform is an infrastructure as code tool that lets you define, provision and version
infrastructure across providers using a declarative configuration language.

The workflow is: you describe the desired end state in `.tf` files, Terraform reads the current
state (from the state file plus a refresh against the provider APIs), computes the difference, and
produces an execution plan describing what it will create, update or destroy. Applying that plan
calls the provider APIs to reach the desired state and records the result in state.

Because Terraform diffs desired against actual state on every run, the same configuration applied
twice produces no changes the second time.

Reference: [What is Terraform](https://developer.hashicorp.com/terraform/intro)

### Why would you choose Terraform over Ansible, Puppet, or CloudFormation?

An incomplete answer is "Ansible and Puppet are configuration management, Terraform is provisioning".
That is broadly true but does not explain the choice, and it does not address CloudFormation at
all. Better reasons:

- **Declarative rather than procedural.** You state that you want two servers; Terraform works out
  whether that means creating two, creating one more, or destroying one. In Ansible you have to
  write logic that converges to that outcome.
- **A real plan step.** `terraform plan` shows the exact set of creates, updates, replacements and
  destroys before anything happens. This is the single biggest operational advantage in review and
  change-approval workflows.
- **Multi-provider, one language.** CloudFormation is AWS-only. One Terraform configuration can
  span AWS, Cloudflare, Datadog, GitHub and an internal API with the same syntax and one dependency
  graph.
- **Explicit dependency graph and state.** Terraform knows what it owns and in what order to build
  it, which makes destroy, replacement and drift detection tractable.

Honest counterpoints worth raising: Terraform state is an artefact you must manage and secure,
CloudFormation has deeper native AWS integration (automatic rollback, drift detection built into
the service), and Ansible is a better fit for in-guest configuration after the machine exists.
Since the 2023 licence change, OpenTofu is a relevant open-source fork to mention.

### Name some competitors of Terraform.

Genuine alternatives, meaning tools that also provision infrastructure declaratively from code:

- **OpenTofu** - the open-source fork created after the 2023 BSL licence change, still largely
  configuration-compatible.
- **Pulumi** - the same model, but configuration is written in TypeScript, Python, Go or C#.
- **AWS CloudFormation** and **AWS CDK** - AWS-native, deeply integrated but single-cloud.
- **Azure Resource Manager / Bicep** and **Google Cloud Infrastructure Manager** - the equivalents
  for the other two major clouds. Google Cloud Deployment Manager was retired on March 31, 2026
  and should only be described as the legacy predecessor.
- **Crossplane** - provisions cloud resources through Kubernetes CRDs and a reconciliation loop
  rather than a state file.

Packer, Ansible, Puppet, Chef and Kubernetes are frequently listed as competitors but are not. They
solve adjacent problems: Packer builds machine images, Ansible/Puppet/Chef configure software
inside machines that already exist, and Kubernetes schedules workloads onto infrastructure that
something else provisioned. They are commonly used alongside Terraform, not instead of it.

Reference: [Google Cloud Infrastructure Manager](https://cloud.google.com/infrastructure-manager/docs/overview)

### What is a "Terraform configuration"?

A root module together with the tree of child modules it calls. "Configuration" means the whole
unit Terraform evaluates in one run, not an individual `.tf` file: Terraform loads every `.tf` file
in the working directory as a single namespace, so splitting code across `main.tf`, `variables.tf`
and `outputs.tf` is a readability convention, not a structural one.

A root configuration declares at most one backend, but it does not always map to one physical state
snapshot. The selected workspace chooses the state within that backend:

- With the local backend, the `default` workspace uses `terraform.tfstate`; non-default workspaces
  use separate files under `terraform.tfstate.d/`.
- With remote backends, the backend's workspace or key rules determine which remote state object is
  selected. One backend configuration can therefore address multiple workspace states.
- HCP Terraform workspaces each maintain their own state and run settings; they are not the same
  concept as CLI workspaces, despite the shared name.

The precise relationship is: **configuration -> configured backend -> selected workspace -> one
state snapshot**.

Reference: [Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)

### Can you add policies to open-source Terraform?

Not with Sentinel. Policy as code is a commercial feature: Sentinel and native OPA integration run
between plan and apply in HCP Terraform (on paid tiers) and Terraform Enterprise, where they can
block an apply before it happens.

With the open-source CLI you get the same outcome by adding checks to the pipeline instead:

- Run `conftest` or `opa eval` against the JSON plan
  (`terraform show -json tfplan`) and fail the job on a policy violation.
- Use `tfsec`, `checkov` or `trivy config` for security and compliance rule sets.
- Enforce guardrails outside Terraform with cloud-native controls such as AWS Service Control
  Policies or Azure Policy, which apply regardless of how the request was made.

The difference is where enforcement lives. Sentinel is part of the run and cannot be bypassed by
someone running Terraform locally; a CI check can be, unless the cloud credentials are only
available to the pipeline.

### What is HCL?

HashiCorp Configuration Language, the declarative language used by Terraform and other HashiCorp
tools. It is designed to be readable by humans and machines: JSON is a valid alternative syntax
(`.tf.json`), so configuration can be generated programmatically when needed.

HCL supports expressions, functions, conditionals, loops (`for`, `for_each`, `count`), and type
constraints, but it deliberately has no user-defined functions and no general-purpose control flow.

### Is Terraform mutable or immutable? Declarative or imperative?

Immutable and declarative.

Immutable in the sense that changing an attribute that a provider cannot update in place causes
Terraform to destroy and recreate the object rather than mutate it. Declarative in the sense that
you describe the desired end state, not the steps to reach it.

Note that immutability is a property of the provider and resource, not of Terraform itself: many
attributes are updatable in place, and Terraform will do so when the provider supports it. The plan
output tells you which is happening (`~ update in-place` versus `-/+ must be replaced`).

### Define the core Terraform terminology.

| Term | Meaning |
| :--- | :--- |
| Provider | Plugin that implements resource types for an API (AWS, Azure, Kubernetes, GitHub). |
| Resource | A block describing one infrastructure object Terraform manages. |
| Data source | A read-only lookup of something Terraform does not manage. |
| Module | A directory of `.tf` files used as a reusable unit. Every configuration has a root module. |
| State | Terraform's record of which real objects correspond to which configuration addresses. |
| Backend | Where state is stored and, for some backends, where operations run. |
| Plan | The computed set of changes needed to reach the desired state. |
| Apply | Executing a plan against the provider APIs. |
| Output value | A value a module returns to its caller or prints to the CLI. |

### What are the main features of Terraform?

- **Execution plans** that show what will change before it changes.
- **Resource graph**, which lets Terraform parallelise independent work and order dependent work.
- **Change automation**, applying complex change sets with minimal human interaction.
- **Infrastructure as code**, so infrastructure is versioned, reviewed and reproducible.
- **Provider ecosystem** covering thousands of APIs through a single language.

### Can Terraform manage on-premises infrastructure?

Yes. Any system with an API can have a provider. Existing providers cover VMware vSphere, Nutanix,
OpenStack, Proxmox, libvirt/KVM, F5, NetApp, Kubernetes and many others. If no provider exists you
can write one with the Terraform Plugin Framework.

The practical constraint is not on-prem versus cloud, but whether the target exposes a stable API
with the CRUD semantics Terraform needs.

### How do you structure a Terraform project?

A typical root module splits by concern rather than by resource:

```
.
├── versions.tf     # terraform block: required_version, required_providers, backend
├── providers.tf    # provider configurations and aliases
├── variables.tf    # input variables
├── main.tf         # resources and module calls
├── outputs.tf      # output values
└── terraform.tfvars
```

For anything beyond a single stack, the important decisions are the ones above the file layout:

- One state file per environment and per blast radius, not one giant state.
- Shared behaviour lives in versioned modules, ideally in their own repositories with tags.
- Environments differ only by `.tfvars` and backend key, not by copies of the resource code.

## Configuration Language

### What categories of built-in functions does Terraform provide?

Numeric, string, collection, encoding, filesystem, date and time, hash and crypto, IP network, and
type conversion functions.

HCL has no user-defined functions. If you need logic that the built-ins cannot express, the options
are a `locals` block with nested expressions, an external data source, or generating configuration
with another tool. Use `terraform console` to experiment with expressions interactively.

Reference: [Built-in functions](https://developer.hashicorp.com/terraform/language/functions)

### What is a data source, and when do you need one?

A data source reads information from a provider without managing it. Common cases:

- Referencing something Terraform does not own, such as a shared VPC or an AMI published by another
  team: `data "aws_ami" "ubuntu" { most_recent = true ... }`.
- Reading outputs from another state file with `terraform_remote_state`.
- Computing a value with type checking and provider-side validation, such as building an IAM policy
  with `aws_iam_policy_document` instead of embedding raw JSON.

Data sources are read during plan, so a value that only exists after apply cannot be looked up in
the same run.

### What are local values and when should you use them?

A `locals` block names an expression so you can reuse it without repeating it:

```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
```

Use them for values derived from variables or resource attributes that appear in several places. Do
not use them as a substitute for input variables: a local cannot be overridden by the caller.

## Resources and Meta-Arguments

### What is a resource, and what do the parts of a resource block mean?

A resource block describes one or more infrastructure objects that Terraform manages.

```hcl
resource "aws_instance" "web_server" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.micro"
}
```

- `resource` is the block keyword.
- `aws_instance` is the resource **type**; its prefix identifies the provider (`aws`).
- `web_server` is the **local name**, unique within the module.
- The resource **address** is `aws_instance.web_server`, and that is how you reference it elsewhere.

Within the block:

- **Arguments** are the inputs you set (`instance_type`).
- **Attributes** are values the provider returns (`aws_instance.web_server.private_ip`). Some are
  known only after apply.
- **Meta-arguments** (`count`, `for_each`, `depends_on`, `provider`, `lifecycle`) are handled by
  Terraform itself and work with every provider.

### Explain the resource meta-arguments: depends_on, count, for_each, provider, lifecycle.

**`depends_on`** forces ordering when the dependency is not visible in the configuration. Terraform
infers dependencies from references, so you only need this for hidden ones, such as an IAM policy
that must exist before an instance can use its role:

```hcl
resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = "t3.micro"
  depends_on    = [aws_iam_role_policy.example]
}
```

**`count`** creates a fixed number of near-identical instances, indexed by `count.index`:

```hcl
resource "aws_instance" "server" {
  count = 3
  tags  = { Name = "server-${count.index}" }
}
```

**`for_each`** creates one instance per element of a map or set of strings, keyed by `each.key`:

```hcl
resource "aws_iam_user" "users" {
  for_each = toset(["alice", "bob", "charlie"])
  name     = each.key
}
```

**`provider`** selects a non-default provider configuration, which is how you deploy to more than
one region or account in a single configuration (see
[Deploying to multiple regions or accounts](#10-deploying-to-multiple-regions-or-accounts-in-one-configuration)):

```hcl
resource "aws_vpc" "west" {
  provider   = aws.west
  cidr_block = "10.0.0.0/16"
}
```

**`lifecycle`** changes how Terraform plans the change:

- `create_before_destroy` builds the replacement before removing the old object, for zero-downtime
  replacement.
- `prevent_destroy` fails the plan if anything would delete the resource. Useful for databases.
  See [Plan wants to destroy and recreate a production database](#2-plan-wants-to-destroy-and-recreate-a-production-database).
- `ignore_changes` tells Terraform to accept out-of-band changes to specific attributes.
- `replace_triggered_by` forces replacement when another resource or attribute changes.

### When should you use for_each instead of count?

Prefer `for_each` whenever the instances are distinguishable.

`count` keys instances by position. Removing the middle element of a three-element list shifts every
later index down by one, so Terraform plans to destroy and recreate resources that did not actually
change. `for_each` keys instances by a stable map key or set value, so removing one leaves the
others untouched.

| | `count` | `for_each` |
| :--- | :--- | :--- |
| Input type | Number | Map or set of strings |
| Best for | Truly identical copies, or a 0/1 conditional | Distinct, named instances |
| Address | `aws_instance.web[0]` | `aws_instance.web["prod"]` |
| Stability | Index-based, shifts on removal | Key-based, stable |

`count` is still the right tool for conditional creation: `count = var.enabled ? 1 : 0`.

Migrating between the two, or renaming keys, is a state operation: use `moved` blocks (Terraform
1.1+) rather than `terraform state mv` so the change is reviewable in the plan. The full
count-to-`for_each` walkthrough is in
[Migrating count to for_each](#9-migrating-count-to-for_each-without-destroying-everything).

### What is a dynamic block?

A `dynamic` block generates repeated nested blocks from a collection, so you do not have to write
the same nested block many times:

```hcl
resource "aws_security_group" "web" {
  name = "web"

  dynamic "ingress" {
    for_each = var.allowed_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

The trade-off is readability: dynamic blocks hide the shape of the resulting configuration and make
plan output harder to reason about. Use them for genuinely variable-length nested blocks, not to
save a few lines.

### What is a "tainted" resource?

A resource that Terraform created successfully but whose provisioning step failed. Terraform cannot
know whether the object is usable, so it marks it tainted in state and replaces it on the next
apply.

You can mark a resource for replacement yourself. The modern command is:

```bash
terraform apply -replace="aws_instance.web"
```

`terraform taint` did the same thing by editing state directly. It has been deprecated since
Terraform 0.15.2 because `-replace` shows the replacement in a plan you can review first.

### What is the null_resource, and what replaced it?

`null_resource` implements the normal resource lifecycle but creates nothing. Its purpose is to be
a container for provisioners, or to run an action when its `triggers` map changes:

```hcl
resource "null_resource" "run_migration" {
  triggers = {
    schema_version = var.schema_version
  }

  provisioner "local-exec" {
    command = "./migrate.sh"
  }
}
```

Since Terraform 1.4, `terraform_data` is the built-in equivalent and needs no external provider.
Prefer it in new code.

Reference: [terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data)

## Providers

### What is a provider?

A plugin that teaches Terraform how to talk to an API. Each provider contributes resource types and
data sources; without a provider, Terraform can manage nothing. Providers are separate binaries
distributed through a registry, not part of the Terraform core binary.

In `resource "libvirt_domain" "instance" {}` the provider is `libvirt`, inferred from the resource
type prefix.

### How does Terraform find and install providers?

`terraform init` reads the configuration, determines which providers the resource and data types
require, resolves versions against any constraints in `required_providers`, downloads the plugins
into `.terraform/providers`, and records the exact versions and checksums in `.terraform.lock.hcl`.

Commit the lock file. It guarantees that everyone, including CI, resolves the same provider
versions, and the recorded checksums protect against a tampered plugin. Run
`terraform init -upgrade` when you deliberately want to move within the allowed constraints.
Laptop-versus-CI drift from an uncommitted or incomplete lock file is covered in
[Provider version drift between laptop and CI](#5-provider-version-drift-between-laptop-and-ci).

Terraform can also install from a filesystem mirror or network mirror, which is how air-gapped
environments work.

Reference: [Dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)

### How do you pin provider and module versions?

Providers go in `required_providers`, with the constraint on the `version` argument:

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

Registry modules use the `version` argument, which accepts the same constraint syntax:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.1"
}
```

Git-sourced modules have no `version` argument; pin them in the source URL with `?ref=`, using a tag
or a commit SHA:

```hcl
module "vpc" {
  source = "git::https://github.com/org/tf-modules.git//vpc?ref=v1.4.0"
}
```

`~> 5.1` allows 5.1 and later 5.x releases but not 6.0. Terraform core and providers version
independently, so their major numbers need not match.

### What is the "random" provider used for?

Generating values that must be stable across runs but not predictable: suffixes for globally unique
names such as S3 buckets, initial passwords, or `random_uuid` values.

The value is generated once and stored in state, so it does not change on subsequent applies unless
you change the `keepers` map. Note that anything `random` generates is written to state in
plaintext, so a generated password still needs an encrypted backend.

## Variables and Outputs

### What are input variables and why use them?

Input variables are a module's parameters. They let one configuration serve several environments,
and they define the contract a module exposes to its callers, so a module is usable without reading
its internals.

```hcl
variable "app_id" {
  type        = string
  description = "Identifier of the application"
  default     = "some_value"
}
```

Reference them as `var.app_id`. Only `type` is worth treating as effectively mandatory: none of
`type`, `default` or `description` is required by Terraform, but a variable with no default is a
required input.

### What variable types does Terraform support?

Primitives: `string`, `number`, `bool`.

Collections: `list(TYPE)`, `set(TYPE)`, `map(TYPE)`.

Structural: `object({ATTR = TYPE, ...})`, `tuple([TYPE, ...])`.

Plus `any` where you deliberately want no constraint. Use `object` when a single variable must
carry several typed fields, for example a server definition with a string name and a numeric memory
size.

### How do you enforce constraints on a variable's value?

With one or more `validation` blocks:

```hcl
variable "instance_count" {
  type        = number
  description = "Number of application instances"

  validation {
    condition     = var.instance_count > 1
    error_message = "instance_count must be greater than 1."
  }
}
```

The condition must be an expression over the variable itself. For cross-variable or post-plan
invariants, use `precondition` and `postcondition` blocks in a `lifecycle` block, or a `check`
block (Terraform 1.5+).

### What is the effect of marking a variable or output as sensitive?

`sensitive = true` is an output-redaction control. It hides the value in normal `terraform plan`
and `terraform apply` output, and Terraform propagates that marking to expressions derived from it.

It does **not** encrypt the value, omit it from plan or state files, prevent provider transmission,
or make an unsafe storage location safe. The value is normally still present in Terraform
artifacts. Protect those artifacts with backend encryption and strict access control, and never
commit state or saved plan files to Git. Machine-readable commands such as
`terraform output -json` can disclose sensitive values, so do not print their output in CI logs.
Incident response when secrets are already in state is in
[Secrets found in plaintext in the state file](#6-secrets-found-in-plaintext-in-the-state-file).

Reference: [Sensitive data in state](https://developer.hashicorp.com/terraform/language/state/sensitive-data)

### How do ephemeral values and write-only arguments keep secrets out of Terraform artifacts?

Terraform 1.10 introduced ephemeral variables, child-module outputs and `ephemeral` resource
blocks. Terraform makes these values available during a run but omits them from saved plans and
state. Mark a secret both `sensitive` and `ephemeral`: `sensitive` redacts normal display, while
`ephemeral` controls persistence.

Terraform 1.11 introduced provider-defined **write-only arguments**, commonly named with a `_wo`
suffix. They accept a value during an operation but are always `null` in plan and state. This lets
an ephemeral value reach an API without becoming a Terraform artifact:

```hcl
variable "db_password" {
  type      = string
  sensitive = true
  ephemeral = true
}

variable "db_password_version" {
  type = number
}

resource "aws_db_instance" "app" {
  # Provider support and exact argument names vary by resource version.
  password_wo         = var.db_password
  password_wo_version = var.db_password_version
}
```

Terraform cannot diff a value it never stores. Providers therefore often pair a write-only
argument with a persisted version argument; increment that version to signal rotation. Ephemeral
values can only flow into ephemeral-compatible contexts, such as provider configuration,
provisioners, ephemeral outputs and write-only arguments. Provider and resource support varies, so
check the Registry schema before relying on a `_wo` argument.

References:
- [Manage sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
- [Write-only arguments](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only)

### What is the precedence order when the same variable is set in several places?

Terraform loads values in this order, and **later sources override earlier ones**:

1. The variable's `default` argument (lowest precedence)
2. Environment variables (`TF_VAR_name`)
3. `terraform.tfvars`
4. `terraform.tfvars.json`
5. `*.auto.tfvars` and `*.auto.tfvars.json`, in lexical order of filename
6. `-var` and `-var-file` options on the command line, in the order given

So a `-var` flag wins over everything, while the declaration default is used only when no other
source supplies the value. Files given explicitly with `-var-file` are not loaded automatically;
only the `terraform.tfvars` and `*.auto.tfvars` names are.

Reference: [Variable definition precedence](https://developer.hashicorp.com/terraform/language/values/variables#variable-definition-precedence)

### How do you define many variable values without repeating them on the command line?

Put them in a `.tfvars` file, which is a flat set of assignments:

```hcl
region         = "eu-west-1"
instance_count = 2
tags = {
  owner = "platform"
}
```

Terraform loads `terraform.tfvars` and any `*.auto.tfvars` automatically; pass anything else with
`-var-file=prod.tfvars`. Keep `.tfvars` files containing secrets out of version control.

### What are output values, and what does terraform output do?

Outputs are the return values of a module. A child module's outputs are how its caller reads
computed values (`module.vpc.vpc_id`); a root module's outputs are what Terraform prints after
apply and what other configurations can read through the `terraform_remote_state` data source.

`terraform output` reads them from state without running a plan; `terraform output -json` emits
machine-readable output, which is the usual way to hand values to a CI pipeline.

Only the root module's outputs are printed. To surface a child module's value on the CLI you must
declare an output in the child *and* re-export it in the root.

## State

### What is terraform.tfstate used for?

State is Terraform's mapping from configuration addresses to real objects. It records resource IDs
and attribute values, module and provider metadata, output values, and resource dependencies.

It exists because provider APIs cannot answer "which of these objects do you manage, and under what
name". State is also a performance cache: Terraform can produce a plan by diffing configuration
against state rather than enumerating every object in the account.

### Where should you store state, and why does it matter?

Not in Git. State should live in a remote backend with encryption, versioning and access control:
S3 with a KMS key and object versioning, Azure Blob Storage, GCS, or HCP Terraform.

The reasons:

- State frequently contains secrets in plaintext (database passwords, generated keys, any variable
  marked sensitive), so a public or broadly readable location is a data leak.
- Concurrent writes corrupt state, so it needs a location that supports locking.
- State is the record of what you own. Losing it means adopting every resource again by hand, so it
  needs versioning and backups.

### What is remote state, and what does it give you beyond a local file?

Remote state stores `terraform.tfstate` in a shared backend instead of on one engineer's disk. That
gives you a single source of truth for the team, state locking, encryption at rest, version history
for rollback, and the ability for other configurations to read published outputs through the
`terraform_remote_state` data source.

Some backends (HCP Terraform, and the `remote` backend generally) additionally run the operations
themselves, so `plan` and `apply` execute on shared infrastructure with centrally managed
credentials.

### Explain state locking.

Before any operation that could write state, Terraform acquires a lock on the backend, and releases
it when the operation finishes. A second run against the same state fails fast with
`Error acquiring the state lock` instead of racing and corrupting it. This happens automatically on
backends that support it; nothing needs enabling.

Support varies by backend. S3 now performs locking natively with conditional writes; older setups
use a DynamoDB table via `dynamodb_table`. The local backend locks with OS file locking. Some
backends do not support locking at all.

If a process is killed mid-run the lock can be left behind. Never clear it until you have confirmed
that no run is active. The full investigation and guarded `force-unlock` procedure is in
[Error acquiring the state lock](#1-error-acquiring-the-state-lock).

Do not confuse state locking with `.terraform.lock.hcl`. That is the dependency lock file: it pins
provider versions and checksums, is created and updated by `terraform init`, and belongs in version
control.

### How do you manage state across multiple environments?

The two common patterns:

- **Directory per environment**, each with its own backend key and `.tfvars`, sharing modules. More
  files, but the environments are visibly separate and can diverge in provider configuration,
  permissions and backend.
- **CLI workspaces**, one distinct state snapshot per workspace within the configured backend. With
  the local backend these are separate files; remote backends map workspace names to distinct
  remote objects according to backend-specific rules. They still share configuration, backend
  settings and usually credentials, so they suit short-lived or low-risk environments better than
  strongly isolated production environments.

Either way, isolate each environment and blast radius in a distinct state snapshot. Do not put dev
and prod resources in the same snapshot: a dev plan could then affect prod, and one damaged state
would affect both.

### How do you rename or move a resource without destroying it?

Prefer a `moved` block, which makes the change part of the reviewable plan and works for anyone who
applies the configuration:

```hcl
moved {
  from = aws_instance.web
  to   = aws_instance.web_server
}
```

The imperative equivalent is `terraform state mv aws_instance.web aws_instance.web_server`, which
edits state directly on one machine only. Use it for one-off surgery, not for changes you want your
team to reproduce.

### State file best practices.

- Never edit it by hand. Use `terraform state` subcommands, `moved` blocks or `import`.
- Before any imperative state change, confirm the workspace/backend, acquire exclusive control,
  run `(umask 077; terraform state pull > state-backup-$(date +%s).json)`, and verify the affected
  addresses. The backup contains secrets; store and remove it accordingly.
- Treat `terraform state rm` as a deliberate handoff: it stops management but does not destroy the
  object. A later apply may create a duplicate if the resource remains in configuration.
- Treat `terraform state push` as disaster recovery only. Prefer restoring through backend
  versioning; review a diff, verify lineage/serial checks, and never use `-force` casually.
- Store it in a remote backend with encryption at rest and least-privilege access.
- Enable object versioning on the bucket so you can roll back a bad apply.
- Enable locking so concurrent runs cannot interleave.
- Keep one state per environment and per blast radius.
- Treat it as secret material: it contains plaintext values, including anything marked sensitive.

### Which command creates the state file, and where does it go by default?

`terraform apply` writes it. By default it goes to `terraform.tfstate` in the working directory,
using the local backend; the previous version is kept as `terraform.tfstate.backup`.

Configure a different location with a `backend` block inside the `terraform` block, then run
`terraform init` to migrate the existing state:

```hcl
terraform {
  backend "s3" {
    bucket = "my-tf-state"
    key    = "prod/network/terraform.tfstate"
    region = "eu-west-1"
  }
}
```

## Provisioners

### What are provisioners, and why are they a last resort?

Provisioners run actions on the local machine or on a newly created remote resource, typically to
bootstrap software that no provider models.

HashiCorp documents them as a last resort, and interviewers expect you to know why:

- They are not part of the declarative model. Terraform cannot plan them, detect drift in what they
  did, or undo them.
- A failed creation-time provisioner taints the resource, so the next apply destroys and recreates
  it.
- They usually require SSH or WinRM connectivity and credentials from the machine running Terraform,
  which is awkward in CI.

Better alternatives: cloud-init or `user_data` for first boot, a purpose-built image from Packer,
a configuration management tool triggered after apply, or a provider that models the thing directly.

### Explain local-exec and remote-exec.

**`local-exec`** runs a command on the machine executing Terraform, after the resource is created.
Use it for local side effects such as writing an inventory file or invoking another CLI:

```hcl
resource "aws_instance" "web" {
  # ...
  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> inventory.txt"
  }
}
```

**`remote-exec`** runs commands on the remote resource over SSH or WinRM, so it needs a `connection`
block:

```hcl
resource "aws_instance" "web" {
  # ...
  provisioner "remote-exec" {
    inline = ["sudo apt-get update", "sudo apt-get install -y nginx"]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}
```

The related `file` provisioner copies files to the remote resource over the same connection.

## Modules

### What is a module?

Any directory containing `.tf` files. The directory Terraform runs in is the **root module**; any
module it calls with a `module` block is a **child module**. A module groups related resources
behind input variables and output values so it can be reused and versioned like a library.

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.1"

  name = "prod-vpc"
  cidr = "10.0.0.0/16"
}
```

### How do variables and outputs cross module boundaries?

They do not do so implicitly. Scope stops at the module boundary in both directions: a child module
cannot see `var.x` from its parent, and a parent cannot see a child's resources.

To pass a value **down**, declare a variable in the child and set it in the `module` block:

```hcl
# modules/app/variables.tf
variable "environment" {
  type = string
}

# root main.tf
module "app" {
  source      = "./modules/app"
  environment = var.environment
}
```

To pass a value **up**, declare an output in the child and reference it as
`module.<NAME>.<OUTPUT>`:

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.this.id
}

# root main.tf
subnet_vpc_id = module.vpc.vpc_id
```

To have the value appear in `terraform apply` CLI output, the root module must declare an output of
its own that re-exports it.

### How do you inject dependencies between separately managed stacks?

The built-in mechanism is the `terraform_remote_state` data source, which reads another
configuration's published outputs:

```hcl
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-tf-state"
    key    = "prod/network/terraform.tfstate"
    region = "eu-west-1"
  }
}

resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.network.outputs.private_subnet_id
}
```

This couples the consumer to the producer's state file and requires read access to it. A looser
alternative is to publish the value to a data store both sides can read (SSM Parameter Store,
Consul, a tag) and look it up with a normal data source.

Terragrunt is a common third-party wrapper that makes this explicit with `dependency` blocks.

### What is the Terraform Registry?

A public index of providers and modules at
[registry.terraform.io](https://registry.terraform.io). It exposes each module's required and
optional inputs, defaults, outputs, and version history, all derived from the source repository.
Module versions come from the repository's release tags, not from anything in the module code.

Anyone can publish. "Verified" and "Partner" badges indicate the publisher is a HashiCorp partner,
not that the code has been audited; read the source before depending on it.

HCP Terraform and Terraform Enterprise add a **private registry** with the same interface, scoped to
your organisation, which is the standard answer for sharing internal modules with version
constraints and a browsable catalogue.

### How do you test a Terraform module?

In layers, cheapest first:

1. `terraform fmt -check` and `terraform validate` for syntax and internal consistency.
2. Static analysis: `tflint` for provider-specific mistakes, `tfsec`/`checkov`/`trivy` for security
   policy.
3. `terraform test` (built in since Terraform 1.6), which runs `.tftest.hcl` files containing plan-
   or apply-based assertions against the module.
4. Integration tests with Terratest, a Go library that applies the module against a real account,
   asserts on the result, and destroys it.
5. Policy as code with Sentinel or OPA in the pipeline for organisation-wide rules.

The classic interview answer is Terratest; mentioning the native `terraform test` framework shows
current knowledge.

### What is Terragrunt and what problems does it solve?

A thin wrapper around Terraform aimed at keeping large multi-environment setups DRY. Its main uses:

- Generating backend and provider configuration instead of copying it into every environment.
- Declaring dependencies between stacks and passing outputs between them.
- Running a command across many modules at once (`terragrunt run-all apply`).
- Keeping repeated CLI flags in configuration.

Much of the original motivation has been absorbed by native features: partial backend
configuration, `for_each` on modules, `moved` blocks, and stacks in HCP Terraform. It is still
widely used, but treat "we use Terragrunt" as a decision to justify rather than a default.

## Operations and Tooling

### Explain terraform init, plan, validate and apply.

- **`terraform init`** prepares the working directory: it installs providers, downloads modules,
  configures the backend and writes the dependency lock file. It is safe to re-run and is required
  after changing providers, modules or the backend.
- **`terraform validate`** checks that the configuration is syntactically valid and internally
  consistent (correct argument names, resolvable references, type-correct expressions). It makes no
  API calls and does not look at state, so it cannot tell you whether the infrastructure matches.
  The working directory must be initialised first.
- **`terraform plan`** refreshes state, compares it with the configuration and prints the changes it
  would make. It never modifies state or infrastructure. `-out=tfplan` saves the plan for a later
  `apply`.
- **`terraform apply`** executes the plan, calling provider APIs and writing the result to state.
  Without a saved plan file it computes a fresh plan and prompts for approval.

### What is terraform import, and how do you use it?

`terraform import` brings an object that already exists into Terraform state, so Terraform manages
it from then on. It does **not** generate configuration.

The workflow:

1. Identify the resource and its provider-specific ID.
2. Write configuration matching it.
3. Import it: `terraform import aws_instance.web i-0123456789abcdef0`.
4. Run `terraform plan` and expect an empty diff. A non-empty diff means your configuration does not
   yet match reality; fix the configuration, not the infrastructure.

Since Terraform 1.5 you can do this declaratively with an `import` block, which makes the import
part of a reviewable plan and can generate a starting configuration:

```hcl
import {
  to = aws_instance.web
  id = "i-0123456789abcdef0"
}
```

```bash
terraform plan -generate-config-out=generated.tf
```

Reference: [Import](https://developer.hashicorp.com/terraform/language/import)

### How do you recover from a failed apply?

A failed apply is partial, not atomic: completed operations remain in infrastructure and are
normally recorded in state. Diagnose the provider error, run a fresh plan, fix the root cause and
apply again; reverting code alone does not undo infrastructure.

For the evidence sequence, orphan-resource case and state-recovery safeguards, see
[Apply failed halfway](#8-apply-failed-halfway-and-left-partial-infrastructure)
and [State file lost or corrupted](#4-state-file-lost-corrupted-or-partially-deleted).

### How do you detect and handle drift?

Drift is any change made outside Terraform. Detect it with a refresh-only plan, which compares real
objects with the prior state and reports what would be recorded without proposing
configuration-driven infrastructure changes:

```bash
terraform plan -refresh-only
terraform apply -refresh-only   # review, approve, and record observed values in state
```

`terraform apply -refresh-only` is the explicit, reviewable way to adopt observed drift into state.
It does not make the configuration match that drift, so a later normal plan can still propose
restoring the configured value. Never use `-lock=false` for drift adoption; that flag merely
disables concurrency protection and can corrupt shared state.

For deciding whether to revert, codify, ignore or adopt each change, see
[Someone changed infrastructure in the console](#3-someone-changed-infrastructure-in-the-console-drift).
The standalone `terraform refresh` command is deprecated because it writes state without a
reviewable apply step.

### What is HCP Terraform (Terraform Cloud), and what does it add over the CLI?

A hosted service for running Terraform as a team. Over and above the open-source CLI it provides:

- Remote state storage with locking, encryption and version history.
- Remote runs on managed or self-hosted agents, so credentials live in the platform rather than on
  laptops.
- Encrypted variable storage, including workspace and variable-set level secrets.
- VCS integration: speculative plans on pull requests, applies on merge.
- Role-based access control and approval workflows for applies.
- A private module registry.
- Policy as code with Sentinel or OPA, evaluated between plan and apply.

Terraform Enterprise is the self-hosted distribution of the same product. A free tier exists; audit
logging and the richer governance features are paid.

### How do you check the installed Terraform version, and why does it matter?

```bash
terraform version
```

It also reports provider versions and warns when a newer release is available. Pin the range in
configuration so a colleague or CI runner on a different version cannot silently write an
incompatible state file:

```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
}
```

State format upgrades are one-way: once a newer Terraform writes the state, older versions refuse to
read it.

### Which commands are useful for debugging and inspection?

Use [first-response triage](#first-response-triage) for the default evidence sequence, plan
symbols, and the rule against dumping JSON state or outputs into logs.

`terraform console` is the extra tool for interviews: it evaluates expressions and functions
against current state without planning a change. `TF_LOG=DEBUG` with `TF_LOG_PATH` captures
provider API calls on stderr when the plan or apply error is not enough.

## Troubleshooting scenarios

### First-response triage

```bash
terraform version                        # core and provider versions actually in use
terraform providers                      # requirements across the root and all modules
terraform plan -refresh-only             # has anything changed outside Terraform?
terraform state list                     # what does Terraform think it owns?
terraform state show <ADDRESS>           # full attributes of one resource
terraform graph | dot -Tsvg > graph.svg  # dependency ordering
TF_LOG=DEBUG TF_LOG_PATH=./tf.log terraform plan   # provider API calls, logs go to stderr
```

Do not include `terraform show -json`, `terraform state pull` or `terraform output -json` in routine
triage output. They can disclose every sensitive value to terminal history, CI logs or retained
artifacts. Use targeted `state show` only in a restricted local session, and still assume it may
contain secrets.

Read the plan symbols before doing anything else:

| Symbol | Meaning |
| :--- | :--- |
| `+` | create |
| `-` | destroy |
| `~` | update in place; interruption depends on the resource and provider operation |
| `-/+` | destroy then create; the object is replaced and its ID changes |
| `+/-` | create then destroy, because `create_before_destroy` is set |
| `<=` | read a data source during apply |

A `-/+` on a stateful resource requires explicit review. Always find the "forces replacement"
annotation next to the attribute that caused it, and verify backup and recovery requirements before
approval.

### 1. Error acquiring the state lock

**Symptom:** every run fails immediately with `Error acquiring the state lock`, quoting a lock ID,
the operation, who created it and when.

**Evidence:**

```bash
# The error itself carries the important fields
# ID, Operation, Who, Created, Path
```

Check whether the holder is real before assuming it is stale: look for a currently running pipeline
job on the same workspace, and compare the `Created` timestamp with the age of that job.

**Cause:** a previous run was killed before it could release the lock (CI job cancelled, runner
evicted, laptop closed), or two runs really are executing concurrently against the same state.

**Fix:**

1. Confirm no apply is in flight. Breaking a live lock can interleave two writers and corrupt state.
2. Take the lock ID from the error message.
3. `terraform force-unlock <LOCK_ID>`.
4. Run `terraform plan` and confirm state still reflects reality before applying.

**Prevention:** serialise runs per state file with pipeline concurrency controls
(`concurrency:` in GitHub Actions, `resource_group:` in GitLab CI). Keep applies out of interactive
shells so a closed laptop cannot orphan a lock. Never disable locking with `-lock=false` to work
around it.

### 2. Plan wants to destroy and recreate a production database

**Symptom:** a small configuration change produces `-/+ must be replaced` against an RDS instance,
managed disk or other stateful resource.

**Evidence:**

```bash
terraform plan -out=tfplan
terraform show -json tfplan | jq '.resource_changes[]
  | select(.change.actions | index("delete"))
  | {address, actions: .change.actions, replace: .change.replace_paths}'
```

`replace_paths` names the exact attribute that forced replacement; the human-readable plan prints
`# forces replacement` on the same line.

**Cause:** you changed an immutable attribute. Common triggers are availability zone, subnet,
engine version on some providers, `name` on resources that cannot be renamed, and any change to a
`for_each` key or `count` index, which changes the resource address rather than the resource.

**Fix:**

- If the change is not actually required, revert that attribute and find another way to achieve the
  goal.
- If it is an address change rather than a real change (renaming a resource, moving it into a
  module, migrating `count` to `for_each`), it is not a replacement. Record the move in
  configuration as below; the reviewable `moved` pattern is also in
  [How do you rename or move a resource without destroying it?](#how-do-you-rename-or-move-a-resource-without-destroying-it).

  ```hcl
  moved {
    from = aws_instance.web[0]
    to   = aws_instance.web["primary"]
  }
  ```

- If the resource genuinely must be replaced, plan the migration explicitly: snapshot, provision
  the replacement alongside with `create_before_destroy`, cut over, then remove the old one.

**Prevention:** put `lifecycle { prevent_destroy = true }` on databases and other resources whose
loss is unrecoverable, so an unintended destroy plan fails instead of proceeding. Require plan output in the
pull request, and fail CI automatically when a plan contains a delete against a protected address.

### 3. Someone changed infrastructure in the console (drift)

**Symptom:** a plan proposes changes nobody made in code, or an apply reverts a fix that an engineer
applied by hand during an incident.

**Evidence:**

```bash
terraform plan -refresh-only    # what reality says, versus state
terraform state show aws_lb_listener.https
```

**Cause:** an out-of-band change. Terraform's job is to converge on the configuration, so on the
next apply it will undo anything it owns that does not match.

**Fix:** decide who owns the attribute, then pick one:

- The manual change was wrong: `terraform apply` and let Terraform restore the declared state.
- The manual change was right and should become desired state: codify it, then run a normal plan and
  apply. Terraform refreshes state as part of that plan.
- You need to accept only the newly observed remote values into state, without changing
  infrastructure: review and run `terraform apply -refresh-only`. This does not update the
  configuration, so a later normal plan can still propose reversing the drift.
- Another system legitimately owns the attribute (an autoscaler setting desired capacity, a
  deployment tool setting the image tag):

  ```hcl
  lifecycle {
    ignore_changes = [desired_count, task_definition]
  }
  ```

- The object was deleted outside Terraform: if it should remain deleted, remove it from
  configuration and use `terraform apply -refresh-only` to record the observed deletion. If it
  should exist, use a normal `terraform apply` to rebuild it.

Never add `-lock=false` to either workflow. It only disables concurrency protection; it does not
turn a normal apply into drift adoption.

**Prevention:** remove or tightly restrict human write access to environments Terraform manages, and
grant break-glass roles that are time-limited and audited. Run `terraform plan -detailed-exitcode`
on a schedule and alert on exit code 2, which means drift exists.

### 4. State file lost, corrupted, or partially deleted

**Symptom:** `terraform plan` proposes creating everything from scratch, or fails with a JSON parse
error, and the resources plainly already exist.

**Evidence:**

```bash
terraform state list                       # empty or much shorter than expected
aws s3api list-object-versions --bucket my-tf-state --prefix prod/terraform.tfstate
```

**Cause:** the state object was deleted or overwritten, an interrupted write left it truncated, or
someone ran in the wrong directory against an uninitialised backend.

**Fix:**

1. Stop all pipelines targeting that state. A single apply against empty state will duplicate the
   whole stack.
2. Confirm the active backend and workspace, record the current backend object version/ETag, and
   preserve the current state object even if it appears corrupt. Restore the previous version
   through the backend's native versioning when possible; this preserves its audit trail and avoids
   bypassing backend controls.
3. If native restoration is impossible and `terraform state push` is required, download the
   candidate version to a mode-0600 file, inspect the diff against the current state, verify its
   lineage and serial are appropriate, and obtain peer approval. Push without `-force`; a lineage
   or serial rejection is a safety signal to investigate, not a reason to add `-force`.
4. If no backup exists, rebuild state by importing each resource. Terraform 1.5+ makes this
   tolerable with `import` blocks and generated configuration:

   ```hcl
   import {
     to = aws_vpc.main
     id = "vpc-0123456789abcdef0"
   }
   ```

   ```bash
   terraform plan -generate-config-out=generated.tf
   ```

5. Verify with `terraform plan -refresh-only`, then a normal `terraform plan`, before re-enabling
   applies. Remove any local state copies securely.

**Prevention:** object versioning and MFA delete on the state bucket, deny `s3:DeleteObject` on the
state prefix for CI roles, and one distinct state snapshot per environment so a single mistake
cannot affect every environment. Test the restore path before you need it.

### 5. Provider version drift between laptop and CI

**Symptom:** the plan is clean locally but CI proposes unrelated changes, or an apply fails on an
argument that does not exist in the provider version CI resolved.

**Evidence:**

```bash
terraform version
terraform providers
git status .terraform.lock.hcl      # is it committed, and does it match?
```

**Cause:** `.terraform.lock.hcl` is not committed, or the constraint is loose (`>= 5.0`) and the two
environments resolved different versions. Provider upgrades change defaults and add computed
attributes, which shows up as spurious diffs.

**Fix:**

1. Commit the lock file.
2. Pin deliberately with a pessimistic constraint: `version = "~> 5.31"`.
3. Upgrade on purpose with `terraform init -upgrade`, review the resulting plan, and commit the
   updated lock file as its own change.
4. If the lock file was generated on one platform only, add the others so CI can use it:
   `terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`.

**Prevention:** pin `required_version` for Terraform core as well as providers, and install the
pinned version in CI with `tfenv` or `hashicorp/setup-terraform` rather than "latest".

### 6. Secrets found in plaintext in the state file

**Symptom:** a security scan reports database passwords or private keys inside
`terraform.tfstate`, even though the variables were marked `sensitive`.

**Evidence:** do not confirm the finding by dumping JSON state or piping it through `grep`; that
creates another plaintext copy and can place secrets in terminal or CI logs. Start with the
scanner's protected finding, provider/resource schema documentation, backend access logs, and state
version metadata. If direct verification is authorised, inspect only the named resource in a
restricted local session, redirect output to a mode-0600 temporary file, never print the value, and
securely remove the file afterward.

**Cause:** working as designed. `sensitive = true` only redacts CLI output; it does not keep secrets
out of state. See
[What is the effect of marking a variable or output as sensitive?](#what-is-the-effect-of-marking-a-variable-or-output-as-sensitive).

**Fix:**

1. Treat the state file as a compromised secret store: rotate every credential it contains.
2. Move state to a backend with encryption at rest and least-privilege access (S3 with a KMS key and
   a bucket policy, or HCP Terraform).
3. Preserve evidence according to the incident process, then purge old unencrypted versions from
   the bucket's version history. Coordinate this with retention and legal requirements.
4. Stop putting the secret in Terraform where possible: have the target service generate it, or
   pass only a secret-manager ARN/path rather than the value. With Terraform 1.10+, an ephemeral
   value can avoid plan/state persistence; with Terraform 1.11+, a provider-supported write-only
   argument can safely terminate that value at the API. Do not write a secret to an ordinary
   resource argument and assume the secret manager makes state safe.

**Prevention:** deny public access and enforce encryption on the state bucket, restrict who can read
the state prefix, and scan Terraform artifacts only with tools and storage approved for secrets.
Remember that `terraform output -json`, `terraform show -json` and `terraform state pull` can reveal
sensitive values by design; never echo them into pipeline logs. See
[ephemeral values and write-only arguments](#how-do-ephemeral-values-and-write-only-arguments-keep-secrets-out-of-terraform-artifacts)
for the version and provider constraints.

### 7. Cycle error, or resources created in the wrong order

**Symptom:** `Error: Cycle: aws_security_group.a, aws_security_group.b`, or an apply fails because a
dependency was not ready even though it exists in the configuration.

**Evidence:**

```bash
terraform graph | dot -Tsvg > graph.svg
terraform graph -type=plan | grep -A5 'aws_security_group'
```

**Cause:** two resources reference each other's attributes, so neither can be created first. The
"wrong order" variant is the opposite problem: there is a real dependency that Terraform cannot see
because nothing in the configuration references it.

**Fix:**

- Break the cycle by extracting the mutual reference into a separate resource. For security groups,
  replace inline `ingress` rules with standalone `aws_security_group_rule` (or
  `aws_vpc_security_group_ingress_rule`) resources that reference both groups.
- For an invisible dependency, state it explicitly:

  ```hcl
  depends_on = [aws_iam_role_policy.example]
  ```

**Prevention:** prefer referencing attributes over `depends_on`; the graph is then derived from real
data flow and stays correct as the code changes. Reserve `depends_on` for genuine hidden ordering,
such as IAM propagation, and comment why it is there.

### 8. Apply failed halfway and left partial infrastructure

**Symptom:** apply stops with a provider error after creating some resources. Re-running seems risky
because you do not know what exists.

**Evidence:**

```bash
terraform state list                # what got recorded before the failure
terraform plan                      # what Terraform now believes is missing
TF_LOG=DEBUG TF_LOG_PATH=./tf.log terraform apply   # the actual API error and request
```

**Cause:** apply is not atomic. Resources created before the failure exist and are in state. Typical
triggers are quota limits, permission gaps that only appear for one resource type, and eventual
consistency in the provider API.

**Fix:**

1. Read the provider error; it usually names the exact quota or permission.
2. Fix the underlying cause, then re-run `terraform apply`. Terraform creates only what is missing,
   which is why re-running is the normal recovery path rather than a risk.
3. If a resource was created but its provisioner failed, it is tainted and will be replaced on the
   next apply. Confirm that replacement is acceptable before approving.
4. If the provider created an object but failed before recording it, state and reality disagree:
   import the orphan rather than letting the next apply create a duplicate.

**Prevention:** keep blast radius small so a failed apply affects one stack. Use
`create_before_destroy` on anything serving traffic. In CI, save the plan with `-out=tfplan` and
apply that exact plan, so the applied change is the one that was reviewed.

### 9. Migrating count to for_each without destroying everything

**Symptom:** switching a resource from `count` to `for_each`, or removing one element from a
`count`-based list, plans to destroy and recreate resources that did not change.

**Evidence:**

```bash
terraform state list | grep 'aws_instance.web'
# aws_instance.web[0]
# aws_instance.web[1]
# aws_instance.web[2]
terraform plan     # shows -/+ for [1] and [2] after removing [0]
```

**Cause:** `count` addresses instances by position, so deleting or remapping an element shifts later
indexes. The addressing trade-off is in
[When should you use for_each instead of count?](#when-should-you-use-for_each-instead-of-count).

**Fix:** map the old addresses to the new ones with `moved` blocks, so the change is a state
rename rather than a replacement:

```hcl
moved {
  from = aws_instance.web[0]
  to   = aws_instance.web["app-1"]
}

moved {
  from = aws_instance.web[1]
  to   = aws_instance.web["app-2"]
}
```

Then confirm `terraform plan` reports no changes other than the moves. `terraform state mv` does the
same thing imperatively, but only on the machine that runs it, so `moved` blocks are the better
answer for team workflows.

**Prevention:** use `for_each` from the start whenever instances are distinguishable, and reserve
`count` for identical copies and `count = var.enabled ? 1 : 0` conditionals.

### 10. Deploying to multiple regions or accounts in one configuration

**Symptom:** resources intended for a second region are created in the default one, or an apply
fails with a credentials error for the secondary account.

**Evidence:**

```bash
terraform providers          # which provider configurations exist
terraform state show aws_vpc.west | grep -i arn
```

**Cause:** a resource did not select the aliased provider, so it inherited the default
configuration.

**Fix:** declare aliased provider configurations and select them explicitly:

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_vpc" "west" {
  provider   = aws.west
  cidr_block = "10.1.0.0/16"
}
```

Modules do not inherit aliases automatically; pass them in:

```hcl
module "west_network" {
  source    = "./modules/network"
  providers = {
    aws = aws.west
  }
}
```

**Prevention:** for cross-account work, prefer one configuration and state per account with an
assumed role, rather than one configuration spanning accounts. It keeps blast radius and
credentials aligned with the account boundary.
