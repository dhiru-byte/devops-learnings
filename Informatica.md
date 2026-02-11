### Informatica IDMC Deployment & Operations Architecture
*   **Terraform**: For repeatable, version-controlled management of cloud VMs (Secure Agents) and IDMC objects (Connections, Runtime Groups). [Terraform](https://registry.terraform.io/providers/Tzrlk/idmc/latest/docs)
*   **Bitbucket Pipelines**: For automated CI/CD, reducing manual errors through automated testing and deployment gates.
*   **Audit Logging**: For compliance and operational transparency via immutable logs of every infrastructure change.
---
### Directory Structure Modular Approach
```text
📂terraform-informatica/
├── modules/
|   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── s3_landing/           # Bronze Layer: S3 Bucket & Security
│   │   └── main.tf
│   ├── redshift/             # Gold Layer: Redshift Cluster & IAM
│   │   └── main.tf
│   ├── secure_agent/         # Informatica Secure Agent VMs
│   │   └── main.tf
│   └── idmc_connection/      # IDMC API Logic
│       └── main.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf           # Dev-specific configuration
│   │   └── backend.tf        # S3 Remote State
│   └── prod/
│       ├── main.tf           # Prod-specific configuration
│       └── backend.tf
└── bitbucket-pipelines.yml
```
---
### Module Samples for reusability.

#### 1. S3 Backend State-Locking Config with DynamoDB **backend.tf**.
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

#### Highlights
* **State Separation:** Each environment (Dev/Prod) maintains its own isolated state file via its respective backend.tf.
* **Encapsulation:** Network logic (VPCs, Subnets) is defined once and passed into the Redshift and S3 modules as input variables, ensuring environment parity.
* **Security:** The Public Access Block on S3 prevents accidental data exposure in the landing zone. 

#### 1. VPC & Networking Module (modules/networking/main.tf)
```
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags                 = { Name = "${var.env}-vpc" }
}

# Private Subnets for Redshift and Secure Agents
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_cidrs[count.index]
  availability_zone = var.azs[count.index]
  tags              = { Name = "${var.env}-private-${count.index}" }
}

# S3 Gateway Endpoint (Allows private S3 access without NAT costs)
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.region}.s3"
  route_table_ids = [aws_route_table.private.id]
}
```

#### 2. S3 Landing Zone Module **(modules/s3_landing/main.tf)**.
```
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  tags   = { Environment = var.env }
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

# Restrict all public access to the landing zone
resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

#### 3. Redshift Cluster Module **(modules/redshift/main.tf)**
```
resource "aws_redshift_cluster" "this" {
  cluster_identifier = "${var.env}-redshift-cluster"
  database_name      = var.db_name
  master_username    = var.db_user
  master_password    = var.db_password # Injected from Bitbucket Secrets
  node_type          = "ra3.xlplus"
  cluster_type       = "multi-node"
  number_of_nodes    = 2
  
  encrypted          = true
  publicly_accessible = false
  vpc_security_group_ids = [var.security_group_id]
  cluster_subnet_group_name = var.subnet_group_name
  
  iam_roles = [var.redshift_role_arn]
}
```

#### 4. Secure Agent Module **(modules/secure_agent/main.tf)**.
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

#### 5. IDMC Connection Module **(modules/idmc_connection/main.tf)**.
```
resource "idmc_connection" "this" {
  name                = var.conn_name
  type                = var.conn_type # e.g., "Snowflake Cloud Data Warehouse"
  runtime_environment = var.runtime_env_name

  # Sensitive properties are passed as a map
  properties = var.conn_properties
}
```
#### 5. IDMC User & Roles Module **(modules/idmc_iam/main.tf)**.

```
resource "idmc_user" "data_engineer" {
  username   = var.user_email
  first_name = var.first_name
  last_name  = var.last_name
  roles      = ["Data Integration Developer", "Designer"]
}
```

#### How to call these modules in environments/prod/main.tf
```
# 1. Provision S3 Bronze Layer
module "s3_landing" {
  source      = "../../modules/s3_landing"
  bucket_name = "corp-data-prod-landing"
  env         = "prod"
}

# 2. Provision Redshift Gold Layer
module "redshift_dw" {
  source      = "../../modules/redshift"
  env         = "prod"
  db_password = var.prod_redshift_password # From Bitbucket Variables
  # ... other network variables
}

# 3. Create IDMC Connection using S3 Bucket output
module "idmc_s3_connection" {
  source           = "../../modules/idmc_connection"
  conn_name        = "S3_LANDING_ZONE"
  conn_type        = "Amazon S3"
  runtime_env_name = "PROD_AGENT_GROUP"

  conn_properties = {
    "Bucket" = module.s3_landing.bucket_name
    "Region" = "us-east-1"
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
# bitbucket-pipelines.yml
image: hashicorp/terraform:latest

# 1. Define reusable logic (Anchors)
definitions:
  steps:
    - step: &tf-plan
        name: "Terraform Plan"
        oidc: true
        script:
          # Dynamic OIDC Auth using Deployment Variables
          - export AWS_WEB_IDENTITY_TOKEN_FILE=$(pwd)/web-identity-token
          - echo $BITBUCKET_STEP_OIDC_TOKEN > $AWS_WEB_IDENTITY_TOKEN_FILE
          # Note: $AWS_ROLE_ARN and $ENV_DIR come from Deployment/Repo Variables
          - cd $ENV_DIR
          - terraform init
          - terraform plan -out=tfplan
        artifacts:
          - "**/tfplan"

    - step: &tf-apply
        name: "Terraform Apply"
        oidc: true
        trigger: manual # Safety gate for human review
        script:
          - export AWS_WEB_IDENTITY_TOKEN_FILE=$(pwd)/web-identity-token
          - echo $BITBUCKET_STEP_OIDC_TOKEN > $AWS_WEB_IDENTITY_TOKEN_FILE
          - cd $ENV_DIR
          - terraform init
          - terraform apply -auto-approve tfplan

pipelines:
  branches:
    # Development Environment (Automatic plan, Manual apply)
    develop:
      - step:
          <<: *tf-plan
          deployment: Development
          variables:
            ENV_DIR: "environments/dev"
      - step:
          <<: *tf-apply
          deployment: Development
          variables:
            ENV_DIR: "environments/dev"

    # Production Environment (Stricter gates)
    master:
      - step:
          <<: *tf-plan
          deployment: Production
          variables:
            ENV_DIR: "environments/prod"
      - step:
          <<: *tf-apply
          deployment: Production
          variables:
            ENV_DIR: "environments/prod"
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
