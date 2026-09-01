# Terraform

Pointer-style interview guide: tables for the decisions, HCL only where the pattern itself is the answer,
and ten troubleshooting scenarios in symptom -> evidence -> fix -> prevent form. Multiple-choice practice
is in [terraform-certification-drills.md](terraform-certification-drills.md).

Terraform Cloud was renamed **HCP Terraform** in 2024; both names appear in older docs and in the exam.
What scores well: say what you would check *before* changing anything, and how you would make the fix
reviewable rather than applying it from your laptop.

## Contents

- [Safety rules](#safety-rules)
- [Fundamentals](#fundamentals)
- [Configuration language](#configuration-language)
- [Resources and meta-arguments](#resources-and-meta-arguments)
- [Providers and versions](#providers-and-versions)
- [Variables and outputs](#variables-and-outputs)
- [Sensitive, ephemeral and write-only data](#sensitive-ephemeral-and-write-only-data)
- [State and workspaces](#state-and-workspaces)
- [Modules](#modules)
- [Operations and tooling](#operations-and-tooling)
- [Troubleshooting scenarios](#troubleshooting-scenarios) — [triage](#first-response-triage) plus ten scenarios

## Safety rules

> **State is secret material.** It holds plaintext values, including everything marked `sensitive`. Treat
> every state file, saved plan and JSON dump as a credential store.

> **Collect evidence before you change state.** Before any `state rm`, `state mv`, `state push` or
> `force-unlock`: confirm the selected workspace and backend, stop concurrent runs, and take a restricted
> backup. Keep it only in an approved secure location and delete it when recovery is complete; it may
> contain plaintext secrets.

```bash
terraform workspace show                 # confirm the target before anything else
(umask 077; terraform state pull > state-backup-$(date +%s).json)
```

| Operation | What it actually does | Caveat you must state |
| :--- | :--- | :--- |
| `state rm` | Stops managing an object; does **not** destroy it | A later apply recreates a duplicate if the resource is still in configuration |
| `state mv` | Renames an address, on one machine only | Not reviewable; prefer a `moved` block |
| `state push` | Overwrites the remote state object | Disaster recovery only; prefer backend versioning, review the diff, never add `-force` casually |
| `force-unlock` | Deletes the backend lock | Breaking a live lock lets two writers interleave and corrupt state |
| `apply -refresh-only` | Records observed values into state | Does not change configuration; a later normal plan can still revert the drift |
| `taint` (deprecated 0.15.2) | Marks for replacement by editing state | Use `apply -replace=ADDR` so the replacement appears in a reviewable plan |
| `-lock=false` | Disables concurrency protection only | Never a fix for a lock error, and never how you adopt drift |
| `refresh` (deprecated) | Writes state with no reviewable apply | Use `plan -refresh-only` then `apply -refresh-only` |

Never commit state, saved plans, or `.tfvars` containing secrets. `show -json`, `state pull` and
`output -json` disclose sensitive values by design; keep them out of CI logs and shell history.

**Docs:** [Sensitive data in state](https://developer.hashicorp.com/terraform/language/state/sensitive-data) · [State CLI](https://developer.hashicorp.com/terraform/cli/commands/state)

## Fundamentals

Terraform is a declarative infrastructure-as-code tool. You describe the desired end state; Terraform reads prior
state, refreshes it against provider APIs, diffs it against the configuration, and produces a plan of creates,
updates, replacements and destroys. Applying it records the result in state, so applying twice is a no-op.

| Term | Meaning |
| :--- | :--- |
| Provider | Plugin implementing resource types for an API (AWS, Azure, Kubernetes, GitHub) |
| Resource | Block describing one infrastructure object Terraform manages |
| Data source | Read-only lookup of something Terraform does not manage |
| Module | A directory of `.tf` files used as a reusable unit; every configuration has a root module |
| State | Mapping from configuration addresses to real objects |
| Backend | Where state is stored and, for some backends, where runs execute |

| Why Terraform | The point that answers the question |
| :--- | :--- |
| Declarative, not procedural | You state "two servers"; Terraform decides create/update/destroy. Ansible needs convergence logic |
| Real plan step | The exact change set is reviewable before anything happens — the biggest operational advantage |
| Multi-provider, one language | CloudFormation is AWS-only; one config can span AWS, Cloudflare, Datadog and GitHub in one graph |
| Explicit graph and state | Terraform knows what it owns and in what order, making destroy, replacement and drift tractable |
| Honest counterpoints | State is an artefact you must secure, CloudFormation has deeper native AWS integration (service-side rollback, built-in drift detection), and Ansible fits in-guest configuration better |

| Real alternatives | Mislabelled as competitors |
| :--- | :--- |
| **OpenTofu** — open-source fork after the 2023 BSL change, largely config-compatible | **Packer** — builds machine images |
| **Pulumi** — same model in TypeScript, Python, Go, C# | **Ansible / Puppet / Chef** — configure software inside existing machines |
| **CloudFormation / AWS CDK** — AWS-native, single-cloud | **Kubernetes** — schedules workloads onto infrastructure something else provisioned |
| **ARM / Bicep**, **Google Cloud Infrastructure Manager** (Deployment Manager retired 31 Mar 2026) | All are used *alongside* Terraform, not instead of it |
| **Crossplane** — provisions via Kubernetes CRDs and a reconciliation loop | |

| Property | What to say |
| :--- | :--- |
| Immutable and declarative | Immutability belongs to the *provider and resource*, not to Terraform: many attributes update in place, and the plan says which (`~` versus `-/+`) |
| HCL | Expressions, functions, conditionals and loops, but deliberately no user-defined functions and no general-purpose control flow. JSON (`.tf.json`) is a valid alternative syntax |
| "A configuration" | The root module plus the child modules it calls — the unit evaluated in one run. Every `.tf` file in the directory loads into one namespace, so splitting into `versions.tf` / `variables.tf` / `main.tf` / `outputs.tf` is convention, not structure |
| Policy as code | Commercial: Sentinel and native OPA run between plan and apply in HCP Terraform (paid) and Enterprise. Open-source equivalent is `conftest`/`opa eval` against `terraform show -json tfplan`, plus `tfsec`/`checkov`, plus AWS SCPs or Azure Policy — but a CI check is bypassable unless cloud credentials exist only in the pipeline |
| On-premises | Any stable CRUD API can have a provider (vSphere, Nutanix, OpenStack, Proxmox, libvirt, F5, NetApp); write your own with the Plugin Framework |
| Structure | One state per environment and per blast radius, shared behaviour in versioned modules, environments differing only by `.tfvars` and backend key — not by copies of the resource code |

**Docs:** [What is Terraform](https://developer.hashicorp.com/terraform/intro) · [HCL syntax](https://developer.hashicorp.com/terraform/language/syntax/configuration) · [Policy enforcement](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement)

## Configuration language

| Construct | Use it for | Watch out for |
| :--- | :--- | :--- |
| Built-in functions | Numeric, string, collection, encoding, filesystem, date/time, hash/crypto, IP network, type conversion | No user-defined functions; experiment in `terraform console` |
| `locals` | Naming a derived expression reused in several places | A local **cannot** be overridden by the caller — that is what variables are for |
| Data source | Something Terraform does not own; `terraform_remote_state`; provider-validated documents such as `aws_iam_policy_document` | Read during **plan**, so a value that only exists after apply cannot be looked up in the same run |
| `dynamic` block | Genuinely variable-length nested blocks | Hides the shape of the config and makes plan output harder to read; not a line-saving device |
| `check` block (1.5+) | Post-apply assertions that warn rather than fail | Not a substitute for `validation` or `precondition` |

**Docs:** [Functions](https://developer.hashicorp.com/terraform/language/functions) · [Expressions](https://developer.hashicorp.com/terraform/language/expressions) · [Data sources](https://developer.hashicorp.com/terraform/language/data-sources)

## Resources and meta-arguments

In `resource "aws_instance" "web_server"`, `aws_instance` is the **type** (its prefix names the provider),
`web_server` the **local name**, `aws_instance.web_server` the **address**. **Arguments** are inputs you set,
**attributes** are provider-returned values (some known only after apply), and **meta-arguments** work everywhere.

| Meta-argument | Purpose | Interview point |
| :--- | :--- | :--- |
| `depends_on` | Force ordering the config does not reveal | Only for *hidden* dependencies such as IAM propagation; prefer attribute references so the graph follows real data flow |
| `count` | Fixed number of near-identical instances, indexed by `count.index` | Position-keyed, so addresses shift on removal |
| `for_each` | One instance per map/set element, keyed by `each.key` | Key-stable; the default choice |
| `provider` | Select a non-default (aliased) provider configuration | See [scenario 10](#10-deploying-to-multiple-regions-or-accounts-in-one-configuration) |
| `lifecycle` | Change how Terraform plans the change | See below |

| `lifecycle` argument | Effect |
| :--- | :--- |
| `create_before_destroy` | Build the replacement before removing the old object; zero-downtime replacement |
| `prevent_destroy` | Fail the plan if anything would delete the resource; use on databases |
| `ignore_changes` | Accept out-of-band changes to named attributes because another system owns them |
| `replace_triggered_by` | Force replacement when another resource or attribute changes |
| `precondition` / `postcondition` | Assert invariants a single-variable `validation` block cannot express |

### count versus for_each

Prefer `for_each` whenever instances are distinguishable. `count` keys by position, so removing the middle
element of a three-element list shifts every later index down one and Terraform plans to destroy and
recreate resources that did not change.

| | `count` | `for_each` |
| :--- | :--- | :--- |
| Input type | Number | Map or set of strings |
| Best for | Truly identical copies, or a 0/1 conditional | Distinct, named instances |
| Address | `aws_instance.web[0]` | `aws_instance.web["prod"]` |
| Stability | Index-based, shifts on removal | Key-based, stable |

`count` stays correct for conditional creation: `count = var.enabled ? 1 : 0`. Migrating between the two, or
renaming keys, is a **state operation**: use a `moved` block (1.1+) rather than `terraform state mv`, so the change
is reviewable in the plan and works for everyone. Example in [scenario 9](#9-migrating-count-to-for_each-without-destroying-everything).

### Replacement and side-effect containers

- **Tainted:** Terraform created the object but its provisioner failed, so it cannot know the object is usable and replaces it on the next apply.
- Force a replacement yourself with `terraform apply -replace="aws_instance.web"`, which appears in a reviewable plan.
- `null_resource` runs the resource lifecycle while creating nothing: a provisioner container, or an action fired by a changed `triggers` map.
- Since **1.4, `terraform_data` is the built-in equivalent** and needs no external provider.

| Provisioner | Runs where | Needs |
| :--- | :--- | :--- |
| `local-exec` | The machine executing Terraform, after create | Nothing extra; local side effects such as writing an inventory file |
| `remote-exec` | The remote resource over SSH/WinRM | A `connection` block, with credentials on the Terraform runner |
| `file` | Copies files to the remote resource | The same `connection` block |

Provisioners are a documented last resort: outside the declarative model (Terraform cannot plan, drift-detect or
undo them), a failed creation-time provisioner taints the resource, and they need connectivity plus credentials on
the runner. Prefer `user_data`/cloud-init, a Packer image, post-apply configuration management, or a real provider.

**Docs:** [Resource syntax](https://developer.hashicorp.com/terraform/language/resources/syntax) · [moved blocks](https://developer.hashicorp.com/terraform/language/moved) · [terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data) · [Provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax)

## Providers and versions

A provider is a plugin that teaches Terraform to talk to an API — a separate binary from a registry, not
part of the core binary. `terraform init` resolves versions against `required_providers`, downloads plugins
into `.terraform/providers`, and records exact versions and checksums in `.terraform.lock.hcl`.

> **Commit `.terraform.lock.hcl`.** It guarantees laptops and CI resolve identical provider versions, and
> its checksums detect a tampered plugin. Move versions deliberately with `terraform init -upgrade`, review
> the plan, and commit the updated lock as its own change.

| | `.terraform.lock.hcl` | State lock |
| :--- | :--- | :--- |
| Purpose | Pins provider versions and checksums | Prevents concurrent state writes |
| Created by | `terraform init` | Automatically per operation, by the backend |
| Lives in | Version control | The backend (S3 conditional write, DynamoDB, OS file lock) |
| Cleared by | `init -upgrade`, `providers lock` | `force-unlock`, only after confirming no run is active |

| Pinning | Syntax |
| :--- | :--- |
| Terraform core | `required_version = ">= 1.5.0, < 2.0.0"` |
| Provider | `version = "~> 5.31"` inside `required_providers` |
| Registry module | `version = "~> 5.1"` in the `module` block |
| Git module | No `version` argument; pin in the source URL with `?ref=v1.4.0` or a commit SHA |

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

`~> 5.1` allows 5.1 and later 5.x but not 6.0. Core and providers version independently, so their major
numbers need not match. Terraform can also install from a filesystem or network mirror, which is how
air-gapped environments work.

The **`random` provider** generates values that must be stable across runs but unpredictable (bucket-name
suffixes, initial passwords, `random_uuid`). The value is generated once and kept until `keepers` changes —
in **plaintext state**, so it still needs an encrypted backend.

**Docs:** [Provider requirements](https://developer.hashicorp.com/terraform/language/providers/requirements) · [Dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock) · [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)

## Variables and outputs

- **Contract:** variables are a module's parameters. `type`, `default` and `description` are all optional, but treat `type` as mandatory; no `default` means a required input.
- **Types:** `string`, `number`, `bool`; `list(TYPE)`, `set(TYPE)`, `map(TYPE)`; `object({ATTR = TYPE, ...})`, `tuple([TYPE, ...])`; `any` removes the constraint.
- **Assertions:** a `validation` condition must be an expression over the variable itself; use `precondition`/`postcondition` or a `check` block (1.5+) for cross-variable and post-plan invariants.

```hcl
variable "instance_count" {
  type = number
  validation {
    condition     = var.instance_count > 1
    error_message = "instance_count must be greater than 1."
  }
}
```

### Variable definition precedence

Values load in this order and **later sources override earlier ones**:

| Order | Source |
| :--- | :--- |
| 1 (lowest) | The variable's `default` argument |
| 2 | Environment variables (`TF_VAR_name`) |
| 3 | `terraform.tfvars` |
| 4 | `terraform.tfvars.json` |
| 5 | `*.auto.tfvars` and `*.auto.tfvars.json`, in lexical filename order |
| 6 (highest) | `-var` and `-var-file` on the command line, in the order given |

Only `terraform.tfvars` and `*.auto.tfvars` load automatically; a file passed with `-var-file` is not
otherwise loaded. Keep `.tfvars` files holding secrets out of Git.

- Outputs are a child module's return values (`module.vpc.vpc_id`), and a root module's publication to the CLI and to other configurations via `terraform_remote_state`.
- **Only root module outputs are printed** — surfacing a child value needs an output in the child *and* a re-export in the root.
- `terraform output` reads state without planning; `output -json` is the usual CI hand-off and can disclose sensitive values.

**Docs:** [Input variables](https://developer.hashicorp.com/terraform/language/values/variables) · [Definition precedence](https://developer.hashicorp.com/terraform/language/values/variables#variable-definition-precedence) · [Output values](https://developer.hashicorp.com/terraform/language/values/outputs)

## Sensitive, ephemeral and write-only data

> **`sensitive = true` is display redaction, not protection.** It hides the value in normal `plan` and
> `apply` output and propagates to derived expressions. It does **not** encrypt the value, omit it from plan
> or state files, prevent transmission to the provider, or make an unsafe storage location safe. The value
> is normally still present in Terraform artifacts.

| Control | Version | What it guarantees |
| :--- | :--- | :--- |
| `sensitive = true` | 0.14+ | Redacts normal CLI display and propagates to derived values. Nothing about persistence |
| `ephemeral = true` on variables, child-module outputs, `ephemeral` resources | 1.10+ | Available during the run, **omitted from saved plans and state** |
| Write-only arguments (`_wo` suffix) | 1.11+ | Accepted during an operation, always `null` in plan and state |
| Backend encryption plus least privilege | Always | The only thing that protects the artifact at rest |

Mark a secret **both** `sensitive` and `ephemeral`: one controls display, the other persistence.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
  ephemeral = true
}

resource "aws_db_instance" "app" {
  # Provider support and exact argument names vary by resource version.
  password_wo         = var.db_password
  password_wo_version = var.db_password_version
}
```

- Terraform cannot diff a value it never stores, so providers pair a write-only argument with a persisted **version** argument; increment it to signal rotation.
- Ephemeral values may only flow into ephemeral-compatible contexts: provider configuration, provisioners, ephemeral outputs and write-only arguments.
- Check the Registry schema before relying on a `_wo` argument. Incident response is [scenario 6](#6-secrets-found-in-plaintext-in-the-state-file).

**Docs:** [Manage sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data) · [Write-only arguments](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only)

## State and workspaces

- State maps configuration addresses to real objects: resource IDs, attribute values, module and provider metadata, outputs and dependencies.
- It exists because provider APIs cannot say which objects you manage and under what name; it also caches, so a plan diffs against state instead of enumerating the account.
- `terraform apply` writes it — by default `terraform.tfstate` locally, previous version kept as `terraform.tfstate.backup`. Add a `backend` block, then `terraform init` to migrate.

| Requirement | Why | How |
| :--- | :--- | :--- |
| Not in Git | Contains plaintext secrets | S3+KMS, Azure Blob, GCS, HCP Terraform |
| Encryption at rest | Same | Backend-native encryption, restricted key policy |
| Object versioning | Losing state means re-importing everything by hand | Bucket versioning, MFA delete, deny `DeleteObject` on the state prefix for CI roles |
| Locking | Concurrent writes corrupt state | Backend support; automatic, nothing to enable |
| One state per environment and blast radius | A dev plan must not be able to touch prod | Separate backend keys or workspaces |
| Never hand-edited | Serial and lineage integrity | `terraform state` subcommands, `moved` blocks, `import` |

- Remote state publishes outputs readable through `terraform_remote_state`; some backends (HCP Terraform, and `remote` generally) **run** the operations, so credentials stay off laptops.
- Terraform locks before any operation that could write state, so a second run fails fast with `Error acquiring the state lock` instead of racing.
- **S3 locks natively with conditional writes** (older setups use a DynamoDB table via `dynamodb_table`), the local backend uses OS file locking, and some backends do not lock at all.
- A killed process can leave a stale lock — see [scenario 1](#1-error-acquiring-the-state-lock).

### Workspace distinctions

The relationship is **configuration -> configured backend -> selected workspace -> one state snapshot**. A
root configuration declares at most one backend, but that does not mean one state file.

| Kind | What it is | Isolation |
| :--- | :--- | :--- |
| Local backend, `default` workspace | `terraform.tfstate` | — |
| Local backend, non-default workspace | A separate file under `terraform.tfstate.d/` | State only |
| Remote backend CLI workspace | Backend-specific key rules select a distinct remote object | State only; shares configuration, backend settings and usually credentials |
| HCP Terraform workspace | Its own state, variables, run settings, RBAC and history | Full; **not the same concept** as a CLI workspace despite the shared name |
| Directory per environment | Own backend key and `.tfvars`, shared modules | Strongest: environments may diverge in provider config, permissions and backend. Default for production |

- CLI workspaces mean less duplication but shared configuration and credentials, so they suit short-lived or low-risk environments rather than isolated production.
- Rename or move without destroying by using a `moved` block, which makes the change part of the reviewable plan.
- `terraform state mv` does the same imperatively on one machine only — one-off surgery, never a change the team must reproduce. Re-read the [safety rules](#safety-rules) first.

```hcl
moved {
  from = aws_instance.web
  to   = aws_instance.web_server
}
```

**Docs:** [State](https://developer.hashicorp.com/terraform/language/state) · [State locking](https://developer.hashicorp.com/terraform/language/state/locking) · [Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces) · [Backends](https://developer.hashicorp.com/terraform/language/backend)

## Modules

A module is any directory of `.tf` files. The directory Terraform runs in is the **root module**; anything
called with a `module` block is a **child module**. Scope stops at the boundary in **both** directions: a
child cannot see `var.x` from its parent, and a parent cannot see a child's resources.

| Direction | Mechanism |
| :--- | :--- |
| Down | Declare `variable` in the child, set it as an argument in the `module` block |
| Up | Declare `output` in the child, read it as `module.<NAME>.<OUTPUT>` |
| To the CLI | The root module must declare its own output re-exporting the child value |
| Across separate states | `terraform_remote_state`, or a shared store (SSM Parameter Store, Consul, a tag) read with a normal data source |

- `terraform_remote_state` couples the consumer to the producer's state file and needs read access to it, so publishing to a shared store is the looser alternative; Terragrunt makes the coupling explicit with `dependency` blocks.
- The public [Terraform Registry](https://registry.terraform.io) derives inputs, outputs and versions from the source repository — module versions come from **release tags**, not the module code.
- Anyone can publish: "Verified" and "Partner" mean HashiCorp partnership, **not** an audit. HCP Terraform adds a private registry with the same interface.

| Test layer | Tooling |
| :--- | :--- |
| 1 | `terraform fmt -check`, `terraform validate` — free, instant, no API calls |
| 2 | `tflint` for provider mistakes; `tfsec`/`checkov`/`trivy config` for security policy |
| 3 | `terraform test` with `.tftest.hcl` files (built in since 1.6): plan- or apply-based assertions |
| 4 | Terratest (Go) against a real account, then Sentinel or OPA in the pipeline for organisation-wide rules |

- The classic testing answer is Terratest; mentioning native `terraform test` shows current knowledge.
- **Terragrunt** keeps large multi-environment setups DRY: generated backend and provider configuration, inter-stack dependencies, `run-all` across modules, and repeated CLI flags.
- Native features absorbed much of that (partial backend config, `for_each` on modules, `moved` blocks, HCP stacks), so justify Terragrunt rather than defaulting to it.

**Docs:** [Modules](https://developer.hashicorp.com/terraform/language/modules) · [Module sources](https://developer.hashicorp.com/terraform/language/modules/sources) · [Tests](https://developer.hashicorp.com/terraform/language/tests)

## Operations and tooling

| Command | Does | Does not |
| :--- | :--- | :--- |
| `init` | Installs providers and modules, configures the backend, writes the lock file; safe to re-run, required after changing providers, modules or backend | Touch infrastructure |
| `validate` | Checks syntax and internal consistency — argument names, resolvable references, expression types; needs an initialised directory | Call APIs or read state, so it cannot tell you whether infrastructure matches |
| `plan` | Refreshes state, diffs against configuration, prints the change set; `-out=tfplan` saves it | Modify state or infrastructure |
| `apply` | Executes the plan and writes results to state; without a saved plan it computes a fresh one and prompts | Roll back automatically — it is not atomic |
| `console` | Evaluates expressions and functions against current state | Change anything; the best tool for expression questions |
| `output` | Reads outputs from state without planning | Redact under `-json` |

State format upgrades are **one-way**: once a newer Terraform writes state, older versions refuse to read it. Pin
`required_version` and install that version in CI with `tfenv` or `hashicorp/setup-terraform`, never "latest".

- `terraform import` brings an existing object into state but does **not** generate configuration.
- Workflow: identify the provider-specific ID, write matching configuration, import, then plan and expect an empty diff. A non-empty diff means fixing the configuration, not the infrastructure.
- Since 1.5 the `import` block makes this reviewable, and `terraform plan -generate-config-out=generated.tf` can scaffold the configuration.

```hcl
import {
  to = aws_instance.web
  id = "i-0123456789abcdef0"
}
```

Drift is any change made outside Terraform. A refresh-only plan reports what would be recorded without
proposing configuration-driven changes.

```bash
terraform plan -refresh-only
terraform apply -refresh-only     # review, approve, record observed values in state
terraform plan -detailed-exitcode # exit code 2 means changes exist; alert on it
```

- `apply -refresh-only` adopts observed values into state but does **not** change the configuration, so a later normal plan can still propose restoring the configured value.
- Never use `-lock=false` for drift adoption; decision table in [scenario 3](#3-someone-changed-infrastructure-in-the-console-drift).
- A failed apply is likewise partial, not atomic: completed operations remain and are normally recorded in state, so reverting code alone does not undo them — see [scenario 8](#8-apply-failed-halfway-and-left-partial-infrastructure) and [scenario 4](#4-state-file-lost-corrupted-or-partially-deleted).

- **HCP Terraform** over the CLI: remote state with locking and version history, plus remote runs on managed or self-hosted agents so credentials leave laptops.
- Also encrypted variable and variable-set storage, VCS integration (speculative plans on pull requests, applies on merge), RBAC and apply approvals, and a private module registry.
- Policy runs with Sentinel or OPA sit between plan and apply. Terraform Enterprise is the self-hosted distribution of the same product.

**Docs:** [CLI commands](https://developer.hashicorp.com/terraform/cli/commands) · [Import](https://developer.hashicorp.com/terraform/language/import) · [HCP Terraform](https://developer.hashicorp.com/terraform/cloud-docs)

## Troubleshooting scenarios

### First-response triage

```bash
terraform version                        # core and provider versions actually in use
terraform workspace show                 # which state am I about to touch?
terraform providers                      # requirements across root and all modules
terraform plan -refresh-only             # has anything changed outside Terraform?
terraform state list                     # what does Terraform think it owns?
terraform state show <ADDRESS>           # full attributes of one resource
```

> **Keep secrets out of triage output.** Do not put `show -json`, `state pull` or `output -json` in routine
> triage; they can disclose every sensitive value to shell history, CI logs or retained artifacts. Use
> targeted `state show` only in a restricted local session, and still assume it contains secrets.

| Symbol | Meaning |
| :--- | :--- |
| `+` | create |
| `-` | destroy |
| `~` | update in place; interruption depends on the resource and provider operation |
| `-/+` | destroy then create; the object is replaced and its ID changes |
| `+/-` | create then destroy, because `create_before_destroy` is set |
| `<=` | read a data source during apply |

A `-/+` on a stateful resource requires explicit review: find the `# forces replacement` annotation next to
the attribute that caused it, and verify backup and recovery requirements before approval.

### 1. Error acquiring the state lock

**Symptom:** every run fails immediately with `Error acquiring the state lock`, quoting a lock ID, operation,
who created it and when.

**Evidence:** the error carries ID, Operation, Who, Created and Path. Before assuming the lock is stale, look for a
running pipeline job on the same workspace and compare its age with `Created`. A stale lock means a previous run was
killed before releasing it (CI cancelled, runner evicted, laptop closed); otherwise two runs really are concurrent.

**Fix:** confirm no apply is in flight — breaking a live lock interleaves two writers and corrupts state. Then
`terraform force-unlock <LOCK_ID>` with the ID from the error, and confirm with `terraform plan` that state
still reflects reality before applying.

**Prevent:** serialise runs per state file with pipeline concurrency controls (`concurrency:` in GitHub
Actions, `resource_group:` in GitLab CI). Keep applies out of interactive shells so a closed laptop cannot
orphan a lock. Never use `-lock=false`.

### 2. Plan wants to destroy and recreate a production database

**Symptom:** a small configuration change produces `-/+ must be replaced` against an RDS instance, managed
disk or other stateful resource.

**Evidence:** the plan prints `# forces replacement`, and `replace_paths` in the JSON plan names the attribute.
Treat the JSON plan as sensitive. The cause is always an immutable attribute:

- Availability zone, subnet, engine version, or `name` where renaming is unsupported.
- A changed `for_each` key or `count` index, which changes the *address* rather than the resource.

```bash
terraform plan -out=tfplan
terraform show -json tfplan | jq '.resource_changes[] | select(.change.actions | index("delete")) | {address, replace: .change.replace_paths}'
```

**Fix:**

| Situation | Action |
| :--- | :--- |
| The change is not actually required | Revert that attribute and reach the goal another way |
| It is an address change (rename, move into a module, `count` to `for_each`) | Not a replacement — record it with a `moved` block so the plan shows a move |
| The resource genuinely must be replaced | Snapshot, provision the replacement alongside with `create_before_destroy`, cut over, then remove the old one |

**Prevent:** `lifecycle { prevent_destroy = true }` on resources whose loss is unrecoverable, plan output
required in the pull request, and CI that fails when a plan contains a delete against a protected address.

### 3. Someone changed infrastructure in the console (drift)

**Symptom:** a plan proposes changes nobody made in code, or an apply reverts a fix an engineer applied by
hand during an incident.

**Evidence:** `terraform plan -refresh-only` for what reality says versus state, then
`terraform state show <ADDRESS>` on the affected resource. The cause is an out-of-band change: Terraform
converges on the configuration, so the next apply undoes anything it owns that does not match.

**Fix:** decide who owns the attribute, then pick one row.

| Decision | Action |
| :--- | :--- |
| The manual change was wrong | `terraform apply` and let Terraform restore declared state |
| It was right and should become desired state | Codify it, then a normal plan and apply — the plan refreshes state |
| Accept only the observed values into state, changing nothing | Review and run `apply -refresh-only`; configuration is unchanged, so a later plan can still propose reversing it |
| Another system legitimately owns it (autoscaler, deployment tool) | `lifecycle { ignore_changes = [desired_count, task_definition] }` |
| Deleted outside Terraform and should stay deleted | Remove it from configuration, then `apply -refresh-only` to record the deletion |
| Deleted outside Terraform and should exist | Normal `terraform apply` to rebuild it |

Never add `-lock=false` to either workflow; it only disables concurrency protection and does not turn a
normal apply into drift adoption.

**Prevent:** remove or tightly restrict human write access to Terraform-managed environments, make
break-glass roles time-limited and audited, and run `terraform plan -detailed-exitcode` on a schedule
alerting on exit code 2.

### 4. State file lost, corrupted, or partially deleted

**Symptom:** `terraform plan` proposes creating everything from scratch, or fails with a JSON parse error,
and the resources plainly already exist.

**Evidence:** `terraform state list` returns empty or far fewer addresses than expected; list the backend's version
history (for S3, `aws s3api list-object-versions --bucket my-tf-state --prefix prod/terraform.tfstate`). Causes:

- The state object was deleted or overwritten, or an interrupted write truncated it.
- Someone ran in the wrong directory against an uninitialised backend.

**Fix:**

1. **Stop all pipelines targeting that state.** One apply against empty state duplicates the stack.
2. Confirm the active backend and workspace, record the current object version/ETag, and **preserve the
   current state object even if it looks corrupt**. Restore the previous version through the backend's native
   versioning where possible; that keeps the audit trail and does not bypass backend controls.
3. Only if native restoration is impossible and `state push` is required: download the candidate to a
   mode-0600 file, diff it against the current state, verify lineage and serial are appropriate, get peer
   approval, and push **without** `-force`. A lineage or serial rejection is a safety signal to investigate,
   not a reason to add `-force`.
4. If no backup exists, rebuild state by importing each resource; 1.5+ `import` blocks with
   `terraform plan -generate-config-out=generated.tf` make this tolerable.
5. Verify with `plan -refresh-only`, then a normal `plan`, before re-enabling applies. Securely remove any
   local state copies.

**Prevent:** object versioning and MFA delete on the state bucket, deny `s3:DeleteObject` on the state prefix
for CI roles, one distinct state snapshot per environment, and a tested restore path.

### 5. Provider version drift between laptop and CI

**Symptom:** the plan is clean locally but CI proposes unrelated changes, or an apply fails on an argument
that does not exist in the version CI resolved.

**Evidence:** `terraform version` and `terraform providers` in both places, then `git status .terraform.lock.hcl` —
is it committed, and does it match? Either the lock is uncommitted, or the constraint is loose (`>= 5.0`) and the
two environments resolved different versions; upgrades change defaults and add computed attributes as spurious diffs.

**Fix:**

- Commit the lock file and pin pessimistically: `version = "~> 5.31"`.
- Upgrade deliberately with `terraform init -upgrade`, review the plan, and commit the updated lock as its own change.
- If the lock covers one platform only, add the others: `terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`.

**Prevent:** pin `required_version` for core as well as providers, and install the pinned version in CI with
`tfenv` or `hashicorp/setup-terraform`.

### 6. Secrets found in plaintext in the state file

**Symptom:** a security scan reports database passwords or private keys inside `terraform.tfstate`, even
though the variables were marked `sensitive`.

**Evidence:** do **not** confirm the finding by dumping JSON state or piping it through `grep` — that creates
another plaintext copy and can place secrets in shell or CI logs.

- Start with the scanner's protected finding, provider schema docs, backend access logs and state version metadata.
- If direct verification is authorised, inspect only the named resource in a restricted local session, redirect to a mode-0600 file, never print the value, and securely remove it.
- This is by design: `sensitive = true` only redacts CLI output — see [Sensitive, ephemeral and write-only data](#sensitive-ephemeral-and-write-only-data).

**Fix:**

1. Treat the state file as a compromised secret store: **rotate every credential it contains.**
2. Move state to a backend with encryption at rest and least-privilege access (S3 with a KMS key and bucket
   policy, or HCP Terraform).
3. Preserve evidence per the incident process, then purge old unencrypted versions from the bucket's version
   history, coordinating with retention and legal requirements.
4. Stop putting the secret in Terraform where possible: have the target service generate it, or pass only a
   secret-manager ARN or path. With 1.10+ an `ephemeral` value avoids plan and state persistence; with 1.11+ a
   provider-supported write-only argument terminates the value at the API. Do not write a secret to an
   ordinary resource argument and assume the secret manager makes state safe.

**Prevent:** deny public access and enforce encryption on the state bucket, restrict who can read the state
prefix, and scan Terraform artifacts only with tools and storage approved for secrets.

### 7. Cycle error, or resources created in the wrong order

**Symptom:** `Error: Cycle: aws_security_group.a, aws_security_group.b`, or an apply fails because a
dependency was not ready even though it is in the configuration.

**Evidence:** `terraform graph | dot -Tsvg > graph.svg`, or `terraform graph -type=plan | grep -A5 'aws_security_group'`.

- A cycle means two resources reference each other's attributes, so neither can be created first.
- The "wrong order" variant is the opposite problem: a real dependency Terraform cannot see because nothing references it.

**Fix:**

- Break the cycle by extracting the mutual reference into a separate resource — for security groups, replace inline `ingress` rules with standalone `aws_security_group_rule` (or `aws_vpc_security_group_ingress_rule`) resources that reference both groups.
- For an invisible dependency, state it explicitly with `depends_on = [aws_iam_role_policy.example]`.

**Prevent:** prefer attribute references over `depends_on` so the graph derives from real data flow and stays
correct as code changes. Reserve `depends_on` for genuine hidden ordering such as IAM propagation, and
comment why it is there.

### 8. Apply failed halfway and left partial infrastructure

**Symptom:** apply stops with a provider error after creating some resources, and re-running feels risky
because you do not know what exists.

**Evidence:** `terraform state list` for what got recorded before the failure, `terraform plan` for what Terraform
now believes is missing, and `TF_LOG=DEBUG TF_LOG_PATH=./tf.log terraform apply` for the actual API error.

- Apply is not atomic, so resources created before the failure exist and are in state.
- Typical triggers: quota limits, permission gaps affecting one resource type, and eventual consistency in the provider API.

**Fix:**

- Read the provider error — it usually names the exact quota or permission — fix the underlying cause, then re-run `terraform apply`. Terraform creates only what is missing, which is why re-running is the normal recovery path rather than a risk.
- If a resource was created but its provisioner failed it is tainted and will be replaced next apply, so confirm that is acceptable.
- If the provider created an object but failed before recording it, state and reality disagree: **import the orphan** rather than letting the next apply duplicate it.

**Prevent:** keep blast radius small so a failed apply affects one stack, use `create_before_destroy` on
anything serving traffic, and in CI save the plan with `-out=tfplan` and apply that exact plan so the applied
change is the reviewed one.

### 9. Migrating count to for_each without destroying everything

**Symptom:** switching a resource from `count` to `for_each`, or removing one element from a `count`-based
list, plans to destroy and recreate resources that did not change.

**Evidence:** `terraform state list | grep 'aws_instance.web'` shows position-keyed addresses (`web[0]`, `web[1]`,
`web[2]`), and `terraform plan` shows `-/+` for `[1]` and `[2]` after `[0]` is removed, because `count` addresses by
position and any removal shifts later indexes. Trade-off in [count versus for_each](#count-versus-for_each).

**Fix:** map old addresses to new ones with `moved` blocks — one per instance — so the change is a state rename
rather than a replacement, then confirm `terraform plan` reports no changes other than the moves.
`terraform state mv` does the same imperatively, but only on the machine that runs it.

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

**Prevent:** use `for_each` from the start whenever instances are distinguishable, and reserve `count` for
identical copies and `count = var.enabled ? 1 : 0` conditionals.

### 10. Deploying to multiple regions or accounts in one configuration

**Symptom:** resources intended for a second region are created in the default one, or an apply fails with a
credentials error for the secondary account.

**Evidence:** `terraform providers` for which provider configurations exist, then
`terraform state show aws_vpc.west | grep -i arn` to see where the object actually landed. The resource did
not select the aliased provider, so it inherited the default configuration.

**Fix:** declare aliased provider configurations and select them explicitly. **Modules do not inherit
aliases** — pass them in with `providers`:

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

module "west_network" {
  source    = "./modules/network"
  providers = { aws = aws.west }
}
```

**Prevent:** for cross-account work, prefer one configuration and state per account with an assumed role
rather than one configuration spanning accounts; that keeps blast radius and credentials aligned with the
account boundary.

**Docs:** [Provider configuration and aliases](https://developer.hashicorp.com/terraform/language/providers/configuration) · [Debugging](https://developer.hashicorp.com/terraform/internals/debugging) · [Certification drills](terraform-certification-drills.md)
