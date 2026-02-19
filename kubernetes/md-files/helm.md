## HELM
<details>
<summary>What is a Helm Chart and Why Do We Use It?. </summary><br><b>
   
Helm chart is a package format used by Helm, the leading package manager for Kubernetes.A Helm chart is a collection of files that describe a set of Kubernetes resources (such as deployments, services, config maps, etc.) and their configuration.
```
my-chart/
├── Chart.yaml          # Chart metadata (name, version, description)
├── values.yaml         # Default configuration values (can be overridden)
├── templates/          # Kubernetes resource templates (YAML manifests)
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── _helpers.tpl    # Template helpers (optional)
├── charts/             # Subcharts (dependencies, optional)
├── .helmignore         # Patterns to ignore when packaging the chart
└── README.md           # Documentation for the chart
```
* **Simplifies Kubernetes Deployments:** Helm charts package all the resources and configuration needed for an application, making it easy to deploy complex apps with a single command.

* **Parameterization & Reusability:** You can customize deployments by overriding values in values.yaml, allowing the same chart to be used for different environments (dev, prod, etc.).

* **Version Control & Upgrades:** Charts are versioned, so you can track changes, roll back to previous versions, and upgrade applications easily.

* **Sharing & Collaboration:** Charts can be shared via Helm repositories, enabling teams to reuse and collaborate on deployment patterns.

* **Automated Management:** Helm handles installation, upgrades, and uninstallation of applications, reducing manual errors and operational complexity.
</b></details>  

<details>
<summary> Difference Between values.yaml and --set Flag in Helm.</summary><br><b>

* **Purpose:** The values.yaml file is used to define default configuration values for a Helm chart.
* **Usage:** You edit this file to set the standard values for your application (e.g., image tags, replica counts, environment variables).
* **Scope:** Applies to all installations of the chart unless overridden.
* **Version Control:** Typically checked into your Git repository with the chart.
```
replicaCount: 2
image:
  repository: nginx
  tag: stable
```
### --set Flag
* **Purpose:** The --set flag is used to override values from values.yaml directly from the command line when installing or upgrading a Helm release.
* **Usage:** Useful for quick, one-off changes or for automation in CI/CD pipelines.
* **Scope:** Only applies to the specific Helm command where it is used.
* **Not Version Controlled:** Since it’s a CLI argument, it’s not stored in the chart’s files.
```
helm install my-release my-chart --set replicaCount=3,image.tag=latest
```  
</b></details>

<details>
<summary> Difference Between helm install, helm upgrade, helm rollback, & helm repo update?.</summary><br><b>

```
helm install <release-name> <chart> [flags]
helm install my-app ./my-chart                      #Fails if a release with the same name already exists.
helm upgrade <release-name> <chart> [flags]         #Applies changes to resources (e.g., new image, more replicas).
helm upgrade my-app ./my-chart --set image.tag=2.0  #Can upgrade the chart version or override values.
helm rollback <release-name> [revision]             #Restores the release to the specified previous state.
helm rollback my-app 1                              #If no revision is specified, rolls back to the previous one.
```

| Command | Purpose | Typical Use Case |
| :-- | :-- | :-- |
| helm install | Deploy new release | First-time deployment |
| helm upgrade | Update existing release | Change config, update image, etc. |
| helm rollback | Revert to previous revision | Undo failed or unwanted upgrade |
| helm repo update | Refresh chart repository index | Get latest chart versions from repo |

</b></details>

<details>
<summary> What is Helm Diff?.</summary><br><b>

Helm diff is a plugin for Helm that shows you the differences between your current deployed release and what would change if you ran a helm upgrade or helm install. It’s a powerful tool for previewing changes before actually applying them to your Kubernetes cluster.

Helm diff is a Helm plugin that compares a Helm chart’s manifests against:

* The currently deployed release (**helm diff upgrade**)
* The chart’s default values (**helm diff install**)
* Or between two chart versions (**helm diff revision**)
Purpose:
To preview and review changes (additions, deletions, modifications) in Kubernetes resources before deploying, helping prevent unintended consequences.

</b></details>

