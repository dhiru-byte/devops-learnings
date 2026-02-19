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
