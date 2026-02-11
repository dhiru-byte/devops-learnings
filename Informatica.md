### Informatica IDMC Deployment & Operations Architecture

*   **Terraform**: For repeatable, version-controlled management of cloud VMs (Secure Agents) and IDMC objects (Connections, Runtime Groups).
*   **Bitbucket Pipelines**: For automated CI/CD, reducing manual errors through automated testing and deployment gates.
*   **Audit Logging**: For compliance and operational transparency via immutable logs of every infrastructure change.
---
### Directory Structure Modular Approach

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
---
### Module Samples for reusability.
#### 1. Secure Agent Module **(modules/secure_agent/main.tf)**.
```
resource "aws_instance" "informatica_agent" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  subnet_id     = var.subnet_id

  # Automated Installation Script
  user_data = templatefile("${path.module}/install_agent.sh", {
    registration_token = var.registration_token
    install_dir        = "/opt/informatica"
  })

  tags = { Name = "${var.env}-secure-agent" }
}
```
#### 2. IDMC Connection Module **(modules/idmc_connection/main.tf)**.

```
resource "idmc_connection" "this" {
  name                = var.conn_name
  type                = var.conn_type # e.g., "Snowflake Cloud Data Warehouse"
  runtime_environment = var.runtime_env_name

  # Sensitive properties are passed as a map
  properties = var.conn_properties
}
```
#### 3. IDMC User & Roles Module **(modules/idmc_iam/main.tf)**.

```
resource "idmc_user" "data_engineer" {
  username   = var.user_email
  first_name = var.first_name
  last_name  = var.last_name
  roles      = ["Data Integration Developer", "Designer"]
}
```
#### 4.S3 Backend State-Locking Config with DynamoDB **backend.tf**.
```
terraform {
  backend "s3" {
    bucket         = "your-company-terraform-state"
    key            = "informatica/prod/terraform.tfstate"
    region         = "us-east-1"
    
    # State Locking via DynamoDB (Prevents corruption)
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```
#### Required Infrastructure for the Backend.

Before your pipeline can run, you need this "foundation" infrastructure. You can create this manually or via a separate "bootstrap" Terraform script:

* **S3 Bucket:** Versioning must be Enabled so you can roll back the state if a deployment fails. AWS S3 Versioning Guide.
* **DynamoDB Table:** Must have a Partition Key named LockID (type: String). Terraform S3 Backend Locking.

#### How to call these modules in environments/prod/main.tf
```
# 1. Get the latest registration token from IDMC
data "idmc_agent_registration_token" "prod_token" {}

# 2. Deploy the Infrastructure
module "prod_agent" {
  source             = "../../modules/secure_agent"
  env                = "prod"
  registration_token = data.idmc_agent_registration_token.prod_token.token
  ami_id             = "ami-0c55b159cbfafe1f0"
}

# 3. Provision the Connection
module "snowflake_conn" {
  source           = "../../modules/idmc_connection"
  conn_name        = "SNOWFLAKE_PROD"
  conn_type        = "Snowflake Cloud Data Warehouse"
  runtime_env_name = "PROD_AGENT_GROUP"
  
  conn_properties = {
    "Account"   = "corp_prod_account"
    "Warehouse" = "DATA_LOAD_WH"
    "Password"  = var.prod_snowflake_password # Injected from Bitbucket Variables
  }
}
```
---
#### AWS Side (OIDC Identity Provider) Config (modules/iam_oidc/main.tf) to avoid paasing **AWS

```
# 1. Define the OIDC Provider for Bitbucket
resource "aws_iam_openid_connect_provider" "bitbucket" {
  url             = "https://api.bitbucket.org{var.workspace_id}/pipelines-config/identity/oidc"
  client_id_list  = ["https://bitbucket.org{var.workspace_id}/${var.repo_slug}"]
  thumbprint_list = ["a031c46782e6e6c662c2c87c76da9aa62ccabd8e"] # Bitbucket's OIDC Thumbprint
}

# 2. Create the Role that Terraform will assume
resource "aws_iam_role" "terraform_execution_role" {
  name = "BitbucketTerraformExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRoleWithWebIdentity"
      Effect = "Allow"
      Principal = { Federated = aws_iam_openid_connect_provider.bitbucket.arn }
      Condition = {
        StringLike = {
          "api.bitbucket.org/2.0/workspaces/${var.workspace_id}/pipelines-config/identity/oidc:sub": "{${var.repo_uuid}}:*"
        }
      }
    }]
  })
}
```
#### Business & Security Rationale
* **Zero Key Management:** You no longer need to store AWS_SECRET_ACCESS_KEY in Bitbucket variables. If the repo is compromised, there are no static keys to steal.
* **Least Privilege:** The role is only valid for the duration of the pipeline step.
* **Traceability:** AWS CloudTrail will show that the Bitbucket Identity performed the actions, linking the cloud change directly to a Git commit.
---
### The CI/CD Process Flow
* **Commit:** Developer pushes code to a feature branch.
* **Lint & Validate:** The pipeline runs terraform validate and security scans (Checkov/TFLint).
* **Plan:** A terraform plan is generated and attached to the Bitbucket Pull Request for peer review.
* **Approval:** A manual gate is required for promotion to the master/main branch (Production).
* **Provision:** Terraform interacts with the Informatica IDMC API and Cloud Provider (AWS/Azure) to apply changes.
* **Audit:** Every action is recorded in the Bitbucket Audit Log and Informatica System Audit Logs.

#### Informatica IDMC Infrastructure via Terraform Bitbucket Example (Yaml):
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
#### How to Add Repository Variables
* Navigate to your repository in Bitbucket Cloud.
* Select Repository settings from the left-hand sidebar.
* Scroll down to the Pipelines section and select Repository variables.
* Enter the Variable:
* **Name:** Must be all caps, e.g., **IDMC_PASSWORD** or **AWS_ACCESS_KEY_ID**.
* **Value:** Paste your secret or configuration value.
* **Secure It:** Check the Secured box (padlock icon). This encrypts the value and masks it with ******** in your CI/CD logs.
* Click **Add**.
---
