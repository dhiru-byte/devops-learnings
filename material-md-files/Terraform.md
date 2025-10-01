# Terraform Questions and Answers

<details>
<summary>One remote backend configuration always maps to a single remote workspace.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation**:  
A single remote backend configuration can support multiple remote workspaces. This allows for multiple states to be managed under the same backend configuration, enabling better organization of environments such as development, staging, and production.

</b></details>


<details>
<summary>How is the Terraform remote backend different than other state backends such as S3, Consul, etc.?</summary><br><b>

**Options:**
- `A. It can execute Terraform runs on dedicated infrastructure on premises or in Terraform Cloud`
- `B. It doesn't show the output of a terraform apply locally`
- `C. It is only available to paying customers`
- `D. All of the above`

**Correct Answer:** `A. It can execute Terraform runs on dedicated infrastructure on premises or in Terraform Cloud`

**Explanation**:  
If you and your team are using Terraform to manage meaningful infrastructure, we recommend using the remote backend with Terraform Cloud or Terraform Enterprise.

**Reference**:  
[Terraform Remote Backend Documentation](https://www.terraform.io/docs/language/settings/backends/index.html)

</b></details>


<details>
<summary>What is the workflow for deploying new infrastructure with Terraform?</summary><br><b>

**Options:**
- `A. terraform plan to import the current infrastructure to the state file, make code changes, and terraform apply to update the infrastructure.`
- `B. Write a Terraform configuration, run terraform show to view proposed changes, and terraform apply to create new infrastructure.`
- `C. terraform import to import the current infrastructure to the state file, make code changes, and terraform apply to update the infrastructure.`
- `D. Write a Terraform configuration, run terraform init, run terraform plan to view planned infrastructure changes, and terraform apply to create new infrastructure.`

**Correct Answer:** `D. Write a Terraform configuration, run terraform init, run terraform plan to view planned infrastructure changes, and terraform apply to create new infrastructure.`

**Explanation**:  
To deploy new infrastructure using Terraform, follow these steps:
1. Write the Terraform configuration specifying the desired infrastructure resources.
2. Run `terraform init` to initialize the configuration and download necessary provider plugins.
3. Run `terraform plan` to see the execution plan and ensure the desired changes match your expectation.
4. Run `terraform apply` to provision the specified resources and create the new infrastructure.

</b></details>


<details>
<summary>A provider configuration block is required in every Terraform configuration.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Explanation**:  
In Terraform, a provider configuration block is essential as it specifies which provider (e.g., AWS, Azure) Terraform should use to interact with the underlying infrastructure. Without a provider configuration block, Terraform cannot manage resources associated with a specific provider.

**Reference**:  
[GitHub - HashiCorp Terraform Issues](https://github.com/hashicorp/terraform/issues/17928)

</b></details>


<details>
<summary>You run a local-exec provisioner in a null resource called null_resource.run_script and realize that you need to rerun the script. Which of the following commands would you use first?</summary><br><b>

**Options:**
- `A. terraform taint null_resource.run_script`
- `B. terraform apply -target=null_resource.run_script`
- `C. terraform validate null_resource.run_script`
- `D. terraform plan -target=null_resource.run_script`

**Correct Answer:** `B. terraform apply -target=null_resource.run_script`

**Explanation**:  
To rerun a specific resource in Terraform, the `-target` flag is used to isolate the execution onto that resource. Running `terraform apply -target=null_resource.run_script` ensures that the null resource (`run_script`) is executed again without impacting other resources defined in the configuration.

</b></details>


<details>
<summary>Which provisioner invokes a process on the resource created by Terraform?</summary><br><b>

**Options:**
- `A. remote-exec`
- `B. null-exec`
- `C. local-exec`
- `D. file`

**Correct Answer:** `A. remote-exec`

**Explanation**:  
The `remote-exec` provisioner allows Terraform to execute scripts or commands on a remote resource, such as a newly created virtual machine, after it has been provisioned. This is useful for performing post-provisioning tasks like software installation or configuration.

**Reference**:  
[Terraform Remote-Exec Provisioner Documentation](https://www.terraform.io/docs/language/resources/provisioners/remote-exec.html)

</b></details>


<details>
<summary>Which of the following is not true of Terraform providers?</summary><br><b>

**Options:**
- `A. Providers can be written by individuals`
- `B. Providers can be maintained by a community of users`
- `C. Some providers are maintained by HashiCorp`
- `D. Major cloud vendors and non-cloud vendors can write, maintain, or collaborate on Terraform providers`
- `E. None of the above`

**Correct Answer:** `E. None of the above`

**Explanation**:  
All the statements about Terraform providers are true:
- Providers can indeed be written by individuals.
- Providers can also be maintained by a community of users.
- Some providers are officially maintained by HashiCorp to ensure reliability and consistency.
- Major cloud vendors, as well as non-cloud vendors, actively contribute to developing and maintaining Terraform providers, enabling better integration and usability.

</b></details>


<details>
<summary>What command does Terraform require the first time you run it within a configuration directory?</summary><br><b>

**Options:**
- `A. terraform import`
- `B. terraform init`
- `C. terraform plan`
- `D. terraform workspace`

**Correct Answer:** `B. terraform init`

**Explanation**:  
The `terraform init` command is used to initialize a working directory containing Terraform configuration files. This command prepares the directory for use by downloading the required provider plugins and setting up the Terraform environment.

**Reference**:  
[Terraform Init Command Documentation](https://www.terraform.io/docs/cli/commands/init.html)
</b></details>

<details>
<summary>You have deployed a new web app with a public IP address on a cloud provider. However, you did not create any outputs for your code. What is the best method to quickly find the IP address of the resource you deployed?</summary><br><b>

**Options:**
- `A. Run terraform output ip_address to view the result`
- `B. In a new folder, use the terraform_remote_state data source to load in the state file, then write an output for each resource that you find in the state file`
- `C. Run terraform state list to find the name of the resource, then terraform state show to find the attributes including public IP address`
- `D. Run terraform destroy then terraform apply and look for the IP address in stdout`

**Correct Answer:** `C. Run terraform state list to find the name of the resource, then terraform state show to find the attributes including public IP address`

**Explanation**:  
Using `terraform state list` allows you to identify all resources managed in the current state file. Once you find the name of the desired resource, you can run `terraform state show` to inspect its attributes, including the public IP address. This method avoids unnecessary operations like destroying or reapplying resources and enables quick discovery of resource details.

</b></details>

<details>
<summary>Which of the following is not a key principle of infrastructure as code?</summary><br><b>

**Options:**
- `A. Versioned infrastructure`
- `B. Golden images`
- `C. Idempotence`
- `D. Self-describing infrastructure`

**Correct Answer:** `B. Golden images`

**Explanation**:  
Golden images are preconfigured disk images used to deploy environments and are not a core principle of infrastructure as code (IaC). The key principles of IaC include:
- **Versioned infrastructure:** Treating infrastructure as version-controlled code.
- **Idempotence:** Ensuring deployments produce the same results no matter how many times they are applied.
- **Self-describing infrastructure:** Clearly defining the desired state within configuration files.

</b></details>

<details>
<summary>Terraform variables and outputs that set the "description" argument will store that description in the state file.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation**:  
The "description" argument set in Terraform variables or outputs is purely informational and is not stored in the state file. Terraform state files only contain essential resource attributes and metadata required for infrastructure management, not descriptive information.

</b></details>

<details>
<summary>What is the provider for this fictitious resource?</summary><br><b>

**Options:**
- `A. vpc`
- `B. main`
- `C. aws`
- `D. test`

**Correct Answer:** `C. aws`

**Explanation**:  
In Terraform, the provider is specified at the beginning of a resource type. For example, `aws_vpc` denotes that the resource is managed by the AWS provider. Here, `aws` is the provider, `vpc` is the resource type, and `main` is the resource name.

**Reference**:  
[AWS Resource Types Documentation](https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-types.html)

</b></details>


<details>
<summary>If you manually destroy infrastructure, what is the best practice reflecting this change in Terraform?</summary><br><b>

**Options:**
- `A. Run terraform refresh`
- `B. It will happen automatically`
- `C. Manually update the state file`
- `D. Run terraform import`

**Correct Answer:** `A. Run terraform refresh`

**Explanation**:  
When you manually destroy infrastructure outside of Terraform, the Terraform state file will not be automatically updated. Running `terraform refresh` allows Terraform to sync the state file with the actual resources by querying the real-world infrastructure and ensuring the state file reflects the current reality.

</b></details>


<details>
<summary>What is not processed when running a terraform refresh?</summary><br><b>

**Options:**
- `A. State file`
- `B. Configuration file`
- `C. Credentials`
- `D. Cloud provider`

**Correct Answer:** `B. Configuration file`

**Explanation**:  
When running `terraform refresh`, Terraform updates the state file to match the actual infrastructure by querying the cloud provider or other resource APIs. The configuration file is not processed during this operation, as the refresh only deals with the state file and actual infrastructure resources.

</b></details>

<details>
<summary>What information does the public Terraform Module Registry automatically expose about published modules?</summary><br><b>

**Options:**
- `A. Required input variables`
- `B. Optional input variables and default values`
- `C. Outputs`
- `D. All of the above`
- `E. None of the above`

**Correct Answer:** `D. All of the above`

**Explanation**:  
The public Terraform Module Registry automatically exposes the following information about published modules:
- **Required input variables**: Variables that must be defined for the module to function.
- **Optional input variables and default values**: Variables with default values that can be overridden.
- **Outputs**: Values generated by the module, which can be used in other parts of the Terraform configuration.

These details help users understand how to use and integrate the module effectively.

</b></details>

<details>
<summary>If a module uses a local value, you can expose that value with a terraform output.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Explanation**:  
Output values in Terraform serve as a way to expose data from a module to be used in other parts of the configuration or by the user. If a module uses a local value, it can be referenced in an output block within that module to expose it for consumption elsewhere.

**References**:  
- [Terraform Locals Documentation](https://www.terraform.io/docs/language/values/locals.html)  
- [Terraform Outputs Documentation](https://www.terraform.io/docs/language/values/outputs.html)

</b></details>

<details>
<summary>You should store secret data in the same version control repository as your Terraform configuration.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation**:  
Storing secrets (e.g., credentials, API keys) in the same version control repository as your Terraform configuration is a bad practice as it exposes sensitive information to potential security risks. Instead, use secret management mechanisms like environment variables, Vault, AWS Secrets Manager, or Terraform's own `sensitive` attribute to protect sensitive data.

**Reference**:  
[A Comprehensive Guide to Managing Secrets in Terraform Code](https://blog.gruntwork.io/a-comprehensive-guide-to-managing-secrets-in-your-terraform-code-1d6586955ace1)

</b></details>

<details>
<summary>Which of the following is not a valid string function in Terraform?</summary><br><b>

**Options:**
- `A. split`
- `B. join`
- `C. slice`
- `D. chomp`

**Correct Answer:** `C. slice`

**Explanation**:  
In Terraform, `split`, `join`, and `chomp` are valid string functions:
- **split**: Splits a string into a list based on a delimiter.
- **join**: Joins elements of a list into a single string with a delimiter.
- **chomp**: Removes trailing newline characters from a string.

The `slice` function, however, is not a valid Terraform string function, as slicing operations are not directly supported in Terraform. For more advanced text manipulation, you'd need to use workarounds or external tools.

</b></details>

<details>
<summary>You have provisioned some virtual machines (VMs) on Google Cloud Platform (GCP) using the gcloud command-line tool. However, you are standardizing with Terraform and want to manage these VMs using Terraform instead. What are the two things you must do to achieve this? (Choose two.)</summary><br><b>

**Options:**
- `A. Provision new VMs using Terraform with the same VM names`
- `B. Use the terraform import command for the existing VMs`
- `C. Write Terraform configuration for the existing VMs`
- `D. Run the terraform import-gcp command`

**Correct Answer:** `B. Use the terraform import command for the existing VMs`  
`C. Write Terraform configuration for the existing VMs`

**Explanation**:  
To bring existing infrastructure under Terraform's management without recreating it:
1. Use the `terraform import` command to manually import the existing resources (e.g., VMs) into Terraform's state file.
2. Write Terraform configuration that mirrors the current state of the resources. The configuration must define the same attributes and parameters for successful management after import.

Terraform does not automatically generate configuration files, so manual configuration writing is necessary.

**References**:  
- [Terraform Import Command Documentation](https://www.terraform.io/docs/cli/import/usage.html)  
- [Google Cloud and Terraform Documentation](https://cloud.google.com/docs/terraform)

</b></details>

<details>
<summary>You are an engineer tasked with evaluating multiple outages that occurred during peak traffic times. You discover that the team manually deploys and configures new compute instances. This led to inconsistent configurations between each compute instance. How would you solve this using infrastructure as code?</summary><br><b>

**Options:**
- `A. Implement a ticketing workflow that makes engineers submit a ticket before manually provisioning and configuring a resource`
- `B. Implement a checklist that engineers can follow when configuring compute instances`
- `C. Replace the compute instance type with a larger version to reduce the number of required deployments`
- `D. Build a provisioning pipeline that deploys infrastructure configurations committed to your version control system, following code reviews`

**Correct Answer:** `D. Build a provisioning pipeline that deploys infrastructure configurations committed to your version control system, following code reviews`

**Explanation**:  
Using infrastructure as code (IaC) encourages consistent deployment by:
- Storing configuration in version control systems for better collaboration and traceability.
- Automating provisioning pipelines to ensure all resources are deployed in a standardized and repeatable manner.
- Enabling code reviews to ensure all infrastructure changes are reviewed and approved before deployment.

This approach minimizes human error and ensures reliability during deployments.

</b></details>

<details>
<summary>terraform init initializes a sample main.tf file in the current directory.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation**:  
The `terraform init` command initializes a working directory with all the necessary files for Terraform to manage infrastructure. It downloads provider plugins, sets up the backend, and prepares the directory for running Terraform commands. However, it does **not** create a `main.tf` file or any configuration files. Users must write their own `.tf` configuration files manually or copy them into the directory.

</b></details>

<details>
<summary>Which two steps are required to provision new infrastructure in the Terraform workflow? (Choose two.)</summary><br><b>

**Options:**
- `A. Destroy`
- `B. Apply`
- `C. Import`
- `D. Init`
- `E. Validate`

**Correct Answer:** `B. Apply`  
`D. Init`

**Explanation**:  
To provision new infrastructure using Terraform, the following steps are required:  
1. **Init (`terraform init`)**: Initializes the working directory by downloading necessary provider plugins and preparing the backend for state management.  
2. **Apply (`terraform apply`)**: Executes the Terraform configuration to create or modify infrastructure resources.  

Other steps like `terraform validate` or `terraform import` are not mandatory for provisioning new infrastructure, while `terraform destroy` is used for removing resources.

**Reference**:  
[Terraform Core Workflow Guide](https://www.terraform.io/guides/core-workflow.html)

</b></details>

<details>
<summary>Why would you use the terraform taint command?</summary><br><b>

**Options:**
- `A. When you want to force Terraform to destroy a resource on the next apply`
- `B. When you want to force Terraform to destroy and recreate a resource on the next apply`
- `C. When you want Terraform to ignore a resource on the next apply`
- `D. When you want Terraform to destroy all the infrastructure in your workspace`

**Correct Answer:** `B. When you want to force Terraform to destroy and recreate a resource on the next apply`

**Explanation**:  
The `terraform taint` command is used to manually mark a resource as tainted. A tainted resource will be destroyed and recreated on the next `terraform apply`. This is useful in cases where a resource needs to be replaced due to corruption, misconfiguration, or a manual override.

**Reference**:  
[Terraform Taint Command Documentation](https://www.terraform.io/docs/cli/commands/taint.html)

</b></details>

<details>
<summary>Terraform requires the Go runtime as a prerequisite for installation.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Explanation**:  
Terraform is written in the Go programming language, and the Go runtime is required for its development and installation processes. However, for simply using Terraform as an end-user, the Go runtime is not required, as Terraform distributions include precompiled binaries.

</b></details>

<details>
<summary>When should you use the force-unlock command?</summary><br><b>

**Options:**
- `A. You see a status message that you cannot acquire the lock`
- `B. You have a high priority change`
- `C. Automatic unlocking failed`
- `D. apply failed due to a state lock`

**Correct Answer:** `C. Automatic unlocking failed`

**Explanation**:  
The `terraform force-unlock` command is used to manually unlock a Terraform state that is locked. This is typically required when automatic unlocking fails due to unexpected scenarios, such as a crash or a stale lock held by a previous operation. Use this command cautiously to avoid corrupting the state file.

**Reference**:  
[Terraform Force Unlock Command Documentation](https://www.terraform.io/docs/cli/commands/force-unlock.html)

</b></details>


<details>
<summary>Terraform can import modules from a number of sources – which of the following is not a valid source?</summary><br><b>

**Options:**
- `A. FTP server`
- `B. GitHub repository`
- `C. Local path`
- `D. Terraform Module Registry`

**Correct Answer:** `A. FTP server`

**Explanation**:  
Terraform supports importing modules from various sources, including:
- **GitHub repository:** Sources hosted on Git or other version control systems.
- **Local path:** Local files and directories.
- **Terraform Module Registry:** A centralized location for reusable Terraform modules.

However, Terraform does not support pulling modules from an **FTP server**, making it an invalid source.

</b></details>

<details>
<summary>Which of the following is available only in Terraform Enterprise or Cloud workspaces and not in Terraform CLI?</summary><br><b>

**Options:**
- `A. Secure variable storage`
- `B. Support for multiple cloud providers`
- `C. Dry runs with terraform plan`
- `D. Using the workspace as a data source`

**Correct Answer:** `A. Secure variable storage`

**Explanation**:  
Secure storage of sensitive variables is a feature exclusive to Terraform Cloud and Terraform Enterprise. This enables users to store and manage variables securely using encryption. 

Other features, such as support for multiple cloud providers, `terraform plan` for dry runs, and workspaces as a data source, are available in the Terraform CLI and are not limited to Terraform Cloud or Enterprise.

</b></details>

