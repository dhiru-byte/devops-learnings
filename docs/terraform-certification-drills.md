# Terraform Certification Drills

Multiple-choice practice questions for the [HashiCorp Certified: Terraform Associate](https://developer.hashicorp.com/terraform/tutorials/certification-003)
exam. Each question lists the options, the correct answer in full, and a short explanation.

The interview guide (concepts plus troubleshooting scenarios) is
[Terraform interview guide](terraform-interview-guide.md).

Notes on currency: the exam still tests some commands that HashiCorp has since deprecated
(`terraform taint`, standalone `terraform refresh`). Where that happens the explanation gives both
the exam answer and the command you should use in real work. Terraform Cloud was renamed
**HCP Terraform** in 2024; the two names refer to the same product.

## Contents

- [Infrastructure as Code Concepts](#infrastructure-as-code-concepts) (14 questions)
- [Terraform Basics: Providers and Plugin Architecture](#terraform-basics-providers-and-plugin-architecture) (30 questions)
- [The Core Workflow: init, plan, apply, destroy](#the-core-workflow-init-plan-apply-destroy) (48 questions)
- [Configuration Language: Variables, Outputs, Expressions](#configuration-language-variables-outputs-expressions) (21 questions)
- [Resources, Meta-Arguments and Provisioners](#resources-meta-arguments-and-provisioners) (23 questions)
- [Modules and the Registry](#modules-and-the-registry) (32 questions)
- [State, Backends and Locking](#state-backends-and-locking) (34 questions)
- [Outside the Core Workflow: Import, State CLI, Replace, Debug](#outside-the-core-workflow-import-state-cli-replace-debug) (34 questions)
- [Workspaces, HCP Terraform (Terraform Cloud) and Enterprise](#workspaces-hcp-terraform-terraform-cloud-and-enterprise) (22 questions)
- [Secrets and Sensitive Data](#secrets-and-sensitive-data) (13 questions)


## Infrastructure as Code Concepts

<details>
<summary>Which of the following is not a key principle of infrastructure as code?</summary>

**Options:**

- **A.** Versioned infrastructure
- **B.** Golden images
- **C.** Idempotence
- **D.** Self-describing infrastructure

**Answer:** **B.** Golden images

**Explanation:**
Golden images are preconfigured disk images used to deploy environments and are not a core principle of infrastructure as code (IaC). The key principles of IaC include:
- **Versioned infrastructure:** Treating infrastructure as version-controlled code.
- **Idempotence:** Ensuring deployments produce the same results no matter how many times they are applied.
- **Self-describing infrastructure:** Clearly defining the desired state within configuration files.

</details>

<details>
<summary>You are an engineer tasked with evaluating multiple outages that occurred during peak traffic times. You discover that the team manually deploys and configures new compute instances. This led to inconsistent configurations between each compute instance. How would you solve this using infrastructure as code?</summary>

**Options:**

- **A.** Implement a ticketing workflow that makes engineers submit a ticket before manually provisioning and configuring a resource
- **B.** Implement a checklist that engineers can follow when configuring compute instances
- **C.** Replace the compute instance type with a larger version to reduce the number of required deployments
- **D.** Build a provisioning pipeline that deploys infrastructure configurations committed to your version control system, following code reviews

**Answer:** **D.** Build a provisioning pipeline that deploys infrastructure configurations committed to your version control system, following code reviews

**Explanation:**
Using infrastructure as code (IaC) encourages consistent deployment by:
- Storing configuration in version control systems for better collaboration and traceability.
- Automating provisioning pipelines to ensure all resources are deployed in a standardized and repeatable manner.
- Enabling code reviews to ensure all infrastructure changes are reviewed and approved before deployment.

This approach minimizes human error and ensures reliability during deployments.

</details>

<details>
<summary>Which statement describes a goal of infrastructure as code?</summary>

**Options:**

- **A.** An abstraction from vendor specific APIs
- **B.** Write once, run anywhere
- **C.** A pipeline process to test and deliver software
- **D.** The programmatic configuration of resources

**Answer:** **D.** The programmatic configuration of resources

**Explanation:**
Infrastructure as Code (IaC) focuses on the programmatic configuration and management of infrastructure resources through code, treating infrastructure in the same way as application code. This approach allows for versioning, consistency, and automation of infrastructure deployments.

**Reference:**
[Infrastructure as Code Documentation](https://developer.hashicorp.com/terraform/intro)

</details>

<details>
<summary>How can a ticket-based system slow down infrastructure provisioning and limit the ability to scale? (Choose two.)</summary>

**Options:**

- **A.** A full audit trail of the request and fulfillment process is generated
- **B.** A request must be submitted for infrastructure changes
- **C.** As additional resources are required, more tickets are submitted
- **D.** A catalog of approved resources can be accessed from drop-down lists in a request form

**Answer:** **B.** A request must be submitted for infrastructure changes, **C.** As additional resources are required, more tickets are submitted

**Reference:**
[Infrastructure as Code Best Practices](https://developer.hashicorp.com/terraform/docs)

</details>

<details>
<summary>What advantage does an operations team that uses infrastructure as code have?</summary>

**Options:**

- **A.** The ability to delete infrastructure
- **B.** The ability to update existing infrastructure
- **C.** The ability to reuse best practice configurations and settings
- **D.** The ability to autoscale a group of servers

**Answer:** **C.** The ability to reuse best practice configurations and settings

</details>

<details>
<summary>Which of the following is **not** an advantage of using infrastructure as code operations?</summary>

**Options:**

- **A.** Self-service infrastructure deployment
- **B.** Troubleshoot via a Linux `diff` command
- **C.** Public cloud console configuration workflows
- **D.** Modify a count parameter to scale resources
- **E.** API-driven workflows

**Answer:** **C.** Public cloud console configuration workflows

</details>

<details>
<summary>Which of the following is true about Terraform's implementation of infrastructure as code? (Choose two.)</summary>

**Options:**

- **A.** It is only compatible with AWS infrastructure management
- **B.** You cannot reuse infrastructure configuration
- **C.** You can version your infrastructure configuration
- **D.** It requires manual configuration of infrastructure resources
- **E.** It allows you to automate infrastructure provisioning

**Answer:** **C.** You can version your infrastructure configuration, **E.** It allows you to automate infrastructure provisioning

</details>

<details>
<summary>As a member of an operations team that uses infrastructure as code (IaC) practices, you are tasked with making a change to an infrastructure stack running in a public cloud. Which pattern would follow IaC best practices for making a change?</summary>

**Options:**

- **A.** Clone the repository containing your infrastructure code and then run the code
- **B.** Use the public cloud console to make the change after a database record has been approved
- **C.** Make the change programmatically via the public cloud CLI
- **D.** Make the change via the public cloud API endpoint
- **E.** Submit a pull request and wait for an approved merge of the proposed changes

**Answer:** **E.** Submit a pull request and wait for an approved merge of the proposed changes

</details>

<details>
<summary>If a DevOps team adopts AWS CloudFormation as their standardized method for provisioning public cloud resources, which of the following scenarios poses a challenge for this team?</summary>

**Options:**

- **A.** The team is asked to build a service code base that can deploy resources into any AWS region
- **B.** The team is asked to manage a new application stack built on AWS-native services
- **C.** The organization decides to expand into Azure and wishes to deploy new infrastructure using their existing codebase
- **D.** The DevOps team is tasked with automating a manual provisioning process

**Answer:** **C.** The organization decides to expand into Azure and wishes to deploy new infrastructure using their existing codebase

</details>

<details>
<summary>Which are examples of infrastructure as code? (Choose two.)</summary>

**Options:**

- **A.** Cloned virtual machine images
- **B.** Change management database records
- **C.** Versioned configuration files
- **D.** Docker files

**Answer:** **C.** Versioned configuration files, **D.** Docker files

</details>

<details>
<summary>Infrastructure as Code (IaC) can be stored in a version control system along with application code.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>Which of the following methods, used to provision resources into a public cloud, demonstrates the concept of infrastructure as code?</summary>

**Options:**

- **A.** curl commands manually run from a terminal
- **B.** A sequence of REST requests you pass to a public cloud API endpoint
- **C.** A script that contains a series of public cloud CLI commands
- **D.** A series of commands you enter into a public cloud console

**Answer:** **C.** A script that contains a series of public cloud CLI commands

</details>

<details>
<summary>Which of the following are advantages of using Infrastructure as Code (IaC) instead of provisioning with a graphical user interface (GUI)? (Choose two.)</summary>

**Options:**

- **A.** Secures your credentials
- **B.** Lets you version, reuse, and share infrastructure configuration
- **C.** Provisions the same resources at a lower cost
- **D.** Reduces risk of operator error
- **E.** Prevents manual modifications to your resources

**Answer:** **B.** Lets you version, reuse, and share infrastructure configuration, **E.** Prevents manual modifications to your resources

</details>

<details>
<summary>Which of the following is **not** a benefit of adopting infrastructure as code?</summary>

**Options:**

- **A.** Reusability of code
- **B.** Automation
- **C.** Graphical User Interface
- **D.** Versioning

**Answer:** **C.** Graphical User Interface

</details>


## Terraform Basics: Providers and Plugin Architecture

<details>
<summary>A provider configuration block is required in every Terraform configuration.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Terraform infers which providers it needs from the resource and data source types used in the
configuration, then installs them during `terraform init`. An explicit `provider` block is only
needed when you must set arguments (region, credentials, endpoints) or define aliased
configurations. A configuration whose provider is fully configured through environment variables
or provider defaults needs no `provider` block at all.

**Reference:**
[Provider Configuration](https://developer.hashicorp.com/terraform/language/providers/configuration)

</details>

<details>
<summary>Which of the following is not true of Terraform providers?</summary>

**Options:**

- **A.** Providers can be written by individuals
- **B.** Providers can be maintained by a community of users
- **C.** Some providers are maintained by HashiCorp
- **D.** Major cloud vendors and non-cloud vendors can write, maintain, or collaborate on Terraform providers
- **E.** None of the above

**Answer:** **E.** None of the above

**Explanation:**
All the statements about Terraform providers are true:
- Providers can indeed be written by individuals.
- Providers can also be maintained by a community of users.
- Some providers are officially maintained by HashiCorp to ensure reliability and consistency.
- Major cloud vendors, as well as non-cloud vendors, actively contribute to developing and maintaining Terraform providers, enabling better integration and usability.

</details>

<details>
<summary>What is the provider for this fictitious resource?</summary>

**Configuration:**
```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "test"
  }
}
```

**Options:**

- **A.** vpc
- **B.** main
- **C.** aws
- **D.** test

**Answer:** **C.** aws

**Explanation:**
The resource type is `aws_vpc`. Terraform derives the provider from the prefix of the resource
type, so `aws` is the provider, `aws_vpc` is the resource type and `main` is the local name used to
reference the resource (`aws_vpc.main`).

**Reference:**
[Provider Requirements](https://developer.hashicorp.com/terraform/language/providers/requirements)

</details>

<details>
<summary>Terraform requires the Go runtime as a prerequisite for installation.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Terraform is written in Go, but it is distributed as a single statically linked binary with no
runtime dependency. You only need a Go toolchain if you intend to build Terraform or a provider
from source.

**Reference:**
[Install Terraform](https://developer.hashicorp.com/terraform/install)

</details>

<details>
<summary>Terraform can run on Windows or Linux, but it requires a Server version of the Windows operating system.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Terraform does not require a Server version of the Windows operating system to run. It is supported on both Windows (including non-server versions), Linux, and macOS. Terraform is a lightweight binary and works across multiple operating systems without requiring specialized versions.

**Reference:**
[Terraform Downloads and Platform Support](https://developer.hashicorp.com/terraform/downloads)

</details>

<details>
<summary>Outside of the `required_providers` block, Terraform configurations always refer to providers by their local names.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

**Explanation:**
In Terraform configurations, providers are often defined in a `required_providers` block where an alias or local name is associated with the provider source (e.g., `hashicorp/aws`). Outside of the `required_providers` block, Terraform references providers using the local names defined in your configuration, such as `aws` or `azurerm`.

**Example:**
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}
```

</details>

<details>
<summary>Terraform providers are always installed from the Internet.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Terraform configurations must declare which providers they require, so that Terraform can install and use them. Providers can also be installed locally if needed, rather than retrieving them from the Internet.

**Reference:**
[Terraform Provider Configuration Documentation](https://developer.hashicorp.com/terraform/language/providers/configuration)

</details>

<details>
<summary>A Terraform provider is **not** responsible for:</summary>

**Options:**

- **A.** Understanding API interactions with some service
- **B.** Provisioning infrastructure in multiple clouds
- **C.** Exposing resources and data sources based on an API
- **D.** Managing actions to take based on resource differences

**Answer:** **B.** Provisioning infrastructure in multiple clouds

</details>

<details>
<summary>You need to constrain the GitHub provider to version 2.1 or greater. Which of the following should you put into the Terraform configuration?</summary>

**Options:**

- **A.** version >= 2.1
- **B.** version ~> 2.1
- **C.** version = "<= 2.1"
- **D.** version => 2.1

**Answer:** **A.** version >= 2.1

**Explanation:**
`>=` is the "this version or newer" operator. `~>` is the pessimistic operator (`~> 2.1` allows
2.1 up to but not including 3.0), `<=` is the opposite bound, and `=>` is not a valid Terraform
operator.

Written as real HCL the constraint belongs in `required_providers` and the value must be quoted:

```hcl
terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = ">= 2.1"
    }
  }
}
```

**Reference:**
[Version Constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)

</details>

<details>
<summary>Terraform and Terraform providers must use the same major version number in a single configuration. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Terraform and its providers do not need to use the same major version number. Terraform Core (e.g., version 1.x) and providers (e.g., `aws` provider version 5.x) are versioned independently. Each provider version is specified and managed separately from the Terraform Core version, allowing flexibility in configuration.

**Reference:**
[Terraform Version Constraints Documentation](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)

</details>

<details>
<summary>Most Terraform providers interact with _____________.</summary>

**Options:**

- **A.** APIs
- **B.** VCS Systems
- **C.** Shell scripts
- **D.** None of the above

**Answer:** **A.** APIs

**Reference:**
[Terraform Provider Documentation](https://developer.hashicorp.com/terraform/language/providers)

</details>

<details>
<summary>You just upgraded the version of a provider in an existing Terraform project. What do you need to do to install the new provider?</summary>

**Options:**

- **A.** Run terraform apply -upgrade
- **B.** Run terraform init -upgrade
- **C.** Run terraform refresh
- **D.** Upgrade your version of Terraform

**Answer:** **B.** Run terraform init -upgrade

**Reference:**
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)

</details>

<details>
<summary>What does Terraform use `.terraform.lock.hcl` file for?</summary>

**Options:**

- **A.** Tracking provider dependencies
- **B.** There is no such file
- **C.** Preventing Terraform runs from occurring
- **D.** Storing references to workspaces which are locked

**Answer:** **A.** Tracking provider dependencies

**Reference:**
[Terraform Dependency Lock File Documentation](https://developer.hashicorp.com/terraform/language/files/dependency-lock)

</details>

<details>
<summary>What does Terraform use providers for? (Choose three.)</summary>

**Options:**

- **A.** Provision resources for on-premises infrastructure services
- **B.** Simplify API interactions
- **C.** Provision resources for public cloud infrastructure services
- **D.** Enforce security and compliance policies
- **E.** Group a collection of Terraform configuration files that map to a single state file

**Answer:** **A.** Provision resources for on-premises infrastructure services, **B.** Simplify API interactions, **C.** Provision resources for public cloud infrastructure services

</details>

<details>
<summary>What does this code do?</summary>

```hcl
terraform {
  required_providers {
    aws = "~> 3.0"
  }
}
```

**Options:**

- **A.** Requires any version of the AWS provider >= 3.0 and < 4.0
- **B.** Requires any version of the AWS provider >= 3.0
- **C.** Requires any version of the AWS provider after the 3.0 major release, like 4.1
- **D.** Requires any version of the AWS provider > 3.0

**Answer:** **A.** Requires any version of the AWS provider >= 3.0 and < 4.0

**Explanation:**
The pessimistic constraint operator `~>` allows the rightmost version component to increment only.
`~> 3.0` therefore permits 3.0, 3.1, 3.75 but not 4.0, while `~> 3.0.1` would permit 3.0.x only.

The bare-string form shown here is legacy syntax. Current configurations should name the source
explicitly so Terraform does not guess the registry namespace:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}
```

**Reference:**
[Version Constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)

</details>

<details>
<summary>Terraform installs its providers during which phase?</summary>

**Options:**

- **A.** Plan
- **B.** Init
- **C.** Refresh
- **D.** All of the above

**Answer:** **B.** Init

</details>

<details>
<summary>Where can Terraform **not** load a provider from?</summary>

**Options:**

- **A.** Source code
- **B.** Plugins directory
- **C.** Official HashiCorp distribution on `releases.hashicorp.com`
- **D.** Provider plugin cache

**Answer:** **A.** Source code

</details>

<details>
<summary>You cannot install third-party plugins using terraform init.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>The ________ determines how Terraform creates, updates, or deletes resources.</summary>

**Options:**

- **A.** Terraform configuration
- **B.** Terraform core
- **C.** Terraform provider
- **D.** Terraform provisioner

**Answer:** **C.** Terraform provider

</details>

<details>
<summary>Terraform configuration (including any module references) can contain only one Terraform provider type.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Which of the following should you put into the `required_providers` block?</summary>

**Options:**

- **A.** version >= 3.1
- **B.** version = ">= 3.1"
- **C.** version ~> 3.1

**Answer:** **B.** version = ">= 3.1"

</details>

<details>
<summary>You add a new resource to an existing Terraform configuration but do not update the version constraint in the configuration. The existing and new resources use the same provider. The working directory contains a `.terraform.lock.hcl` file. How will Terraform choose which version of the provider to use?</summary>

**Options:**

- **A.** Terraform will use the latest version of the provider for the new resource and the version recorded in the lock file to manage existing resources
- **B.** Terraform will use the version recorded in your lock file
- **C.** Terraform will check your state file to determine the provider version to use
- **D.** Terraform will use the latest version of the provider available at the time you provision your new resource

**Answer:** **B.** Terraform will use the version recorded in your lock file

**Explanation:**
The dependency lock file pins the exact provider versions selected by a previous `terraform init`,
and Terraform reuses them for the whole configuration until you change the version constraint or
run `terraform init -upgrade`. Terraform never runs two versions of the same provider in one
configuration.

**Reference:**
[Dependency Lock File](https://developer.hashicorp.com/terraform/language/files/dependency-lock)

</details>

<details>
<summary>You must use different Terraform commands depending on the cloud provider you use.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>The Terraform binary version and provider versions must match each other in a single configuration.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>The `.terraform.lock.hcl` file tracks module versions.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>You can develop a custom provider to manage its resources using Terraform.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>If you update the version constraint in your Terraform configuration, Terraform will update your lock file the next time you run `terraform init`.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Terraform providers are part of the Terraform core binary.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Which of these is true about Terraform's plugin-based architecture?</summary>

**Options:**

- **A.** Terraform can only source providers from the internet
- **B.** You can create a provider for your API if none exists
- **C.** Every provider in a configuration has its own state file for its resources
- **D.** All providers are part of the Terraform core binary

**Answer:** **B.** You can create a provider for your API if none exists

</details>

<details>
<summary>When does Terraform create the `.terraform.lock.hcl` file?</summary>

**Options:**

- **A.** After your first `terraform plan`
- **B.** After your first `terraform apply`
- **C.** After your first `terraform init`
- **D.** Whenever you enable state locking

**Answer:** **C.** After your first `terraform init`

</details>


## The Core Workflow: init, plan, apply, destroy

<details>
<summary>What is the workflow for deploying new infrastructure with Terraform?</summary>

**Options:**

- **A.** terraform plan to import the current infrastructure to the state file, make code changes, and terraform apply to update the infrastructure.
- **B.** Write a Terraform configuration, run terraform show to view proposed changes, and terraform apply to create new infrastructure.
- **C.** terraform import to import the current infrastructure to the state file, make code changes, and terraform apply to update the infrastructure.
- **D.** Write a Terraform configuration, run terraform init, run terraform plan to view planned infrastructure changes, and terraform apply to create new infrastructure.

**Answer:** **D.** Write a Terraform configuration, run terraform init, run terraform plan to view planned infrastructure changes, and terraform apply to create new infrastructure.

**Explanation:**
To deploy new infrastructure using Terraform, follow these steps:
1. Write the Terraform configuration specifying the desired infrastructure resources.
2. Run `terraform init` to initialize the configuration and download necessary provider plugins.
3. Run `terraform plan` to see the execution plan and ensure the desired changes match your expectation.
4. Run `terraform apply` to provision the specified resources and create the new infrastructure.

</details>

<details>
<summary>What command does Terraform require the first time you run it within a configuration directory?</summary>

**Options:**

- **A.** terraform import
- **B.** terraform init
- **C.** terraform plan
- **D.** terraform workspace

**Answer:** **B.** terraform init

**Explanation:**
The `terraform init` command is used to initialize a working directory containing Terraform configuration files. This command prepares the directory for use by downloading the required provider plugins and setting up the Terraform environment.

**Reference:**
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)

</details>

<details>
<summary>terraform init initializes a sample main.tf file in the current directory.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
The `terraform init` command initializes a working directory with all the necessary files for Terraform to manage infrastructure. It downloads provider plugins, sets up the backend, and prepares the directory for running Terraform commands. However, it does **not** create a `main.tf` file or any configuration files. Users must write their own `.tf` configuration files manually or copy them into the directory.

</details>

<details>
<summary>Which two steps are required to provision new infrastructure in the Terraform workflow? (Choose two.)</summary>

**Options:**

- **A.** Destroy
- **B.** Apply
- **C.** Import
- **D.** Init
- **E.** Validate

**Answer:** **B.** Apply, **D.** Init

**Explanation:**
To provision new infrastructure using Terraform, the following steps are required:
1. **Init (`terraform init`)**: Initializes the working directory by downloading necessary provider plugins and preparing the backend for state management.
2. **Apply (`terraform apply`)**: Executes the Terraform configuration to create or modify infrastructure resources.

Other steps like `terraform validate` or `terraform import` are not mandatory for provisioning new infrastructure, while `terraform destroy` is used for removing resources.

**Reference:**
[Terraform Core Workflow Guide](https://developer.hashicorp.com/terraform/intro/core-workflow)

</details>

<details>
<summary>terraform validate validates the syntax of Terraform files.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

**Explanation:**
The `terraform validate` command is used to validate the syntax and arguments of Terraform configuration files. It checks whether the configuration is syntactically valid and internally consistent but does not interact with any APIs or create any resources.

**Reference:**
[Terraform Validate Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/validate)

</details>

<details>
<summary>You have used Terraform to create an ephemeral development environment in the cloud and are now ready to destroy all the infrastructure described by your Terraform configuration. To be safe, you would like to first see all the infrastructure that will be deleted by Terraform. Which command should you use to show all of the resources that will be deleted? (Choose two.)</summary>

**Options:**

- **A.** Run terraform plan -destroy.
- **B.** This is not possible. You can only show resources that will be created.
- **C.** Run terraform state rm *.
- **D.** Run terraform destroy and it will first output all the resources that will be deleted before prompting for approval.

**Answer:** **A.** Run terraform plan -destroy., **D.** Run terraform destroy and it will first output all the resources that will be deleted before prompting for approval.

**Explanation:**
- **`terraform plan -destroy`**: This command creates and displays an execution plan for destroying resources. It allows you to review the resources that will be deleted without actually destroying them.
- **`terraform destroy`**: This command prompts for confirmation and outputs all the resources that will be destroyed before performing the action, allowing you to review the list of resources.

**Why the other options are wrong:**
- **B**: It is possible to preview deletions with the correct commands.
- **C**: `terraform state rm` is used to remove resources from the state file without affecting the actual infrastructure, not to preview deletions.

**Reference:**
[Terraform State RM Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/state/rm)

</details>

<details>
<summary>You have multiple team members collaborating on infrastructure as code (IaC) using Terraform, and want to apply formatting standards for readability. How can you format Terraform HCL (HashiCorp Configuration Language) code according to standard Terraform style convention?</summary>

**Options:**

- **A.** Run the terraform fmt command during the code linting phase of your CI/CD process
- **B.** Designate one person in each team to review and format everyone's code
- **C.** Manually apply two spaces indentation and align equal sign "=" characters in every Terraform file (*.tf)
- **D.** Write a shell script to transform Terraform files using tools such as AWK, Python, and sed

**Answer:** **A.** Run the terraform fmt command during the code linting phase of your CI/CD process

**Explanation:**
The `terraform fmt` command automatically formats Terraform code (*.tf files) to follow the standard style convention defined by Terraform. It ensures uniform indentation and alignment, making the code consistent and readable for all team members. Running this command regularly as part of the CI/CD process helps enforce code formatting across the team without requiring manual intervention.

**Why the other options are wrong:**
- **B**: Designating someone to manually review and format code is time-consuming and error-prone.
- **C**: Manually formatting is inefficient and prone to inconsistencies.
- **D**: Writing custom scripts is unnecessary since Terraform provides the `fmt` command for this purpose.

**Reference:**
[Terraform Formatting Documentation](https://developer.hashicorp.com/terraform/cli/commands/fmt)

</details>

<details>
<summary>Which task does terraform init **not** perform?</summary>

**Options:**

- **A.** Sources all providers present in the configuration and ensures they are downloaded and available locally
- **B.** Connects to the backend
- **C.** Sources any modules and copies the configuration locally
- **D.** Validates all required variables are present

**Answer:** **D.** Validates all required variables are present

**Explanation:**
The `terraform init` command is used to initialize a working directory containing a Terraform configuration. It handles tasks such as downloading providers, setting up the backend, and sourcing any modules used in the configuration. However, it does not validate the presence of required variables during initialization. Variable validation occurs at the `terraform plan` or `terraform apply` stages.

**Why the other options are wrong:**
- **A**: `terraform init` sources and downloads providers defined in the configuration.
- **B**: It connects to the backend to allow for remote state storage if a backend is configured.
- **C**: It fetches and copies any external modules defined in the configuration.

**Reference:**
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)

</details>

<details>
<summary>You have created a new virtual machine (VM) using Terraform and want to delete it. What should you do to delete the newly-created VM with Terraform?</summary>

**Options:**

- **A.** The Terraform state file contains all 16 VMs in the team account. Execute terraform destroy and select the newly-created VM.
- **B.** The Terraform state file only contains the one new VM. Execute terraform destroy.
- **C.** Delete the Terraform state file and execute terraform apply.
- **D.** Delete the VM using the cloud provider console and terraform apply to apply the changes to the Terraform state file.

**Answer:** **B.** The Terraform state file only contains the one new VM. Execute terraform destroy.

**Explanation:**
Terraform manages resources defined in your configuration using the state file. Since the state file for this configuration only tracks the newly-created VM, you can run `terraform destroy`. This command will use the state file to identify and delete the resources it manages—in this case, the one VM created by Terraform. There is no need to delete resources manually or interfere with the state file.

**Why the other options are wrong:**
- **A:** The Terraform state file does not include unmanaged resources (e.g., the other 15 VMs created outside of Terraform), so destroying all resources is unnecessary in this context.
- **C:** Deleting the state file would remove Terraform's ability to manage existing resources, such as the VM. This is not recommended.
- **D:** Using the cloud provider console to delete resources manually may leave the Terraform state file out of sync with the actual infrastructure unless properly reconciled, which requires additional steps.

**Reference:**
[Terraform Destroy Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/destroy)

</details>

<details>
<summary>When does `terraform apply` reflect changes in the cloud environment?</summary>

**Options:**

- **A.** Immediately
- **B.** However long it takes the resource provider to fulfill the request
- **C.** After updating the state file
- **D.** Based on the value provided to the -refresh command line argument
- **E.** None of the above

**Answer:** **B.** However long it takes the resource provider to fulfill the request

**Explanation:**
When `terraform apply` is executed, Terraform sends requests to the resource provider (e.g., AWS, Azure) to create, update, or delete infrastructure. The time it takes for changes to reflect in the cloud environment depends on how long the resource provider needs to fulfill those requests. This process can vary depending on the type of resource and the provider's performance.

**Reference:**
[Terraform Apply Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)

</details>

<details>
<summary>What is the name of the flag you would add to `terraform plan` to save the execution plan to a file?</summary>

**Answer:** -out=FILENAME

**Reference:**
[Terraform Plan Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/plan)

</details>

<details>
<summary>How can `terraform plan` aid in the development process?</summary>

**Options:**

- **A.** Validates your expectations against the execution plan without permanently modifying state
- **B.** Initializes your working directory containing your Terraform configuration files
- **C.** Formats your Terraform configuration files
- **D.** Reconciles Terraform's state against deployed resources and permanently modifies state using the current status of deployed resources

**Answer:** **A.** Validates your expectations against the execution plan without permanently modifying state

**Reference:**
[terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)

</details>

<details>
<summary>You have a simple Terraform configuration containing one virtual machine (VM) in a cloud provider. You run `terraform apply` and the VM is created successfully. What will happen if you delete the VM using the cloud provider console and run `terraform apply` again without changing any Terraform code?</summary>

**Options:**

- **A.** Terraform will remove the VM from the state file
- **B.** Terraform will report an error
- **C.** Terraform will not make any changes
- **D.** Terraform will recreate the VM

**Answer:** **D.** Terraform will recreate the VM

</details>

<details>
<summary>You write a new Terraform configuration and immediately run `terraform apply` in the CLI using the local backend. Why will the apply fail?</summary>

**Options:**

- **A.** Terraform needs you to format your code according to best practices first
- **B.** Terraform needs to install the necessary plugins first
- **C.** The Terraform CLI needs you to log into Terraform cloud first
- **D.** Terraform requires you to manually run terraform plan first

**Answer:** **B.** Terraform needs to install the necessary plugins first

**Explanation:**
When you execute a Terraform command for the first time, Terraform automatically looks for the necessary provider plugins. If they are not installed, the program will fail. Running `terraform init` ensures that all required plugins are downloaded.

**Reference:**
[Terraform CLI Commands Documentation](https://developer.hashicorp.com/terraform/cli)

</details>

<details>
<summary>A terraform apply can **not** __________ infrastructure.</summary>

**Options:**

- **A.** change
- **B.** destroy
- **C.** provision
- **D.** import

**Answer:** **D.** import

**Explanation:**
`terraform apply` creates, updates and destroys resources to reach the desired state. Historically
it could not adopt pre-existing objects into state; that required the separate `terraform import`
command.

Terraform 1.5 added declarative `import` blocks, so a plan/apply cycle *can* now import when the
configuration contains an `import` block. The exam answer remains `import`, but be ready to
mention the 1.5+ behaviour in an interview.

**Reference:**
[Import blocks](https://developer.hashicorp.com/terraform/language/import)

</details>

<details>
<summary>You just scaled your VM infrastructure and realized you set the count variable to the wrong value. You correct the value and save your change. What do you do next to make your infrastructure match your configuration?</summary>

**Options:**

- **A.** Run terraform apply and confirm the planned changes
- **B.** Inspect your Terraform state because you want to change it
- **C.** Reinitialize because your configuration has changed
- **D.** Inspect all Terraform outputs to make sure they are correct

**Answer:** **A.** Run terraform apply and confirm the planned changes

**Explanation:**
After fixing the count variable and saving the configuration, you need to run `terraform apply` to implement the changes in your infrastructure. Terraform will refresh the state, show you a proposed plan of changes, and ask for confirmation before making updates.

**Reference:**
[Terraform Apply Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)

</details>

<details>
<summary>Terraform validate reports syntax check errors from which of the following scenarios?</summary>

**Options:**

- **A.** Code contains tabs indentation instead of spaces
- **B.** There is missing value for a variable
- **C.** The state files do not match the current infrastructure
- **D.** None of the above

**Answer:** **D.** None of the above

**Explanation:**
`terraform validate` checks the syntax and consistency of a Terraform configuration but does not perform validation for issues like code styling (e.g., tabs vs. spaces) or runtime errors such as missing variables or state file mismatches. These types of problems are addressed during `terraform plan` or `terraform apply` execution.

**Reference:**
[Terraform Validate Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/validate)

</details>

<details>
<summary>Which of the following is **not** an action performed by `terraform init`?</summary>

**Options:**

- **A.** Create a sample main.tf file
- **B.** Initialize a configured backend
- **C.** Retrieve the source code for all referenced modules
- **D.** Load required provider plugins

**Answer:** **A.** Create a sample main.tf file

**Explanation:**
The `terraform init` command is responsible for setting up the working directory. It initializes the backend for storing state, retrieves remote modules, and downloads the necessary provider plugins. However, it does **not** create any sample configuration files like `main.tf`. Users need to create configuration files manually.

**Reference:**
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)

</details>

<details>
<summary>`terraform validate` validates that your infrastructure matches the Terraform state file. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Reference:**
[Terraform Validate Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/validate)

</details>

<details>
<summary>You have a simple Terraform configuration containing one virtual machine (VM) in a cloud provider. You run `terraform apply` and the VM is created successfully. What will happen if you run `terraform apply` again immediately afterwards without changing any Terraform code?</summary>

**Options:**

- **A.** Terraform will terminate and recreate the VM
- **B.** Terraform will create another duplicate VM
- **C.** Terraform will apply the VM to the state file
- **D.** Nothing

**Answer:** **D.** Nothing

**Reference:**
[Terraform Plan and Apply Workflow](https://developer.hashicorp.com/terraform/cli/commands/apply)

</details>

<details>
<summary>A junior admin accidentally deleted some of your cloud instances. What does Terraform do when you run `terraform apply`?</summary>

**Options:**

- **A.** Build a completely brand new set of infrastructure
- **B.** Tear down the entire workspace infrastructure and rebuild it
- **C.** Rebuild only the instances that were deleted
- **D.** Stop and generate an error message about the missing instances

**Answer:** **C.** Rebuild only the instances that were deleted

**Reference:**
[Terraform Apply Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)

</details>

<details>
<summary>You have created a `main.tf` Terraform configuration consisting of an application server, a database, and a load balancer. You ran `terraform apply` and all resources were created successfully. Now you realize that you do not actually need the load balancer, so you run `terraform destroy` without any flags. What will happen?</summary>

**Options:**

- **A.** Terraform will destroy the application server because it is listed first in the code
- **B.** Terraform will prompt you to confirm that you want to destroy all the infrastructure
- **C.** Terraform will destroy the `main.tf` file
- **D.** Terraform will prompt you to pick which resource you want to destroy
- **E.** Terraform will immediately destroy all the infrastructure

**Answer:** **B.** Terraform will prompt you to confirm that you want to destroy all the infrastructure

**Reference:**
[Terraform Destroy Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/destroy)

</details>

<details>
<summary>You have just developed a new Terraform configuration for two virtual machines with a cloud provider. You would like to create the infrastructure for the first time. Which Terraform command should you run first?</summary>

**Options:**

- **A.** terraform apply
- **B.** terraform plan
- **C.** terraform show
- **D.** terraform init

**Answer:** **D.** terraform init

**Reference:**
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)

</details>

<details>
<summary>Which of the following does `terraform apply` change after you approve the execution plan? (Choose two.)</summary>

**Options:**

- **A.** Cloud infrastructure
- **B.** The .terraform directory
- **C.** The execution plan
- **D.** State file
- **E.** Terraform code

**Answer:** **A.** Cloud infrastructure, **D.** State file

**Reference:**
[Terraform Apply Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)

</details>

<details>
<summary>Terraform plan updates your state file. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Reference:**
[Terraform Plan Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/plan)

</details>

<details>
<summary>To check if all code in a Terraform configuration with multiple modules is properly formatted without making changes, what command should be run?</summary>

**Options:**

- **A.** terraform fmt -check
- **B.** terraform fmt -write=false
- **C.** terraform fmt -list -recursive
- **D.** terraform fmt -check -recursive

**Answer:** **D.** terraform fmt -check -recursive

**Reference:**
[Terraform Fmt Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/fmt)

</details>

<details>
<summary>Which of the following is **not** a way to trigger `terraform destroy`?</summary>

**Options:**

- **A.** Using the `destroy` command with auto-approve
- **B.** Running `terraform destroy` from the correct directory and then typing "yes" when prompted in the CLI
- **C.** Passing `--destroy` at the end of a plan request
- **D.** Delete the state file and run `terraform apply`

**Answer:** **D.** Delete the state file and run `terraform apply`

</details>

<details>
<summary>Which of the following is true about `terraform apply`? (Choose two.)</summary>

**Options:**

- **A.** It only operates on infrastructure defined in the current working directory or workspace
- **B.** You must pass the output of a terraform plan command to it
- **C.** Depending on provider specification, Terraform may need to destroy and recreate your infrastructure resources
- **D.** By default, it does not refresh your state file to reflect current infrastructure configuration
- **E.** You cannot target specific resources for the operation

**Answer:** **A.** It only operates on infrastructure defined in the current working directory or workspace, **C.** Depending on provider specification, Terraform may need to destroy and recreate your infrastructure resources

</details>

<details>
<summary>`terraform apply` will fail if you have not run `terraform plan` first to update the plan output.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>You have modified your local Terraform configuration and ran `terraform plan` to review the changes. Simultaneously, your teammate manually modified the infrastructure component you are working on. Since you already ran `terraform plan` locally, the execution plan for `terraform apply` will be the same.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Running `terraform fmt` without any flags in a directory with Terraform configuration files will check the formatting of those files without changing their contents.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>You have a Terraform configuration that defines a single virtual machine with no references to it. You have run `terraform apply` to create the resource and then removed the resource definition from your Terraform configuration file. What will happen when you run `terraform apply` in the working directory again?</summary>

**Options:**

- **A.** Nothing
- **B.** Terraform will destroy the virtual machine
- **C.** Terraform will error
- **D.** Terraform will remove the virtual machine from the state file, but the resource will still exist

**Answer:** **B.** Terraform will destroy the virtual machine

</details>

<details>
<summary>Which configuration consistency errors does `terraform validate` report?</summary>

**Options:**

- **A.** A mix of spaces and tabs in configuration files
- **B.** Differences between local and remote state
- **C.** Terraform module isn't the latest version
- **D.** Declaring a resource identifier more than once

**Answer:** **D.** Declaring a resource identifier more than once

</details>

<details>
<summary>What does terraform destroy do?</summary>

**Options:**

- **A.** Destroy all infrastructure in the Terraform state file
- **B.** Destroy all Terraform code files in the current directory while leaving the state file intact
- **C.** Destroy all infrastructure in the configured Terraform provider
- **D.** Destroy the Terraform state file while leaving infrastructure intact

**Answer:** **A.** Destroy all infrastructure in the Terraform state file

</details>

<details>
<summary>Which of the following can you do with terraform plan? (Choose two.)</summary>

**Options:**

- **A.** Save a generated execution plan to apply later
- **B.** Reexecute a plan in a different workspace
- **C.** View the execution plan and check if the changes match your expectations
- **D.** Schedule Terraform to run at a planned time in the future

**Answer:** **A.** Save a generated execution plan to apply later, **C.** View the execution plan and check if the changes match your expectations

</details>

<details>
<summary>You updated the Terraform code to change the port from 80 to 443, but another team member manually updates the port to 443 through the Cloud provider console. What will happen when you terraform apply?</summary>

**Options:**

- **A.** Terraform will fail with an error because the state file is no longer accurate
- **B.** Terraform will change the load balancer port to 80, and then change it back to 443
- **C.** Terraform will not make any changes to the Load Balancer and will update the state file to reflect any changes made
- **D.** Terraform will change the port back to 80 in your code

**Answer:** **C.** Terraform will not make any changes to the Load Balancer and will update the state file to reflect any changes made

</details>

<details>
<summary>Terraform destroy is the only way to remove infrastructure.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>When should you run terraform init?</summary>

**Options:**

- **A.** After you run terraform apply for the first time in a new Terraform project and before you run terraform plan
- **B.** After you run terraform plan for the first time in a new Terraform project and before you run terraform apply
- **C.** After you start coding a new Terraform project and before you run terraform plan for the first time
- **D.** Before you start coding a new Terraform project

**Answer:** **C.** After you start coding a new Terraform project and before you run terraform plan for the first time

</details>

<details>
<summary>You are making changes to existing Terraform code to add some new infrastructure. When is the best time to run terraform validate?</summary>

**Options:**

- **A.** After you run terraform plan so you can validate that your state file is consistent with your infrastructure
- **B.** Before you run terraform plan so you can validate your code syntax
- **C.** Before you run terraform apply so you can validate your infrastructure changes
- **D.** After you run terraform apply so you can validate that your infrastructure is reflected in your code

**Answer:** **B.** Before you run terraform plan so you can validate your code syntax

</details>

<details>
<summary>What does running a terraform plan do?</summary>

**Options:**

- **A.** Imports all of your existing cloud provider resources to the state file
- **B.** Compares the state file to your Terraform code and determines if any changes need to be made
- **C.** Imports all of your existing cloud provider resources to your Terraform configuration file
- **D.** Compares your Terraform code and local state file to the remote state file in a cloud provider and determines if any changes need to be made

**Answer:** **B.** Compares the state file to your Terraform code and determines if any changes need to be made

</details>

<details>
<summary>Which of these commands makes your code more human-readable?</summary>

**Options:**

- **A.** terraform validate
- **B.** terraform output
- **C.** terraform plan
- **D.** terraform fmt

**Answer:** **D.** terraform fmt

</details>

<details>
<summary>You must initialize your working directory before running `terraform validate`.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>Which command must you first run before performing further Terraform operations in a working directory?</summary>

**Options:**

- **A.** terraform plan
- **B.** terraform workspace
- **C.** terraform init
- **D.** terraform import

**Answer:** **C.** terraform init

</details>

<details>
<summary>When do changes invoked by `terraform apply` take effect?</summary>

**Options:**

- **A.** After Terraform has updated the state file
- **B.** Once the resource provider has fulfilled the request
- **C.** Immediately
- **D.** None of the above are correct

**Answer:** **D.** None of the above are correct

</details>

<details>
<summary>Which Terraform command checks that your configuration syntax is correct?</summary>

**Options:**

- **A.** terraform fmt
- **B.** terraform validate
- **C.** terraform init
- **D.** terraform show

**Answer:** **B.** terraform validate

</details>

<details>
<summary>`terraform validate` uses provider APIs to verify your infrastructure settings.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>You should run `terraform fmt` to rewrite all Terraform configurations within the current working directory to conform to Terraform-style conventions.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>You have been working in a Cloud provider account that is shared with other team members. You previously used Terraform to create a load balancer that is listening on port 80. After some application changes, you updated the Terraform code to change the port to 443. What will happen when you `terraform apply` upon returning to your desk?</summary>

**Options:**

- **A.** Terraform will fail with an error because the state file is no longer accurate.
- **B.** Terraform will change the load balancer port to 80, and then change it back to 443.
- **C.** Terraform will not make any changes to the Load Balancer and will update the state file to reflect any changes made.
- **D.** Terraform will recreate the load balancer.

**Answer:** **D.** Terraform will recreate the load balancer.

</details>


## Configuration Language: Variables, Outputs, Expressions

<details>
<summary>If a module uses a local value, you can expose that value with a terraform output.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

**Explanation:**
Output values in Terraform serve as a way to expose data from a module to be used in other parts of the configuration or by the user. If a module uses a local value, it can be referenced in an output block within that module to expose it for consumption elsewhere.

**Reference:**
- [Terraform Locals Documentation](https://developer.hashicorp.com/terraform/language/values/locals)
- [Terraform Outputs Documentation](https://developer.hashicorp.com/terraform/language/values/outputs)

</details>

<details>
<summary>Which of the following is not a valid string function in Terraform?</summary>

**Options:**

- **A.** split
- **B.** join
- **C.** slice
- **D.** chomp

**Answer:** **C.** slice

**Explanation:**
`split`, `join` and `chomp` are string functions. `slice` does exist in Terraform, but it is a
*collection* function: `slice(list, startindex, endindex)` returns a sub-list, and it errors on a
string input. The string equivalent is `substr(string, offset, length)`.

**Reference:**
[Terraform Built-in Functions](https://developer.hashicorp.com/terraform/language/functions)

</details>

<details>
<summary>You have declared a variable called `var.list` which is a list of objects that all have an attribute `id`. Which options will produce a list of the IDs? (Choose two.)</summary>

**Options:**

- **A.** { for o in var.list : o => o.id }
- **B.** var.list[*].id
- **C.** [ var.list[*].id ]
- **D.** [ for o in var.list : o.id ]

**Answer:** **B.** var.list[*].id, **D.** [ for o in var.list : o.id ]

**Explanation:**
- **`B. var.list[*].id`**: This uses Terraform's splat expression syntax to create a list of the `id` attributes from all objects in the `var.list`. The `[*].id` extracts the `id` for each element in the list.

- **`D. [ for o in var.list : o.id ]`**: This uses Terraform's for expressions to loop over each object in `var.list` and extract the `id` attribute, returning a new list of the `id` values.

**Why the other options are wrong:**
- **A**: This syntax is incorrect. The use of `{}` creates a map, not a list, and `=>` is not valid syntax in Terraform for constructing a map.
- **C**: This syntax wraps the splat expression in additional brackets, producing a list containing a single element, which is itself another list. It does not flatten into a list of `id` values.

**Reference:**
[Terraform Expressions Documentation](https://developer.hashicorp.com/terraform/language/expressions)

</details>

<details>
<summary>Which argument(s) is (are) required when declaring a Terraform variable?</summary>

**Options:**

- **A.** type
- **B.** default
- **C.** description
- **D.** All of the above
- **E.** None of the above

**Answer:** **E.** None of the above

**Explanation:**
When declaring a Terraform variable, none of the arguments (`type`, `default`, `description`) are strictly required. Terraform can infer the type of a variable based on its value or usage, and a default value or description is optional. If a variable does not have a default value, Terraform treats it as mandatory and expects the user to provide a value either via input or a `.tfvars` file.

**Why the other options are wrong:**
- **A. type**: While defining the type explicitly is helpful for clarity, it is not mandatory since Terraform can infer the type.
- **B. default**: Providing a default value is optional. Without a default, the variable must be supplied as input.
- **C. description**: The description is purely informative and optional.
- **D. All of the above**: None of these are mandatory.

**Reference:**
[Terraform Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>What value should you enter for the `ami` argument in the AWS instance resource to use the AWS AMI data source?</summary>

**Terraform Configuration:**
```hcl
data "aws_ami" "ubuntu" {
}
resource "aws_instance" "web" {
  ami             = _______________
  instance_type   = "t2.micro"
  tags = {
    Name = "HelloWorld"
  }
}
```

**Options:**

- **A.** aws_ami.ubuntu
- **B.** data.aws_ami.ubuntu
- **C.** data.aws_ami.ubuntu.id
- **D.** aws_ami.ubuntu.id

**Answer:** **C.** data.aws_ami.ubuntu.id

**Explanation:**
When referencing a data source in Terraform, you need to use the data.<type>.<name> syntax. To retrieve the id of the AMI from the aws_ami data source, the correct property is id. Thus, the correct reference for the ami attribute is data.aws_ami.ubuntu.id.

</details>

<details>
<summary>A Terraform local value can reference other Terraform local values.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

**Reference:**
[Terraform Local Values Documentation](https://developer.hashicorp.com/terraform/language/values/locals)

</details>

<details>
<summary>Which of the following is **not** a valid Terraform collection type?</summary>

**Options:**

- **A.** list
- **B.** map
- **C.** tree
- **D.** set

**Answer:** **C.** tree

**Reference:**
[Terraform Type Constraints Documentation](https://developer.hashicorp.com/terraform/language/expressions/type-constraints)

</details>

<details>
<summary>Which of the following is allowed as a Terraform variable name?</summary>

**Options:**

- **A.** count
- **B.** name
- **C.** source
- **D.** version

**Answer:** **B.** name

**Explanation:**
Terraform reserves certain keywords (e.g., `count`, `source`, `version`, `lifecycle`, etc.) for its own use, and they cannot be used as variable names. However, `name` is not a reserved keyword and can be used as a valid variable name.

**Reference:**
[Terraform Variable Names Documentation](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>What is the Terraform style convention for indenting a nesting level compared to the one above it?</summary>

**Options:**

- **A.** With four spaces
- **B.** With a tab
- **C.** With three spaces
- **D.** With two spaces

**Answer:** **D.** With two spaces

**Explanation:**
The recommended style convention for Terraform code is to indent by **two spaces** for each nesting level. This helps maintain consistency across configuration files and improves readability. Tabs, four spaces, or other styles are discouraged but not technically invalid.

**Reference:**
[Terraform Style Conventions Documentation](https://developer.hashicorp.com/terraform/language/syntax/style)

</details>

<details>
<summary>HashiCorp Configuration Language (HCL) supports user-defined functions. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
HCL does not support user-defined functions. It includes a set of built-in functions that allow transformation and combination of values, but it does not permit creating custom functions by users. Users can only use the predefined functions provided by Terraform.

**Reference:**
[HCL Functions Documentation](https://developer.hashicorp.com/terraform/language/functions)

</details>

<details>
<summary>Which of the following arguments are required when declaring a Terraform output?</summary>

**Options:**

- **A.** sensitive
- **B.** description
- **C.** default
- **D.** value

**Answer:** **D.** value

**Reference:**
[Terraform Output Values Documentation](https://developer.hashicorp.com/terraform/language/values/outputs)

</details>

<details>
<summary>How would you reference the Volume IDs associated with the `ebs_block_device` blocks in this configuration?</summary>

**Configuration:**
```hcl
resource "aws_instance" "example" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"

  ebs_block_device {
    device_name = "sda2"
    volume_size = 16
  }

  ebs_block_device {
    device_name = "sda3"
    volume_size = 20
  }
}
```

**Options:**

- **A.** aws_instance.example.ebs_block_device.[*].volume_id
- **B.** aws_instance.example.ebs_block_device.volume_id
- **C.** aws_instance.example.ebs_block_device[sda2, sda3].volume_id
- **D.** aws_instance.example.ebs_block_device.*.volume_id

**Answer:** **D.** aws_instance.example.ebs_block_device.*.volume_id

**Explanation:**
Repeated nested blocks are exposed as a list of objects, so you need a splat expression to project
one attribute out of every element. Option A is invalid because a `.` cannot precede `[*]`.
Option C is not valid Terraform indexing syntax.

Both splat forms work here:
- Legacy attribute-only splat: `aws_instance.example.ebs_block_device.*.volume_id`
- Modern full splat: `aws_instance.example.ebs_block_device[*].volume_id`

Prefer the `[*]` form in new code; the `.*.` form is retained for compatibility with Terraform 0.11
configurations.

**Reference:**
[Splat Expressions](https://developer.hashicorp.com/terraform/language/expressions/splat)

</details>

<details>
<summary>Which type of block fetches or computes information for use elsewhere in a Terraform configuration?</summary>

**Options:**

- **A.** provider
- **B.** resource
- **C.** local
- **D.** data

**Answer:** **D.** data

**Reference:**
[Terraform Data Sources Documentation](https://developer.hashicorp.com/terraform/language/data-sources)

</details>

<details>
<summary>Which Terraform collection type should you use to store key/value pairs?</summary>

**Options:**

- **A.** tuple
- **B.** set
- **C.** map
- **D.** list

**Answer:** **C.** map

**Reference:**
[Terraform Data Types](https://developer.hashicorp.com/terraform/language/expressions/types)

</details>

<details>
<summary>You're writing a Terraform configuration that needs to read input from a local file called `id_rsa.pub`. Which built-in Terraform function can you use to import the file's contents as a string?</summary>

**Options:**

- **A.** fileset("id_rsa.pub")
- **B.** filebase64("id_rsa.pub")
- **C.** templatefile("id_rsa.pub")
- **D.** file("id_rsa.pub")

**Answer:** **D.** file("id_rsa.pub")

</details>

<details>
<summary>You can reference a resource created with `for_each` using a Splat (*) expression.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>How would you reference an attribute from the vsphere_datacenter data source for use with the datacenter_id argument within the vsphere_folder resource in the following configuration?</summary>

**Configuration:**
```hcl
data "vsphere_datacenter" "dc" {
  name = "my-datacenter"
}

resource "vsphere_folder" "folder" {
  path          = "terraform-test-folder"
  type          = "vm"
  datacenter_id = _______________
}
```

**Options:**

- **A.** data.dc.id
- **B.** data.vsphere_datacenter.dc
- **C.** vsphere_datacenter.dc.id
- **D.** data.vsphere_datacenter.dc.id

**Answer:** **D.** data.vsphere_datacenter.dc.id

**Explanation:**
Data sources are referenced as `data.<TYPE>.<NAME>.<ATTRIBUTE>`. Omitting the `data.` prefix
(option C) would refer to a managed resource of that type, which does not exist here.

**Reference:**
[Data Sources](https://developer.hashicorp.com/terraform/language/data-sources)

</details>

<details>
<summary>You want to tag multiple resources with a string that is a combination of a generated random_id and a variable. How should you use the same value in all these resources without repeating the random_id and variable in each resource?</summary>

**Options:**

- **A.** Local values
- **B.** Data source
- **C.** Modules
- **D.** Outputs

**Answer:** **A.** Local values

</details>

<details>
<summary>You have a list of numbers that represents the number of free CPU cores on each virtual cluster: `numcpus = [ 18, 3, 7, 11, 2 ]`. What Terraform function could you use to select the largest number from the list?</summary>

**Options:**

- **A.** max(numcpus)
- **B.** ceil(numcpus)
- **C.** top(numcpus)
- **D.** high[numcpus]

**Answer:** **A.** max(numcpus)

</details>

<details>
<summary>Which of the following is not a valid Terraform variable type?</summary>

**Options:**

- **A.** list
- **B.** map
- **C.** array
- **D.** string

**Answer:** **C.** array

</details>

<details>
<summary>You want to define a single input variable to capture configuration values for a server. The values must represent memory as a number, and the server name as a string. Which variable type could you use for this input?</summary>

**Options:**

- **A.** List
- **B.** Object
- **C.** Map
- **D.** Terraform does not support complex input variables of different types

**Answer:** **B.** Object

</details>


## Resources, Meta-Arguments and Provisioners

<details>
<summary>You run a local-exec provisioner in a null resource called null_resource.run_script and realize that you need to rerun the script. Which of the following commands would you use first?</summary>

**Options:**

- **A.** terraform taint null_resource.run_script
- **B.** terraform apply -target=null_resource.run_script
- **C.** terraform validate null_resource.run_script
- **D.** terraform plan -target=null_resource.run_script

**Answer:** **A.** terraform taint null_resource.run_script

**Explanation:**
Provisioners run only when the resource is created. Because nothing in the configuration changed,
`terraform apply -target=...` produces an empty plan and the script never reruns. You must first
mark the resource for replacement, then apply. `terraform taint` does that in the state file.

On Terraform 0.15.2 and later, `terraform taint` is deprecated. The current one-step equivalent is:

```bash
terraform apply -replace="null_resource.run_script"
```

**Reference:**
[The -replace option](https://developer.hashicorp.com/terraform/cli/commands/plan#replace-address)

</details>

<details>
<summary>Which provisioner invokes a process on the resource created by Terraform?</summary>

**Options:**

- **A.** remote-exec
- **B.** null-exec
- **C.** local-exec
- **D.** file

**Answer:** **A.** remote-exec

**Explanation:**
The `remote-exec` provisioner allows Terraform to execute scripts or commands on a remote resource, such as a newly created virtual machine, after it has been provisioned. This is useful for performing post-provisioning tasks like software installation or configuration.

**Reference:**
[Terraform Remote-Exec Provisioner Documentation](https://developer.hashicorp.com/terraform/language/resources/provisioners/remote-exec)

</details>

<details>
<summary>A Terraform provisioner must be nested inside a resource configuration block.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

**Explanation:**
Most provisioners in Terraform require access to the remote resource (typically using SSH or WinRM protocols) and must be defined within a resource block. Provisioners enable you to execute scripts or perform configuration tasks on the resources after they are created. Additionally, the resource block often includes a nested connection block to specify details about how Terraform communicates with the resource.

**Reference:**
[Terraform Provisioners Documentation](https://developer.hashicorp.com/terraform/language/resources/provisioners/connection)

</details>

<details>
<summary>What is one disadvantage of using dynamic blocks in Terraform?</summary>

**Options:**

- **A.** They cannot be used to loop through a list of values
- **B.** Dynamic blocks can construct repeatable nested blocks
- **C.** They make configuration harder to read and understand
- **D.** Terraform will run more slowly

**Answer:** **C.** They make configuration harder to read and understand

**Explanation:**
Dynamic blocks are a powerful feature in Terraform that allow you to generate nested blocks programmatically, typically by looping through a list of values. However, their main disadvantage is that they can reduce the readability and clarity of the configuration, especially for users unfamiliar with the `dynamic` syntax. Clear and readable configurations are generally preferred for collaboration and maintainability.

**Why the other options are wrong:**
- **A.** Dynamic blocks can absolutely be used to loop through a list of values, which is one of their primary use cases.
- **B.** This statement is true, but it is not a disadvantage; it's a core feature of dynamic blocks.
- **D.** Using dynamic blocks does not have a significant impact on Terraform's runtime performance.

**Reference:**
[Terraform Dynamic Blocks Documentation](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)

</details>

<details>
<summary>You need to specify a dependency manually. What resource meta-parameter can you use to make sure Terraform respects the dependency?</summary>

**Answer:** depends_on

**Explanation:**
The `depends_on` meta-parameter allows you to explicitly specify a dependency between resources in Terraform. This ensures that Terraform respects the order of operations by waiting for the dependent resource to finish its creation, update, or destruction before proceeding. It is useful in scenarios where Terraform might not automatically infer dependencies.

**Example Usage:**
```hcl
resource "aws_instance" "example" {
  # Resource configuration
}

resource "aws_eip" "example" {
  depends_on = [aws_instance.example]
  # Ensures the EIP is associated only after the instance is created
}
```

</details>

<details>
<summary>What is the name assigned by Terraform to reference this resource?</summary>

**Terraform Configuration:**
```hcl
resource "azurerm_resource_group" "dev" {
  name     = "test"
  location = "westus"
}
```

**Options:**

- **A.** dev
- **B.** azurerm_resource_group
- **C.** azurerm
- **D.** test

**Answer:** **A.** dev

**Explanation:**
In Terraform, the name assigned to reference a resource is defined in the resource block after the resource type. In this case:

azurerm_resource_group is the resource type (Azure resource group).
dev is the local name (or resource name) that you use to reference this specific resource in the configuration.
To reference this resource elsewhere, you would use azurerm_resource_group.dev.

Incorrect Options:

- B. azurerm_resource_group: This is the type of the resource, not the specific name assigned to it.
- C. azurerm: This is part of the provider name but not relevant to the specific resource's reference name.
- D. test: This is the value of the name attribute, not the name for referencing the resource in the configuration.

</details>

<details>
<summary>How would you reference the "name" value of the second instance of this fictitious resource?</summary>

**Terraform Configuration:**
```hcl
resource "aws_instance" "web" {
  count = 2
  name  = "terraform-${count.index}"
}
```

**Options:**

- **A.** element(aws_instance.web, 2)
- **B.** aws_instance.web[1].name
- **C.** aws_instance.web[1]
- **D.** aws_instance.web[2].name
- **E.** aws_instance.web.*.name

**Answer:** **B.** aws_instance.web[1].name

</details>

<details>
<summary>Terraform provisioners can be added to any resource block.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

**Reference:**
[Terraform Provisioners Documentation](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax)

</details>

<details>
<summary>Terraform can only manage resource dependencies if you set them explicitly using the `depends_on` argument. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Terraform automatically manages resource dependencies by analyzing the configuration and determining resource relationships based on references to other resources, data sources, or variables. The `depends_on` argument is optional and only used to explicitly define dependencies when Terraform cannot automatically infer them.

**Reference:**
[Terraform Resource Dependencies Documentation](https://developer.hashicorp.com/terraform/language/resources/behavior)

</details>

<details>
<summary>Terraform provisioners that require authentication can use the ______ block.</summary>

**Options:**

- **A.** connection
- **B.** credentials
- **C.** secrets
- **D.** ssh

**Answer:** **A.** connection

**Explanation:**
The `connection` block in Terraform is used for configuring the authentication settings required by provisioners. It typically includes details such as the type of connection (e.g., SSH or WinRM) along with the credentials (username, password, or private key) required to access the resource.

**Reference:**
[Terraform Provisioner Connection Settings Documentation](https://developer.hashicorp.com/terraform/language/resources/provisioners/connection)

</details>

<details>
<summary>What type of block is used to construct a collection of nested configuration blocks?</summary>

**Options:**

- **A.** for_each
- **B.** repeated
- **C.** nesting
- **D.** dynamic

**Answer:** **D.** dynamic

**Explanation:**
In Terraform, a `dynamic` block is used to create a collection of nested configuration blocks dynamically. This is particularly useful when the number of nested blocks or their content depends on external data. The `dynamic` block iterates over a collection and renders nested blocks based on its content.

**Reference:**
[Terraform Dynamic Blocks Documentation](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)

</details>

<details>
<summary>You need to deploy resources into two different cloud regions in the same Terraform configuration. What meta-argument do you need to configure in a resource block to deploy the resource to the `us-west-2` AWS region?</summary>

**Options:**

- **A.** alias = west
- **B.** provider = west
- **C.** provider = aws.west
- **D.** alias = aws.west

**Answer:** **C.** provider = aws.west

**Explanation:**
When using multiple provider configurations, the `alias` argument allows you to define alternate configurations for a single provider. To specify which provider configuration a resource should use, you must include the `provider` meta-argument in your resource block. In this case, `provider = aws.west` refers to the provider configuration with the `alias = "west"` (region `us-west-2`).

**Why the other options are wrong:**
- `A. alias = west`: The `alias` is defined in the provider block, not in the resource block.
- `B. provider = west`: This is incorrect syntax. The provider name must be prefixed (e.g., `aws.west`).
- `D. alias = aws.west`: The `alias` keyword cannot be used in a resource block—it is used only in provider configurations.

**Reference:**
[Terraform Multiple AWS Provider Configurations Documentation](https://developer.hashicorp.com/terraform/language/providers/configuration#multiple-provider-configurations)

</details>

<details>
<summary>As a member of the operations team, you need to run a script on a virtual machine created by Terraform. Which provisioner is best to use in your Terraform code?</summary>

**Options:**

- **A.** null-exec
- **B.** local-exec
- **C.** remote-exec
- **D.** file

**Answer:** **C.** remote-exec

**Reference:**
[Terraform Remote-Exec Provisioner Documentation](https://developer.hashicorp.com/terraform/language/resources/provisioners/remote-exec)

</details>

<details>
<summary>How does Terraform determine dependencies between resources?</summary>

**Options:**

- **A.** Terraform automatically builds a resource graph based on resources, provisioners, special meta-parameters, and the state file
- **B.** Terraform requires all dependencies between resources to be specified using the `depends_on` parameter
- **C.** Terraform requires resources in a configuration to be listed in the order they will be created to determine dependencies
- **D.** Terraform requires resource dependencies to be defined as modules and stored in order

**Answer:** **A.** Terraform automatically builds a resource graph based on resources, provisioners, special meta-parameters, and the state file

</details>

<details>
<summary>You need to write some Terraform code that adds 42 firewall rules to a security group. What can you use to avoid writing 42 different nested ingress config blocks by hand?</summary>

**Options:**

- **A.** A count loop
- **B.** A for block
- **C.** A for each block
- **D.** A dynamic block

**Answer:** **D.** A dynamic block

</details>

<details>
<summary>How would you reference the attribute "name" of this fictitious resource in HCL?</summary>

```hcl
resource "kubernetes_namespace" "example" {
  name = "test"
}
```

**Options:**

- **A.** resource.kubernetes_namespace.example.name
- **B.** kubernetes_namespace.test.name
- **C.** kubernetes_namespace.example.name
- **D.** data.kubernetes_namespace.name
- **E.** None of the above

**Answer:** **C.** kubernetes_namespace.example.name

</details>

<details>
<summary>If a Terraform creation-time provisioner fails, what will occur by default?</summary>

**Options:**

- **A.** The resource will not be affected, but the provisioner will need to be applied again
- **B.** The resource will be destroyed
- **C.** The resource will be marked as "tainted"
- **D.** Nothing, provisioners will not show errors in the command line

**Answer:** **C.** The resource will be marked as "tainted"

</details>

<details>
<summary>While deploying a virtual machine, the first launch user_data script fails due to a race condition with another resource deployed during the same Terraform run. What is the least disruptive method to correct the issue?</summary>

**Options:**

- **A.** Run terraform taint against the virtual machine's resource name, then terraform apply
- **B.** Restart the virtual machine from the cloud portal
- **C.** Run terraform apply again
- **D.** Run terraform destroy then terraform apply

**Answer:** **A.** Run terraform taint against the virtual machine's resource name, then terraform apply

</details>

<details>
<summary>You want to define multiple data disks as nested blocks inside the resource block for a virtual machine. What Terraform feature would help you define the blocks using the values in a variable?</summary>

**Options:**

- **A.** Local values
- **B.** Collection functions
- **C.** Dynamic blocks
- **D.** Count arguments

**Answer:** **C.** Dynamic blocks

</details>

<details>
<summary>How would you refer to the indexing instance from the below configuration?</summary>

**Configuration:**
```hcl
resource "aws_instance" "web" {
  ...
  for_each = {
    "terraform": "value1",
    "resource": "value2",
    "indexing": "value3",
    "example": "value4",
  }
}
```

**Options:**

- **A.** aws_instance["web"]["indexing"]
- **B.** aws_instance.web.indexing
- **C.** aws_instance-web["indexing"]
- **D.** aws_instance.web["indexing"]

**Answer:** **D.** aws_instance.web["indexing"]

</details>

<details>
<summary>Which provisioner invokes a process on the machine running Terraform?</summary>

**Options:**

- **A.** remote-exec
- **B.** file
- **C.** local-exec
- **D.** null-exec

**Answer:** **C.** local-exec

**Explanation:**
`local-exec` runs a command on the machine executing Terraform. `remote-exec` runs commands on the
remote resource that was just created, and `file` copies files to it. `null-exec` is not a
provisioner.

**Reference:**
[local-exec provisioner](https://developer.hashicorp.com/terraform/language/resources/provisioners/local-exec)

</details>

<details>
<summary>When using multiple configurations of the same Terraform provider, what meta-argument must be included in any non-default provider configurations?</summary>

**Options:**

- **A.** depends_on
- **B.** alias
- **C.** id
- **D.** name

**Answer:** **B.** alias

**Reference:**
[Terraform Provider Configuration](https://developer.hashicorp.com/terraform/language/providers/configuration)

</details>

<details>
<summary>What kind of configuration block will create an infrastructure object with settings specified within the block?</summary>

**Options:**

- **A.** provider
- **B.** state
- **C.** data
- **D.** resource

**Answer:** **D.** resource

</details>


## Modules and the Registry

<details>
<summary>What information does the public Terraform Module Registry automatically expose about published modules?</summary>

**Options:**

- **A.** Required input variables
- **B.** Optional input variables and default values
- **C.** Outputs
- **D.** All of the above
- **E.** None of the above

**Answer:** **D.** All of the above

**Explanation:**
The public Terraform Module Registry automatically exposes the following information about published modules:
- **Required input variables**: Variables that must be defined for the module to function.
- **Optional input variables and default values**: Variables with default values that can be overridden.
- **Outputs**: Values generated by the module, which can be used in other parts of the Terraform configuration.

These details help users understand how to use and integrate the module effectively.

</details>

<details>
<summary>Terraform can import modules from a number of sources – which of the following is not a valid source?</summary>

**Options:**

- **A.** FTP server
- **B.** GitHub repository
- **C.** Local path
- **D.** Terraform Module Registry

**Answer:** **A.** FTP server

**Explanation:**
Terraform supports importing modules from various sources, including:
- **GitHub repository:** Sources hosted on Git or other version control systems.
- **Local path:** Local files and directories.
- **Terraform Module Registry:** A centralized location for reusable Terraform modules.

However, Terraform does not support pulling modules from an **FTP server**, making it an invalid source.

</details>

<details>
<summary>Which of the following is the correct way to pass the value in the variable `num_servers` into a module with the input `servers`?</summary>

**Options:**

- **A.** servers = num_servers
- **B.** servers = variable.num_servers
- **C.** servers = var(num_servers)
- **D.** servers = var.num_servers

**Answer:** **D.** servers = var.num_servers

**Explanation:**
- **`servers = var.num_servers`**: In Terraform, variables are referenced using the `var.` prefix, followed by the variable name (`num_servers`). This is the correct syntax for passing a variable value to module inputs or other configuration blocks.

**Why the other options are wrong:**
- **A**: Directly referencing `num_servers` without the `var.` prefix is invalid in Terraform syntax.
- **B**: Using `variable.num_servers` is incorrect because `variable` is not the correct usage in this context for variables in Terraform.
- **C**: Syntax like `var(num_servers)` is not recognized in Terraform; parentheses are not used for variable referencing.

**Reference:**
[Terraform Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>When using a module block to reference a module stored on the public Terraform Module Registry, how do you specify version 1.0.0?</summary>

**Options:**

- **A.** Modules stored on the public Terraform Module Registry do not support versioning
- **B.** Append ?ref=v1.0.0 argument to the source path
- **C.** Add version = "1.0.0" attribute to module block
- **D.** Nothing - modules stored on the public Terraform Module Registry always default to version 1.0.0

**Answer:** **C.** Add version = "1.0.0" attribute to module block

**Explanation:**
When referencing modules stored on the public Terraform Module Registry (e.g., `hashicorp/consul/aws`), you specify the desired module version using the `version` argument in the module block. This ensures Terraform fetches and uses the correct version of the module, maintaining version control and consistency across deployments.

**Why the other options are wrong:**
- **A.** Modules in the public registry support versioning via the `version` attribute.
- **B.** While appending `?ref=v1.0.0` is commonly used with Git source URLs, it is not applicable for modules from the public Terraform Module Registry.
- **D.** Modules do not default to version 1.0.0 unless explicitly specified.

</details>

<details>
<summary>When you initialize Terraform, where does it cache modules from the public Terraform Module Registry?</summary>

**Options:**

- **A.** On disk in the /tmp directory
- **B.** In memory
- **C.** On disk in the .terraform sub-directory
- **D.** They are not cached

**Answer:** **C.** On disk in the .terraform sub-directory

**Reference:**
[Terraform Module Sources Documentation](https://developer.hashicorp.com/terraform/language/modules/sources)

</details>

<details>
<summary>Module variable assignments are inherited from the parent module and you do **not** need to explicitly set them. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Variables in a Terraform module must be explicitly set when the module is called. They are **not** automatically inherited from the parent module. If a module variable is not provided, and no default value is defined in the module, Terraform will throw an error requiring that value to be set.

**Reference:**
[Terraform Modules - Input Variables](https://developer.hashicorp.com/terraform/language/modules/syntax#input-variables)

</details>

<details>
<summary>You have declared an input variable called `node_count` in your parent module. What must you do to pass the value to a child module in the configuration?</summary>

**Options:**

- **A.** Nothing, child modules inherit variables of the parent module
- **B.** Declare the variable in a terraform.tfvars file
- **C.** Declare a node_count input variable for the child module and set it in the module block
- **D.** Reference var.node_count directly inside the child module

**Answer:** **C.** Declare a node_count input variable for the child module and set it in the module block

**Explanation:**
Variable scope does not cross module boundaries. The child module must declare its own `variable`
block, and the calling module must pass the value explicitly:

```hcl
module "cluster" {
  source     = "./modules/cluster"
  node_count = var.node_count
}
```

**Reference:**
[Module input variables](https://developer.hashicorp.com/terraform/language/modules/syntax#input-variables)

</details>

<details>
<summary>If a module declares a variable with a default, that variable must also be defined within the module. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Reference:**
[Terraform Input Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>In the below configuration, how would you reference the module output `vpc_id`?</summary>

**Configuration:**
```hcl
module "vpc" {
  source = "terraform-and-modules/vpc/aws"
  cidr = "10.0.0.0/16"
  name = "test-vpc"
}
```

**Answer:** module.vpc.vpc_id

</details>

<details>
<summary>A module can always refer to all variables declared in its parent module. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Reference:**
[Terraform Modules Documentation](https://developer.hashicorp.com/terraform/language/modules/syntax#input-variables)

</details>

<details>
<summary>All modules published on the official Terraform Module Registry have been verified by HashiCorp. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Reference:**
[Terraform Module Registry Documentation](https://registry.terraform.io/)

</details>

<details>
<summary>How do you specify a module's version when publishing it to the public Terraform Module Registry?</summary>

**Options:**

- **A.** The module's configuration page on the Terraform Module Registry
- **B.** Terraform Module Registry does not support versioning modules
- **C.** The release tags in the associated repo
- **D.** The module's Terraform code

**Answer:** **C.** The release tags in the associated repo

**Reference:**
[Terraform Module Registry Versioning Documentation](https://developer.hashicorp.com/terraform/registry/modules/publish)

</details>

<details>
<summary>You are using a networking module in your Terraform configuration with the name label `my_network`. When running `terraform validate`, you encounter an error: "Reference to undeclared output value". What must you do to successfully retrieve this value from your networking module?</summary>

**Options:**

- **A.** Define the attribute vnet_id as a variable in the networking module
- **B.** Change the referenced value to module.my_network.outputs.vnet_id
- **C.** Define the attribute vnet_id as an output in the networking module
- **D.** Change the referenced value to my_network.outputs.vnet_id

**Answer:** **C.** Define the attribute vnet_id as an output in the networking module

**Reference:**
[Terraform Module Output Values Documentation](https://developer.hashicorp.com/terraform/language/values/outputs)

</details>

<details>
<summary>Which of the following statements about Terraform modules is **not** true?</summary>

**Options:**

- **A.** Modules must be publicly accessible
- **B.** Modules can be called multiple times
- **C.** A module is a container for one or more resources
- **D.** Modules can call other modules

**Answer:** **A.** Modules must be publicly accessible

**Reference:**
[Terraform Modules Overview](https://developer.hashicorp.com/terraform/language/modules)

</details>

<details>
<summary>Which of the following is **not** a valid source path for specifying a module?</summary>

**Options:**

- **A.** source = "./module?version=v1.0.0"
- **B.** source = "github.com/hashicorp/example?ref=v1.0.0"
- **C.** source = "./module"
- **D.** source = "hashicorp/consul/aws"

**Answer:** **A.** source = "./module?version=v1.0.0"

</details>

<details>
<summary>Which of the following statements about local modules is incorrect?</summary>

**Options:**

- **A.** Local modules are not cached by the terraform init command
- **B.** Local modules are sourced from a directory on disk
- **C.** Local modules support versions
- **D.** All of the above (all statements above are incorrect)
- **E.** None of the above (all statements above are correct)

**Answer:** **C.** Local modules support versions

</details>

<details>
<summary>Which is the best way to specify a tag of `v1.0.0` when referencing a module stored in Git?</summary>

**Options:**

- **A.** Append `?ref=v1.0.0` argument to the source path
- **B.** Add `version = "1.0.0"` parameter to module block
- **C.** Nothing - modules stored on Git always default to version 1.0.0
- **D.** Modules stored on GitHub do not support versioning

**Answer:** **A.** Append `?ref=v1.0.0` argument to the source path

</details>

<details>
<summary>`terraform init` retrieves the source code for all referenced modules.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>Which of the following locations can Terraform use as a private source for modules? (Choose two.)</summary>

**Options:**

- **A.** Internally hosted SCM (Source Control Manager) platform
- **B.** Public Terraform Module Registry
- **C.** Private repository on GitHub
- **D.** Public repository on GitHub

**Answer:** **A.** Internally hosted SCM (Source Control Manager) platform, **C.** Private repository on GitHub

</details>

<details>
<summary>Open source Terraform can only import publicly-accessible and open-source modules.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>When using a module from the public Terraform Module Registry, the following parameters are required attributes in the module block. (Choose two.)</summary>

**Options:**

- **A.** Each of the module's required inputs
- **B.** The module's source address
- **C.** Terraform Module Registry account token
- **D.** Each of the module's dependencies (example: submodules)
- **E.** The version of the module

**Answer:** **B.** The module's source address, **E.** The version of the module

</details>

<details>
<summary>Module version is required to reference a module on the Terraform Module Registry.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>The public Terraform Module Registry is free to use.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>Which of the following module source paths does not specify a remote module?</summary>

**Options:**

- **A.** source = "./modules/consul"
- **B.** source = "git@github.com:hashicorp/example.git"
- **C.** source = "github.com/hashicorp/example"
- **D.** source = "github.com/hashicorp/consul/aws"

**Answer:** **A.** source = "./modules/consul"

</details>

<details>
<summary>Variables declared within a module are accessible outside of the module.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Which method for sharing Terraform configurations fulfills the following criteria?</summary>

**Criteria:**
1. Keeps the configurations confidential within your organization
2. Supports Terraform's semantic version constraints
3. Provides a browsable directory

**Options:**

- **A.** Generic git repository
- **B.** Public Terraform Module Registry
- **C.** HCP Terraform (Terraform Cloud) private registry
- **D.** Subfolder within a workspace

**Answer:** **C.** HCP Terraform (Terraform Cloud) private registry

**Explanation:**
Only the private registry satisfies all three criteria at once. The public registry fails the
confidentiality requirement. A generic Git repository supports version constraints through tags but
offers no browsable module directory with documented inputs and outputs. A subfolder in a workspace
supports neither versioning nor discovery.

**Reference:**
[Private registry](https://developer.hashicorp.com/terraform/cloud-docs/registry)

</details>

<details>
<summary>From which of these sources can Terraform get modules?</summary>

**Options:**

- **A.** Local path
- **B.** GitHub Repository
- **C.** Terraform Module Registry
- **D.** All of the above

**Answer:** **D.** All of the above

</details>

<details>
<summary>How would you expose a value that a child module computes so that the calling module can use it?</summary>

**Options:**

- **A.** Declare the output in the root configuration
- **B.** Declare the output in the child module
- **C.** Declare the output in both the root and child modules
- **D.** None of the above

**Answer:** **B.** Declare the output in the child module

**Explanation:**
A child module publishes values through its own `output` blocks. The caller then reads them as
`module.<NAME>.<OUTPUT>`. That is all that is required for the parent configuration to *use* the
value.

Printing the value in the CLI output of `terraform apply` is a separate requirement: the root
module must also declare an output that re-exports it. See the companion question below.

**Reference:**
[Module output values](https://developer.hashicorp.com/terraform/language/values/outputs)

</details>

<details>
<summary>Any user can publish modules to the public Terraform Module Registry.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>Which argument helps prevent unexpected updates when calling Terraform Registry modules?</summary>

**Options:**

- **A.** count
- **B.** source
- **C.** version
- **D.** lifecycle

**Answer:** **C.** version

**Explanation:**
The `version` argument is used to specify the module version when pulling from the Terraform Registry. By locking the version, you can prevent Terraform from automatically using newer versions of the module, which may introduce unexpected changes to your infrastructure. This ensures consistency and avoids unintended updates during deployments.

</details>

<details>
<summary>How would you surface a child module's returned values in the Terraform CLI output?</summary>

**Options:**

- **A.** Declare the output in the root configuration
- **B.** Declare the output in the child module
- **C.** Declare the output in both the root and child module
- **D.** None of the above

**Answer:** **C.** Declare the output in both the root and child module

**Explanation:**
Terraform only prints outputs declared in the **root** module. A child module's outputs are
consumable by its caller but are not printed, so you need both halves:

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.this.id
}

# root outputs.tf
output "vpc_id" {
  value = module.vpc.vpc_id
}
```

Contrast this with the previous question: declaring the output in the child alone is enough to
*reference* the value, but not to *display* it.

**Reference:**
[Output values](https://developer.hashicorp.com/terraform/language/values/outputs)

</details>

<details>
<summary>The Terraform CLI will print output values from a child module after running `terraform apply`.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>


## State, Backends and Locking

<details>
<summary>One remote backend configuration always maps to a single remote workspace.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
A backend configuration defines how Terraform stores state, but the selected workspace identifies
the particular state snapshot within that backend. A backend can therefore map multiple workspace
names to separate state objects. With the local backend, `default` uses `terraform.tfstate` and
non-default workspaces use files under `terraform.tfstate.d/`; remote mapping is backend-specific.
HCP Terraform workspaces also each have their own state and run settings and should not be confused
with CLI workspaces.

**Reference:**
[Terraform workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)

</details>

<details>
<summary>Terraform variables and outputs that set the "description" argument will store that description in the state file.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
The "description" argument set in Terraform variables or outputs is purely informational and is not stored in the state file. Terraform state files only contain essential resource attributes and metadata required for infrastructure management, not descriptive information.

</details>

<details>
<summary>When should you use the force-unlock command?</summary>

**Options:**

- **A.** You see a status message that you cannot acquire the lock
- **B.** You have a high priority change
- **C.** Automatic unlocking failed
- **D.** apply failed due to a state lock

**Answer:** **C.** Automatic unlocking failed

**Explanation:**
The `terraform force-unlock` command is used to manually unlock a Terraform state that is locked. This is typically required when automatic unlocking fails due to unexpected scenarios, such as a crash or a stale lock held by a previous operation. Use this command cautiously to avoid corrupting the state file.

**Reference:**
[Terraform Force Unlock Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/force-unlock)

</details>

<details>
<summary>What does the default "local" Terraform backend store?</summary>

**Options:**

- **A.** tfplan files
- **B.** Terraform binary
- **C.** Provider plugins
- **D.** State file

**Answer:** **D.** State file

**Explanation:**
The default "local" backend in Terraform is responsible for storing the state file on the local filesystem. The state file tracks the current state of the infrastructure managed by Terraform and is critical for operations like detecting changes and applying updates. Additionally, the local backend locks the state during updates using system APIs to prevent concurrent modifications.

**Reference:**
[Terraform Local Backend Documentation](https://developer.hashicorp.com/terraform/language/backend/local)

</details>

<details>
<summary>Where does the Terraform local backend store its state?</summary>

**Options:**

- **A.** In the /tmp directory
- **B.** In the terraform file
- **C.** In the terraform.tfstate file
- **D.** In the user's terraform.state file

**Answer:** **C.** In the terraform.tfstate file

**Explanation:**
The local backend stores the Terraform state file in a file named `terraform.tfstate` on the local filesystem. This file represents the current state of the infrastructure managed by Terraform. The state file is crucial for tracking resources, as it allows Terraform to know which resources already exist and whether changes need to be applied during future runs.

**Why the other options are wrong:**
- **A.** The `/tmp` directory is not used for state storage by default in Terraform.
- **B.** Terraform configurations are written in `.tf` files, but the state is not stored in these files.
- **D.** The state file is named `terraform.tfstate`, not `terraform.state`.

**Reference:**
[Terraform Local Backend Documentation](https://developer.hashicorp.com/terraform/language/backend/local)

</details>

<details>
<summary>Where in your Terraform configuration do you specify a state backend?</summary>

**Options:**

- **A.** The terraform block
- **B.** The resource block
- **C.** The provider block
- **D.** The data source block

**Answer:** **A.** The terraform block

**Explanation:**
State backends in Terraform are configured within the top-level `terraform` block of your configuration file. The `backend` block allows you to specify how and where the state data is stored (e.g., locally, remotely on S3, Consul, etc.).

**Example Configuration:**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "path/to/my/state"
    region         = "us-west-2"
  }
}
```

</details>

<details>
<summary>What is the name of the default file where Terraform stores the state?</summary>

**Answer:** terraform.tfstate

**Reference:**
[Terraform State Documentation](https://developer.hashicorp.com/terraform/language/state)

</details>

<details>
<summary>All standard backend types support state storage, locking, and remote operations like plan, apply, and destroy.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Your DevOps team is currently using the local backend for your Terraform configuration. You would like to move to a remote backend to begin storing the state file in a central location. Which of the following backends would not work?</summary>

**Options:**

- **A.** Amazon S3
- **B.** Artifactory
- **C.** Git
- **D.** Terraform Cloud

**Answer:** **C.** Git

</details>

<details>
<summary>Which backend does the Terraform CLI use by default?</summary>

**Options:**

- **A.** Terraform Cloud
- **B.** Consul
- **C.** Remote
- **D.** Local

**Answer:** **D.** Local

**Reference:**
[Terraform Backend Configuration Documentation](https://developer.hashicorp.com/terraform/language/backend)

</details>

<details>
<summary>What feature stops multiple admins from changing the Terraform state at the same time?</summary>

**Options:**

- **A.** Version control
- **B.** Backend types
- **C.** Provider constraints
- **D.** State locking

**Answer:** **D.** State locking

**Explanation:**
State locking ensures that only one operation modifies or accesses the state at a time. This prevents multiple admins or processes from making changes simultaneously, which could corrupt or disrupt the state file.

**Reference:**
[Terraform State Locking Documentation](https://blog.gruntwork.io/how-to-manage-terraform-state-28f5697e68fa)

</details>

<details>
<summary>When using Terraform to deploy resources into Azure, which scenarios are true regarding state files? (Choose two.)</summary>

**Options:**

- **A.** When a change is made to the resources via the Azure Cloud Console, the changes are recorded in a new state file
- **B.** When a change is made to the resources via the Azure Cloud Console, Terraform will update the state file to reflect them during the next plan or apply
- **C.** When a change is made to the resources via the Azure Cloud Console, the current state file will not be updated
- **D.** When a change is made to the resources via the Azure Cloud Console, the changes are recorded in the current state file

**Answer:** **B.** When a change is made to the resources via the Azure Cloud Console, Terraform will update the state file to reflect them during the next plan or apply, **C.** When a change is made to the resources via the Azure Cloud Console, the current state file will not be updated

**Explanation:**
- **B:** Terraform detects changes made to resources outside of Terraform (e.g., via the Azure Cloud Console) during the next `plan` or `apply` command and updates the state file accordingly.
- **C:** The state file does not automatically update when changes are made outside of Terraform. Until a plan or apply is run, the current state file remains outdated.

**Why the other options are wrong:**
- **A:** Terraform does not create a new state file for changes made outside of Terraform. It uses the existing state file and updates it after detecting changes.
- **D:** Changes are not automatically reflected in the current state file when made outside of Terraform.

**Reference:**
[Terraform State Documentation](https://developer.hashicorp.com/terraform/language/state)

</details>

<details>
<summary>What does state locking accomplish?</summary>

**Options:**

- **A.** Copies the state file from memory to disk
- **B.** Encrypts any credentials stored within the state file
- **C.** Blocks Terraform commands from modifying the state file
- **D.** Prevents accidental deletion of the state file

**Answer:** **C.** Blocks Terraform commands from modifying the state file

**Reference:**
[Terraform State Locking Documentation](https://developer.hashicorp.com/terraform/language/state/locking)

</details>

<details>
<summary>When you use a remote backend that needs authentication, HashiCorp recommends that you:</summary>

**Options:**

- **A.** Use partial configuration to load the authentication credentials outside of the Terraform code
- **B.** Push your Terraform configuration to an encrypted git repository
- **C.** Write the authentication credentials in the Terraform configuration files
- **D.** Keep the Terraform configuration files in a secret store

**Answer:** **A.** Use partial configuration to load the authentication credentials outside of the Terraform code

**Reference:**
[Terraform Backend Configuration Documentation](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)

</details>

<details>
<summary>You must initialize a Terraform backend before it can be configured. True or False?</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Reference:**
[Terraform Backend Configuration Documentation](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)

</details>

<details>
<summary>A Terraform backend determines how Terraform loads state and stores updates when you execute ___________.</summary>

**Options:**

- **A.** apply
- **B.** taint
- **C.** destroy
- **D.** All of the above
- **E.** None of the above

**Answer:** **D.** All of the above

**Reference:**
[Terraform Backend Documentation](https://developer.hashicorp.com/terraform/language/settings/backends)

</details>

<details>
<summary>Terraform variable names are saved in the state file.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Once you configure a new Terraform backend with the `terraform backend` block, which command(s) should you use to migrate the state file?</summary>

**Options:**

- **A.** terraform apply
- **B.** terraform push
- **C.** terraform destroy, then terraform apply
- **D.** terraform init

**Answer:** **D.** terraform init

</details>

<details>
<summary>Which are forbidden actions when the Terraform state file is locked? (Choose three.)</summary>

**Options:**

- **A.** terraform destroy
- **B.** terraform fmt
- **C.** terraform state list
- **D.** terraform apply
- **E.** terraform plan

**Answer:** **A.** terraform destroy, **D.** terraform apply, **E.** terraform plan

</details>

<details>
<summary>Changing the Terraform backend from the default "local" backend to a different one after doing your first `terraform apply` is:</summary>

**Options:**

- **A.** Mandatory
- **B.** Optional
- **C.** Impossible
- **D.** Discouraged

**Answer:** **B.** Optional

</details>

<details>
<summary>Why does this backend configuration not follow best practices?</summary>

**Configuration:**
```hcl
terraform {
  backend "s3" {
    bucket     = "tf-state-prod"
    key        = "network/terraform.tfstate"
    region     = "us-east-1"
    access_key = "AKIAIOSFODNN7EXAMPLE"
    secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  }
}
```

**Options:**

- **A.** You should not store credentials in Terraform configuration
- **B.** You should use the local backend whenever possible
- **C.** An alias meta-argument should be included in backend blocks whenever possible
- **D.** The backend configuration should contain multiple credentials so that more than one user can execute terraform plan and terraform apply

**Answer:** **A.** You should not store credentials in Terraform configuration

**Explanation:**
Backend blocks are committed to version control like any other configuration, so hard-coded keys
leak the moment the repository is shared. Supply them instead through environment variables
(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`), a named credentials profile, an instance/IRSA role,
or partial backend configuration passed with `terraform init -backend-config=...`.

Backend blocks also do not accept the `alias` meta-argument, and a configuration can only have one
backend.

**Reference:**
[Partial backend configuration](https://developer.hashicorp.com/terraform/language/backend#partial-configuration)

</details>

<details>
<summary>You need to migrate a workspace to use a remote backend. After updating your configuration, what command do you run to perform the migration?</summary>

**Answer:** terraform init

</details>

<details>
<summary>You can access state stored with the local backend by using the terraform_remote_state data source.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>You decide to move a Terraform state file to Amazon S3 from another location. You write the code below into a file called backend.tf. Which command will migrate your current state file to the new S3 remote backend?</summary>

**Options:**

- **A.** terraform state
- **B.** terraform init
- **C.** terraform refresh
- **D.** terraform push

**Answer:** **B.** terraform init

</details>

<details>
<summary>What is a key benefit of the Terraform state file?</summary>

**Options:**

- **A.** A state file can be used to schedule recurring infrastructure tasks
- **B.** A state file represents a source of truth for resources provisioned with a public cloud console
- **C.** A state file represents the desired state expressed by the Terraform code files
- **D.** A state file represents a source of truth for resources provisioned with Terraform

**Answer:** **D.** A state file represents a source of truth for resources provisioned with Terraform

</details>

<details>
<summary>Define the purpose of state in Terraform.</summary>

**Options:**

- **A.** State is used to map real-world resources to your configuration and keep track of metadata
- **B.** State is a method of codifying the dependencies of related resources
- **C.** State is used to enforce resource configurations that relate to compliance policies
- **D.** State is used to store variables and quickly reuse existing code

**Answer:** **A.** State is used to map real-world resources to your configuration and keep track of metadata

</details>

<details>
<summary>You want to share Terraform state with your team, store it securely, and provide state locking. How would you do this? (Choose three.)</summary>

**Options:**

- **A.** Using the remote Terraform backend with Terraform Cloud / Terraform Enterprise
- **B.** Using the local backend
- **C.** Using the s3 terraform backend. The dynamodb_field option is not needed
- **D.** Using an s3 terraform backend with an appropriate IAM policy and dynamodb_field option configured
- **E.** Using the consul Terraform backend

**Answer:** **A.** Using the remote Terraform backend with Terraform Cloud / Terraform Enterprise, **D.** Using an s3 terraform backend with an appropriate IAM policy and dynamodb_field option configured, **E.** Using the consul Terraform backend

</details>

<details>
<summary>Before you can use Terraform’s remote backend, you must first execute `terraform init`.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>________ backends support state locking.</summary>

**Options:**

- **A.** Some
- **B.** No
- **C.** Only local
- **D.** All

**Answer:** **A.** Some

</details>

<details>
<summary>When using a remote backend or Terraform Cloud integration, where does Terraform save resource state?</summary>

**Options:**

- **A.** On the disk
- **B.** In memory
- **C.** In an environment variable
- **D.** In the remote backend or Terraform Cloud

**Answer:** **D.** In the remote backend or Terraform Cloud

</details>

<details>
<summary>Which of these actions will prevent two Terraform runs from changing the same state file at the same time?</summary>

**Options:**

- **A.** Refresh the state after running Terraform
- **B.** Delete the state before running Terraform
- **C.** Configure state locking for your state backend
- **D.** Run Terraform with parallelism set to 1

**Answer:** **C.** Configure state locking for your state backend

</details>

<details>
<summary>Which of these is **not** a benefit of remote state?</summary>

**Options:**

- **A.** Keeping unencrypted sensitive information off disk
- **B.** Easily share reusable code modules
- **C.** Working in a team
- **D.** Delegate output to other teams

**Answer:** **B.** Easily share reusable code modules

**Reference:**
[Terraform Remote State](https://developer.hashicorp.com/terraform/language/state/remote)

</details>

<details>
<summary>How is the HCP Terraform (Terraform Cloud) integration different from other state backends such as S3, Consul, etc.?</summary>

**Options:**

- **A.** It can execute Terraform runs on dedicated infrastructure in HCP Terraform
- **B.** It does not show the output of a terraform apply locally
- **C.** It is only available to paying customers
- **D.** All of the above

**Answer:** **A.** It can execute Terraform runs on dedicated infrastructure in HCP Terraform

**Explanation:**
S3, Consul and the other standard backends only store state. The HCP Terraform integration (the
`cloud` block, previously the `remote` backend) additionally performs *remote operations*: `plan`
and `apply` execute on HashiCorp-managed or self-hosted agents, with centralised variables, run
history and policy enforcement. Output is still streamed to your local terminal, and a free tier
exists, so B and C are wrong.

**Reference:**
[The cloud block](https://developer.hashicorp.com/terraform/cli/cloud/settings)

</details>

<details>
<summary>If you don't use the local backend, where does Terraform save resource state?</summary>

**Options:**

- **A.** In the remote backend or Terraform Cloud
- **B.** On the disk
- **C.** In memory
- **D.** In an environment variable

**Answer:** **A.** In the remote backend or Terraform Cloud

</details>


## Outside the Core Workflow: Import, State CLI, Replace, Debug

<details>
<summary>You have deployed a new web app with a public IP address on a cloud provider. However, you did not create any outputs for your code. What is the best method to quickly find the IP address of the resource you deployed?</summary>

**Options:**

- **A.** Run terraform output ip_address to view the result
- **B.** In a new folder, use the terraform_remote_state data source to load in the state file, then write an output for each resource that you find in the state file
- **C.** Run terraform state list to find the name of the resource, then terraform state show to find the attributes including public IP address
- **D.** Run terraform destroy then terraform apply and look for the IP address in stdout

**Answer:** **C.** Run terraform state list to find the name of the resource, then terraform state show to find the attributes including public IP address

**Explanation:**
Using `terraform state list` allows you to identify all resources managed in the current state file. Once you find the name of the desired resource, you can run `terraform state show` to inspect its attributes, including the public IP address. This method avoids unnecessary operations like destroying or reapplying resources and enables quick discovery of resource details.

</details>

<details>
<summary>What is not processed when running a terraform refresh?</summary>

**Options:**

- **A.** State file
- **B.** Configuration file
- **C.** Credentials
- **D.** Cloud provider

**Answer:** **B.** Configuration file

**Explanation:**
When running `terraform refresh`, Terraform updates the state file to match the actual infrastructure by querying the cloud provider or other resource APIs. The configuration file is not processed during this operation, as the refresh only deals with the state file and actual infrastructure resources.

</details>

<details>
<summary>You have provisioned some virtual machines (VMs) on Google Cloud Platform (GCP) using the gcloud command-line tool. However, you are standardizing with Terraform and want to manage these VMs using Terraform instead. What are the two things you must do to achieve this? (Choose two.)</summary>

**Options:**

- **A.** Provision new VMs using Terraform with the same VM names
- **B.** Use the terraform import command for the existing VMs
- **C.** Write Terraform configuration for the existing VMs
- **D.** Run the terraform import-gcp command

**Answer:** **B.** Use the terraform import command for the existing VMs, **C.** Write Terraform configuration for the existing VMs

**Explanation:**
To bring existing infrastructure under Terraform's management without recreating it:
1. Use the `terraform import` command to manually import the existing resources (e.g., VMs) into Terraform's state file.
2. Write Terraform configuration that mirrors the current state of the resources. The configuration must define the same attributes and parameters for successful management after import.

Terraform does not automatically generate configuration files, so manual configuration writing is necessary.

**Reference:**
- [Terraform Import Command Documentation](https://developer.hashicorp.com/terraform/cli/import/usage)
- [Google Cloud and Terraform Documentation](https://cloud.google.com/docs/terraform)

</details>

<details>
<summary>Why would you use the terraform taint command?</summary>

**Options:**

- **A.** When you want to force Terraform to destroy a resource on the next apply
- **B.** When you want to force Terraform to destroy and recreate a resource on the next apply
- **C.** When you want Terraform to ignore a resource on the next apply
- **D.** When you want Terraform to destroy all the infrastructure in your workspace

**Answer:** **B.** When you want to force Terraform to destroy and recreate a resource on the next apply

**Explanation:**
The `terraform taint` command is used to manually mark a resource as tainted. A tainted resource will be destroyed and recreated on the next `terraform apply`. This is useful in cases where a resource needs to be replaced due to corruption, misconfiguration, or a manual override.

**Reference:**
[Terraform Taint Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/taint)

</details>

<details>
<summary>When you run `terraform taint` against a managed resource, Terraform immediately destroys and recreates the resource.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
`terraform taint` only edits the state file, marking the object for replacement. Nothing happens to
real infrastructure until the next `terraform apply`, which plans a destroy-and-create for that
address. The command is deprecated since Terraform 0.15.2 in favour of
`terraform apply -replace="ADDRESS"`.

**Reference:**
[terraform taint](https://developer.hashicorp.com/terraform/cli/commands/taint)

</details>

<details>
<summary>You want to know from which paths Terraform is loading providers referenced in your Terraform configuration (*.tf files). You need to enable debug messages to find this out. Which of the following would achieve this?</summary>

**Options:**

- **A.** Set the environment variable TF_LOG=TRACE
- **B.** Set verbose logging for each provider in your Terraform configuration
- **C.** Set the environment variable TF_VAR_log=TRACE
- **D.** Set the environment variable TF_LOG_PATH

**Answer:** **A.** Set the environment variable TF_LOG=TRACE

**Reference:**
[Terraform Environment Variables Documentation](https://developer.hashicorp.com/terraform/cli/config/environment-variables)

</details>

<details>
<summary>How is `terraform import` run?</summary>

**Options:**

- **A.** As a part of terraform init
- **B.** As a part of terraform plan
- **C.** As a part of terraform refresh
- **D.** By an explicit call
- **E.** All of the above

**Answer:** **D.** By an explicit call

</details>

<details>
<summary>A fellow developer on your team is asking for some help in refactoring their Terraform code. They need to tell Terraform to no longer manage a specific resource. What command should be used?</summary>

**Options:**

- **A.** terraform apply rm aws_instance.ubuntu[1]
- **B.** terraform state rm aws_instance.ubuntu[1]
- **C.** terraform plan rm aws_instance.ubuntu[1]
- **D.** terraform delete aws_instance.ubuntu[1]

**Answer:** **B.** terraform state rm aws_instance.ubuntu[1]

**Explanation:**
The `terraform state rm` command removes a resource from state without deleting the real object.
Terraform immediately stops managing it. Before running the command, confirm the active backend and
workspace, stop concurrent runs, back up state with `terraform state pull` to a restricted file,
and verify the exact address with `terraform state list`. Remove or change the corresponding
configuration too; otherwise a later apply can create a duplicate object.

**Reference:**
[Terraform State RM Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/state/rm)

</details>

<details>
<summary>What does `terraform import` allow you to do?</summary>

**Options:**

- **A.** Import a new Terraform module
- **B.** Use a state file to import infrastructure to the cloud
- **C.** Import provisioned infrastructure to your state file
- **D.** Import an existing state file to a new Terraform workspace

**Answer:** **C.** Import provisioned infrastructure to your state file

**Reference:**
[Terraform Import Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/import)

</details>

<details>
<summary>You have used Terraform to deploy a virtual machine and a database. You want to replace this virtual machine instance with an identical one without affecting the database. What is the best way to achieve this using Terraform?</summary>

**Options:**

- **A.** Use the terraform state rm command to remove the VM from the state file
- **B.** Mark the VM for replacement, then run terraform plan and terraform apply
- **C.** Run terraform apply without targeting the VM resource
- **D.** Delete the VM resource from your Terraform code, then run terraform apply

**Answer:** **B.** Mark the VM for replacement, then run terraform plan and terraform apply

**Explanation:**
Marking only the VM for replacement leaves every other resource, including the database,
untouched. On current Terraform this is a single command:

```bash
terraform apply -replace="aws_instance.vm"
```

The older equivalent was `terraform taint aws_instance.vm` followed by `terraform apply`; `taint`
has been deprecated since Terraform 0.15.2.

Option A only forgets the VM (it keeps running, unmanaged), and option D destroys it without
creating a replacement.

**Reference:**
[Force replacement of a resource](https://developer.hashicorp.com/terraform/cli/state/taint)

</details>

<details>
<summary>When do you need to explicitly execute a refresh-only run?</summary>

**Options:**

- **A.** Before every terraform plan
- **B.** Before every terraform apply
- **C.** Before every terraform import
- **D.** None of the above

**Answer:** **D.** None of the above

**Explanation:**
`terraform plan` and `terraform apply` refresh state automatically before building the plan, so a
separate refresh is not part of the normal workflow. You run `terraform apply -refresh-only`
deliberately, when you want to inspect and accept out-of-band drift as its own reviewable change,
or `-refresh=false` when you want to skip refreshing for speed.

**Reference:**
[terraform refresh](https://developer.hashicorp.com/terraform/cli/commands/refresh)

</details>

<details>
<summary>Which parameters does `terraform import` require? (Choose two.)</summary>

**Options:**

- **A.** Path
- **B.** Provider
- **C.** Resource ID
- **D.** Resource address

**Answer:** **C.** Resource ID, **D.** Resource address

</details>

<details>
<summary>What does `terraform refresh` modify?</summary>

**Options:**

- **A.** Your cloud infrastructure
- **B.** Your state file
- **C.** Your Terraform plan
- **D.** Your Terraform configuration

**Answer:** **B.** Your state file

</details>

<details>
<summary>`terraform apply` is failing with an "Access Denied" error. What next step should you take to determine the root cause of the problem?</summary>

**Options:**

- **A.** Set `TF_LOG=DEBUG`
- **B.** Review syslog for Terraform error messages
- **C.** Run `terraform login` to reauthenticate with the provider
- **D.** Review `/var/log/terraform.log` for error messages

**Answer:** **A.** Set `TF_LOG=DEBUG`

</details>

<details>
<summary>What command can you run to generate DOT (Document Template) formatted data to visualize Terraform dependencies?</summary>

**Options:**

- **A.** terraform refresh
- **B.** terraform show
- **C.** terraform graph
- **D.** terraform output

**Answer:** **C.** terraform graph

</details>

<details>
<summary>When should Terraform configuration files be written when running `terraform import` on existing infrastructure?</summary>

**Options:**

- **A.** Infrastructure can be imported without corresponding Terraform code
- **B.** Terraform will generate the corresponding configuration files for you
- **C.** You should write Terraform configuration files after the next `terraform import` is executed
- **D.** Terraform configuration should be written before `terraform import` is executed

**Answer:** **D.** Terraform configuration should be written before `terraform import` is executed

</details>

<details>
<summary>Which command lets you experiment with Terraform's built-in functions?</summary>

**Options:**

- **A.** terraform env
- **B.** terraform console
- **C.** terraform test
- **D.** terraform validate

**Answer:** **B.** terraform console

</details>

<details>
<summary>Which environment variable must be configured to make Terraform's logging more verbose?</summary>

**Options:**

- **A.** TF_LOG_LEVEL
- **B.** TF_LOG_FILE
- **C.** TF_LOG
- **D.** TP_LOG_PATH

**Answer:** **C.** TF_LOG

</details>

<details>
<summary>Which of the following commands would you use to access all of the attributes and details of a resource managed by Terraform?</summary>

**Options:**

- **A.** terraform state list <RESOURCE ID>
- **B.** terraform state show <RESOURCE ID>
- **C.** terraform get <RESOURCE ID>
- **D.** terraform state list

**Answer:** **B.** terraform state show <RESOURCE ID>

</details>

<details>
<summary>Using the terraform state rm command against a resource will destroy it.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
`terraform state rm` forgets the state binding but leaves the real object running and unmanaged.
That makes it operationally risky even though it does not destroy anything. Confirm the selected
backend/workspace, stop concurrent runs, take a protected state backup, and verify the address
before using it. If the resource remains in configuration, a later apply may create a replacement
and leave both objects running.

</details>

<details>
<summary>Select the command that doesn’t cause Terraform to refresh its state.</summary>

**Options:**

- **A.** terraform apply
- **B.** terraform destroy
- **C.** terraform plan
- **D.** terraform state list

**Answer:** **D.** terraform state list

</details>

<details>
<summary>When should you write Terraform configuration files for existing infrastructure that you want to start managing with Terraform?</summary>

**Options:**

- **A.** Before you run `terraform import`
- **B.** You can import infrastructure without corresponding Terraform code
- **C.** Terraform will generate the corresponding configuration files for you
- **D.** After you run `terraform import`

**Answer:** **A.** Before you run `terraform import`

</details>

<details>
<summary>What does Terraform **not** reference when running a `terraform apply -refresh-only`?</summary>

**Options:**

- **A.** Credentials
- **B.** State file
- **C.** Terraform resource definitions in configuration files
- **D.** Cloud provider

**Answer:** **C.** Terraform resource definitions in configuration files

</details>

<details>
<summary>While attempting to deploy resources into your cloud provider using Terraform, you begin to see some odd behavior and experience slow responses. In order to troubleshoot, you decide to turn on Terraform debugging. Which environment variable must be configured to make Terraform’s logging more verbose?</summary>

**Options:**

- **A.** TF_LOG_PATH
- **B.** TF_VAR_log_level
- **C.** TF_LOG
- **D.** TF_VAR_log_path

**Answer:** **C.** TF_LOG

</details>

<details>
<summary>A developer accidentally launched a VM (virtual machine) outside of the Terraform workflow and ended up with two servers with the same name. They don’t know which VM Terraform manages but do have a list of all active VM IDs. Which of the following methods could you use to discover which instance Terraform manages?</summary>

**Options:**

- **A.** Run `terraform taint/code` on all the VMs to recreate them
- **B.** Update the code to include outputs for the ID of all VMs, then run `terraform plan` to view the outputs
- **C.** Run `terraform state list` to find the names of all VMs, then run `terraform state show` for each of them to find which VM ID Terraform manages
- **D.** Use `terraform refresh/code` to find out which IDs are already part of state

**Answer:** **C.** Run `terraform state list` to find the names of all VMs, then run `terraform state show` for each of them to find which VM ID Terraform manages

**Reference:**
[Terraform State CLI Commands](https://developer.hashicorp.com/terraform/cli/commands/state/list)

</details>

<details>
<summary>If you manually destroy infrastructure, what is the best practice for reflecting this change in Terraform?</summary>

**Options:**

- **A.** Manually update the state file
- **B.** Remove the resource definition from your configuration and run terraform apply -refresh-only
- **C.** Run terraform import
- **D.** It will happen automatically

**Answer:** **B.** Remove the resource definition from your configuration and run terraform apply -refresh-only

**Explanation:**
A refresh-only apply reconciles state with the real world and records that the object is gone,
without proposing any other change. Dropping the resource from the configuration first means
Terraform will not simply recreate it on the next normal apply.

Never hand-edit `terraform.tfstate`. The standalone `terraform refresh` command does the same
reconciliation but has been deprecated since Terraform 0.15.4 because it updates state with no
plan to review; use `terraform apply -refresh-only` instead.

**Reference:**
[Refresh-only mode](https://developer.hashicorp.com/terraform/cli/commands/refresh)

</details>

<details>
<summary>You created infrastructure outside of the Terraform workflow that you now want to manage using Terraform. Which command brings the infrastructure into Terraform state?</summary>

**Options:**

- **A.** terraform init
- **B.** terraform get
- **C.** terraform refresh
- **D.** terraform import

**Answer:** **D.** terraform import

**Explanation:**
The `terraform import` command is used to bring existing infrastructure into your Terraform state. This allows Terraform to start managing resources that were created outside of Terraform's workflow.

**Reference:**
[Terraform CLI - Import Command](https://developer.hashicorp.com/terraform/cli/import)

</details>

<details>
<summary>Which command adds existing resources into Terraform state?</summary>

**Options:**

- **A.** terraform init
- **B.** terraform plan
- **C.** terraform refresh
- **D.** terraform import
- **E.** All of these

**Answer:** **D.** terraform import

**Explanation:**
The `terraform import` command is used to bring existing infrastructure resources under Terraform management by adding them to the Terraform state. This is useful for resources that were created outside of Terraform.

</details>

<details>
<summary>Setting the `TF_LOG` environment variable to `DEBUG` causes debug messages to be logged to stdout.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
`TF_LOG` enables levelled logging (`TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`), but Terraform writes
those logs to **stderr**, not stdout, and never to syslog. Set `TF_LOG_PATH` to send them to a file
instead:

```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform.log
```

Keeping logs off stdout is deliberate: it means `terraform output -json` and similar commands stay
machine-parseable while debugging is on.

**Reference:**
[Debugging Terraform](https://developer.hashicorp.com/terraform/internals/debugging)

</details>

<details>
<summary>A developer on your team is going to tear down an existing deployment managed by Terraform and deploy a new one. However, there is a specific resource named `aws_instance.ubuntu[1]` that they want to keep. What command should they use to tell Terraform to stop managing that specific resource?</summary>

**Options:**

- **A.** terraform destroy aws_instance.ubuntu[1]
- **B.** terraform apply rm aws_instance.ubuntu[1]
- **C.** terraform state rm aws_instance.ubuntu[1]
- **D.** terraform plan rm aws_instance.ubuntu[1]

**Answer:** **C.** terraform state rm aws_instance.ubuntu[1]

**Explanation:**
This command leaves the instance running but removes its binding from Terraform state. Before using
it, confirm the selected backend and workspace, stop concurrent runs, save a protected state
backup, and verify the address. Remove or change the corresponding configuration too; otherwise a
later apply can create a duplicate instance.

</details>

<details>
<summary>Which Terraform command records out-of-band infrastructure changes in state without making configuration-driven infrastructure changes?</summary>

**Options:**

- **A.** terraform plan -refresh-only
- **B.** terraform show -json
- **C.** terraform apply -refresh-only
- **D.** terraform plan -target-state

**Answer:** **C.** terraform apply -refresh-only

**Explanation:**
`terraform plan -refresh-only` previews the observed drift but does not persist it.
`terraform apply -refresh-only` presents that refresh-only plan for approval and then records the
observed remote values in state. It does not update configuration, so a later normal plan may still
propose restoring the configured values.

Never use `-lock=false` to adopt drift. It only disables concurrency protection and can allow two
runs to corrupt shared state. `terraform show` is read-only, and `-target-state` is not a valid
flag.

**Reference:**
[terraform apply -refresh-only](https://developer.hashicorp.com/terraform/cli/commands/refresh)

</details>

<details>
<summary>What is `terraform apply -refresh-only` intended to detect?</summary>

**Options:**

- **A.** Empty state files
- **B.** Corrupt state files
- **C.** Terraform configuration code changes
- **D.** State file drift

**Answer:** **D.** State file drift

**Explanation:**
Refresh-only mode queries the provider for the real state of every managed object and shows how it
has diverged from the state file, without proposing any configuration-driven change. That is
exactly the definition of drift: changes made outside the Terraform workflow.

The standalone `terraform refresh` command does the same thing but is deprecated since Terraform
0.15.4 because it writes state with no reviewable plan.

**Reference:**
[Managing resource drift](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift)

</details>

<details>
<summary>Why would you use the `-replace` flag for `terraform apply`?</summary>

**Options:**

- **A.** You want to force Terraform to destroy a resource on the next apply
- **B.** You want Terraform to ignore a resource on the next apply
- **C.** You want Terraform to destroy and recreate a resource on the next apply
- **D.** You want Terraform to destroy all the infrastructure in your workspace

**Answer:** **C.** You want Terraform to destroy and recreate a resource on the next apply

**Explanation:**
`terraform apply -replace="aws_instance.web"` plans a destroy-then-create for exactly that resource
address while leaving everything else alone. It is the supported replacement for the deprecated
`terraform taint` workflow, and it is safer because the replacement shows up in a plan you can
review before approving.

Note the single leading dash: `-replace`, not `--replace`.

**Reference:**
[The -replace option](https://developer.hashicorp.com/terraform/cli/commands/plan#replace-address)

</details>

<details>
<summary>You can configure Terraform to log to a file using the `TF_LOG` environment variable.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>


## Workspaces, HCP Terraform (Terraform Cloud) and Enterprise

<details>
<summary>Which of the following is available only in Terraform Enterprise or Cloud workspaces and not in Terraform CLI?</summary>

**Options:**

- **A.** Secure variable storage
- **B.** Support for multiple cloud providers
- **C.** Dry runs with terraform plan
- **D.** Using the workspace as a data source

**Answer:** **A.** Secure variable storage

**Explanation:**
Secure storage of sensitive variables is a feature exclusive to Terraform Cloud and Terraform Enterprise. This enables users to store and manage variables securely using encryption.

Other features, such as support for multiple cloud providers, `terraform plan` for dry runs, and workspaces as a data source, are available in the Terraform CLI and are not limited to Terraform Cloud or Enterprise.

</details>

<details>
<summary>What value does the Terraform Cloud/Terraform Enterprise private module registry provide over the public Terraform Module Registry?</summary>

**Options:**

- **A.** The ability to share modules with public Terraform users and members of Terraform Enterprise Organizations
- **B.** The ability to tag modules by version or release
- **C.** The ability to restrict modules to members of Terraform Cloud or Enterprise organizations
- **D.** The ability to share modules publicly with any user of Terraform

**Answer:** **C.** The ability to restrict modules to members of Terraform Cloud or Enterprise organizations

**Explanation:**
The private module registry in Terraform Cloud or Enterprise provides the capability to securely host and manage private modules. Unlike the public module registry, the private module registry allows you to restrict access to modules so that only authenticated members of specific Terraform Cloud or Enterprise organizations can fetch and use them. This is particularly useful for sensitive or proprietary infrastructure code.

**Why the other options are wrong:**
- **A**: Modules in the private registry are not shared publicly or with public Terraform users.
- **B**: Module versioning is supported in both public and private registries, but it is not unique to the private registry.
- **D**: The private module registry does not allow public sharing; it is specifically used for organizational access control.

**Reference:**
[Terraform Private Module Registry](https://developer.hashicorp.com/terraform/cloud-docs/registry)

</details>

<details>
<summary>What features does the hosted service Terraform Cloud provide? (Choose two)</summary>

**Options:**

- **A.** Automated infrastructure deployment visualization
- **B.** Automatic backups
- **C.** Remote state storage
- **D.** A web-based user interface (UI)

**Answer:** **C.** Remote state storage, **D.** A web-based user interface (UI)

**Explanation:**
Terraform Cloud offers the following key features:
- **Remote state storage (C):** Terraform Cloud provides centralized state storage, making it easier to collaborate in a team environment by ensuring that state is securely stored and shared across team members.
- **Web-based user interface (D):** Terraform Cloud includes a web UI for managing workspaces, user access, state versions, and other administrative controls.

**Why the other options are wrong:**
- **A.** Terraform Cloud does not provide automated infrastructure deployment visualization as a built-in feature.
- **B.** While Terraform manages state safely, it does not provide general-purpose automatic backup functionality as a specific feature.

**References:**
- [Terraform Cloud Remote State Documentation](https://developer.hashicorp.com/terraform/language/state/remote)
- [Terraform Cloud Overview](https://www.hashicorp.com/products/terraform)

</details>

<details>
<summary>Only the user that generated a plan may apply it.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Terraform does not require the same user who generated a plan to apply it. Terraform separates the `plan` and `apply` steps, but the saved plan file (`terraform plan -out=<file>`) can be used by any user with appropriate access to apply the changes. This flexibility allows teams to collaborate effectively, enabling one user to generate the plan and another user to apply it.

**Why the other options are wrong:**
- **A. True:** This is incorrect; there is no restriction that limits the application of a saved plan file to the same user who generated it.

**Reference:**
[Terraform Plan and Apply Workflow Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)

</details>

<details>
<summary>What command should you run to display all workspaces for the current configuration?</summary>

**Options:**

- **A.** terraform workspace
- **B.** terraform workspace show
- **C.** terraform workspace list
- **D.** terraform show workspace

**Answer:** **C.** terraform workspace list

**Explanation:**
The `terraform workspace list` command is used to display all existing workspaces for the current configuration. Workspaces in Terraform allow you to manage multiple states for the same configuration, such as for different environments (e.g., dev, staging, production).

**Example Command:**
```bash
terraform workspace list
```

</details>

<details>
<summary>You would like to reuse the same Terraform configuration for your development and production environments with a different state file for each. Which command would you use?</summary>

**Options:**

- **A.** terraform import
- **B.** terraform workspace
- **C.** terraform state
- **D.** terraform init

**Answer:** **B.** terraform workspace

</details>

<details>
<summary>In contrast to Terraform Open Source, when working with Terraform Enterprise and Cloud Workspaces, conceptually you could think about them as completely separate working directories.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>How can you trigger a run in a Terraform Cloud workspace that is connected to a Version Control System (VCS) repository?</summary>

**Options:**

- **A.** Only Terraform Cloud organization owners can set workspace variables on VCS connected workspaces
- **B.** Commit a change to the VCS working directory and branch that the Terraform Cloud workspace is connected to
- **C.** Only members of a VCS organization can open a pull request against repositories that are connected to Terraform Cloud workspaces
- **D.** Only Terraform Cloud organization owners can approve plans in VCS connected workspaces

**Answer:** **B.** Commit a change to the VCS working directory and branch that the Terraform Cloud workspace is connected to

**Explanation:**
When a Terraform Cloud workspace is connected to a VCS repository, any commits made to the specified working directory and branch automatically trigger a Terraform Cloud run. This workflow allows changes to be tracked and infrastructure updates to be automated based on version-controlled changes.

**Reference:**
[Terraform Cloud VCS Integration Documentation](https://developer.hashicorp.com/terraform/cloud-docs/vcs)

</details>

<details>
<summary>Your risk management organization requires that new AWS S3 buckets must be private and encrypted at rest. How can Terraform Enterprise automatically and proactively enforce this security control?</summary>

**Options:**

- **A.** With a Sentinel policy, which runs before every apply
- **B.** By adding variables to each TFE workspace to ensure these settings are always enabled
- **C.** With an S3 module with proper settings for buckets
- **D.** Auditing cloud storage buckets with a vulnerability scanning tool

**Answer:** **A.** With a Sentinel policy, which runs before every apply

**Reference:**
[Terraform Sentinel Documentation](https://developer.hashicorp.com/terraform/enterprise/sentinel)

</details>

<details>
<summary>All Terraform Cloud tiers support team management and governance.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Terraform Cloud is available only as a paid offering from HashiCorp.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Reference:**
[Terraform Cloud Pricing](https://www.hashicorp.com/products/terraform/pricing)
(Note: Terraform Cloud offers a free tier suitable for small teams and personal projects, with paid tiers providing additional features.)

</details>

<details>
<summary>When does Sentinel enforce policy logic during a Terraform Enterprise run?</summary>

**Options:**

- **A.** Before the plan phase
- **B.** During the plan phase
- **C.** Before the apply phase
- **D.** After the apply phase

**Answer:** **C.** Before the apply phase

</details>

<details>
<summary>What is the purpose of a Terraform workspace in either open source or enterprise?</summary>

**Options:**

- **A.** Workspaces allow you to manage collections of infrastructure in state files
- **B.** A logical separation of business units
- **C.** A method of grouping multiple infrastructure security policies
- **D.** Provides limited access to a cloud environment

**Answer:** **A.** Workspaces allow you to manage collections of infrastructure in state files

</details>

<details>
<summary>In a Terraform Cloud workspace linked to a version control repository, speculative plan runs start automatically when you merge or commit changes to version control.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>You want to deploy the same Terraform code in the staging environment with a separate variable definition file and a separate state file. Which two actions should you perform? (Choose two.)</summary>

**Options:**

- **A.** Copy the existing terraform.tfstate file and save it as staging.terraform.tfstate
- **B.** Write a new staging.auto.tfvars variable definition file and run Terraform with the `-var-file="staging.auto.tfvars"` flag
- **C.** Create a new Terraform workspace for staging
- **D.** Create a new Terraform provider for staging
- **E.** Add new Terraform code (*.tf files) for staging in the same directory

**Answer:** **B.** Write a new staging.auto.tfvars variable definition file and run Terraform with the `-var-file="staging.auto.tfvars"` flag, **C.** Create a new Terraform workspace for staging

</details>

<details>
<summary>Both Terraform Cloud and Terraform Enterprise support policy as code (Sentinel).</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>Which of these statements about Terraform Enterprise workspaces is false?</summary>

**Options:**

- **A.** They can securely store cloud credentials
- **B.** You must use the CLI to switch between workspaces
- **C.** Plans and applies can be triggered via version control system integrations
- **D.** They have role-based access controls

**Answer:** **B.** You must use the CLI to switch between workspaces

</details>

<details>
<summary>Which feature is not included in the HCP Terraform (Terraform Cloud) free tier?</summary>

**Options:**

- **A.** Workspaces
- **B.** Remote state management
- **C.** Audit logging
- **D.** Private module registry

**Answer:** **C.** Audit logging

**Explanation:**
The free tier covers workspaces, remote state with locking, VCS-driven runs and the private module
registry. Audit logging is a governance feature reserved for the paid Plus tier and Terraform
Enterprise.

Tier boundaries change; confirm against current pricing before quoting specifics in an interview.

**Reference:**
[HCP Terraform pricing](https://www.hashicorp.com/products/terraform/pricing)

</details>

<details>
<summary>What are some benefits of using Sentinel with Terraform Cloud/Terraform Enterprise? (Choose three.)</summary>

**Options:**

- **A.** Policy-as-code can enforce security best practices
- **B.** You can restrict specific resource configurations, such as disallowing the use of CIDR=0.0.0.0/0
- **C.** You can enforce a list of approved AWS AMIs
- **D.** Sentinel Policies can be written in HashiCorp Configuration Language (HCL)
- **E.** You can check out and check in cloud access keys

**Answer:** **A.** Policy-as-code can enforce security best practices, **B.** You can restrict specific resource configurations, such as disallowing the use of CIDR=0.0.0.0/0, **C.** You can enforce a list of approved AWS AMIs

</details>

<details>
<summary>You have decided to create a new Terraform workspace to deploy a development environment. What is different about this workspace?</summary>

**Options:**

- **A.** It has its own state file
- **B.** It pulls in a different `terraform.tfvars` file
- **C.** It uses a different branch of code
- **D.** It uses a different backend

**Answer:** **A.** It has its own state file

</details>

<details>
<summary>Sentinel policy-as-code is available in Terraform Enterprise.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **A.** True

</details>

<details>
<summary>You are working on some new application features and you want to spin up a copy of your production deployment to perform some quick tests. In order to avoid having to configure a new state backend, what open source Terraform feature would allow you to create multiple states but still be associated with your current code?</summary>

**Options:**

- **A.** Terraform data sources
- **B.** Terraform local values
- **C.** Terraform modules
- **D.** Terraform workspaces
- **E.** None of the above

**Answer:** **D.** Terraform workspaces

</details>


## Secrets and Sensitive Data

<details>
<summary>You should store secret data in the same version control repository as your Terraform configuration.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

**Explanation:**
Storing secrets (e.g., credentials, API keys) in the same version control repository as your Terraform configuration is a bad practice as it exposes sensitive information to potential security risks. Instead, use secret management mechanisms like environment variables, Vault, AWS Secrets Manager, or Terraform's own `sensitive` attribute to protect sensitive data.

**Reference:**
[A Comprehensive Guide to Managing Secrets in Terraform Code](https://blog.gruntwork.io/a-comprehensive-guide-to-managing-secrets-in-your-terraform-code-1d586955ace1)

</details>

<details>
<summary>Which of these is not a real mechanism for keeping secrets out of Terraform configuration files?</summary>

**Options:**

- **A.** A Terraform provider
- **B.** Environment variables
- **C.** A -var flag
- **D.** secure string

**Answer:** **D.** secure string

**Explanation:**
There is no `secure string` type in Terraform. The other three all supply a value at run time
instead of committing it:
- A provider (Vault, AWS Secrets Manager, Azure Key Vault) reads the secret from a secret store.
- `TF_VAR_<name>` environment variables inject values without touching the code.
- `-var` / `-var-file` passes values on the command line from outside version control.

Compare this with the related question on marking a variable `sensitive`: that flag hides a value
in output but does not keep it out of configuration or state.

**Reference:**
[Input variables](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>Which of these is the best practice to protect sensitive values in state files?</summary>

**Options:**

- **A.** Blockchain
- **B.** Secure Sockets Layer (SSL)
- **C.** Enhanced remote backends
- **D.** Signed Terraform providers

**Answer:** **C.** Enhanced remote backends

**Explanation:**
Use of remote backends, and especially the availability of Terraform Cloud, ensures state encryption at rest and avoids storing state in clear text on local machines. Remote backends are the best practice for protecting sensitive data in state files.

**Reference:**
[Terraform Best Practices for Sensitive State](https://developer.hashicorp.com/terraform/language/state/sensitive-data)

</details>

<details>
<summary>You are building a CI/CD pipeline and need to inject sensitive variables into your Terraform run. How can you do this safely?</summary>

**Options:**

- **A.** Pass variables to Terraform with a -var flag
- **B.** Copy the sensitive variables into your Terraform code
- **C.** Store the sensitive variables in a secure_vars.tf file
- **D.** Store the sensitive variables as plain text in a source code repository

**Answer:** **A.** Pass variables to Terraform with a -var flag

**Explanation:**
Only option A keeps the value out of version control: the secret is supplied at run time from the
pipeline's own secret store instead of being committed. B, C and D all place plaintext secrets in
the repository.

In practice, prefer `TF_VAR_<name>` environment variables over `-var` on the command line, because
CLI arguments are visible in process listings and are frequently echoed into build logs. Better
still, read the secret at run time through a provider such as Vault, AWS Secrets Manager or Azure
Key Vault.

**Reference:**
[Sensitive input variables](https://developer.hashicorp.com/terraform/tutorials/configuration-language/sensitive-variables)

</details>

<details>
<summary>Your security team scanned some Terraform workspaces and found secrets stored in plaintext in state files. How can you protect that data?</summary>

**Options:**

- **A.** Delete the state file every time you run Terraform
- **B.** Store the state in an encrypted backend
- **C.** Edit your state file to scrub out the sensitive data
- **D.** Always store your secrets in a secrets.tfvars file

**Answer:** **B.** Store the state in an encrypted backend

**Reference:**
[Terraform Sensitive Data in State Documentation](https://developer.hashicorp.com/terraform/language/state/sensitive-data)

</details>

<details>
<summary>Which of these options is the **most secure** place to store secrets for connecting to a Terraform remote backend?</summary>

**Options:**

- **A.** Defined in Environment variables
- **B.** Inside the backend block within the Terraform configuration
- **C.** Defined in a connection configuration outside of Terraform
- **D.** None of above

**Answer:** **A.** Defined in Environment variables

</details>

<details>
<summary>Which option cannot be used to keep secrets out of Terraform configuration files?</summary>

**Options:**

- **A.** Environment variables
- **B.** Mark the variable as sensitive
- **C.** A Terraform provider
- **D.** A -var flag

**Answer:** **B.** Mark the variable as sensitive

**Explanation:**
`sensitive = true` is only a redaction control for normal CLI output. It does not remove a literal
from configuration, encrypt the value, or omit it from plan and state artifacts.

The other three do keep the literal out of the `.tf` files:
- `TF_VAR_<name>` environment variables supply the value at run time.
- A provider (Vault, AWS Secrets Manager, Azure Key Vault) fetches the value from a secret store.
- `-var` / `-var-file` supplies the value at run time from outside version control.

**Reference:**
[Sensitive values in state](https://developer.hashicorp.com/terraform/language/state/sensitive-data)

</details>

<details>
<summary>Which of the following is the safest way to inject sensitive values into a Terraform Cloud workspace?</summary>

**Options:**

- **A.** Write the value to a file and specify the file with the `-var-file` flag
- **B.** Set a value for the variable in the UI and check the "Sensitive" check box
- **C.** Edit the state file directly just before running `terraform apply`
- **D.** Set the variable value on the command line with the `-var` flag

**Answer:** **B.** Set a value for the variable in the UI and check the "Sensitive" check box

</details>

<details>
<summary>A Terraform output that sets the "sensitive" argument to true will not store that value in the state file.</summary>

**Options:**

- **A.** True
- **B.** False

**Answer:** **B.** False

</details>

<details>
<summary>Which provider authentication method prevents credentials from being stored in the Terraform state file?</summary>

**Options:**

- **A.** Using environment variables
- **B.** Specifying the login credentials in the provider block
- **C.** Setting credentials as Terraform variables
- **D.** None of the above

**Answer:** **A.** Using environment variables

</details>

<details>
<summary>Why should secrets **not** be hard coded into Terraform code? (Choose two.)</summary>

**Options:**

- **A.** It makes the code less reusable.
- **B.** Version control, developer workstations and CI workspaces can expose the configuration to more users and systems than should know the secret.
- **C.** Removing the literal from the current file does not remove it from Git history, forks, caches or retained build artifacts.
- **D.** All passwords should be rotated on a quarterly basis.

**Answer:** **B.** Version control, developer workstations and CI workspaces can expose the configuration to more users and systems than should know the secret., **C.** Removing the literal from the current file does not remove it from Git history, forks, caches or retained build artifacts.

**Explanation:**
Terraform sends API requests from the machine running Terraform; it does not normally copy the
configuration to target resources for local execution. Keep secret literals out of configuration
and Git history. `sensitive = true` only redacts normal output; use ephemeral values (Terraform
1.10+) and provider-supported write-only arguments (Terraform 1.11+) when the value must also be
omitted from plan and state.

**Reference:**
[Manage sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)

</details>

<details>
<summary>Which of these are secure options for storing secrets for connecting to a Terraform remote backend? (Choose two.)</summary>

**Options:**

- **A.** Inside the backend block within the Terraform configuration
- **B.** Defined in Environment variables
- **C.** Defined in a connection configuration outside of Terraform
- **D.** A variable file

**Answer:** **B.** Defined in Environment variables, **C.** Defined in a connection configuration outside of Terraform

</details>

<details>
<summary>Which of the following is **not** considered a safe way to inject sensitive values into a Terraform Cloud workspace?</summary>

**Options:**

- **A.** Edit the state file directly just before running `terraform apply`
- **B.** Set the variable value on the command line with the `-var` flag
- **C.** Write the value to a file and specify the file with the `-var-file` flag

**Answer:** **A.** Edit the state file directly just before running `terraform apply`

**Reference:**
[Terraform Cloud Workspaces Variables](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables)

</details>
