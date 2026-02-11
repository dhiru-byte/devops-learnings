## Informatica IDMC Deployment & Operations Architecture

This repository contains the **Infrastructure as Code (IaC)** and **CI/CD Pipelines** for managing the Informatica Intelligent Data Management Cloud (IDMC) ecosystem. 

### 1. Architectural Vision
The goal of this layer is to automate infrastructure provisioning, code promotion, and deployment validation to ensure consistency, security, and traceability across all environments.

### Core Technologies
*   **Terraform**: For repeatable, version-controlled management of cloud VMs (Secure Agents) and IDMC objects (Connections, Runtime Groups).
*   **Bitbucket Pipelines**: For automated CI/CD, reducing manual errors through automated testing and deployment gates.
*   **Audit Logging**: For compliance and operational transparency via immutable logs of every infrastructure change.

---

### 2. Directory Structure
We follow a modular approach to separate resource definitions from environment-specific configurations.

```text
.
├── modules/
│   ├── secure_agent/          # Provisions Cloud VMs & Registers Agents
│   ├── idmc_connection/       # Logic for IDMC Connectors (S3, Snowflake, etc.)
│   └── idmc_runtime/          # Manages Runtime Environments/Groups
├── environments/
│   ├── dev/
│   │   ├── main.tf            # Calls modules with DEV variables
│   │   └── terraform.tfvars   # Dev-specific secrets & settings
│   └── prod/
│       ├── main.tf            # Calls modules with PROD variables
│       └── terraform.tfvars   # Prod-specific secrets (Restricted)
├── scripts/
│   └── agent_bootstrap.sh     # User-data script for agent installation
└── bitbucket-pipelines.yml     # CI/CD Pipeline Definition
```

### 3. The CI/CD Process Flow
* **Commit:** Developer pushes code to a feature branch.
* **Lint & Validate:** The pipeline runs terraform validate and security scans (Checkov/TFLint).
* **Plan:** A terraform plan is generated and attached to the Bitbucket Pull Request for peer review.
* **Approval:** A manual gate is required for promotion to the master/main branch (Production).
* **Provision:** Terraform interacts with the Informatica IDMC API and Cloud Provider (AWS/Azure) to apply changes.
* **Audit:** Every action is recorded in the Bitbucket Audit Log and Informatica System Audit Logs.

### 4. Deployment Logic (Example)
* **IDMC Connection Module:** abstract connection logic to ensure security (using sensitive variables) and reusability.

```
resource "idmc_connection" "data_source" {
  name                = var.conn_name
  type                = var.conn_type
  runtime_environment = var.agent_group
  
  properties = {
    "Username" = var.db_user
    "Password" = var.db_password  # Sensitive: Managed via Bitbucket Secrets
  }
}
```
## Informatica IDMC Infrastructure via Terraform Bitbucket Example (Yaml):

```
image: hashicorp/terraform:latest

# Template for re-usable steps
definitions:
  steps:
    - step: &lint-and-validate
        name: "Security Scan & Lint"
        script:
          - terraform init -backend=false
          - terraform validate
          # Optional: Add TFLint or Checkov for enhanced security audits
          # - tflint

pipelines:
  # 1. Automatic validation for all Pull Requests (Feature Branches)
  branches:
    feature/*:
      - step: *lint-and-validate
      - step:
          name: "Plan Development"
          script:
            - cd environments/dev
            - terraform init
            - terraform plan

  # 2. Main/Master Branch Deployment (Staging & Production)
  branches:
    master:
      - step: *lint-and-validate
      - step:
          name: "Plan Production"
          script:
            - cd environments/prod
            - terraform init
            - terraform plan -out=prod.tfplan
          artifacts:
            - environments/prod/prod.tfplan
      
      - step:
          name: "Manual Approval & Production Deploy"
          trigger: manual # The "Gate" required for compliance & traceability
          deployment: Production
          script:
            - cd environments/prod
            - terraform init
            - terraform apply "prod.tfplan"
```
