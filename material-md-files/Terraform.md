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

<details>
<summary>terraform validate validates the syntax of Terraform files.</summary><br><b>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Explanation**:  
The `terraform validate` command is used to validate the syntax and arguments of Terraform configuration files. It checks whether the configuration is syntactically valid and internally consistent but does not interact with any APIs or create any resources.

**Reference**:  
[Terraform Validate Command Documentation](https://www.terraform.io/docs/cli/code/index.html)

</b></details>

<details>
<summary>You have used Terraform to create an ephemeral development environment in the cloud and are now ready to destroy all the infrastructure described by your Terraform configuration. To be safe, you would like to first see all the infrastructure that will be deleted by Terraform. Which command should you use to show all of the resources that will be deleted? (Choose two.)</summary><br><b>

**Options:**
- `A. Run terraform plan -destroy.`
- `B. This is not possible. You can only show resources that will be created.`
- `C. Run terraform state rm *.`
- `D. Run terraform destroy and it will first output all the resources that will be deleted before prompting for approval.`

**Correct Answer:** `A. Run terraform plan -destroy.`  
`D. Run terraform destroy and it will first output all the resources that will be deleted before prompting for approval.`

**Explanation**:  
- **`terraform plan -destroy`**: This command creates and displays an execution plan for destroying resources. It allows you to review the resources that will be deleted without actually destroying them.
- **`terraform destroy`**: This command prompts for confirmation and outputs all the resources that will be destroyed before performing the action, allowing you to review the list of resources.

**Incorrect Options:**
- **B**: It is possible to preview deletions with the correct commands.
- **C**: `terraform state rm` is used to remove resources from the state file without affecting the actual infrastructure, not to preview deletions.

**Reference**:  
[Terraform State RM Command Documentation](https://www.terraform.io/docs/cli/commands/state/rm.html)

</b></details>

<details>
<summary>Which of the following is the correct way to pass the value in the variable `num_servers` into a module with the input `servers`?</summary>

**Options:**
- `A. servers = num_servers`
- `B. servers = variable.num_servers`
- `C. servers = var(num_servers)`
- `D. servers = var.num_servers`

**Correct Answer:** `D. servers = var.num_servers`

**Explanation**:  
- **`servers = var.num_servers`**: In Terraform, variables are referenced using the `var.` prefix, followed by the variable name (`num_servers`). This is the correct syntax for passing a variable value to module inputs or other configuration blocks.
  
**Incorrect Options:**  
- **A**: Directly referencing `num_servers` without the `var.` prefix is invalid in Terraform syntax.  
- **B**: Using `variable.num_servers` is incorrect because `variable` is not the correct usage in this context for variables in Terraform.  
- **C**: Syntax like `var(num_servers)` is not recognized in Terraform; parentheses are not used for variable referencing.

**Reference**:  
[Terraform Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>A Terraform provisioner must be nested inside a resource configuration block.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Explanation**:  
Most provisioners in Terraform require access to the remote resource (typically using SSH or WinRM protocols) and must be defined within a resource block. Provisioners enable you to execute scripts or perform configuration tasks on the resources after they are created. Additionally, the resource block often includes a nested connection block to specify details about how Terraform communicates with the resource.

**Reference**:  
[Terraform Provisioners Documentation](https://www.terraform.io/docs/language/resources/provisioners/connection.html)

</details>

<details>
<summary>Terraform can run on Windows or Linux, but it requires a Server version of the Windows operating system.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation**:  
Terraform does not require a Server version of the Windows operating system to run. It is supported on both Windows (including non-server versions), Linux, and macOS. Terraform is a lightweight binary and works across multiple operating systems without requiring specialized versions.

**Reference**:  
[Terraform Downloads and Platform Support](https://developer.hashicorp.com/terraform/downloads)

</details>

<details>
<summary>What does the default "local" Terraform backend store?</summary>

**Options:**
- `A. tfplan files`
- `B. Terraform binary`
- `C. Provider plugins`
- `D. State file`

**Correct Answer:** `D. State file`

**Explanation**:  
The default "local" backend in Terraform is responsible for storing the state file on the local filesystem. The state file tracks the current state of the infrastructure managed by Terraform and is critical for operations like detecting changes and applying updates. Additionally, the local backend locks the state during updates using system APIs to prevent concurrent modifications.

**Reference**:  
[Terraform Local Backend Documentation](https://www.terraform.io/docs/language/settings/backends/local.html)

</details>

<details>
<summary>You have multiple team members collaborating on infrastructure as code (IaC) using Terraform, and want to apply formatting standards for readability. How can you format Terraform HCL (HashiCorp Configuration Language) code according to standard Terraform style convention?</summary>

**Options:**
- `A. Run the terraform fmt command during the code linting phase of your CI/CD process`
- `B. Designate one person in each team to review and format everyone's code`
- `C. Manually apply two spaces indentation and align equal sign "=" characters in every Terraform file (*.tf)`
- `D. Write a shell script to transform Terraform files using tools such as AWK, Python, and sed`

**Correct Answer:** `A. Run the terraform fmt command during the code linting phase of your CI/CD process`

**Explanation**:  
The `terraform fmt` command automatically formats Terraform code (*.tf files) to follow the standard style convention defined by Terraform. It ensures uniform indentation and alignment, making the code consistent and readable for all team members. Running this command regularly as part of the CI/CD process helps enforce code formatting across the team without requiring manual intervention.

**Incorrect Options:**
- **B**: Designating someone to manually review and format code is time-consuming and error-prone.
- **C**: Manually formatting is inefficient and prone to inconsistencies.
- **D**: Writing custom scripts is unnecessary since Terraform provides the `fmt` command for this purpose.

**Reference**:  
[Terraform Formatting Documentation](https://developer.hashicorp.com/terraform/cli/commands/fmt)

</details>

<details>
<summary>What value does the Terraform Cloud/Terraform Enterprise private module registry provide over the public Terraform Module Registry?</summary>

**Options:**
- `A. The ability to share modules with public Terraform users and members of Terraform Enterprise Organizations`
- `B. The ability to tag modules by version or release`
- `C. The ability to restrict modules to members of Terraform Cloud or Enterprise organizations`
- `D. The ability to share modules publicly with any user of Terraform`

**Correct Answer:** `C. The ability to restrict modules to members of Terraform Cloud or Enterprise organizations`

**Explanation**:  
The private module registry in Terraform Cloud or Enterprise provides the capability to securely host and manage private modules. Unlike the public module registry, the private module registry allows you to restrict access to modules so that only authenticated members of specific Terraform Cloud or Enterprise organizations can fetch and use them. This is particularly useful for sensitive or proprietary infrastructure code.

**Incorrect Options:**
- **A**: Modules in the private registry are not shared publicly or with public Terraform users.
- **B**: Module versioning is supported in both public and private registries, but it is not unique to the private registry.
- **D**: The private module registry does not allow public sharing; it is specifically used for organizational access control.

**Reference**:  
[Terraform Private Module Registry](https://developer.hashicorp.com/terraform/cloud-docs/registry)

</details>

<details>
<summary>Which task does terraform init <u>not</u> perform?</summary>

**Options:**
- `A. Sources all providers present in the configuration and ensures they are downloaded and available locally`
- `B. Connects to the backend`
- `C. Sources any modules and copies the configuration locally`
- `D. Validates all required variables are present`

**Correct Answer:** `D. Validates all required variables are present`

**Explanation**:  
The `terraform init` command is used to initialize a working directory containing a Terraform configuration. It handles tasks such as downloading providers, setting up the backend, and sourcing any modules used in the configuration. However, it does not validate the presence of required variables during initialization. Variable validation occurs at the `terraform plan` or `terraform apply` stages.

**Incorrect Options:**
- **A**: `terraform init` sources and downloads providers defined in the configuration.
- **B**: It connects to the backend to allow for remote state storage if a backend is configured.
- **C**: It fetches and copies any external modules defined in the configuration.

**Reference**:  
[Terraform Init Command Documentation](https://www.terraform.io/docs/cli/commands/init.html)

</details>

<details>
<summary>You have declared a variable called `var.list` which is a list of objects that all have an attribute `id`. Which options will produce a list of the IDs? (Choose two.)</summary>

**Options:**
- `A. { for o in var.list : o => o.id }`
- `B. var.list[*].id`
- `C. [ var.list[*].id ]`
- `D. [ for o in var.list : o.id ]`

**Correct Answers:** `B. var.list[*].id` and `D. [ for o in var.list : o.id ]`

**Explanation**:  
- **`B. var.list[*].id`**: This uses Terraform's splat expression syntax to create a list of the `id` attributes from all objects in the `var.list`. The `[*].id` extracts the `id` for each element in the list.
  
- **`D. [ for o in var.list : o.id ]`**: This uses Terraform's for expressions to loop over each object in `var.list` and extract the `id` attribute, returning a new list of the `id` values.

**Incorrect Options:**
- **A**: This syntax is incorrect. The use of `{}` creates a map, not a list, and `=>` is not valid syntax in Terraform for constructing a map.
- **C**: This syntax wraps the splat expression in additional brackets, producing a list containing a single element, which is itself another list. It does not flatten into a list of `id` values.

**Reference**:  
[Terraform Expressions Documentation](https://developer.hashicorp.com/terraform/language/expressions)

</details>

<details>
<summary>Which argument(s) is (are) required when declaring a Terraform variable?</summary>

**Options:**
- `A. type`
- `B. default`
- `C. description`
- `D. All of the above`
- `E. None of the above`

**Correct Answer:** `E. None of the above`

**Explanation**:  
When declaring a Terraform variable, none of the arguments (`type`, `default`, `description`) are strictly required. Terraform can infer the type of a variable based on its value or usage, and a default value or description is optional. If a variable does not have a default value, Terraform treats it as mandatory and expects the user to provide a value either via input or a `.tfvars` file.

**Incorrect Options:**
- **A. type**: While defining the type explicitly is helpful for clarity, it is not mandatory since Terraform can infer the type.
- **B. default**: Providing a default value is optional. Without a default, the variable must be supplied as input.
- **C. description**: The description is purely informative and optional.
- **D. All of the above**: None of these are mandatory.

**Reference**:  
[Terraform Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>When using a module block to reference a module stored on the public Terraform Module Registry, how do you specify version 1.0.0?</summary>

**Options:**
- `A. Modules stored on the public Terraform Module Registry do not support versioning`
- `B. Append ?ref=v1.0.0 argument to the source path`
- `C. Add version = "1.0.0" attribute to module block`
- `D. Nothing – modules stored on the public Terraform Module Registry always default to version 1.0.0`

**Correct Answer:** `C. Add version = "1.0.0" attribute to module block`

**Explanation**:  
When referencing modules stored on the public Terraform Module Registry (e.g., `hashicorp/consul/aws`), you specify the desired module version using the `version` argument in the module block. This ensures Terraform fetches and uses the correct version of the module, maintaining version control and consistency across deployments.

**Incorrect Options:**
- **A.** Modules in the public registry support versioning via the `version` attribute.
- **B.** While appending `?ref=v1.0.0` is commonly used with Git source URLs, it is not applicable for modules from the public Terraform Module Registry.
- **D.** Modules do not default to version 1.0.0 unless explicitly specified.

</details>


<details>
<summary>What features does the hosted service Terraform Cloud provide? (Choose two)</summary>

**Options:**
- `A. Automated infrastructure deployment visualization`
- `B. Automatic backups`
- `C. Remote state storage`
- `D. A web-based user interface (UI)`

**Correct Answers:** `C. Remote state storage` and `D. A web-based user interface (UI)`

**Explanation**:  
Terraform Cloud offers the following key features:  
- **Remote state storage (C):** Terraform Cloud provides centralized state storage, making it easier to collaborate in a team environment by ensuring that state is securely stored and shared across team members.
- **Web-based user interface (D):** Terraform Cloud includes a web UI for managing workspaces, user access, state versions, and other administrative controls.

**Incorrect Options:**
- **A.** Terraform Cloud does not provide automated infrastructure deployment visualization as a built-in feature.
- **B.** While Terraform manages state safely, it does not provide general-purpose automatic backup functionality as a specific feature.

**References:**  
- [Terraform Cloud Remote State Documentation](https://www.terraform.io/docs/language/state/remote.html)  
- [Terraform Cloud Overview](https://www.terraform.io/cloud)

</details>

<details>
<summary>Where does the Terraform local backend store its state?</summary>

**Options:**
- `A. In the /tmp directory`
- `B. In the terraform file`
- `C. In the terraform.tfstate file`
- `D. In the user's terraform.state file`

**Correct Answer:** `C. In the terraform.tfstate file`

**Explanation**:  
The local backend stores the Terraform state file in a file named `terraform.tfstate` on the local filesystem. This file represents the current state of the infrastructure managed by Terraform. The state file is crucial for tracking resources, as it allows Terraform to know which resources already exist and whether changes need to be applied during future runs.

**Incorrect Options:**
- **A.** The `/tmp` directory is not used for state storage by default in Terraform.  
- **B.** Terraform configurations are written in `.tf` files, but the state is not stored in these files.  
- **D.** The state file is named `terraform.tfstate`, not `terraform.state`.  

**Reference:**  
[Terraform Local Backend Documentation](https://www.terraform.io/docs/language/settings/backends/local.html)

</details>

<details>
<summary>Which option can not be used to keep secrets out of Terraform configuration files?</summary>

**Options:**
- `A. A Terraform provider`
- `B. Environment variables`
- `C. A -var flag`
- `D. secure string`

**Correct Answer:** `D. secure string`

**Explanation**:  
Terraform does not natively support a "secure string" type as a method to securely manage sensitive information directly in configuration files. Instead, secrets should be managed via other mechanisms, such as:  
- **Using environment variables (B):** You can set sensitive data like credentials in environment variables and use `TF_VAR_` prefixes to reference them in configurations.  
- **Using the `-var` flag (C):** You can pass sensitive values at runtime via the `-var` flag when running commands like `terraform plan` or `terraform apply`.  
- **Through a Terraform provider (A):** Some providers enable integration with secret management systems (e.g., AWS Secrets Manager, HashiCorp Vault).

**Incorrect Option:**
- **D. secure string:** This is not a Terraform feature or supported mechanism to secure secrets.

**Reference:**  
[Terraform Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)

</details>

<details>
<summary>What is one disadvantage of using dynamic blocks in Terraform?</summary>

**Options:**
- `A. They cannot be used to loop through a list of values`
- `B. Dynamic blocks can construct repeatable nested blocks`
- `C. They make configuration harder to read and understand`
- `D. Terraform will run more slowly`

**Correct Answer:** `C. They make configuration harder to read and understand`

**Explanation**:  
Dynamic blocks are a powerful feature in Terraform that allow you to generate nested blocks programmatically, typically by looping through a list of values. However, their main disadvantage is that they can reduce the readability and clarity of the configuration, especially for users unfamiliar with the `dynamic` syntax. Clear and readable configurations are generally preferred for collaboration and maintainability.

**Incorrect Options:**
- **A.** Dynamic blocks can absolutely be used to loop through a list of values, which is one of their primary use cases.  
- **B.** This statement is true, but it is not a disadvantage; it's a core feature of dynamic blocks.  
- **D.** Using dynamic blocks does not have a significant impact on Terraform's runtime performance.

**Reference:**  
[Terraform Dynamic Blocks Documentation](https://developer.hashicorp.com/terraform/language/expressions/dynamic)

</details>

<details>
<summary>Only the user that generated a plan may apply it.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation**:  
Terraform does not require the same user who generated a plan to apply it. Terraform separates the `plan` and `apply` steps, but the saved plan file (`terraform plan -out=<file>`) can be used by any user with appropriate access to apply the changes. This flexibility allows teams to collaborate effectively, enabling one user to generate the plan and another user to apply it.

**Incorrect Options:**
- **A. True:** This is incorrect; there is no restriction that limits the application of a saved plan file to the same user who generated it.

**Reference:**  
[Terraform Plan and Apply Workflow Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)

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

- A. aws_ami.ubuntu
- B. data.aws_ami.ubuntu
- C. data.aws_ami.ubuntu.id
- D. aws_ami.ubuntu.id

**Correct Answer:** C. data.aws_ami.ubuntu.id

Explanation:
When referencing a data source in Terraform, you need to use the data.<type>.<name> syntax. To retrieve the id of the AMI from the aws_ami data source, the correct property is id. Thus, the correct reference for the ami attribute is data.aws_ami.ubuntu.id.

</details>

<details>
<summary>You need to specify a dependency manually. What resource meta-parameter can you use to make sure Terraform respects the dependency?</summary>

**Correct Answer:** `depends_on`

**Explanation**:  
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
<summary>You have created a new virtual machine (VM) using Terraform and want to delete it. What should you do to delete the newly-created VM with Terraform?</summary>

**Options:**
- `A. The Terraform state file contains all 16 VMs in the team account. Execute terraform destroy and select the newly-created VM.`
- `B. The Terraform state file only contains the one new VM. Execute terraform destroy.`
- `C. Delete the Terraform state file and execute terraform apply.`
- `D. Delete the VM using the cloud provider console and terraform apply to apply the changes to the Terraform state file.`

**Correct Answer:** `B. The Terraform state file only contains the one new VM. Execute terraform destroy.`

**Explanation**:  
Terraform manages resources defined in your configuration using the state file. Since the state file for this configuration only tracks the newly-created VM, you can run `terraform destroy`. This command will use the state file to identify and delete the resources it manages—in this case, the one VM created by Terraform. There is no need to delete resources manually or interfere with the state file.

**Incorrect Options:**
- **A:** The Terraform state file does not include unmanaged resources (e.g., the other 15 VMs created outside of Terraform), so destroying all resources is unnecessary in this context.  
- **C:** Deleting the state file would remove Terraform's ability to manage existing resources, such as the VM. This is not recommended.  
- **D:** Using the cloud provider console to delete resources manually may leave the Terraform state file out of sync with the actual infrastructure unless properly reconciled, which requires additional steps.

**Reference:**  
[Terraform Destroy Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/destroy)

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

- A. dev
- B. azurerm_resource_group
- C. azurerm
- D. test

**Correct Answer:** A. dev

Explanation:
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
<summary>Setting the `TF_LOG` environment variable to `DEBUG` causes debug messages to be logged into syslog.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation**:  
The `TF_LOG` environment variable controls Terraform's log level, such as `TRACE`, `DEBUG`, `INFO`, `WARN`, or `ERROR`. When set to `DEBUG`, debug messages are displayed directly in the terminal or the log file specified, but they are not logged into syslog. Terraform does not integrate directly with syslog for logging purposes. 

To redirect the log messages to a specific destination, such as a file, you can use output redirection.

**Incorrect Option:**
- **A. True:** This is incorrect because Terraform debug messages are not logged into syslog automatically.

**Reference:**  
[Terraform Debugging Workflow Documentation](https://developer.hashicorp.com/terraform/internals/debugging)

</details>

<details>
<summary>Where in your Terraform configuration do you specify a state backend?</summary>

**Options:**
- `A. The terraform block`
- `B. The resource block`
- `C. The provider block`
- `D. The data source block`

**Correct Answer:** `A. The terraform block`

**Explanation**:  
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
<summary>Outside of the `required_providers` block, Terraform configurations always refer to providers by their local names.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Explanation**:  
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
<summary>What command should you run to display all workspaces for the current configuration?</summary>

**Options:**
- `A. terraform workspace`
- `B. terraform workspace show`
- `C. terraform workspace list`
- `D. terraform show workspace`

**Correct Answer:** `C. terraform workspace list`

**Explanation**:  
The `terraform workspace list` command is used to display all existing workspaces for the current configuration. Workspaces in Terraform allow you to manage multiple states for the same configuration, such as for different environments (e.g., dev, staging, production).

**Example Command:**
```bash
terraform workspace list
```
</details>

<details>
<summary>Terraform providers are always installed from the Internet.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation:**  
Terraform configurations must declare which providers they require, so that Terraform can install and use them. Providers can also be installed locally if needed, rather than retrieving them from the Internet.

**Reference:**  
[Terraform Provider Configuration Documentation](https://www.terraform.io/docs/language/providers/configuration.html)

</details>

<details>
<summary>Which of these is the best practice to protect sensitive values in state files?</summary>

**Options:**
- `A. Blockchain`
- `B. Secure Sockets Layer (SSL)`
- `C. Enhanced remote backends`
- `D. Signed Terraform providers`

**Correct Answer:** `C. Enhanced remote backends`

**Explanation:**  
Use of remote backends, and especially the availability of Terraform Cloud, ensures state encryption at rest and avoids storing state in clear text on local machines. Remote backends are the best practice for protecting sensitive data in state files.

**Reference:**  
[Terraform Best Practices for Sensitive State](https://www.terraform.io/docs/extend/best-practices/sensitive-state.html)

</details>

<details>
<summary>When does `terraform apply` reflect changes in the cloud environment?</summary>

**Options:**
- `A. Immediately`
- `B. However long it takes the resource provider to fulfill the request`
- `C. After updating the state file`
- `D. Based on the value provided to the -refresh command line argument`
- `E. None of the above`

**Correct Answer:** `B. However long it takes the resource provider to fulfill the request`

**Explanation:**  
When `terraform apply` is executed, Terraform sends requests to the resource provider (e.g., AWS, Azure) to create, update, or delete infrastructure. The time it takes for changes to reflect in the cloud environment depends on how long the resource provider needs to fulfill those requests. This process can vary depending on the type of resource and the provider's performance.

**Reference:**  
[Terraform Apply Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)

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

- A. element(aws_instance.web, 2)
- B. aws_instance.web[1].name
- C. aws_instance.web[1]
- D. aws_instance.web[2].name
- E. aws_instance.web.*.name

**Correct Answer:** 
- B. aws_instance.web[1].name

</details>

<details>
<summary>A Terraform provider is <u>not</u> responsible for:</summary>

**Options:**
- `A. Understanding API interactions with some service`
- `B. Provisioning infrastructure in multiple clouds`
- `C. Exposing resources and data sources based on an API`
- `D. Managing actions to take based on resource differences`

**Correct Answer:** `B. Provisioning infrastructure in multiple clouds`

</details>

<details>
<summary>Terraform provisioners can be added to any resource block.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Reference:**  
[Terraform Provisioners Documentation](https://www.terraform.io/docs/language/resources/provisioners/syntax.html)

</details>

<details>
<summary>What is `terraform refresh` intended to detect?</summary>

**Options:**
- `A. Terraform configuration code changes`
- `B. Empty state files`
- `C. State file drift`
- `D. Corrupt state files`

**Correct Answer:** `C. State file drift`

**Reference:**  
[Detecting and Managing Drift with Terraform](https://www.hashicorp.com/blog/detecting-and-managing-drift-with-terraform)

</details>

<details>
<summary>What is the name of the flag you would add to `terraform plan` to save the execution plan to a file?</summary>

**Correct Answer:** `-out=FILENAME`

**Reference:**  
[Terraform Plan Command Documentation](https://www.terraform.io/docs/cli/commands/plan.html)

</details>

<details>
<summary>What is the name of the default file where Terraform stores the state?</summary>

**Correct Answer:** `terraform.tfstate`

**Reference:**  
[Terraform State Documentation](https://www.terraform.io/docs/language/state/index.html)

</details>

<details>
<summary>A Terraform local value can reference other Terraform local values.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

**Reference:**  
[Terraform Local Values Documentation](https://www.terraform.io/docs/configuration-0-11/locals.html)

</details>

<details>
<summary>Which of the following is <u>not</u> a valid Terraform collection type?</summary>

**Options:**
- `A. list`
- `B. map`
- `C. tree`
- `D. set`

**Correct Answer:** `C. tree`

**Reference:**  
[Terraform Type Constraints Documentation](https://www.terraform.io/docs/language/expressions/type-constraints.html)

</details>

<details>
<summary>When running the command `terraform taint` against a managed resource you want to force recreation upon, Terraform will immediately destroy and recreate the resource.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Reference:**  
[Terraform Taint and Untaint Explained](https://www.devopsschool.com/blog/terraform-taint-and-untaint-explained-with-example-programs-and-tutorials/)

</details>

<details>
<summary>All standard backend types support state storage, locking, and remote operations like plan, apply, and destroy.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

</details>

<details>
<summary>How can `terraform plan` aid in the development process?</summary>

**Options:**
- `A. Validates your expectations against the execution plan without permanently modifying state`
- `B. Initializes your working directory containing your Terraform configuration files`
- `C. Formats your Terraform configuration files`
- `D. Reconciles Terraform’s state against deployed resources and permanently modifies state using the current status of deployed resources`

**Correct Answer:** `A. Validates your expectations against the execution plan without permanently modifying state`

**Reference:**  
[GitHub: Terraform Issues](https://github.com/hashicorp/terraform/issues/19235)

</details>

<details>
<summary>You would like to reuse the same Terraform configuration for your development and production environments with a different state file for each. Which command would you use?</summary>

**Options:**
- `A. terraform import`
- `B. terraform workspace`
- `C. terraform state`
- `D. terraform init`

**Correct Answer:** `B. terraform workspace`

</details>

<details>
<summary>What is the name assigned by Terraform to reference this resource?</summary>

**Configuration:**
```hcl
resource "google_compute_instance" "main" {
  name = "test"
}
```
**Options:**

- A. compute_instance
- B. main
- C. google
- D. test

**Correct Answer:** 
- B. main

</details>

<details>
<summary>You’re building a CI/CD pipeline and need to inject sensitive variables into your Terraform run. How can you do this safely?</summary>

**Options:**
- `A. Pass variables to Terraform with a -var flag`
- `B. Copy the sensitive variables into your Terraform code`
- `C. Store the sensitive variables in a secure_vars.tf file`
- `D. Store the sensitive variables as plain text in a source code repository`

**Correct Answer:** `A. Pass variables to Terraform with a -var flag`

</details>

<details>
<summary>Your security team scanned some Terraform workspaces and found secrets stored in plaintext in state files. How can you protect that data?</summary>

**Options:**
- `A. Delete the state file every time you run Terraform`
- `B. Store the state in an encrypted backend`
- `C. Edit your state file to scrub out the sensitive data`
- `D. Always store your secrets in a secrets.tfvars file`

**Correct Answer:** `B. Store the state in an encrypted backend`

**Reference:**  
[Terraform Sensitive Data in State Documentation](https://www.terraform.io/docs/language/state/sensitive-data.html)

</details>

<details>
<summary>In contrast to Terraform Open Source, when working with Terraform Enterprise and Cloud Workspaces, conceptually you could think about them as completely separate working directories.</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `A. True`

</details>

<details>
<summary>You want to know from which paths Terraform is loading providers referenced in your Terraform configuration (*.tf files). You need to enable debug messages to find this out. Which of the following would achieve this?</summary>

**Options:**
- `A. Set the environment variable TF_LOG=TRACE`
- `B. Set verbose logging for each provider in your Terraform configuration`
- `C. Set the environment variable TF_VAR_log=TRACE`
- `D. Set the environment variable TF_LOG_PATH`

**Correct Answer:** `A. Set the environment variable TF_LOG=TRACE`

**Reference:**  
[Terraform Environment Variables Documentation](https://www.terraform.io/docs/cli/config/environment-variables.html)

</details>

<details>
<summary>How is `terraform import` run?</summary>

**Options:**
- `A. As a part of terraform init`
- `B. As a part of terraform plan`
- `C. As a part of terraform refresh`
- `D. By an explicit call`
- `E. All of the above`

**Correct Answer:** `D. By an explicit call`

</details>

<details>
<summary>You have a simple Terraform configuration containing one virtual machine (VM) in a cloud provider. You run `terraform apply` and the VM is created successfully. What will happen if you delete the VM using the cloud provider console and run `terraform apply` again without changing any Terraform code?</summary>

**Options:**
- `A. Terraform will remove the VM from the state file`
- `B. Terraform will report an error`
- `C. Terraform will not make any changes`
- `D. Terraform will recreate the VM`

**Correct Answer:** `D. Terraform will recreate the VM`

</details>

<details>
<summary>Which of these options is the <u>most secure</u> place to store secrets for connecting to a Terraform remote backend?</summary>

**Options:**
- `A. Defined in Environment variables`
- `B. Inside the backend block within the Terraform configuration`
- `C. Defined in a connection configuration outside of Terraform`
- `D. None of above`

**Correct Answer:** `A. Defined in Environment variables`

</details>

<details>
<summary>Your DevOps team is currently using the local backend for your Terraform configuration. You would like to move to a remote backend to begin storing the state file in a central location. Which of the following backends would not work?</summary>

**Options:**
- `A. Amazon S3`
- `B. Artifactory`
- `C. Git`
- `D. Terraform Cloud`

**Correct Answer:** `C. Git`

</details>

<details>
<summary>Which backend does the Terraform CLI use by default?</summary>

**Options:**
- `A. Terraform Cloud`
- `B. Consul`
- `C. Remote`
- `D. Local`

**Correct Answer:** `D. Local`

**Reference:**  
[Terraform Backend Configuration Documentation](https://www.terraform.io/docs/language/settings/backends/configuration.html)

</details>

<details>
<summary>When you initialize Terraform, where does it cache modules from the public Terraform Module Registry?</summary>

**Options:**
- `A. On disk in the /tmp directory`
- `B. In memory`
- `C. On disk in the .terraform sub-directory`
- `D. They are not cached`

**Correct Answer:** `C. On disk in the .terraform sub-directory`

**Reference:**  
[Terraform Module Sources Documentation](https://www.terraform.io/docs/language/modules/sources.html)

</details>

<details>
<summary>You write a new Terraform configuration and immediately run `terraform apply` in the CLI using the local backend. Why will the apply fail?</summary>

**Options:**
- `A. Terraform needs you to format your code according to best practices first`
- `B. Terraform needs to install the necessary plugins first`
- `C. The Terraform CLI needs you to log into Terraform cloud first`
- `D. Terraform requires you to manually run terraform plan first`

**Correct Answer:** `B. Terraform needs to install the necessary plugins first`

**Explanation:**  
When you execute a Terraform command for the first time, Terraform automatically looks for the necessary provider plugins. If they are not installed, the program will fail. Running `terraform init` ensures that all required plugins are downloaded.

**Reference:**  
[Terraform CLI Commands Documentation](https://www.terraform.io/docs/cli/index.html)
</details>

<details>
<summary>What feature stops multiple admins from changing the Terraform state at the same time?</summary>

**Options:**
- `A. Version control`
- `B. Backend types`
- `C. Provider constraints`
- `D. State locking`

**Correct Answer:** `D. State locking`

**Explanation:**  
State locking ensures that only one operation modifies or accesses the state at a time. This prevents multiple admins or processes from making changes simultaneously, which could corrupt or disrupt the state file.

**Reference:**  
[Terraform State Locking Documentation](https://blog.gruntwork.io/how-to-manage-terraform-state-28f5697e68fa)
</details>

<details>
<summary>A fellow developer on your team is asking for some help in refactoring their Terraform code. They need to tell Terraform to no longer manage a specific resource. What command should be used?</summary>

**Options:**
- `A. terraform apply rm aws_instance.ubuntu[1]`
- `B. terraform state rm aws_instance.ubuntu[1]`
- `C. terraform plan rm aws_instance.ubuntu[1]`
- `D. terraform delete aws_instance.ubuntu[1]`

**Correct Answer:** `B. terraform state rm aws_instance.ubuntu[1]`

**Explanation:**  
The `terraform state rm` command removes a resource from the Terraform state without deleting the actual infrastructure. This is useful when the resource needs to be managed outside of Terraform or temporarily excluded from Terraform's management.

**Reference:**  
[Terraform State RM Command Documentation](https://www.terraform.io/docs/cli/commands/state/rm.html)
</details>

<details>
<summary>Terraform can only manage resource dependencies if you set them explicitly using the `depends_on` argument. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation:**  
Terraform automatically manages resource dependencies by analyzing the configuration and determining resource relationships based on references to other resources, data sources, or variables. The `depends_on` argument is optional and only used to explicitly define dependencies when Terraform cannot automatically infer them.

**Reference:**  
[Terraform Resource Dependencies Documentation](https://www.terraform.io/docs/language/resources/relationships.html)
</details>

<details>
<summary>A terraform apply can **not** __________ infrastructure.</summary>

**Options:**
- `A. change`
- `B. destroy`
- `C. provision`
- `D. import`

**Correct Answer:** `D. import`

**Explanation:**  
The `terraform apply` command is used to change, destroy, or provision infrastructure based on the current configuration. However, it cannot **import** existing infrastructure into the Terraform state. To import an existing resource, you must use the `terraform import` command.

**Reference:**  
[Terraform Apply Command Documentation](https://www.terraform.io/docs/cli/commands/apply.html)
[Terraform Import Command Documentation](https://www.terraform.io/docs/cli/commands/import.html)
</details>

<details>
<summary>You need to constrain the GitHub provider to version 2.1 or greater. Which of the following should you put into the Terraform configuration's provider block?</summary>

**Options:**
- `A. version >= 2.1`
- `B. version ~> 2.1`
- `C. version = "<= 2.1"`
- `D. version => 2.1`

**Correct Answer:** `A. version >= 2.1`

**Explanation:**  
To specify a version constraint in Terraform for a provider, the syntax `>= 2.1` ensures that the provider's version is 2.1 or greater. Careful consideration should be given to version constraints to avoid introducing breaking changes.

**Reference:**  
[Terraform Provider Version Constraints Documentation](https://developer.hashicorp.com/terraform/language/providers/requirements)
</details>

<details>
<summary>You just scaled your VM infrastructure and realized you set the count variable to the wrong value. You correct the value and save your change. What do you do next to make your infrastructure match your configuration?</summary>

**Options:**
- `A. Run terraform apply and confirm the planned changes`
- `B. Inspect your Terraform state because you want to change it`
- `C. Reinitialize because your configuration has changed`
- `D. Inspect all Terraform outputs to make sure they are correct`

**Correct Answer:** `A. Run terraform apply and confirm the planned changes`

**Explanation:**  
After fixing the count variable and saving the configuration, you need to run `terraform apply` to implement the changes in your infrastructure. Terraform will refresh the state, show you a proposed plan of changes, and ask for confirmation before making updates.

**Reference:**  
[Terraform Apply Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)
</details>

<details>
<summary>Terraform provisioners that require authentication can use the ______ block.</summary>

**Options:**
- `A. connection`
- `B. credentials`
- `C. secrets`
- `D. ssh`

**Correct Answer:** `A. connection`

**Explanation:**  
The `connection` block in Terraform is used for configuring the authentication settings required by provisioners. It typically includes details such as the type of connection (e.g., SSH or WinRM) along with the credentials (username, password, or private key) required to access the resource.

**Reference:**  
[Terraform Provisioner Connection Settings Documentation](https://www.terraform.io/docs/language/resources/provisioners/connection.html)
</details>

<details>
<summary>Terraform validate reports syntax check errors from which of the following scenarios?</summary>

**Options:**
- `A. Code contains tabs indentation instead of spaces`
- `B. There is missing value for a variable`
- `C. The state files do not match the current infrastructure`
- `D. None of the above`

**Correct Answer:** `D. None of the above`

**Explanation:**  
`terraform validate` checks the syntax and consistency of a Terraform configuration but does not perform validation for issues like code styling (e.g., tabs vs. spaces) or runtime errors such as missing variables or state file mismatches. These types of problems are addressed during `terraform plan` or `terraform apply` execution.

**Reference:**  
[Terraform Validate Command Documentation](https://www.terraform.io/docs/cli/commands/validate.html)
</details>

<details>
<summary>Which of the following is allowed as a Terraform variable name?</summary>

**Options:**
- `A. count`
- `B. name`
- `C. source`
- `D. version`

**Correct Answer:** `B. name`

**Explanation:**  
Terraform reserves certain keywords (e.g., `count`, `source`, `version`, `lifecycle`, etc.) for its own use, and they cannot be used as variable names. However, `name` is not a reserved keyword and can be used as a valid variable name.

**Reference:**  
[Terraform Variable Names Documentation](https://developer.hashicorp.com/terraform/language/values/variables)
</details>

<details>
<summary>What type of block is used to construct a collection of nested configuration blocks?</summary>

**Options:**
- `A. for_each`
- `B. repeated`
- `C. nesting`
- `D. dynamic`

**Correct Answer:** `D. dynamic`

**Explanation:**  
In Terraform, a `dynamic` block is used to create a collection of nested configuration blocks dynamically. This is particularly useful when the number of nested blocks or their content depends on external data. The `dynamic` block iterates over a collection and renders nested blocks based on its content.

**Reference:**  
[Terraform Dynamic Blocks Documentation](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)
</details>

<details>
<summary>Module variable assignments are inherited from the parent module and you do **not** need to explicitly set them. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation:**  
Variables in a Terraform module must be explicitly set when the module is called. They are **not** automatically inherited from the parent module. If a module variable is not provided, and no default value is defined in the module, Terraform will throw an error requiring that value to be set.

**Reference:**  
[Terraform Modules - Input Variables](https://developer.hashicorp.com/terraform/language/modules/inputs)
</details>

<details>
<summary>What is the Terraform style convention for indenting a nesting level compared to the one above it?</summary>

**Options:**
- `A. With four spaces`
- `B. With a tab`
- `C. With three spaces`
- `D. With two spaces`

**Correct Answer:** `D. With two spaces`

**Explanation:**  
The recommended style convention for Terraform code is to indent by **two spaces** for each nesting level. This helps maintain consistency across configuration files and improves readability. Tabs, four spaces, or other styles are discouraged but not technically invalid.

**Reference:**  
[Terraform Style Conventions Documentation](https://developer.hashicorp.com/terraform/language/syntax/style)
</details>

<details>
<summary>Which of the following is **not** an action performed by `terraform init`?</summary>

**Options:**
- `A. Create a sample main.tf file`
- `B. Initialize a configured backend`
- `C. Retrieve the source code for all referenced modules`
- `D. Load required provider plugins`

**Correct Answer:** `A. Create a sample main.tf file`

**Explanation:**  
The `terraform init` command is responsible for setting up the working directory. It initializes the backend for storing state, retrieves remote modules, and downloads the necessary provider plugins. However, it does **not** create any sample configuration files like `main.tf`. Users need to create configuration files manually.

**Reference:**  
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)
</details>

<details>
<summary>HashiCorp Configuration Language (HCL) supports user-defined functions. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation:**  
HCL does not support user-defined functions. It includes a set of built-in functions that allow transformation and combination of values, but it does not permit creating custom functions by users. Users can only use the predefined functions provided by Terraform.

**Reference:**  
[HCL Functions Documentation](https://developer.hashicorp.com/terraform/language/functions)
</details>

<details>
<summary>How can you trigger a run in a Terraform Cloud workspace that is connected to a Version Control System (VCS) repository?</summary>

**Options:**
- `A. Only Terraform Cloud organization owners can set workspace variables on VCS connected workspaces`
- `B. Commit a change to the VCS working directory and branch that the Terraform Cloud workspace is connected to`
- `C. Only members of a VCS organization can open a pull request against repositories that are connected to Terraform Cloud workspaces`
- `D. Only Terraform Cloud organization owners can approve plans in VCS connected workspaces`

**Correct Answer:** `B. Commit a change to the VCS working directory and branch that the Terraform Cloud workspace is connected to`

**Explanation:**  
When a Terraform Cloud workspace is connected to a VCS repository, any commits made to the specified working directory and branch automatically trigger a Terraform Cloud run. This workflow allows changes to be tracked and infrastructure updates to be automated based on version-controlled changes.

**Reference:**  
[Terraform Cloud VCS Integration Documentation](https://www.terraform.io/docs/cloud/vcs/index.html)
</details>

<details>
<summary>Terraform and Terraform providers must use the same major version number in a single configuration. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Explanation:**  
Terraform and its providers do not need to use the same major version number. Terraform Core (e.g., version 1.x) and providers (e.g., `aws` provider version 5.x) are versioned independently. Each provider version is specified and managed separately from the Terraform Core version, allowing flexibility in configuration.

**Reference:**  
[Terraform Version Constraints Documentation](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
</details>

<details>
<summary>Which statement describes a goal of infrastructure as code?</summary>

**Options:**
- `A. An abstraction from vendor specific APIs`
- `B. Write once, run anywhere`
- `C. A pipeline process to test and deliver software`
- `D. The programmatic configuration of resources`

**Correct Answer:** `D. The programmatic configuration of resources`

**Explanation:**  
Infrastructure as Code (IaC) focuses on the programmatic configuration and management of infrastructure resources through code, treating infrastructure in the same way as application code. This approach allows for versioning, consistency, and automation of infrastructure deployments.

**Reference:**  
[Infrastructure as Code Documentation](https://developer.hashicorp.com/terraform/intro)
</details>

<details>
<summary>When using Terraform to deploy resources into Azure, which scenarios are true regarding state files? (Choose two.)</summary>

**Options:**
- `A. When a change is made to the resources via the Azure Cloud Console, the changes are recorded in a new state file`
- `B. When a change is made to the resources via the Azure Cloud Console, Terraform will update the state file to reflect them during the next plan or apply`
- `C. When a change is made to the resources via the Azure Cloud Console, the current state file will not be updated`
- `D. When a change is made to the resources via the Azure Cloud Console, the changes are recorded in the current state file`

**Correct Answers:** `B, C`

**Explanation:**  
- **B:** Terraform detects changes made to resources outside of Terraform (e.g., via the Azure Cloud Console) during the next `plan` or `apply` command and updates the state file accordingly.
- **C:** The state file does not automatically update when changes are made outside of Terraform. Until a plan or apply is run, the current state file remains outdated.

**Incorrect Options:**
- **A:** Terraform does not create a new state file for changes made outside of Terraform. It uses the existing state file and updates it after detecting changes.
- **D:** Changes are not automatically reflected in the current state file when made outside of Terraform.

**Reference:**  
[Terraform State Documentation](https://developer.hashicorp.com/terraform/language/state)
</details>

<details>
<summary>You need to deploy resources into two different cloud regions in the same Terraform configuration. What meta-argument do you need to configure in a resource block to deploy the resource to the `us-west-2` AWS region?</summary>

**Options:**
- `A. alias = west`
- `B. provider = west`
- `C. provider = aws.west`
- `D. alias = aws.west`

**Correct Answer:** `C. provider = aws.west`

**Explanation:**  
When using multiple provider configurations, the `alias` argument allows you to define alternate configurations for a single provider. To specify which provider configuration a resource should use, you must include the `provider` meta-argument in your resource block. In this case, `provider = aws.west` refers to the provider configuration with the `alias = "west"` (region `us-west-2`).

**Incorrect Options:**
- `A. alias = west`: The `alias` is defined in the provider block, not in the resource block.
- `B. provider = west`: This is incorrect syntax. The provider name must be prefixed (e.g., `aws.west`).
- `D. alias = aws.west`: The `alias` keyword cannot be used in a resource block—it is used only in provider configurations.

**Reference:**  
[Terraform Multiple AWS Provider Configurations Documentation](https://developer.hashicorp.com/terraform/language/providers/configuration#multiple-provider-configurations)
</details>

<details>
<summary>You have declared an input variable called `environment` in your parent module. What must you do to pass the value to a child module in the configuration?</summary>

**Options:**
- `A. Add node_count = var.node_count`
- `B. Declare the variable in a terraform.tfvars file`
- `C. Declare a node_count input variable for the child module`
- `D. Nothing, child modules inherit variables of parent module`

**Correct Answer:** `C. Declare a node_count input variable for the child module`

**Reference:**  
[Terraform Modules - Input Variables](https://developer.hashicorp.com/terraform/language/modules/inputs)
</details>

<details>
<summary>If a module declares a variable with a default, that variable must also be defined within the module. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Reference:**  
[Terraform Input Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)
</details>

<details>
<summary>Which option cannot be used to keep secrets out of Terraform configuration files?</summary>

**Options:**
- `A. Environment Variables`
- `B. Mark the variable as sensitive`
- `C. A Terraform provider`
- `D. -var flag`

**Correct Answer:** `C. A Terraform provider`

**Reference:**  
[Terraform Input Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)
</details>

<details>
<summary>Which of the following arguments are required when declaring a Terraform output?</summary>

**Options:**
- `A. sensitive`
- `B. description`
- `C. default`
- `D. value`

**Correct Answer:** `D. value`

**Reference:**  
[Terraform Output Values Documentation](https://developer.hashicorp.com/terraform/language/values/outputs)
</details>

<details>
<summary>Your risk management organization requires that new AWS S3 buckets must be private and encrypted at rest. How can Terraform Enterprise automatically and proactively enforce this security control?</summary>

**Options:**
- `A. With a Sentinel policy, which runs before every apply`
- `B. By adding variables to each TFE workspace to ensure these settings are always enabled`
- `C. With an S3 module with proper settings for buckets`
- `D. Auditing cloud storage buckets with a vulnerability scanning tool`

**Correct Answer:** `A. With a Sentinel policy, which runs before every apply`

**Reference:**  
[Terraform Sentinel Documentation](https://developer.hashicorp.com/terraform/enterprise/sentinel)
</details>

<details>
<summary>Most Terraform providers interact with _____________.</summary>

**Options:**
- `A. APIs`
- `B. VCS Systems`
- `C. Shell scripts`
- `D. None of the above`

**Correct Answer:** `A. APIs`

**Reference:**  
[Terraform Provider Documentation](https://developer.hashicorp.com/terraform/language/providers)
</details>

<details>
<summary>`terraform validate` validates that your infrastructure matches the Terraform state file. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Reference:**  
[Terraform Validate Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/validate)
</details>

<details>
<summary>What does `terraform import` allow you to do?</summary>

**Options:**
- `A. Import a new Terraform module`
- `B. Use a state file to import infrastructure to the cloud`
- `C. Import provisioned infrastructure to your state file`
- `D. Import an existing state file to a new Terraform workspace`

**Correct Answer:** `C. Import provisioned infrastructure to your state file`

**Reference:**  
[Terraform Import Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/import)
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
**Answer:**  module.vpc.vpc_id
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

- A. aws_instance.example.ebs_block_device.[*].volume_id
- B. aws_instance.example.ebs_block_device.volume_
- C. aws_instance.example.ebs_block_device[sda2, sda3].volume_id
- D. aws_instance.example.ebs_block_device.*.volume_id

**Correct Answer:**  A. aws_instance.example.ebs_block_device.[*].volume_id

</details>

<details>
<summary>What does state locking accomplish?</summary>

**Options:**
- `A. Copies the state file from memory to disk`
- `B. Encrypts any credentials stored within the state file`
- `C. Blocks Terraform commands from modifying the state file`
- `D. Prevents accidental deletion of the state file`

**Correct Answer:** `C. Blocks Terraform commands from modifying the state file`

**Reference:**  
[Terraform State Locking Documentation](https://developer.hashicorp.com/terraform/language/state/locking)
</details>

<details>
<summary>You just upgraded the version of a provider in an existing Terraform project. What do you need to do to install the new provider?</summary>

**Options:**
- `A. Run terraform apply -upgrade`
- `B. Run terraform init -upgrade`
- `C. Run terraform refresh`
- `D. Upgrade your version of Terraform`

**Correct Answer:** `B. Run terraform init -upgrade`

**Reference:**  
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)
</details>

<details>
<summary>A module can always refer to all variables declared in its parent module. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Reference:**  
[Terraform Modules Documentation](https://developer.hashicorp.com/terraform/language/modules/inputs)
</details>

<details>
<summary>When you use a remote backend that needs authentication, HashiCorp recommends that you:</summary>

**Options:**
- `A. Use partial configuration to load the authentication credentials outside of the Terraform code`
- `B. Push your Terraform configuration to an encrypted git repository`
- `C. Write the authentication credentials in the Terraform configuration files`
- `D. Keep the Terraform configuration files in a secret store`

**Correct Answer:** `A. Use partial configuration to load the authentication credentials outside of the Terraform code`

**Reference:**  
[Terraform Backend Configuration Documentation](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)
</details>

<details>
<summary>You have a simple Terraform configuration containing one virtual machine (VM) in a cloud provider. You run `terraform apply` and the VM is created successfully. What will happen if you run `terraform apply` again immediately afterwards without changing any Terraform code?</summary>

**Options:**
- `A. Terraform will terminate and recreate the VM`
- `B. Terraform will create another duplicate VM`
- `C. Terraform will apply the VM to the state file`
- `D. Nothing`

**Correct Answer:** `D. Nothing`

**Reference:**  
[Terraform Plan and Apply Workflow](https://developer.hashicorp.com/terraform/cli/commands/apply)
</details>

<details>
<summary>A junior admin accidentally deleted some of your cloud instances. What does Terraform do when you run `terraform apply`?</summary>

**Options:**
- `A. Build a completely brand new set of infrastructure`
- `B. Tear down the entire workspace infrastructure and rebuild it`
- `C. Rebuild only the instances that were deleted`
- `D. Stop and generate an error message about the missing instances`

**Correct Answer:** `C. Rebuild only the instances that were deleted`

**Reference:**  
[Terraform Apply Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)
</details>

<details>
<summary>You have created a `main.tf` Terraform configuration consisting of an application server, a database, and a load balancer. You ran `terraform apply` and all resources were created successfully. Now you realize that you do not actually need the load balancer, so you run `terraform destroy` without any flags. What will happen?</summary>

**Options:**
- `A. Terraform will destroy the application server because it is listed first in the code`
- `B. Terraform will prompt you to confirm that you want to destroy all the infrastructure`
- `C. Terraform will destroy the `main.tf` file`
- `D. Terraform will prompt you to pick which resource you want to destroy`
- `E. Terraform will immediately destroy all the infrastructure`

**Correct Answer:** `B. Terraform will prompt you to confirm that you want to destroy all the infrastructure`

**Reference:**  
[Terraform Destroy Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/destroy)
</details>

<details>
<summary>Which type of block fetches or computes information for use elsewhere in a Terraform configuration?</summary>

**Options:**
- `A. provider`
- `B. resource`
- `C. local`
- `D. data`

**Correct Answer:** `D. data`

**Reference:**  
[Terraform Data Sources Documentation](https://developer.hashicorp.com/terraform/language/data-sources)
</details>

<details>
<summary>You have just developed a new Terraform configuration for two virtual machines with a cloud provider. You would like to create the infrastructure for the first time. Which Terraform command should you run first?</summary>

**Options:**
- `A. terraform apply`
- `B. terraform plan`
- `C. terraform show`
- `D. terraform init`

**Correct Answer:** `D. terraform init`

**Reference:**  
[Terraform Init Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/init)
</details>

<details>
<summary>All modules published on the official Terraform Module Registry have been verified by HashiCorp. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Reference:**  
[Terraform Module Registry Documentation](https://registry.terraform.io/)
</details>

<details>
<summary>You must initialize a Terraform backend before it can be configured. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Reference:**  
[Terraform Backend Configuration Documentation](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)
</details>

<details>
<summary>Which of the following does `terraform apply` change after you approve the execution plan? (Choose two.)</summary>

**Options:**
- `A. Cloud infrastructure`
- `B. The .terraform directory`
- `C. The execution plan`
- `D. State file`
- `E. Terraform code`

**Correct Answers:** `A. Cloud infrastructure`, `D. State file`

**Reference:**  
[Terraform Apply Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/apply)
</details>

<details>
<summary>A Terraform backend determines how Terraform loads state and stores updates when you execute ___________.</summary>

**Options:**
- `A. apply`
- `B. taint`
- `C. destroy`
- `D. All of the above`
- `E. None of the above`

**Correct Answer:** `D. All of the above`

**Reference:**  
[Terraform Backend Documentation](https://developer.hashicorp.com/terraform/language/settings/backends)
</details>

<details>
<summary>What does Terraform use `.terraform.lock.hcl` file for?</summary>

**Options:**
- `A. Tracking provider dependencies`
- `B. There is no such file`
- `C. Preventing Terraform runs from occurring`
- `D. Storing references to workspaces which are locked`

**Correct Answer:** `A. Tracking provider dependencies`

**Reference:**  
[Terraform Dependency Lock File Documentation](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
</details>

<details>
<summary>You've used Terraform to deploy a virtual machine and a database. You want to replace this virtual machine instance with an identical one without affecting the database. What is the best way to achieve this using Terraform?</summary>

**Options:**
- `A. Use the terraform state rm command to remove the VM from state file`
- `B. Use the terraform taint command targeting the VM, then run terraform plan and terraform apply`
- `C. Use the terraform apply command without targeting the VM resources only`
- `D. Delete the Terraform VM resources from your Terraform code then run terraform apply`

**Correct Answer:** `B. Use the terraform taint command targeting the VM, then run terraform plan and terraform apply`

**Reference:**  
[Terraform Taint Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/taint)
</details>

<details>
<summary>How do you specify a module's version when publishing it to the public Terraform Module Registry?</summary>

**Options:**
- `A. The module's configuration page on the Terraform Module Registry`
- `B. Terraform Module Registry does not support versioning modules`
- `C. The release tags in the associated repo`
- `D. The module's Terraform code`

**Correct Answer:** `C. The release tags in the associated repo`

**Reference:**  
[Terraform Module Registry Versioning Documentation](https://developer.hashicorp.com/terraform/registry/modules/publish)
</details>

<details>
<summary>Terraform plan updates your state file. True or False?</summary>

**Options:**
- `A. True`
- `B. False`

**Correct Answer:** `B. False`

**Reference:**  
[Terraform Plan Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/plan)
</details>

<details>
<summary>To check if all code in a Terraform configuration with multiple modules is properly formatted without making changes, what command should be run?</summary>

**Options:**
- `A. terraform fmt -check`
- `B. terraform fmt -write=false`
- `C. terraform fmt -list -recursive`
- `D. terraform fmt -check -recursive`

**Correct Answer:** `D. terraform fmt -check -recursive`

**Reference:**  
[Terraform Fmt Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/fmt)
</details>

<details>
<summary>As a member of the operations team, you need to run a script on a virtual machine created by Terraform. Which provisioner is best to use in your Terraform code?</summary>

**Options:**
- `A. null-exec`
- `B. local-exec`
- `C. remote-exec`
- `D. file`

**Correct Answer:** `C. remote-exec`

**Reference:**  
[Terraform Remote-Exec Provisioner Documentation](https://developer.hashicorp.com/terraform/language/resources/provisioners/remote-exec)
</details>

<details>
<summary>You are using a networking module in your Terraform configuration with the name label `my_network`. When running `terraform validate`, you encounter an error: "Reference to undeclared output value". What must you do to successfully retrieve this value from your networking module?</summary>

**Options:**
- `A. Define the attribute vnet_id as a variable in the networking module`
- `B. Change the referenced value to module.my_network.outputs.vnet_id`
- `C. Define the attribute vnet_id as an output in the networking module`
- `D. Change the referenced value to my_network.outputs.vnet_id`

**Correct Answer:** `C. Define the attribute vnet_id as an output in the networking module`

**Reference:**  
[Terraform Module Output Values Documentation](https://developer.hashicorp.com/terraform/language/modules/outputs)
</details>

<details>
<summary>How can a ticket-based system slow down infrastructure provisioning and limit the ability to scale? (Choose two.)</summary>

**Options:**

- `A.` A full audit trail of the request and fulfillment process is generated  
- `B.` A request must be submitted for infrastructure changes  
- `C.` As additional resources are required, more tickets are submitted  
- `D.` A catalog of approved resources can be accessed from drop-down lists in a request form  

**Correct Answer:** `B, C`

**Reference:**  
[Infrastructure as Code Best Practices](https://developer.hashicorp.com/terraform/docs)
</details>

<details>
<summary>Which of the following statements about Terraform modules is <u>not</u> true?</summary>

**Options:**

- `A.` Modules must be publicly accessible  
- `B.` Modules can be called multiple times  
- `C.` A module is a container for one or more resources  
- `D.` Modules can call other modules  

**Correct Answer:** `A`

**Reference:**  
[Terraform Modules Overview](https://developer.hashicorp.com/terraform/language/modules)
</details>

<details>
<summary>Which Terraform collection type should you use to store key/value pairs?</summary>

**Options:**

- `A.` tuple  
- `B.` set  
- `C.` map  
- `D.` list  

**Correct Answer:** `C`

**Reference:**  
[Terraform Data Types](https://developer.hashicorp.com/terraform/language/expressions/types)
</details>

<details>
<summary>You have used Terraform to create an ephemeral development environment in the cloud and are now ready to destroy all the infrastructure described by your Terraform configuration. To be safe, you would like to first see all the infrastructure that will be deleted by Terraform. Which command should you use to show all of the resources that will be deleted? (Choose two.)</summary>

**Options:**

- `A.` Run `terraform plan -destroy`  
- `B.` Run `terraform state rm *`  
- `C.` Run `terraform destroy` and it will first output all the resources that will be deleted before prompting for approval  
- `D.` Run `terraform show -destroy`  

**Correct Answer:** `A, C`

**Reference:**  
[Terraform Destroy Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/destroy)  
[Terraform Plan Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/plan)
</details>

<details>
<summary>When do you need to explicitly execute <code>terraform refresh</code>?</summary>

**Options:**

- `A.` Before every `terraform plan`  
- `B.` Before every `terraform apply`  
- `C.` Before every `terraform import`  
- `D.` None of the above  

**Correct Answer:** `D`

**Reference:**  
[Terraform Refresh Command Documentation](https://developer.hashicorp.com/terraform/cli/commands/refresh)  
(Note: `terraform refresh` is typically not needed explicitly as `terraform plan` and `terraform apply` automatically refresh the state.)
</details>

<details>
<summary>All Terraform Cloud tiers support team management and governance.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`

</details>

<details>
<summary>What advantage does an operations team that uses infrastructure as code have?</summary>

**Options:**

- `A.` The ability to delete infrastructure  
- `B.` The ability to update existing infrastructure  
- `C.` The ability to reuse best practice configurations and settings  
- `D.` The ability to autoscale a group of servers  

**Correct Answer:** `C`

</details>

<details>
<summary>Terraform variable names are saved in the state file.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`
</details>

<details>
<summary>Terraform Cloud is available only as a paid offering from HashiCorp.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`

**Reference:**  
[Terraform Cloud Pricing](https://www.hashicorp.com/products/terraform/pricing)  
(Note: Terraform Cloud offers a free tier suitable for small teams and personal projects, with paid tiers providing additional features.)
</details>

<details>
<summary>Which of the following is <u>not</u> a way to trigger <code>terraform destroy</code>?</summary>

**Options:**

- `A.` Using the `destroy` command with auto-approve  
- `B.` Running `terraform destroy` from the correct directory and then typing "yes" when prompted in the CLI  
- `C.` Passing `--destroy` at the end of a plan request  
- `D.` Delete the state file and run `terraform apply`  

**Correct Answer:** `D`

</details>

<details>
<summary>Which of the following is <u>not</u> an advantage of using infrastructure as code operations?</summary>

**Options:**

- `A.` Self-service infrastructure deployment  
- `B.` Troubleshoot via a Linux `diff` command  
- `C.` Public cloud console configuration workflows  
- `D.` Modify a count parameter to scale resources  
- `E.` API-driven workflows  

**Correct Answer:** `C`
</details>

<details>
<summary>You're writing a Terraform configuration that needs to read input from a local file called <code>id_rsa.pub</code>. Which built-in Terraform function can you use to import the file's contents as a string?</summary>

**Options:**

- `A.` `fileset("id_rsa.pub")`  
- `B.` `filebase64("id_rsa.pub")`  
- `C.` `templatefile("id_rsa.pub")`  
- `D.` `file("id_rsa.pub")`  

**Correct Answer:** `D`
</details>

<details>
<summary>What does Terraform use providers for? (Choose three.)</summary>

**Options:**

- `A.` Provision resources for on-premises infrastructure services  
- `B.` Simplify API interactions  
- `C.` Provision resources for public cloud infrastructure services  
- `D.` Enforce security and compliance policies  
- `E.` Group a collection of Terraform configuration files that map to a single state file  

**Correct Answer:** `A, B, C`
</details>

<details>
<summary>You can reference a resource created with <code>for_each</code> using a Splat (*) expression.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`
</details>

<details>
<summary>How does Terraform determine dependencies between resources?</summary>

**Options:**

- `A.` Terraform automatically builds a resource graph based on resources, provisioners, special meta-parameters, and the state file  
- `B.` Terraform requires all dependencies between resources to be specified using the `depends_on` parameter  
- `C.` Terraform requires resources in a configuration to be listed in the order they will be created to determine dependencies  
- `D.` Terraform requires resource dependencies to be defined as modules and stored in order  

**Correct Answer:** `A`
</details>

<details>
<summary>Which parameters does <code>terraform import</code> require? (Choose two.)</summary>

**Options:**

- `A.` Path  
- `B.` Provider  
- `C.` Resource ID  
- `D.` Resource address  

**Correct Answer:** `C, D`
</details>

<details>
<summary>Once you configure a new Terraform backend with the <code>terraform backend</code> block, which command(s) should you use to migrate the state file?</summary>

**Options:**

- `A.` terraform apply  
- `B.` terraform push  
- `C.` terraform destroy, then terraform apply  
- `D.` terraform init  

**Correct Answer:** `D`
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

- A. Requires any version of the AWS provider >= 3.0 and < 4.0
- B. Requires any version of the AWS provider >= 3.0
- C. Requires any version of the AWS provider after the 3.0 major release, like 4.1
- D. Requires any version of the AWS provider > 3.0

**Correct Answer:** A
</details>

<details>
<summary>What does <code>terraform refresh</code> modify?</summary>

**Options:**

- `A.` Your cloud infrastructure  
- `B.` Your state file  
- `C.` Your Terraform plan  
- `D.` Your Terraform configuration  

**Correct Answer:** `B`
</details>

<details>
<summary>Which of the following is <u>not</u> a valid source path for specifying a module?</summary>

**Options:**

- `A.` `source = "./module?version=v1.0.0"`  
- `B.` `source = "github.com/hashicorp/example?ref=v1.0.0"`  
- `C.` `source = "./module"`  
- `D.` `source = "hashicorp/consul/aws"`  

**Correct Answer:** `A`
</details>

<details>
<summary>Which of the following is true about <code>terraform apply</code>? (Choose two.)</summary>

**Options:**

- `A.` It only operates on infrastructure defined in the current working directory or workspace  
- `B.` You must pass the output of a terraform plan command to it  
- `C.` Depending on provider specification, Terraform may need to destroy and recreate your infrastructure resources  
- `D.` By default, it does not refresh your state file to reflect current infrastructure configuration  
- `E.` You cannot target specific resources for the operation  

**Correct Answer:** `A, C`
</details>

<details>
<summary>Which of the following statements about local modules is incorrect?</summary>

**Options:**

- `A.` Local modules are not cached by the terraform init command  
- `B.` Local modules are sourced from a directory on disk  
- `C.` Local modules support versions  
- `D.` All of the above (all statements above are incorrect)  
- `E.` None of the above (all statements above are correct)  

**Correct Answer:** `C`
</details>

<details>
<summary>Which of the following is true about Terraform's implementation of infrastructure as code? (Choose two.)</summary>

**Options:**

- `A.` It is only compatible with AWS infrastructure management  
- `B.` You cannot reuse infrastructure configuration  
- `C.` You can version your infrastructure configuration  
- `D.` It requires manual configuration of infrastructure resources  
- `E.` It allows you to automate infrastructure provisioning  

**Correct Answer:** `C, E`
</details>


<details>
<summary>You need to write some Terraform code that adds 42 firewall rules to a security group. What can you use to avoid writing 42 different nested ingress config blocks by hand?</summary>

**Options:**

- `A.` A count loop  
- `B.` A for block  
- `C.` A for each block  
- `D.` A dynamic block  

**Correct Answer:** `D`
</details>

<details>
<summary>Which of the following is the safest way to inject sensitive values into a Terraform Cloud workspace?</summary>

**Options:**

- `A.` Write the value to a file and specify the file with the <code>-var-file</code> flag  
- `B.` Set a value for the variable in the UI and check the "Sensitive" check box  
- `C.` Edit the state file directly just before running <code>terraform apply</code>  
- `D.` Set the variable value on the command line with the <code>-var</code> flag  

**Correct Answer:** `B`
</details>

<details>
<summary><code>terraform apply</code> will fail if you have not run <code>terraform plan</code> first to update the plan output.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`
</details>

<details>
<summary>How would you reference the attribute "name" of this fictitious resource in HCL?</summary>

```hcl
resource "kubernetes_namespace" "example" {
  name = "test"
}
```
**Options:**

- A. resource.kubernetes_namespace.example.name
- B. kubernetes_namespace.test.name
- C. kubernetes_namespace.example.name
- D. data.kubernetes_namespace.name
- E. None of the above

**Correct Answer:** C

</details>

<details>
<summary>A Terraform output that sets the "sensitive" argument to true will not store that value in the state file.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`
</details>

<details>
<summary>Which are forbidden actions when the Terraform state file is locked? (Choose three.)</summary>

**Options:**

- `A.` terraform destroy  
- `B.` terraform fmt  
- `C.` terraform state list  
- `D.` terraform apply  
- `E.` terraform plan  
- `F.` terraform validate  

**Correct Answer:** `A, D, E`
</details>

<details>
<summary>Terraform installs its providers during which phase?</summary>

**Options:**

- `A.` Plan  
- `B.` Init  
- `C.` Refresh  
- `D.` All of the above  

**Correct Answer:** `B`
</details>

<details>
<summary>When does Sentinel enforce policy logic during a Terraform Enterprise run?</summary>

**Options:**

- `A.` Before the plan phase  
- `B.` During the plan phase  
- `C.` Before the apply phase  
- `D.` After the apply phase  

**Correct Answer:** `C`
</details>

<details>
<summary>What is the purpose of a Terraform workspace in either open source or enterprise?</summary>

**Options:**

- `A.` Workspaces allow you to manage collections of infrastructure in state files  
- `B.` A logical separation of business units  
- `C.` A method of grouping multiple infrastructure security policies  
- `D.` Provides limited access to a cloud environment  

**Correct Answer:** `A`
</details>

<details>
<summary>Which is the best way to specify a tag of <code>v1.0.0</code> when referencing a module stored in Git?</summary>

**Options:**

- `A.` Append `?ref=v1.0.0` argument to the source path  
- `B.` Add `version = "1.0.0"` parameter to module block  
- `C.` Nothing – modules stored on Git always default to version 1.0.0  
- `D.` Modules stored on GitHub do not support versioning  

**Correct Answer:** `A`
</details>

<details>
<summary>Changing the Terraform backend from the default "local" backend to a different one after doing your first <code>terraform apply</code> is:</summary>

**Options:**

- `A.` Mandatory  
- `B.` Optional  
- `C.` Impossible  
- `D.` Discouraged  

**Correct Answer:** `B`
</details>

<details>
<summary>You have modified your local Terraform configuration and ran <code>terraform plan</code> to review the changes. Simultaneously, your teammate manually modified the infrastructure component you are working on. Since you already ran <code>terraform plan</code> locally, the execution plan for <code>terraform apply</code> will be the same.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`
</details>

<details>
<summary><code>terraform apply</code> is failing with an "Access Denied" error. What next step should you take to determine the root cause of the problem?</summary>

**Options:**

- `A.` Set `TF_LOG=DEBUG`  
- `B.` Review syslog for Terraform error messages  
- `C.` Run `terraform login` to reauthenticate with the provider  
- `D.` Review `/var/log/terraform.log` for error messages  

**Correct Answer:** `A`
</details>

<details>
<summary>As a member of an operations team that uses infrastructure as code (IaC) practices, you are tasked with making a change to an infrastructure stack running in a public cloud. Which pattern would follow IaC best practices for making a change?</summary>

**Options:**

- `A.` Clone the repository containing your infrastructure code and then run the code  
- `B.` Use the public cloud console to make the change after a database record has been approved  
- `C.` Make the change programmatically via the public cloud CLI  
- `D.` Make the change via the public cloud API endpoint  
- `E.` Submit a pull request and wait for an approved merge of the proposed changes  

**Correct Answer:** `E`
</details>

<details>
<summary>What command can you run to generate DOT (Document Template) formatted data to visualize Terraform dependencies?</summary>

**Options:**

- `A.` terraform refresh  
- `B.` terraform show  
- `C.` terraform graph  
- `D.` terraform output  

**Correct Answer:** `C`
</details>

<details>
<summary>Which provider authentication method prevents credentials from being stored in the Terraform state file?</summary>

**Options:**

- `A.` Using environment variables  
- `B.` Specifying the login credentials in the provider block  
- `C.` Setting credentials as Terraform variables  
- `D.` None of the above  

**Correct Answer:** `A`
</details>

<details>
<summary>Running <code>terraform fmt</code> without any flags in a directory with Terraform configuration files will check the formatting of those files without changing their contents.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `B`
</details>

<details>
<summary><code>terraform init</code> retrieves the source code for all referenced modules.</summary>

**Options:**

- `A.` True  
- `B.` False  

**Correct Answer:** `A`
</details>

<details>
<summary>You have a Terraform configuration that defines a single virtual machine with no references to it. You have run <code>terraform apply</code> to create the resource and then removed the resource definition from your Terraform configuration file. What will happen when you run <code>terraform apply</code> in the working directory again?</summary>

**Options:**

- `A.` Nothing  
- `B.` Terraform will destroy the virtual machine  
- `C.` Terraform will error  
- `D.` Terraform will remove the virtual machine from the state file, but the resource will still exist  

**Correct Answer:** `B`
</details>

<details>
<summary>Which configuration consistency errors does <code>terraform validate</code> report?</summary>

**Options:**

- `A.` A mix of spaces and tabs in configuration files  
- `B.` Differences between local and remote state  
- `C.` Terraform module isn't the latest version  
- `D.` Declaring a resource identifier more than once  

**Correct Answer:** `D`
</details>

<details>
<summary>Where can Terraform <u>not</u> load a provider from?</summary>

**Options:**

- `A.` Source code  
- `B.` Plugins directory  
- `C.` Official HashiCorp distribution on <code>releases.hashicorp.com</code>  
- `D.` Provider plugin cache  

**Correct Answer:** `A`
</details>

<details>
<summary>Which of the following locations can Terraform use as a private source for modules? (Choose two.)</summary>

**Options:**

- `A.` Internally hosted SCM (Source Control Manager) platform  
- `B.` Public Terraform Module Registry  
- `C.` Private repository on GitHub  
- `D.` Public repository on GitHub  

**Correct Answer:** `A, C`
</details>

<details>
<summary>Why should secrets <u>not</u> be hard coded into Terraform code? (Choose two.)</summary>

**Options:**

- `A.` It makes the code less reusable.  
- `B.` Terraform code is typically stored in version control, as well as copied to the systems from which it’s run. Any of these may not have robust security mechanisms.  
- `C.` The Terraform code is copied to the target resources to be applied locally and could expose secrets if a target resource is compromised.  
- `D.` All passwords should be rotated on a quarterly basis.  

**Correct Answer:** `B, C`
</details>

<details>
<summary>If a Terraform creation-time provisioner fails, what will occur by default?</summary>

**Options:**

- `A.` The resource will not be affected, but the provisioner will need to be applied again  
- `B.` The resource will be destroyed  
- `C.` The resource will be marked as "tainted"  
- `D.` Nothing, provisioners will not show errors in the command line  

**Correct Answer:** `C`
</details>

<details>
<summary>When should Terraform configuration files be written when running <code>terraform import</code> on existing infrastructure?</summary>

**Options:**

- `A.` Infrastructure can be imported without corresponding Terraform code  
- `B.` Terraform will generate the corresponding configuration files for you  
- `C.` You should write Terraform configuration files after the next <code>terraform import</code> is executed  
- `D.` Terraform configuration should be written before <code>terraform import</code> is executed  

**Correct Answer:** `D`
</details>

<details>
<summary>Which command lets you experiment with Terraform's built-in functions?</summary>

**Options:**

- `A.` terraform env  
- `B.` terraform console  
- `C.` terraform test  
- `D.` terraform validate  

**Correct Answer:** `B`
</details>

<details>  
<summary>Why does this backend configuration not follow best practices?</summary>  

**Options:**  

- `A.` You should not store credentials in Terraform Configuration  
- `B.` You should use the local enhanced storage backend whenever possible  
- `C.` An alias meta-argument should be included in backend blocks whenever possible  
- `D.` The backend configuration should contain multiple credentials so that more than one user can execute terraform plan and terraform apply  

**Correct Answer:** `A`  

</details>

<details>  
<summary>Open source Terraform can only import publicly-accessible and open-source modules.</summary>  

**Options:**  

- `A.` True  
- `B.` False  

**Correct Answer:** `B`  

</details>

