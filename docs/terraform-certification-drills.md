# Terraform Certification Drills

Pointer guide for **HashiCorp Certified: Terraform Associate (004)**.

- Was a 271-question multiple-choice bank; now carries the *facts* those questions tested, revisable in one sitting.
- Covers the official domain map, a command matrix, the traps that decide borderline passes, and short self-check scenarios.
- Concepts, HCL patterns and production troubleshooting live in [terraform-interview-guide.md](terraform-interview-guide.md).
- Every documentation URL appears exactly once, in [official links](#official-links).

**Read the two labels literally.** They disagree more often than candidates expect.

| Label | Means |
| :--- | :--- |
| **Exam** | What the published objectives and official docs will score, even where real practice differs |
| **Prod** | What to do at work and say in interviews; not always what the exam wants to hear |

## Contents

- [Exam logistics and currency](#exam-logistics-and-currency)
- [Official exam domain map](#official-exam-domain-map)
- [Core workflow command matrix](#core-workflow-command-matrix)
- [High-yield flags](#high-yield-flags)
- [Deprecated on the exam versus current production](#deprecated-on-the-exam-versus-current-production)
- [Providers, versions and the lock file](#providers-versions-and-the-lock-file)
- [Configuration, variables and types](#configuration-variables-and-types)
- [Resources, data sources and dependencies](#resources-data-sources-and-dependencies)
- [Modules and the registry](#modules-and-the-registry)
- [State, backends and locking](#state-backends-and-locking)
- [Workspaces: CLI versus HCP Terraform](#workspaces-cli-versus-hcp-terraform)
- [Sensitive, ephemeral and write-only data](#sensitive-ephemeral-and-write-only-data)
- [HCP Terraform](#hcp-terraform)
- [True or false traps](#true-or-false-traps) — 22 statements
- [Choose-two traps](#choose-two-traps) — 16 questions
- [Self-check scenarios](#self-check-scenarios) — 13 scenarios
- [Official links](#official-links)

## Exam logistics and currency

| Detail | Value |
| :--- | :--- |
| Current version | Terraform Associate **004** |
| Product version tested | **Terraform 1.12** |
| Assessment type | Multiple choice, online proctored |
| Duration | 1 hour |
| Price | $70.50 USD plus local taxes; free retake not included |
| Credential expiration | 2 years |
| Objectives | 8 domains, 37 sub-objectives |

What changed from 003 to 004, per HashiCorp's own summary:

- Four new topics: **4f** `depends_on` and `create_before_destroy`, **4g** validating configuration with custom conditions, **4h** ephemeral values and write-only arguments, **8c** organising HCP Terraform workspaces and projects.
- A move to Terraform **1.12**, and more HCP Terraform content overall.

Three currency traps that cost marks:

- Third-party banks written for 002/003 over-test `terraform taint` and standalone `terraform refresh`.
  **Neither appears anywhere in the 004 objectives.**
- **Terraform Cloud was renamed HCP Terraform in 2024.** Both names appear in older material and in questions;
  they are the same product. Terraform Enterprise is the self-hosted distribution.
- The exam is pinned to 1.12 while the documentation tracks a newer release line (the current upgrade guide
  targets v1.16). Anything documented after 1.12 is **Prod** knowledge, not exam scope.

## Official exam domain map

The numbering is HashiCorp's. Use the right-hand column to revise a concept properly once a domain looks weak.

| # | Domain | Sub-objectives | Revise in |
| :--- | :--- | :--- | :--- |
| 1 | Infrastructure as Code with Terraform | 1a what IaC is · 1b advantages of IaC patterns · 1c multi-cloud, hybrid cloud and service-agnostic workflows | [Fundamentals](terraform-interview-guide.md#fundamentals) |
| 2 | Terraform fundamentals | 2a install and version providers · 2b how Terraform uses providers · 2c configuration with multiple providers · 2d how Terraform uses and manages state | [Providers](#providers-versions-and-the-lock-file) |
| 3 | Core Terraform workflow | 3a the workflow · 3b `init` · 3c `validate` · 3d `plan` · 3e `apply` · 3f `destroy` · 3g `fmt` | [Command matrix](#core-workflow-command-matrix) |
| 4 | Terraform configuration | 4a `resource` versus `data` · 4b attribute references · 4c variables and outputs · 4d complex types · 4e expressions and functions · 4f dependencies · 4g custom conditions · 4h sensitive data including Vault | [Configuration](#configuration-variables-and-types), [Resources](#resources-data-sources-and-dependencies) |
| 5 | Terraform modules | 5a how Terraform sources modules · 5b variable scope · 5c using modules · 5d module versions | [Modules](#modules-and-the-registry) |
| 6 | Terraform state management | 6a the local backend · 6b state locking · 6c remote state via the `backend` block · 6d drift and state management | [State](#state-backends-and-locking) |
| 7 | Maintain infrastructure | 7a import existing infrastructure · 7b inspect state with the CLI · 7c verbose logging | [Command matrix](#core-workflow-command-matrix) |
| 8 | HCP Terraform | 8a create infrastructure · 8b collaboration and governance · 8c workspaces and projects · 8d CLI integration | [HCP Terraform](#hcp-terraform) |

Two structural points worth internalising:

- **Domain 4 is the largest** at eight sub-objectives and gained the most new 004 material, so spend revision time there first.
- **CLI workspaces are not a named 004 objective** — the workspace content that *is* named is HCP Terraform workspaces and projects (8c), so a question saying "workspace" usually means the HCP object. Know both, because contrast questions are common.

## Core workflow command matrix

Write → plan → apply is domain 3; state inspection and import are domain 7.

| Command | Does | Does not — the trap |
| :--- | :--- | :--- |
| `init` | Installs providers and modules, configures the backend, writes `.terraform.lock.hcl`; safe to re-run | Touch infrastructure. Required after changing providers, modules or backend |
| `validate` | Checks syntax and internal consistency in an **initialised** directory | Call provider APIs or read state, so it cannot tell you whether reality matches |
| `fmt` | Rewrites files to canonical HCL style | Change meaning, or validate anything. `-check` reports without writing; `-recursive` descends |
| `plan` | Refreshes state in memory, diffs against configuration, prints the change set | Modify state or infrastructure. Without `-out` the plan you approve later is a *fresh* one |
| `apply` | Executes the plan and records results in state | Roll back on failure — apply is **not atomic**. Without a saved plan it re-plans and prompts |
| `destroy` | Plans and applies deletion of everything in state | Consult configuration for what to keep; it is `apply -destroy` underneath |
| `show` | Prints state, or a saved plan file, in human or `-json` form | Redact sensitive values under `-json` |
| `output` | Reads **root module** outputs from state without planning | Print child-module outputs, or redact under `-json` |
| `state list` | Lists managed resource addresses — the domain 7b answer | Show attributes; use `state show <ADDRESS>` |
| `import` | Binds an existing object to a configuration address in state | **Generate configuration.** You write matching HCL first |
| `console` | Evaluates expressions and functions against current state | Change anything; it is the right tool for function questions |
| `graph` | Emits the dependency graph in DOT format | Prove apply-time ordering on its own |
| `providers` | Lists provider requirements across the root and all child modules | Install anything; `providers lock` does the platform work |
| `login` | Obtains and stores an HCP Terraform API token — domain 8d | Configure the backend; that is `cloud` or `backend` plus `init` |
| `workspace` | `list`, `show`, `new`, `select`, `delete` for CLI workspaces | Isolate anything but state |
| `force-unlock` | Deletes the backend lock by ID | Fix a live run. Breaking an active lock lets two writers corrupt state |

**Exam** — the canonical phrasing is **write, plan, apply**; `init` is the prerequisite that makes a directory
usable and `validate` requires it. **Prod** — pin `required_version`, install that exact version in CI, and
gate merges on `fmt -check` and `validate`, which cost nothing and need no credentials.

```bash
terraform init -backend=false    # validate in CI with no backend credentials
terraform fmt -check -recursive && terraform validate
terraform plan -out=tfplan       # then apply the reviewed artefact, not a fresh plan
terraform apply tfplan
```

## High-yield flags

| Flag | On | Point that gets tested |
| :--- | :--- | :--- |
| `-out=FILE` | `plan` | Saves the plan so `apply FILE` executes exactly what was reviewed. The file may contain sensitive values |
| `-detailed-exitcode` | `plan` | Exit `0` no changes, `1` error, `2` changes present. The automation-friendly answer |
| `-refresh-only` | `plan`, `apply` | Reconciles state with reality **without** proposing configuration-driven changes |
| `-replace=ADDR` | `plan`, `apply` | The current, reviewable way to force replacement of one object |
| `-target=ADDR` | `plan`, `apply` | Narrows the operation. Documented as exceptional; it leaves state partially applied |
| `-var`, `-var-file` | `plan`, `apply` | Highest-precedence variable sources; a `-var-file` is not otherwise auto-loaded |
| `-auto-approve` | `apply`, `destroy` | Skips the prompt. Correct in CI after a reviewed plan, wrong from a laptop |
| `-upgrade` | `init` | Re-resolves versions within constraints and rewrites the lock file |
| `-migrate-state` | `init` | Moves existing state when the backend changes; `-reconfigure` discards the old backend instead |
| `-backend=false` | `init` | Initialises modules and providers with no backend, for validation-only CI jobs |
| `-generate-config-out=FILE` | `plan` | With `import` blocks, scaffolds HCL for objects you are adopting |
| `-lock=false` | most | Disables concurrency protection. Never the fix for a lock error |
| `TF_LOG`, `TF_LOG_PATH` | environment | Verbose logging — domain 7c. Levels `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`; logs can contain secrets |
| `TF_VAR_name` | environment | Sets a variable, above `default` but below every `.tfvars` file |

## Deprecated on the exam versus current production

Older banks drill commands 004 does not list. Learn the modern replacement, and recognise the legacy name so a
distractor cannot bait you.

| Legacy | Status | 004 treatment | Use instead |
| :--- | :--- | :--- | :--- |
| `terraform taint` / `untaint` | Deprecated since 0.15.2, still present in 1.x | **Not an objective** | `apply -replace=ADDR`, so replacement appears in a reviewable plan |
| `terraform refresh` | Deprecated since 0.15.4 | **Not an objective**; refresh-only *mode* is (6d) | `plan -refresh-only` then `apply -refresh-only` |
| `state mv` / `state rm` for refactors | Supported, unchanged | Only as CLI state inspection and surgery (7b) | `moved` and `removed` blocks, which are reviewable and reproducible |
| `dynamodb_table` on the S3 backend | Deprecated | Legacy locking questions may still name it | `use_lockfile = true` for native S3 locking |
| "Terraform Cloud" | Renamed 2024 | Appears as **HCP Terraform** | HCP Terraform, or Terraform Enterprise self-hosted |
| `null_resource` | Superseded in 1.4 | Provisioner-container questions may still use it | `terraform_data`, built in and needing no provider |

> **A tainted resource is still a valid exam concept.** It means an object Terraform created whose
> **provisioner failed**, so Terraform cannot know it is usable and replaces it on the next apply. That is the
> *state*, reached without running any command; `terraform taint` was merely the manual way to set it.

Every middle row here mutates state. Before running one for real, work through the [safety rules](terraform-interview-guide.md#safety-rules) and the matching playbook:

- [Database replacement](terraform-interview-guide.md#2-plan-wants-to-destroy-and-recreate-a-production-database)
- [Drift adoption](terraform-interview-guide.md#3-someone-changed-infrastructure-in-the-console-drift)
- [`count` to `for_each`](terraform-interview-guide.md#9-migrating-count-to-for_each-without-destroying-everything)

## Providers, versions and the lock file

Domain 2. A provider is a **separate plugin binary** fetched from a registry, not part of Terraform core.

| Fact | Detail |
| :--- | :--- |
| Where providers come from | `required_providers` gives `source` (`hashicorp/aws`) and `version`; `init` downloads into `.terraform/providers` |
| Default namespace | A bare name resolves to the public registry under `hashicorp/`; anything else needs an explicit `source` |
| Independent versioning | Core and providers version separately, so their major numbers need not match |
| `.terraform.lock.hcl` | Written by `init`, records exact versions and checksums, **belongs in version control** |
| Changing versions | `init -upgrade` re-resolves within constraints and rewrites the lock; commit it as its own change |
| Multiple providers (2c) | Extra `provider` blocks with `alias`, selected per resource with the `provider` meta-argument |
| Air-gapped installs | Filesystem or network mirrors, plus `providers lock` for multi-platform checksums |
| `~> 5.1` | Allows 5.1 and later 5.x, **not** 6.0. `~> 5` would allow any 5.x |

```hcl
terraform {
  required_version = ">= 1.12.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

**Exam** — know that the lock file pins providers and that `init` creates it. **Prod** — provider drift between
a laptop and CI is a real outage class; see
[scenario 5](terraform-interview-guide.md#5-provider-version-drift-between-laptop-and-ci).

## Configuration, variables and types

Domain 4. Precedence is the single most reliably examined table in the objective set: **later sources override
earlier ones.**

| Order | Source |
| :--- | :--- |
| 1 lowest | The variable's `default` |
| 2 | Environment variable `TF_VAR_name` |
| 3 | `terraform.tfvars` |
| 4 | `terraform.tfvars.json` |
| 5 | `*.auto.tfvars` and `*.auto.tfvars.json`, in lexical filename order |
| 6 highest | `-var` and `-var-file` on the command line, in the order given |

Only `terraform.tfvars` and `*.auto.tfvars` load automatically. A missing required variable prompts
interactively and fails outright in a non-interactive run. Full detail:
[variable definition precedence](terraform-interview-guide.md#variable-definition-precedence).

| Type family | Members | Exam point |
| :--- | :--- | :--- |
| Primitive | `string`, `number`, `bool` | Terraform converts between these where unambiguous |
| Collection | `list(TYPE)`, `set(TYPE)`, `map(TYPE)` | One element type. A `set` is unordered and de-duplicated |
| Structural | `object({...})`, `tuple([...])` | Per-attribute or per-position types — the answer to "mixed types in one value" |
| Escape hatch | `any` | Removes the constraint; still a declared type |

| Construct | Use for | Watch out |
| :--- | :--- | :--- |
| `locals` | Naming a derived expression reused in several places | A caller **cannot** override a local; that is what variables are for |
| `output` | Publishing a value up one level | Only **root** outputs print; surfacing a child value needs an output in both |
| `data` | Reading something Terraform does not manage | Normally read during **plan**. If its own arguments depend on values unknown until apply, Terraform **defers the read to apply** — shown as `<=` — and it can then see apply-time attributes |
| `validation` | Asserting on the variable itself (4g) | Cannot reference another variable |
| `precondition` / `postcondition` | Cross-value and post-apply invariants (4g) | Live in a `lifecycle` block on the resource |
| `check` | Post-apply assertions (4g) | Warns rather than fails; not a substitute for `validation` |
| `dynamic` block | Genuinely variable-length nested blocks | Obscures plan output; not a line-saving device |

Functions are **built in only** — HCL has no user-defined functions. Categories: numeric, string, collection,
encoding, filesystem, date and time, hash and crypto, IP network, and type conversion. Test them in
`terraform console` rather than memorising signatures.

## Resources, data sources and dependencies

In `resource "aws_instance" "web"`, `aws_instance` is the **type** whose prefix names the provider, `web` is the
**local name**, and `aws_instance.web` is the **address**. Data sources are addressed `data.TYPE.NAME`.

| Meta-argument | Purpose | Exam point |
| :--- | :--- | :--- |
| `count` | A fixed number of near-identical instances | Position-keyed: `aws_instance.web[0]`. Removing a middle element shifts later indices and forces recreation |
| `for_each` | One instance per element | Key-stable: `aws_instance.web["prod"]`. Accepts a map or a **set of strings** only |
| `depends_on` | Ordering the configuration does not reveal (4f) | For *hidden* dependencies only; prefer attribute references |
| `provider` | Selects an aliased provider configuration | The multi-region and multi-account mechanism |
| `lifecycle` | Changes how the change is planned | `create_before_destroy` builds the replacement first (4f) · `prevent_destroy` fails the plan on deletion · `ignore_changes` tolerates out-of-band edits · `replace_triggered_by` forces replacement |

- **Dependencies are implicit by default (4f):** referencing `aws_vpc.main.id` from a subnet creates the edge, Terraform builds a graph from those references, and independent branches run in parallel.
- `depends_on` is the explicit fallback for edges references do not express, such as IAM propagation.
- Choosing between the loop meta-arguments: [count versus for_each](terraform-interview-guide.md#count-versus-for_each).

| Plan symbol | Meaning |
| :--- | :--- |
| `+` create · `-` destroy · `~` update in place | The three ordinary outcomes |
| `-/+` | Destroy then create; the object is **replaced** and its ID changes |
| `+/-` | Create then destroy, because `create_before_destroy` is set |
| `<=` | A **deferred data-source read**: its arguments were unknown at plan time, so Terraform reads it during apply |

**Prod** — provisioners (`local-exec`, `remote-exec`, `file`) are a documented last resort: Terraform cannot
plan, drift-detect or undo them, and a failed creation-time provisioner taints the resource. Prefer
`user_data`, a prebuilt image, or a real provider.

## Modules and the registry

Domain 5. A module is **any directory of `.tf` files**. The directory Terraform runs in is the **root module**;
anything invoked with a `module` block is a **child module**.

| Source type | `source` value | Versioning |
| :--- | :--- | :--- |
| Local path | `./modules/vpc` | None; must start with `./` or `../` |
| Registry | `terraform-aws-modules/vpc/aws` | The `version` argument, resolved from release tags |
| Git or GitHub | `git::https://...` or `github.com/org/repo` | No `version` argument — pin with `?ref=v1.4.0` or a commit SHA |
| HTTP archive, S3, GCS | A URL to an archive or bucket object | By object path or key |
| Private registry | The same three-part form, HCP Terraform hosted | The `version` argument |

**Variable scope stops at the boundary in both directions (5b).** A child cannot read `var.x` from its parent,
and a parent cannot reach into a child's resources.

| Direction | Mechanism |
| :--- | :--- |
| Parent to child | Declare `variable` in the child, pass it as an argument in the `module` block |
| Child to parent | Declare `output` in the child, read it as `module.NAME.OUTPUT` |
| Child to the CLI | The root module must re-export it as its own output |
| Across separate states | `terraform_remote_state`, or a shared store read with a normal data source |

- Registry facts that get tested: module names follow `NAMESPACE/NAME/PROVIDER`, and versions come from the source repository's **release tags** rather than the module code.
- **"Verified" and "Partner" mean a HashiCorp partnership, not a security audit.** Anyone can publish.
- Registry modules honour constraints such as `~> 5.1`. **Prod** — pin exactly in production and upgrade deliberately.

## State, backends and locking

Domain 6. State maps configuration addresses to real objects, holds attribute values, dependencies and
outputs, and doubles as a cache so a plan diffs against state instead of enumerating the account.

| Fact | Detail |
| :--- | :--- |
| Default backend | **`local`** (6a): `terraform.tfstate` in the working directory, previous version in `terraform.tfstate.backup` |
| Enabling a remote backend | Add a `backend` block, then run `init`; Terraform offers to migrate existing state |
| Backend block limits | One per root module, and it **cannot use variables, locals or data sources** — hence partial configuration with `init -backend-config` |
| Locking (6b) | Automatic before any state-writing operation; nothing to enable in Terraform itself. Support is per backend |
| S3 locking | `use_lockfile = true` for native locking; the `dynamodb_table` argument is deprecated |
| Local backend locking | OS-level file locking. Some backends do not lock at all |
| Format upgrades | **One-way.** Once a newer Terraform writes state, older versions refuse to read it |
| Never hand-edit | Serial and lineage integrity; use `state` subcommands, `moved` and `removed` blocks, or `import` |

Drift management (6d) is the part candidates most often get half-right:

| Operation | Effect |
| :--- | :--- |
| `plan -refresh-only` | Reports what *would* be recorded; changes nothing |
| `apply -refresh-only` | Records observed values into state. Does **not** change configuration, so a later normal plan can still propose reverting the drift |
| `moved` block | Changes a resource's address in state as part of a reviewable plan; no destroy or create |
| `removed` block | Stops managing an object without destroying it, reviewably |
| `import` block | Binds an existing object to an address. Configuration must already match, or the plan is non-empty |

> **State is credential material.** It stores values in plaintext, including everything marked `sensitive`.
> Never commit it. Encrypt at rest, enable object versioning, and restrict who can read the state prefix.
> Playbooks: [lock errors](terraform-interview-guide.md#1-error-acquiring-the-state-lock),
> [lost or corrupted state](terraform-interview-guide.md#4-state-file-lost-corrupted-or-partially-deleted),
> [secrets in state](terraform-interview-guide.md#6-secrets-found-in-plaintext-in-the-state-file),
> [a partial apply](terraform-interview-guide.md#8-apply-failed-halfway-and-left-partial-infrastructure).

## Workspaces: CLI versus HCP Terraform

The chain is **configuration → configured backend → selected workspace → one state snapshot**. One root
module declares at most one backend, which does not mean one state file.

| Kind | What it is | Isolates |
| :--- | :--- | :--- |
| CLI workspace, `default` | `terraform.tfstate` under the local backend | Nothing; it is the implicit starting workspace |
| CLI workspace, non-default, local backend | A separate file under `terraform.tfstate.d/NAME/` | State only |
| CLI workspace, remote backend | A distinct remote object by backend-specific key rules | State only; shares configuration, backend settings and usually credentials |
| **HCP Terraform workspace** | Its own state, variables, run settings, RBAC and run history | Everything — **a different concept despite the shared name** |
| Directory per environment | Own backend key and `.tfvars`, shared versioned modules | Strongest; environments may differ in provider config and permissions |

- `terraform.workspace` returns the selected CLI workspace name, which is how conditional sizing by environment is usually written.
- **Exam** — CLI workspaces let one configuration manage multiple state snapshots.
- **Prod** — they share credentials and code, so they suit short-lived or low-risk environments; production isolation is a directory and backend key per environment.
- Detail: [workspace distinctions](terraform-interview-guide.md#workspace-distinctions).

## Sensitive, ephemeral and write-only data

Objective 4h, and the topic 004 expanded most.

| Control | Since | Guarantees |
| :--- | :--- | :--- |
| `sensitive = true` | 0.14 | **Display redaction only.** Hides the value in normal plan and apply output and propagates to derived values. Nothing about persistence |
| `ephemeral = true` | 1.10 | Available during the run, **omitted from saved plans and state** |
| Write-only arguments (`_wo`) | 1.11 | Accepted during an operation, always `null` in plan and state |
| Backend encryption and least privilege | Always | The only thing protecting the artefact at rest |

Mark a secret **both** `sensitive` and `ephemeral`: one controls display, the other persistence. Because
Terraform cannot diff a value it never stores, providers pair a write-only argument with a persisted
**version** argument that you increment to signal rotation.

**Secure secret injection, in the order the docs prefer it:**

1. A provider that fetches the secret at run time — the **Vault provider** is the example named in 4h.
2. Environment variables or a CI secret store supplying `TF_VAR_*`.
3. An encrypted `.tfvars` kept out of Git. Never a literal in `.tf`, and never a plaintext `.tfvars` in version control.

`show -json`, `output -json`, `state pull` and `TF_LOG` output all disclose sensitive values by design, so keep them
out of CI logs and shell history. Controls and incident response:
[sensitive, ephemeral and write-only data](terraform-interview-guide.md#sensitive-ephemeral-and-write-only-data).

## HCP Terraform

Domain 8 — one of the eight domains, and the part self-taught candidates most often skip.

| Capability | What it gives you |
| :--- | :--- |
| Remote state | Storage with locking, version history and access controls, with no bucket to build |
| Remote runs | Plans and applies execute on managed or self-hosted agents, so **credentials leave laptops** |
| Variables and variable sets | Encrypted storage, marked sensitive, reused across many workspaces (8b) |
| VCS-driven workflow | Speculative plans on pull requests, applies on merge |
| CLI-driven workflow | The `cloud` block plus `terraform login`, keeping local commands with remote execution (8d) |
| Projects (8c) | Group workspaces for organisation and permissions |
| Run triggers (8c) | One workspace's successful apply queues a run in another |
| Private registry | Internal modules and providers behind the same interface |
| Policy enforcement | Sentinel and OPA between plan and apply; paid tiers |
| Health assessments | Scheduled drift detection and continuous validation |
| Teams and permissions | RBAC and apply approvals |

```hcl
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      name = "prod-network"
    }
  }
}
```

**Exam** — the `cloud` block plus `terraform login` is the CLI integration, and Terraform Enterprise is the
self-hosted distribution of the same product. **Prod** — the durable argument for it is that credentials and
state stop living on laptops and every change arrives through a reviewed run.

## True or false traps

Cover the verdict column and work down. Each statement is one that question banks get wrong or bait you with.

| # | Statement | Verdict | Why |
| :--- | :--- | :--- | :--- |
| 1 | `terraform validate` confirms your configuration matches deployed infrastructure | **False** | It never calls an API or reads state; only `plan` compares against reality |
| 2 | `terraform init` is safe to re-run and changes no infrastructure | **True** | It installs plugins and modules and configures the backend only |
| 3 | `sensitive = true` keeps the value out of the state file | **False** | Display redaction only; the value is stored in plaintext |
| 4 | `terraform destroy` is equivalent to `terraform apply -destroy` | **True** | The same operation with a dedicated command name |
| 5 | `terraform import` writes the matching resource configuration for you | **False** | It only updates state; `plan -generate-config-out` scaffolds HCL separately |
| 6 | A failed `terraform apply` rolls back completed changes | **False** | Apply is not atomic; completed operations remain and are recorded in state |
| 7 | `terraform fmt` can change what your configuration means | **False** | It only adjusts whitespace and canonical style |
| 8 | Every CLI workspace of one configuration shares one state file | **False** | Each has its own state snapshot; they share configuration and backend |
| 9 | The `backend` block can take its values from input variables | **False** | Backends resolve before evaluation; use partial config and `-backend-config` |
| 10 | `.terraform.lock.hcl` should be committed to version control | **True** | It makes laptops and CI resolve identical provider versions |
| 11 | State locking must be enabled with a CLI flag | **False** | Automatic where the backend supports it; `-lock=false` only disables it |
| 12 | `~> 5.1` permits version 6.0 | **False** | It permits 5.1 and later 5.x releases only |
| 13 | A child module can read `var.region` declared in its parent | **False** | Scope stops at the boundary; the parent must pass it as an argument |
| 14 | `terraform output` prints outputs declared in child modules | **False** | Only root outputs print; the root must re-export them |
| 15 | "Verified" in the public registry means HashiCorp audited the module's security | **False** | It indicates a partnership, not an audit |
| 16 | `apply -refresh-only` changes your configuration to match reality | **False** | It records observed values in state only; a later plan can still revert the drift |
| 17 | `for_each` accepts a list of strings | **False** | A map or a set of strings; convert a list with `toset()` |
| 18 | Removing the middle element of a `count` list can force unrelated resources to be recreated | **True** | `count` keys by position, so later indices shift |
| 19 | A tainted resource is one you marked with `terraform taint` | **False** | It is any resource whose provisioner failed; the command was only the manual route |
| 20 | Terraform parallelises resource creation where the graph allows it | **True** | Independent graph branches run concurrently, default parallelism 10 |
| 21 | Data sources are always read during the plan phase | **False** | Usually they are, but when their arguments depend on values unknown until apply Terraform defers the read to apply, shown as `<=`. Exam wording normally assumes the plan-time case, so read the question for a same-apply dependency |
| 22 | Once a newer Terraform version writes your state, older versions can still read it | **False** | State format upgrades are one-way |

## Choose-two traps

| # | Question | Correct pair | Reject |
| :--- | :--- | :--- | :--- |
| 1 | Which two commands never modify infrastructure? | `validate`, `plan` | `apply -auto-approve`; `destroy` |
| 2 | Which two files load automatically for variables? | `terraform.tfvars`, `*.auto.tfvars` | A file named by `-var-file` is not otherwise auto-loaded |
| 3 | Which two sources beat `terraform.tfvars` in precedence? | `-var` on the CLI, `*.auto.tfvars` | `TF_VAR_name`, which ranks below it |
| 4 | Which two are valid `for_each` inputs? | A map, a set of strings | A list; a number |
| 5 | Which two `lifecycle` arguments concern replacement and deletion? | `create_before_destroy`, `prevent_destroy` | `ignore_changes`, which merely tolerates drift |
| 6 | Which two events require re-running `terraform init`? | Adding a provider, changing the backend | Editing a resource argument; adding an output |
| 7 | Which two things does `.terraform.lock.hcl` record? | Exact provider versions, provider checksums | The Terraform core version; module versions |
| 8 | Which two module sources cannot use the `version` argument? | Local paths, Git URLs | Public and private registry modules both can |
| 9 | Which two mechanisms change what state manages, reviewably? | A `moved` block, a `removed` block | `terraform state mv`, which is imperative and local |
| 10 | Which two guarantee a value stays out of state? | `ephemeral = true`, a write-only `_wo` argument | `sensitive = true`, which only redacts display |
| 11 | Which two are HCP Terraform-only features? | Sentinel and OPA policy enforcement, variable sets | CLI workspaces and the `backend` block are Community Edition |
| 12 | Which two commands inspect state without changing it? | `state list`, `state show` | `state rm`, `state push`, both of which mutate |
| 13 | Which two are true of the local backend? | It is the default, it keeps a `.backup` of the previous state | That it supports team locking across machines |
| 14 | Which two make an S3 backend safe for a team? | `use_lockfile = true`, bucket versioning with encryption | A `dynamodb_table` argument, now deprecated |
| 15 | Which two describe implicit dependencies? | Built from attribute references, used to order the graph | Declared with `depends_on`, which is the explicit form |
| 16 | Which two plan symbols mean the object is replaced? | `-/+`, `+/-` | `~` updates in place; `<=` is a deferred data-source read |

## Self-check scenarios

Read the scenario, answer aloud, then uncover the last column. Anything touching state links to a full playbook.

| # | Scenario | Answer |
| :--- | :--- | :--- |
| 1 | An apply failed halfway. Reverting the commit does not remove the resources that were created. Why? | Apply is not atomic: completed operations exist and are recorded in state, so reverting code only changes the desired end state. Plan against the reverted code and apply the deletions deliberately. [Playbook](terraform-interview-guide.md#8-apply-failed-halfway-and-left-partial-infrastructure) |
| 2 | Every run fails with `Error acquiring the state lock` and a colleague suggests `-lock=false`. | Refuse. Confirm no run is genuinely active, then `force-unlock` the quoted lock ID. `-lock=false` removes protection and invites two writers to corrupt state. [Playbook](terraform-interview-guide.md#1-error-acquiring-the-state-lock) |
| 3 | The plan shows `-/+` on a production database with `# forces replacement` beside one attribute. | Stop. Identify the forcing attribute, check whether it can change in place, verify backups, and add `prevent_destroy` against a repeat. Approving destroys the object and its ID. [Playbook](terraform-interview-guide.md#2-plan-wants-to-destroy-and-recreate-a-production-database) |
| 4 | Someone resized an instance in the console. You want state to match reality without reverting the instance. | `plan -refresh-only`, review, then `apply -refresh-only`. Configuration still holds the old size, so a later normal plan can propose reverting it. [Playbook](terraform-interview-guide.md#3-someone-changed-infrastructure-in-the-console-drift) |
| 5 | You are adopting 30 existing S3 buckets into Terraform. | Write configuration first, then use `import` blocks so adoption is reviewable, with `plan -generate-config-out` to scaffold. Expect an empty diff; a non-empty diff means fix the configuration, not the bucket |
| 6 | CI applies cleanly but a developer's laptop plans a large diff on the same commit. | Provider or core version drift. Compare `terraform version` and `terraform providers`, confirm the lock file is committed and honoured, and pin the CI version instead of "latest". [Playbook](terraform-interview-guide.md#5-provider-version-drift-between-laptop-and-ci) |
| 7 | A `.tfvars` file containing a database password was committed and applied months ago. | Treat the credential as compromised and rotate it; the value is also in plaintext state and any retained plans. Then move to `ephemeral` plus a write-only argument or a Vault lookup. [Playbook](terraform-interview-guide.md#6-secrets-found-in-plaintext-in-the-state-file) |
| 8 | Rename `aws_instance.web` to `aws_instance.web_server` with no downtime. | A `moved` block, so the address change appears in the reviewable plan as a state move. `terraform state mv` does it on one machine and nobody reproduces it |
| 9 | Deploy the same module to `eu-west-1` and `us-east-1` from one configuration. | Two `provider "aws"` blocks, the second with `alias`, selected per module or resource with the `provider` meta-argument. [Playbook](terraform-interview-guide.md#10-deploying-to-multiple-regions-or-accounts-in-one-configuration) |
| 10 | A three-element `count` list loses its middle entry and the plan wants to recreate two healthy servers. | `count` is position-keyed, so indices shifted. Migrate to `for_each` over a map using `moved` blocks so objects are re-addressed rather than destroyed. [Playbook](terraform-interview-guide.md#9-migrating-count-to-for_each-without-destroying-everything) |
| 11 | A pipeline should fail only when changes are pending, without applying anything. | `plan -detailed-exitcode`, treating exit `2` as changes pending, `0` as none and `1` as an error |
| 12 | Reject a variable outside three allowed instance types, and separately check an endpoint responds after apply. | A `validation` block on the variable, which may only reference that variable, and a `check` block for the post-apply assertion, remembering `check` warns rather than fails |
| 13 | A cycle error appears after you add `depends_on` to resolve an ordering problem. | Remove the manual edge and let attribute references express the real data flow; `depends_on` between two resources that already reference each other creates the cycle. [Playbook](terraform-interview-guide.md#7-cycle-error-or-resources-created-in-the-wrong-order) |

## Official links

Only `developer.hashicorp.com` and `registry.terraform.io`, each URL once.

**Certification** — [overview and exam details](https://developer.hashicorp.com/certifications/infrastructure-automation) · [Associate 004 collection](https://developer.hashicorp.com/terraform/tutorials/certification-004) · [learning path](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-study-004) · [exam content list](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004) · [sample questions](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-questions-004)

**Concepts** — [what is Terraform](https://developer.hashicorp.com/terraform/intro) · [use cases](https://developer.hashicorp.com/terraform/intro/use-cases) · [core workflow](https://developer.hashicorp.com/terraform/intro/core-workflow) · [language overview](https://developer.hashicorp.com/terraform/language) · [configuration syntax](https://developer.hashicorp.com/terraform/language/syntax/configuration) · [terraform block](https://developer.hashicorp.com/terraform/language/block/terraform) · [upgrade guides](https://developer.hashicorp.com/terraform/language/upgrade-guides)

**Expressions and values** — [expressions](https://developer.hashicorp.com/terraform/language/expressions) · [references to values](https://developer.hashicorp.com/terraform/language/expressions/references) · [type constraints](https://developer.hashicorp.com/terraform/language/expressions/types) · [dynamic blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks) · [version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints) · [functions](https://developer.hashicorp.com/terraform/language/functions) · [templatefile](https://developer.hashicorp.com/terraform/language/functions/templatefile)

**Variables, outputs and conditions** — [input variables](https://developer.hashicorp.com/terraform/language/values/variables) · [definition precedence](https://developer.hashicorp.com/terraform/language/values/variables#variable-definition-precedence) · [output values](https://developer.hashicorp.com/terraform/language/values/outputs) · [local values](https://developer.hashicorp.com/terraform/language/values/locals) · [values in modules](https://developer.hashicorp.com/terraform/language/values) · [variable block](https://developer.hashicorp.com/terraform/language/block/variable) · [output block](https://developer.hashicorp.com/terraform/language/block/output) · [locals block](https://developer.hashicorp.com/terraform/language/block/locals) · [check block](https://developer.hashicorp.com/terraform/language/block/check)

**Resources and dependencies** — [resource block](https://developer.hashicorp.com/terraform/language/block/resource) · [data block](https://developer.hashicorp.com/terraform/language/block/data) · [resource behavior](https://developer.hashicorp.com/terraform/language/resources/behavior) · [data sources](https://developer.hashicorp.com/terraform/language/data-sources) · [count](https://developer.hashicorp.com/terraform/language/meta-arguments/count) · [for_each](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each) · [depends_on](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on) · [lifecycle](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle) · [resource graph](https://developer.hashicorp.com/terraform/internals/graph) · [provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax) · [connection block](https://developer.hashicorp.com/terraform/language/resources/provisioners/connection) · [terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data) · [tests](https://developer.hashicorp.com/terraform/language/tests)

**Providers and modules** — [providers](https://developer.hashicorp.com/terraform/language/providers) · [provider requirements](https://developer.hashicorp.com/terraform/language/providers/requirements) · [provider configuration](https://developer.hashicorp.com/terraform/language/providers/configuration) · [provider block](https://developer.hashicorp.com/terraform/language/block/provider) · [plugin architecture](https://developer.hashicorp.com/terraform/plugin) · [dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock) · [modules](https://developer.hashicorp.com/terraform/language/modules) · [module sources](https://developer.hashicorp.com/terraform/language/modules/sources) · [module block](https://developer.hashicorp.com/terraform/language/block/module) · [module composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition) · [standard structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure) · [refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring) · [public registry](https://registry.terraform.io) · [browse modules](https://registry.terraform.io/browse/modules) · [Vault provider](https://registry.terraform.io/providers/hashicorp/vault/latest/docs)

**State, backends and sensitive data** — [state](https://developer.hashicorp.com/terraform/language/state) · [purpose of state](https://developer.hashicorp.com/terraform/language/state/purpose) · [storage and locking](https://developer.hashicorp.com/terraform/language/state/remote) · [state locking](https://developer.hashicorp.com/terraform/language/state/locking) · [sensitive data in state](https://developer.hashicorp.com/terraform/language/state/sensitive-data) · [backends](https://developer.hashicorp.com/terraform/language/backend) · [local backend](https://developer.hashicorp.com/terraform/language/backend/local) · [S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3) · [Kubernetes backend](https://developer.hashicorp.com/terraform/language/backend/kubernetes) · [CLI workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces) · [import](https://developer.hashicorp.com/terraform/language/import) · [state import concepts](https://developer.hashicorp.com/terraform/language/state/import) · [moved block](https://developer.hashicorp.com/terraform/language/block/moved) · [removed block](https://developer.hashicorp.com/terraform/language/block/removed) · [manage sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data) · [write-only arguments](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only) · [ephemeral block](https://developer.hashicorp.com/terraform/language/block/ephemeral)

**CLI** — [command overview](https://developer.hashicorp.com/terraform/cli/commands) · [inspect state](https://developer.hashicorp.com/terraform/cli/state) · [import workflow](https://developer.hashicorp.com/terraform/cli/import) · [inspect configuration](https://developer.hashicorp.com/terraform/cli/inspect) · [init](https://developer.hashicorp.com/terraform/cli/commands/init) · [validate](https://developer.hashicorp.com/terraform/cli/commands/validate) · [fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt) · [plan](https://developer.hashicorp.com/terraform/cli/commands/plan) · [apply](https://developer.hashicorp.com/terraform/cli/commands/apply) · [destroy](https://developer.hashicorp.com/terraform/cli/commands/destroy) · [show](https://developer.hashicorp.com/terraform/cli/commands/show) · [output](https://developer.hashicorp.com/terraform/cli/commands/output) · [console](https://developer.hashicorp.com/terraform/cli/commands/console) · [graph](https://developer.hashicorp.com/terraform/cli/commands/graph) · [providers](https://developer.hashicorp.com/terraform/cli/commands/providers) · [import command](https://developer.hashicorp.com/terraform/cli/commands/import)

**CLI, state and workspaces** — [state](https://developer.hashicorp.com/terraform/cli/commands/state) · [state list](https://developer.hashicorp.com/terraform/cli/commands/state/list) · [state show](https://developer.hashicorp.com/terraform/cli/commands/state/show) · [state mv](https://developer.hashicorp.com/terraform/cli/commands/state/mv) · [state rm](https://developer.hashicorp.com/terraform/cli/commands/state/rm) · [force-unlock](https://developer.hashicorp.com/terraform/cli/commands/force-unlock) · [workspace](https://developer.hashicorp.com/terraform/cli/commands/workspace) · [workspace select](https://developer.hashicorp.com/terraform/cli/commands/workspace/select) · [login](https://developer.hashicorp.com/terraform/cli/commands/login) · [refresh (deprecated)](https://developer.hashicorp.com/terraform/cli/commands/refresh) · [taint (deprecated)](https://developer.hashicorp.com/terraform/cli/commands/taint) · [debugging and verbose logging](https://developer.hashicorp.com/terraform/internals/debugging) · [environment variables](https://developer.hashicorp.com/terraform/cli/config/environment-variables)

**HCP Terraform** — [documentation home](https://developer.hashicorp.com/terraform/cloud-docs) · [overview](https://developer.hashicorp.com/terraform/cloud-docs/overview) · [CLI integration](https://developer.hashicorp.com/terraform/cli/cloud) · [cloud block settings](https://developer.hashicorp.com/terraform/cli/cloud/settings) · [workspaces](https://developer.hashicorp.com/terraform/cloud-docs/workspaces) · [projects](https://developer.hashicorp.com/terraform/cloud-docs/projects) · [manage projects](https://developer.hashicorp.com/terraform/cloud-docs/projects/manage) · [run triggers](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/run-triggers) · [variable sets](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables/managing-variables) · [remote operations](https://developer.hashicorp.com/terraform/cloud-docs/run/remote-operations) · [runs in the UI](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/run/ui) · [private registry](https://developer.hashicorp.com/terraform/cloud-docs/registry) · [policy enforcement](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement) · [workspace health](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/health) · [teams](https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/teams)
