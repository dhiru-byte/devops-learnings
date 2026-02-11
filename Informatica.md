# Informatica IDMC Deployment & Operations Architecture

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

