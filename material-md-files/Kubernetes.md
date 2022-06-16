
### Kubernetes

[CKA](https://github.com/walidshaari/Kubernetes-Certified-Administrator)

[CKAD](https://github.com/dgkanatsios/CKAD-exercises)

<details>
<summary> Pod Security Standards.</summary><br><b>

<!-- overview -->

The Pod Security Standards define three different _policies_ to broadly cover the security
spectrum. These policies are _cumulative_ and range from highly-permissive to highly-restrictive.
This guide outlines the requirements of each policy.

| Profile | Description |
| ------ | ----------- |
| <strong style="white-space: nowrap">Privileged</strong> | Unrestricted policy, providing the widest possible level of permissions. This policy allows for known privilege escalations. |
| <strong style="white-space: nowrap">Baseline</strong> | Minimally restrictive policy which prevents known privilege escalations. Allows the default (minimally specified) Pod configuration. |
| <strong style="white-space: nowrap">Restricted</strong> | Heavily restricted policy, following current Pod hardening best practices. |

<!-- body -->

[Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

</b></details>

<details>
<summary> Translate Docker-compose to kubernetes.</summary><br><b>

What's Kompose? It's a conversion tool for all things compose (namely Docker Compose) to container orchestrators (Kubernetes or OpenShift).

### Use Kompose

In a few steps, we'll take you from Docker Compose to Kubernetes. All
you need is an existing `docker-compose.yml` file.

1. Go to the directory containing your `docker-compose.yml` file. If you don't have one, test using this one.

   ```yaml
   version: "2"

   services:

     redis-master:
       image: k8s.gcr.io/redis:e2e
       ports:
         - "6379"

     redis-slave:
       image: gcr.io/google_samples/gb-redisslave:v3
       ports:
         - "6379"
       environment:
         - GET_HOSTS_FROM=dns

     frontend:
       image: gcr.io/google-samples/gb-frontend:v4
       ports:
         - "80:80"
       environment:
         - GET_HOSTS_FROM=dns
       labels:
         kompose.service.type: LoadBalancer
   ```

2. To convert the `docker-compose.yml` file to files that you can use with
   `kubectl`, run `kompose convert` and then `kubectl apply -f <output file>`.

   ```bash
   kompose convert
   ```

[Kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

</b></details>

<details>
<summary> Define ConfigMap.</summary><br><b>

Many applications rely on configuration which is used during either application initialization or runtime. Most of the times there is a requirement to adjust values assigned to configuration parameters. ConfigMaps is the kubernetes way to inject application pods with configuration data. ConfigMaps allow you to decouple configuration artifacts from image content to keep containerized applications portable. This page provides a series of usage examples demonstrating how to create ConfigMaps and configure Pods using data stored in ConfigMaps.

You can use either `kubectl create configmap` or a ConfigMap generator in `kustomization.yaml` to create a ConfigMap. Note that `kubectl` starts to support `kustomization.yaml` since 1.14.

Use the `kubectl create configmap` command to create ConfigMaps from `directories`, `files`, or `literal values` :

```shell
kubectl create configmap <map-name> <data-source>
```

where \<map-name> is the name you want to assign to the ConfigMap and \<data-source> is the directory, file, or literal value to draw the data from.
The name of a ConfigMap object must be a valid

* `Create ConfigMaps from directories `
```shell
kubectl create configmap test-config --from-file=dirPath
```
* `Create ConfigMaps from files `
```shell
kubectl create configmap test-file3 --from-file=jenkins-deploy-pod-k8s.txt

#If you want to Define the key to use when creating a ConfigMap from a file.
kubectl create configmap test-file3 --from-file=testkey=jenkins-deploy-pod-k8s.txt
```
* `Create ConfigMaps from literal values `
```shell
kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```
You can pass in multiple key-value pairs. Each pair provided on the command line is represented as a separate entry in the `data` section of the ConfigMap.

[ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)

</b></details>

<details>
<summary> What Is Pod Eviction ?.</summary><br><b>

A pod eviction is a characteristic function of Kubernetes used in certain scenarios, such as node NotReady, insufficient node resources, and expelling pods to other nodes. There are two eviction mechanisms in Kubernetes:

* `kube-controller-manager`: Periodically checks the status of all nodes and evicts all pods on the node when the node is in NotReady state for more than a certain period.

following startup parameters are provided to control eviction:

1. `pod-eviction-timeout`: After the NotReady state node exceeds a default time of five minutes, the eviction will be executed.

2. `node-eviction-rate`: The drive rate, or the rate at which the node is driven.

3. `secondary-node-eviction-rate`: When there are too many down nodes in the cluster, the corresponding drive rate is also reduced.

4. `unhealthy-zone-threshold`: When the number of node downtimes in the zone exceeds 55 percent, and the zone is unhealthy.

5.` arge-cluster-size-threshold`: Determines whether the cluster is large. A cluster with over 50 (default) nodes is a large cluster.

* `kubelet`: Periodically checks the resources of the node and evicts some pods according to their priority when resources are insufficient.

The specific resources checked are:

* `memory.available`

* `nodefs.available`

* `nodefs.inodesFree`

* `imagefs.available`

* `imagefs.inodesFree`

</b></details>

<details>
<summary> Pod Lifecycle.</summary><br><b>

A Pod's `status` field is a object, which has a `phase` field.Phase of a Pod is high-level summary of where the Pod is in its lifecycle. Here are the possible values for `phase`:

Value       | Description
:-----------|:-----------
`Pending`   | The Pod has been accepted by the Kubernetes cluster, but one or more of the containers has not been set up and made ready to run. This includes time a Pod spends waiting to be scheduled as well as the time spent downloading container images over the network.
`Running`   | The Pod has been bound to a node, and all of the containers have been created. At least one container is still running, or is in the process of starting or restarting.
`Succeeded` | All containers in the Pod have terminated in success, and will not be restarted.
`Failed`    | All containers in the Pod have terminated, and at least one container has terminated in failure. That is, the container either exited with non-zero status or was terminated by the system.
`Unknown`   | For some reason the state of the Pod could not be obtained. This phase typically occurs due to an error in communicating with the node where the Pod should be running.

* When a Pod is being deleted, it is shown as `Terminating` by some kubectl commands.
This `Terminating` status is not one of the Pod phases.
A Pod is granted a term to terminate gracefully, which defaults to 30 seconds.
You can use the flag `--force` to terminate a Pod by force.

If a node dies or is disconnected from the rest of the cluster, Kubernetes
applies a policy for setting the `phase` of all Pods on the lost node to Failed.

* `Container states `: 3 possible container states: `Waiting`, `Running`, and `Terminated`.

To check the state of a Pod's containers, you can use
`kubectl describe pod <name-of-pod>`. The output shows the state for each container
within that Pod.

* `Waiting` : If a container is not in either the `Running` or `Terminated` state, it is `Waiting`.
A container in the `Waiting` state is still running the operations it requires in order to complete start up: 
for e.g. , pulling the container image from a container image registry, or applying secret data.
When you use `kubectl` to query a Pod with a container that is `Waiting`, you also see
a Reason field to summarize why the container is in that state.

* `Running` : `Running` status indicates that a container is executing without issues. If there
was a `postStart` hook configured, it has already executed and finished. When you use
`kubectl` to query a Pod with a container that is `Running`, you also see information
about when the container entered the `Running` state.

* `Terminated` : `Terminated` state began execution and then either ran to
completion or failed for some reason. When you use `kubectl` to query a Pod with
a container that is `Terminated`, you see a reason, an exit code, and the start and
finish time for that container's period of execution.

If a container has a `preStop` hook configured, this hook runs before the container enters
the `Terminated` state.

[Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)

</b></details>

<details>
<summary> Container Lifecycle Hooks.</summary><br><b>

Kubernetes provides Containers with lifecycle hooks. The hooks enable Containers to be aware of events in their management lifecycle and run code implemented in a handler when the corresponding lifecycle hook is executed.

`There are two hooks that are exposed to Containers:`

`PostStart ` : This hook is executed immediately after a container is created. However, there is no guarantee that the hook will execute before the container ENTRYPOINT. No parameters are passed to the handler.

`PreStop ` : This hook is called immediately before a container is terminated due to an API request or management event such as a liveness/startup probe failure, preemption, resource contention and others. A call to the PreStop hook fails if the container is already in a terminated or completed state and the hook must complete before the TERM signal to stop the container can be sent. The Pod's termination grace period countdown begins before the PreStop hook is executed, so regardless of the outcome of the handler, the container will eventually terminate within the Pod's termination grace period. No parameters are passed to the handler.

[Hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/)

</b></details>

<details>
<summary> What Are Hooks For?.</summary><br><b>

The primary purpose of lifecycle hooks is to provide a mechanism for detecting and responding to container state changes. The surfaced events track each container’s progress through its linear lifecycle. Before starting to use hooks, it’s important to understand what each of the three lifecycle phases means :`Waiting`, `Running`, and `Terminated`.

Being able to track transitions between these phases gives you more insights into the status of your cluster. Registered hook handlers run within the container, so they can prepare or clean up its environment as it moves in and out of the Running state.

As hooks are managed by Kubernetes, they’re guaranteed to be executed, even in a failure scenario. Your hooks will still run if a container becomes Terminated because Kubernetes evicted its pod. You can reliably handle terminations due to resource constraints and cluster-level errors using lifecycle event handlers.

* `Hook Handlers` : Handlers are the second foundational component of the lifecycle hook system. There are two different types, Exec and HTTP.

[Hooks Handlers](https://www.containiq.com/post/kubernetes-container-lifecycle-events-and-hooks)
</b></details>

<details>
<summary> Pod Lifecycle event Handlers.</summary><br><b>

Kubernetes supports the postStart and preStop events. Kubernetes sends the postStart event immediately after a Container is started, and it sends the preStop event immediately before the Container is terminated. A Container may specify one handler per event.

Kubernetes sends the postStart event immediately after the Container is created. There is no guarantee, however, that the postStart handler is called before the Container's entrypoint is called. The postStart handler runs asynchronously relative to the Container's code, but Kubernetes' management of the container blocks until the postStart handler completes. The Container's status is not set to RUNNING until the postStart handler completes.

Kubernetes sends the preStop event immediately before the Container is terminated. Kubernetes' management of the Container blocks until the preStop handler completes, unless the Pod's grace period expires. 

* Kubernetes only sends the preStop event when a Pod is terminated. This means that the preStop hook is not invoked when the Pod is completed.

[Handlers](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/)

</b></details>


<details>
<summary>Pods's DNS Policy.</summary><br><b>

A DNS query may return different results based on the namespace of the Pod making it. DNS queries that don't specify a namespace are limited to the Pod's namespace. Access Services in other namespaces by specifying it in the DNS query.

For example, consider a Pod in a test namespace. A data Service is in the prod namespace.

A query for data returns no results, because it uses the Pod's test namespace.

A query for data.prod returns the intended result, because it specifies the namespace.

DNS queries may be expanded using the Pod's /etc/resolv.conf. Kubelet sets this file for each Pod. For example, a query for just data may be expanded to data.test.svc.cluster.local. The values of the search option are used to expand queries. 

```
nameserver 10.32.0.10
search <namespace>.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

In summary, a Pod in the _test_ namespace can successfully resolve either 
`data.prod` or `data.prod.svc.cluster.local`.

What objects get DNS records?

1. Services
2. Pods

## Services

* `A/AAAA records` : "Normal" (not headless) Services are assigned a DNS A or AAAA record,
depending on the IP family of the Service, for a name of the form
`my-svc.my-namespace.svc.cluster-domain.example`.  This resolves to the cluster IP
of the Service.

"Headless" (without a cluster IP) Services are also assigned a DNS A or AAAA record,
depending on the IP family of the Service, for a name of the form
`my-svc.my-namespace.svc.cluster-domain.example`.  Unlike normal
Services, this resolves to the set of IPs of the Pods selected by the Service.
Clients are expected to consume the set or else use standard round-robin
selection from the set.

* `SRV records` : SRV Records are created for named ports that are part of normal or [Headless
Services].

For each named port, the SRV record would have the form
`_my-port-name._my-port-protocol.my-svc.my-namespace.svc.cluster-domain.example`.

For a regular Service, this resolves to the port number and the domain name:
`my-svc.my-namespace.svc.cluster-domain.example`.

## Pods

* `A/AAAA records` : 

In general a Pod has the following DNS resolution:

`pod-ip-address.my-namespace.pod.cluster-domain.example`.

For example, if a Pod in the `default` namespace has the IP address 172.17.0.3,
and the domain name for your cluster is `cluster.local`, then the Pod has a DNS name:

`172-17-0-3.default.pod.cluster.local`.

Any Pods exposed by a Service have the following DNS resolution available:

`pod-ip-address.service-name.my-namespace.svc.cluster-domain.example`.

* Pod's hostname and subdomain fields

Currently when a Pod is created, its hostname is the Pod's `metadata.name` value.

The Pod spec has an optional `hostname` field, which can be used to specify the
Pod's hostname. When specified, it takes precedence over the Pod's name to be
the hostname of the Pod. For example, given a Pod with `hostname` set to
"`my-host`", the Pod will have its hostname set to "`my-host`".

The Pod spec also has an optional `subdomain` field which can be used to specify
its subdomain. For example, a Pod with `hostname` set to "`foo`", and `subdomain`
set to "`bar`", in namespace "`my-namespace`", will have the fully qualified
domain name (FQDN) "`foo.bar.my-namespace.svc.cluster-domain.example`".

For a headless Service, this resolves to multiple answers, one for each Pod
that is backing the Service, and contains the port number and the domain name of the Pod
of the form `auto-generated-name.my-svc.my-namespace.svc.cluster-domain.example`.

DNS policies can be set on a per-Pod basis. Currently Kubernetes supports the
following Pod-specific DNS policies. These policies are specified in the
`dnsPolicy` field of a Pod Spec.

- "`Default`": The Pod inherits the name resolution configuration from the node
  that the Pods run on.

- "`ClusterFirst`": Any DNS query that does not match the configured cluster
  domain suffix, such as "`www.kubernetes.io`", is forwarded to the upstream
  nameserver inherited from the node. Cluster administrators may have extra
  stub-domain and upstream DNS servers configured.

- "`ClusterFirstWithHostNet`": For Pods running with hostNetwork, you should
  explicitly set its DNS policy "`ClusterFirstWithHostNet`".
  - Note: This is not supported on Windows.

- "`None`": It allows a Pod to ignore DNS settings from the Kubernetes
  environment. All DNS settings are supposed to be provided using the
  `dnsConfig` field in the Pod Spec.

[DNS Policy](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

</b></details>


<details>
<summary>What is DaemonSet?.</summary><br><b>

A _DaemonSet_ ensures that all (or some) Nodes run a copy of a Pod.  As nodes are added to the
cluster, Pods are added to them.  As nodes are removed from the cluster, those Pods are garbage
collected.  Deleting a DaemonSet will clean up the Pods it created.

Some typical uses of a DaemonSet are:

- running a cluster storage daemon on every node
- running a logs collection daemon on every node
- running a node monitoring daemon on every node

In a simple case, one DaemonSet, covering all nodes, would be used for each type of daemon.
A more complex setup might use multiple DaemonSets for a single type of daemon, but with
different flags and/or different memory and cpu requests for different hardware types.

* `Taints and Tolerations` : Although Daemon Pods respect but following tolerations are added to DaemonSet Pods automatically according to the related features.

| Toleration Key                           | Effect     | Version | Description |
| ---------------------------------------- | ---------- | ------- | ----------- |
| `node.kubernetes.io/not-ready`           | NoExecute  | 1.13+   | DaemonSet pods will not be evicted when there are node problems such as a network partition. |
| `node.kubernetes.io/unreachable`         | NoExecute  | 1.13+   | DaemonSet pods will not be evicted when there are node problems such as a network partition. |
| `node.kubernetes.io/disk-pressure`       | NoSchedule | 1.8+    | DaemonSet pods tolerate disk-pressure attributes by default scheduler. |
| `node.kubernetes.io/memory-pressure`     | NoSchedule | 1.8+    | DaemonSet pods tolerate memory-pressure attributes by default scheduler. |
| `node.kubernetes.io/unschedulable`       | NoSchedule | 1.12+   | DaemonSet pods tolerate unschedulable attributes by default scheduler. |
| `node.kubernetes.io/network-unavailable` | NoSchedule | 1.12+   | DaemonSet pods, who uses host network, tolerate network-unavailable attributes by default scheduler. |

[DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
</b></details>

<details>
<summary>What is StatefulSet?.</summary><br><b>

StatefulSet is the workload API object used to manage stateful applications. Manages the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of these Pods. 

Like a Deployment, a StatefulSet manages Pods that are based on an identical container spec.

Unlike a Deployment, a StatefulSet maintains a sticky identity for each of their Pods. These pods are created from the same spec, but are not interchangeable: each has a persistent identifier that it maintains across any rescheduling.

If you want to use storage volumes to provide persistence for your workload, you can use a StatefulSet as part of the solution. Although individual Pods in a StatefulSet are susceptible to failure, the persistent Pod identifiers make it easier to match existing volumes to the new Pods that replace any that have failed.

StatefulSets are valuable for applications that require one or more of the following.

* Stable, unique network identifiers.

* Stable, persistent storage.

* Ordered, graceful deployment and scaling.

* Ordered, automated rolling updates.

StatefulSet Pods have a unique identity that is comprised of an ordinal, a
stable network identity, and stable storage. The identity sticks to the Pod,
regardless of which node it's (re)scheduled on.

* `Ordinal Index` : For a StatefulSet with N replicas, each Pod in the StatefulSet will be
assigned an integer ordinal, from 0 up through N-1, that is unique over the Set.

* `Stable Network ID` : Each Pod in a StatefulSet derives its hostname from the name of the StatefulSet and the ordinal of the Pod. The pattern for the constructed hostname is `$(statefulset name)-$(ordinal)`. for example 3 Pods will be named `web-0,web-1,web-2`.

A StatefulSet can use a Headless Service to control the domain of its Pods. The domain managed by this Service takes the form: 

`$(service name).$(namespace).svc.cluster.local`, where "cluster.local" is the cluster domain.

Each Pod gets a matching DNS subdomain, taking the form: `$(podname).$(governing service domain)`, where the governing service is defined by the `serviceName` field on the StatefulSet.

StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.

Cluster Domain | Service (ns/name) | StatefulSet (ns/name)  | StatefulSet Domain  | Pod DNS | Pod Hostname |
-------------- | ----------------- | ----------------- | -------------- | ------- | ------------ |
 cluster.local | default/nginx     | default/web       | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local | web-{0..N-1} |
 cluster.local | foo/nginx         | foo/web           | nginx.foo.svc.cluster.local     | web-{0..N-1}.nginx.foo.svc.cluster.local     | web-{0..N-1} |
 kube.local    | foo/nginx         | foo/web           | nginx.foo.svc.kube.local        | web-{0..N-1}.nginx.foo.svc.kube.local        | web-{0..N-1} |


[StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
</b></details>

<details>
<summary>What is init container & it's need?.</summary><br><b>

An Init container is the one that starts and executes before other containers in the same Pod. It meant to perform initialization logic for the main application hosted on the Pod. Contain utilities or custom code for setup that is not present in an app image for security reasons. For example, create the necessary user accounts, perform database migrations, create database schemas and so on.

[Init-Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
</b></details>

<details>
<summary>Pod restart policies available ?.</summary><br><b>

* The spec of a Pod has a restartPolicy field with possible values Always, OnFailure, and Never. 

* The default value is Always.

The restartPolicy applies to all containers in the Pod. restartPolicy only refers to restarts of the containers by the kubelet on the same node. After containers in a Pod exit, the kubelet restarts them with an exponential back-off delay (10s, 20s, 40s, …), that is capped at five minutes. Once a container has executed for 10 minutes without any problems, the kubelet resets the restart backoff timer for that container.

</b></details>

<details>
<summary>What are the different ways you can apply probes, (liveness or readiness) for a container ?.</summary><br><b>

The kubelet uses liveness probes to know when to restart a container. For example, liveness probes could catch a deadlock, where an application is running, but unable to make progress. Restarting a container in such a state can help to make the application more available despite bugs.

* liveness exec/command : 

* liveness HTTP request :  kubelet sends an HTTP GET request to the server that is running in the container and listening on port 8080. If the handler for the server's /healthz path returns a success code, the kubelet considers the container to be alive and healthy. If the handler returns a failure code, the kubelet kills the container and restarts it.

Any code greater than or equal to 200 and less than 400 indicates success. Any other code indicates failure.

* liveness TCP request : kubelet will attempt to open a socket to your container on the specified port. If it can establish a connection, the container is considered healthy, if it can't it is considered a failure.

* liveness gRPC request : If your application implements gRPC Health Checking Protocol, kubelet can be configured to use it for application liveness checks. You must enable the GRPCContainerProbe feature gate in order to configure checks that rely on gRPC.

The kubelet uses readiness probes to know when a container is ready to start accepting traffic. A Pod is considered ready when all of its containers are ready. One use of this signal is to control which Pods are used as backends for Services. When a Pod is not ready, it is removed from Service load balancers.

The kubelet uses startup probes to know when a container application has started. If such a probe is configured, it disables liveness and readiness checks until it succeeds, making sure those probes don't interfere with the application startup. This can be used to adopt liveness checks on slow starting containers, avoiding them getting killed by the kubelet before they are up and running.

Protect slow starting containers with startup probes

Sometimes, you have to deal with legacy applications that might require an additional startup time on their first initialization. In such cases, it can be tricky to set up liveness probe parameters without compromising the fast response to deadlocks that motivated such a probe. The trick is to set up a startup probe with the same command, HTTP or TCP check, with a failureThreshold * periodSeconds long enough to cover the worse case startup time.


[Liveness / Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

[Youtube](https://www.youtube.com/watch?v=3TJRkKWuVoM&ab_channel=JustmeandOpensource)

</b></details>

<details>
<summary>Node Affinity & Anti-Affinity ?. </summary><br><b>

You can constrain a Pod so that it can only run on particular set of node(s). There are several ways to do this:

* nodeSelector field matching against node labels

` kubectl get nodes --show-labels `

` kubectl label nodes <your-node-name> disktype=ssd`

* Affinity and anti-affinity
    * Node affinity functions like the nodeSelector field but is more expressive and allows you to specify soft rules.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd            
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
```
* Inter-pod affinity/anti-affinity allows you to constrain Pods against labels on other Pods.

* nodeName field

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  nodeName: kube-01
```

[Node Affinity & Anti-Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity)

</b></details>

<details>
<summary>Different taint effects ?. </summary><br><b>

Tolerations are applied to pods, and allow (but do not require) the pods to schedule onto nodes with matching taints.

Taints and tolerations work together to ensure that pods are not scheduled onto inappropriate nodes. One or more taints are applied to a node; this marks that the node should not accept any pods that do not tolerate the taints.

[Taint & Tolerations](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

</b></details>

<details>
<summary>What is the use of replica set?.</summary><br><b>

A ReplicaSet ensures that a specified number of pod replicas are running at any given time. 

However, a Deployment is a higher-level concept that manages ReplicaSets and provides declarative updates to Pods along with a lot of other useful features. 

Therefore, we recommend using Deployments instead of directly using ReplicaSets, unless you require custom update orchestration or don't require updates at all. 

This actually means that you may never need to manipulate ReplicaSet objects: use a Deployment instead, and define your application in the spec section.

[ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)

</b></details>

<details>
<summary>Different types of secrets available in Kubernetes?.</summary><br><b>

|   Type                            |      Usecase             |
|---------------------------------- |--------------------------|
|Opaque arbitrary                   | user-defined data        |
|kubernetes.io/service-account-token| service account token    |
|kubernetes.io/dockercfg            |serialized .dockercfg file|
|kubernetes.io/dockerconfigjson     |serialized config.jsonfile|
|kubernetes.io/basic-auth           |cred for basic auth       |
|kubernetes.io/ssh-auth             |credentials for SSH auth  |
|kubernetes.io/tls                  |for a TLS client/server   |
|bootstrap.kubernetes.io/token      | bootstrap token data     |

[Types of Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
</b></details>


<details>
<summary>Quality of Service for Pods.</code></summary><br><b>

When Kubernetes creates a Pod it assigns one of these QoS classes to the Pod:

* Guaranteed : 
    * Every Container in the Pod must have a memory limit and a memory request.

    * For every Container in the Pod, the memory limit must equal the memory request. 

    * Every Container in the Pod must have a CPU limit and a CPU request.

    * For every Container in the Pod, the CPU limit must equal the CPU request.

* Burstable : At least one Container in the Pod has a memory or CPU request or limit.

* BestEffort : Containers in the Pod must not have any memory or CPU limits or requests.
</b></details>

<details>
<summary>What happens to a PVC after pod deletion.</code></summary><br><b>

PVCs have a lifetime independent of pods. If PV still exists it may be because it has ReclaimPolicy set to Retain in which case it won't be deleted even if PVC is gone.

PersistentVolumes can have various reclaim policies, including “Retain”, “Recycle”, and “Delete”. For dynamically provisioned PersistentVolumes, the default reclaim policy is “Delete”. This means that a dynamically provisioned volume is automatically deleted when a user deletes the corresponding PersistentVolumeClaim. This automatic behavior might be inappropriate if the volume contains precious data. Notice that the RECLAIM POLICY is Delete (default value), which is one of the two reclaim policies, the other one is Retain. (A third policy Recycle has been deprecated). In case of Delete, the PV is deleted automatically when the PVC is removed, and the data on the PVC will also be lost.

In that case, it is more appropriate to use the “Retain” policy. With the “Retain” policy, if a user deletes a PersistentVolumeClaim, the corresponding PersistentVolume is not be deleted. Instead, it is moved to the Released phase, where all of its data can be manually recovered.

This may also happens too when persistent volume is protected. You should be able to cross verify this:

kubectl describe pvc PVC_NAME | grep Finalizers

</b></details>


<details>
<summary>Get the Node OS image via json path.</code></summary><br><b>

`kubectl get node -o=jsonpath=’{.items[*].status.nodeInfo.osImage}’ `

`kubectl describe nodes | grep -i "OS Image" `
</b></details>

<details>
<summary>Mark ControlPlane/Master node as `Unschedulable`.</code></summary><br><b>

`kubectl taint nodes master/controlplane node-role.kubernetes.io/master:NoSchedule- `
</b></details>

<details>
<summary>The application stores logs at location /log/app.log. View the logs.</code></summary><br><b>

`  kubectl exec webapp cat /log/app.log `

for searching logs for a pattern

`kubectl logs foobar -n pods | grep "file-not-found" `
</b></details>

<details>
<summary>Get the InternalIP of Node .</code></summary><br><b>

`kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}' `

For Node Info

`kubectl get nodes -o custom-columns=NAME:.metadata.name,VER:.status.nodeInfo.kubeletVersion `

` kubectl get nodes -o=jsonpath=’{.items[*].metadata.name}’ `

` kubectl get po -o wide --sort-by=.spec.nodeName `

`kubectl get pod -o=custom-columns=NAME:.metadata.name,IMAGE:.spec.containers[*].image --all-namespaces `

for Deployment

`kubectl get deployment -o=jsonpath={.items[0].metadata.name} `

</b></details>

<details>
<summary>What is the Networking Solution used by this cluster?.</code></summary><br><b>

`Check the config file located at /etc/cni/net.d/ `
</b></details>

<details>
<summary>What is the default gateway configured on the PODs scheduled on node03?.</code></summary><br><b>

` ip addr show weave `

` ip link show weave`
</b></details>

<details>
<summary>What network range are the nodes in the cluster part of?.</code></summary><br><b>

 Run the command `ip addr` and look at the IP address assigned to the `ens3 interfaces`. Derive network range from that. 
</b></details>


<details>
<summary>From the hr pod nslookup the mysql service and redirect the output to a file /root/nslookup.out.</code></summary><br><b>

` kubectl exec -it hr nslookup mysql.payroll > /root/nslookup.out `

` Kubectl run test-dns --image=busybox:1.28 --restart=Never --rm -it nslookup nginx-service > /opt/service.dns `

</b></details>

<details>
<summary>What type of proxy is the kube-proxy configured to use?.</code></summary><br><b>

` kubectl logs kube-proxy-ft6n7 -n kube-system `
</b></details>


<details>
<summary>Status & Restart Kubelet.</code></summary><br><b>

`sudo systemctl status kubelet `

`sudo systemctl start kubelet `
</b></details>


<details>
<summary>Static pod directory.</code></summary><br><b>

Static Pods are managed directly by the kubelet daemon on a specific node, without the API server observing them. Unlike Pods that are managed by the control plane (for example, a Deployment); instead, the kubelet watches each static Pod (and restarts it if it fails).

Static Pods are always bound to one Kubelet on a specific node.

The kubelet automatically tries to create a mirror Pod on the Kubernetes API server for each static Pod. This means that the Pods running on a node are visible on the API server, but cannot be controlled from there. The Pod names will be suffixed with the node hostname with a leading hyphen.

`Dir : /etc/kubernetes/manifests/ `
</b></details>


<details>
<summary>Sort Deployment, Service & Pod by their name.</code></summary><br><b>

` kubectl get deploy --sort-by=.metadata.name `
` kubectl get services --sort-by=.metadata.name `
` kubectl get pod --sort-by=.metadata.name `
</b></details>

<details>
<summary>List all the pod using foo service in namespace production and write the output in a file.</code></summary><br><b>

` kubectl  get po -n production —selectors=labelsUsedByFooService `
</b></details>


<details>
<summary>Deploy a pod called web-foo using the nginx:alpine image.</code></summary><br><b>

`kubectl run web-foo --image=nginx:alpine --restart=Never`
</b></details>

<details>
<summary>Deploy a pod  with  security context `root` to change system time.</code></summary><br><b>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper
  namespace: default
spec:
  securityContext:
    runAsUser: 1010
  containers:
  - command:
    - sleep
    - "4800"
    image: ubuntu
    name: ubuntu-sleeper
    securityContext:
      capabilities:
        add: ["SYS_TIME"]

```
</b></details>


<details>
<summary>Create a static pod named static-busybox 
with busybox image & command sleep 1000.</code></summary><br><b>

` kubectl run --restart=Never --image=busybox static-busybox --dry-run -o yaml --command -- sleep 1000 > /etc/kubernetes/manifests/static-busybox.yaml `
</b></details>


<details>
<summary>Is it possible to edit the specifications of existing pod for modifying the resource limits ?.</summary><br><b>

No, recreate it using updated spec.
</b></details>

<details>
<summary>Create a pod from the busybox image. Add an init container in such a way that it should create a file in the location of /opt/myfile. This file should be accessible from the nginx image as well. The name of pod should be base-pod.</code></summary><br><b>

`kubectl run --generator=run-pod/v1 base-pod --image=busybox --dry-run -o yaml >pod.yaml `

` kubectl exec -it init-pod-example init -c nginx  -- /bin/bash `
`ls -l /opt`
</b></details>

<details>
<summary>Create a pod named multi-pod with a single container for   images running inside : nginx + redis + memcached+ consul.</code></summary><br><b>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  containers:
  - image: nginx
    name: nginx
  - image: redis
    name: redis
  - image: memcached
    name: memcached
  - image: consul
    name: consul 
```
</b></details>


<details>
<summary> Schedule a pod in a specific node.</code></summary><br><b>

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
  containers:
  - image: nginx
    name: nginx
    resources: {}
  nodeSelector:
     disktype: ssd
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
 
```
</b></details>

<details>
<summary>Create a Deployment using nginx image.</code></summary><br><b>

`kubectl create deployment --image=nginx nginx --replicas=2 --dry-run=client -o yaml > nginx-deploy.yaml `
</b></details>

<details>
<summary>Expose the deployment using Nodeport serviceType on port 80.</code></summary><br><b>

`kubectl expose deployment nginx --type=NodePort --port=80 --name=nginx-service --dry-run -o yaml > nginx-service.yaml `
</b></details>

<details>
<summary>Scale deployment to replicas=5.</code></summary><br><b>

`kubectl scale deployment.v1.apps/presentation --replicas=5 ` 
</b></details>

<details>
<summary>Create a new deployment called nginx-deploy, 

* Deployment : nginx-deploy
* image nginx:1.16 and 1 replica & Record the version. 
* Next upgrade the deployment to version 1.17 using rolling update. 
* Make sure that the version upgrade is recorded in the resource annotation.</code></summary><br><b>
 
`kubectl run nginx-deploy --image=nginx:1.16 --replicas=1 --record `
`kubectl rollout history deploy nginx-deploy `

`kubectl set image deployment/nginx-deploy nginx-deploy=nginx:1.17 --record `

#verify

`kubectl rollout history deploy nginx-deploy `

`kubectl describe deploy nginx-deploy | grep -i image `

`kubectl describe pod nginx-deploy-5bd9796fd6-z92f9 | grep image `
</b></details>

<details>
<summary> Deploy nginx daemonSet and ensure it is running on each nodes and don't override any taints (so basically asking don't use any tolerance in your manifest file).</code></summary><br><b>

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
 name: nginx-daemonset
spec:
 selector:
   matchLabels:
     app: nginx-app
 template:
   metadata:
     labels:
       app: nginx-app
   spec:
     containers:
       - name: nginx-app
         image: nginx

```
</b></details>

<details>
<summary> Deploy an init container and create a file in init container and that file should be available in the main container also (basically you need to mount volumes in both the container).</code></summary><br><b>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-pod-example
  labels:
    app: init-demo
spec:
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - name: vol1
          mountPath: "/var/www/html"
  initContainers:
    - name: busybox
      image: busybox
      volumeMounts:
        - name: vol1
          mountPath: "/demo"
      command: ['sh','-c','echo "Hello World" > /demo/hello.txt']
  volumes:
  - name: vol1
    hostPath:
      path: /tmp/demo
```
</b></details>


<details>
<summary> Deploy kubernetes cluster using kubeadm.</code></summary><br><b>

* Install kubeadm package on each node

* Run “kubeadm init” on the master node.

* Run below commands on the master node

* mkdir -p $HOME/.kube

* sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

* sudo chown $(id -u):$(id -g) $HOME/.kube/config”

* Install weavenet network plugin using the below command

` kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')" `

</b></details>


<details>
<summary>To get the Nodes CIDR.</code></summary><br><b>

`kubectl get nodes -o jsonpath=’{.items[*].spec.podCIDR}’ `
</b></details>


<details>
<summary>Create Configmap.</code></summary><br><b>

`kubectl create configmap webapp-config-map --from-literal=APP_COLOR=darkblue  --from-literal=APP_Name=demo `
</b></details>

<details>
<summary>Create a Secret by providing credentials on the command line. 

* create a pod and inject that secret as a volume.
* create a another pod and inject that secret as a env variable.</code></summary><br><b>

` kubectl create secret generic test-secret --from-literal='username=my-app' --from-literal='password=39528$vdg7Jb' `

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
spec:
  containers:
  - name: test-container
    image: nginx
    volumeMounts:
    # name must match the volume name below
    - name: secret-volume
      mountPath: /etc/secret-volume
  # Secret data is exposed to Containers in the Pod through a Volume.
  volumes:
  - name: secret-volume
    secret:
    secretName: test-secret
```

`kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-single-secret
spec:
  containers:
  - name: envars-test-container
    image: nginx
    env:
    - name: SECRET_USERNAME
      valueFrom:
        secretKeyRef:
          name: backend-userkubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
          key: backend-username
```
</b></details>

<details>
<summary> To sort Nodes by CPU, or add -r at the end if you want the largest at the top.</code></summary><br><b>

`kubectl top pod | sort -k2 -n `
</b></details>


<details>
<summary> Label a Node.</code></summary><br><b>

`kubectl label node node01 color=blue `
</b></details>

<details>
<summary> Sort Pods by CPU Usage.</code></summary><br><b>

`kubectl top pods --all-namespaces  --sort-by cpu `
</b></details>

<details>
<summary> List Pod with labels.</code></summary><br><b>

`kubectl get pods --show-labels `
</b></details>

<details>
<summary>How to find out on which node a certain pod is running?.</summary><br><b>

`kubectl get po -o wide`
</b></details>

<details>
<summary> List all Persistence Volumes order by name and write to file or List all PV order by capacity.</code></summary><br><b>

`kubectl get pv --sort-by=.metadata.name `

` kubectl get pv --sort-by=.spec.capacity.storage `
</b></details>

<details>
<summary> Create pod with PV and mount path /data/redis and volume must not be persistent (Create empty directory)</code></summary><br><b>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: two-containers
spec:

  restartPolicy: Never

  volumes:
  - name: shared-data
    emptyDir: {}

  containers:

  - name: nginx-container
    image: nginx
    volumeMounts:
    - name: shared-data
      mountPath: /data/redis

```
</b></details>


<details>
<summary> Create a 'Persistent Volume' with given specification,

* Volume Name: pv-log
* Storage: 100Mi
* Access modes: ReadWriteMany
* Host Path: /pv/log.</code></summary><br><b>

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-1
spec:
  accessModes:
    - ReadWriteMany
  capacity:
    storage: 100Mi
  hostPath:
    path: /pv/log

```
</b></details>


<details>
<summary> Create a 'Persistent Volume Claim' with given specification,

* Volume Name: my-pvc
* Storage: 50Mi
* Access modes: ReadWriteMany
* VolumeMode / plugin : Filesystem.</code></summary><br><b>

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteMany   #ReadWriteOnce pv & pvc should have access modes otherwise they won't bund will be in pending state
  volumeMode: Filesystem
  resources:
    requests:
      storage: 50Mi

```
</b></details>


<details>
<summary> Network policy to

* allow pods listeing on 9000
* allow pods accessible from a namespace </code></summary><br><b>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-port-from-namespace
   namepsace: fubar
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
    ingress:
    - {}
  egress:
  - to:
    - podSelector: {}
    ports:
    - protocol: TCP
      port: 9000

  - to:
    - podSelector:
        matchLabels:
          name: corp-net

```
</b></details>


<details>
<summary> Create a network policy to 

* allow traffic from the 'Internal' application only to the 'payroll-service' and 'db-service'

You might want to enable ingress traffic to the pod to test your rules in the UI. </code></summary><br><b>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      name: internal
  policyTypes:
  - Egress
  - Ingress
  ingress:
    - {}
  egress:
  - to:
    - podSelector:
        matchLabels:
          name: mysql
    ports:
    - protocol: TCP
      port: 3306

  - to:
    - podSelector:
        matchLabels:
          name: payroll
    ports:
    - protocol: TCP
      port: 8080

  - ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP

```
</b></details>


<details>
<summary> Create ingress

* Name: pong
* Namespace ing-internal
* Targetport: 5678  </code></summary><br><b>

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: pong
  namespace: ing-internal
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /hello
        backend:
          serviceName: hello
          servicePort: 5678
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-kusc00401
  labels:
    env: test
spec:
  containers:
  - name: nginx-kusc00401
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disk: spinning

```
</b></details>

<details>
<summary> How many ClusterRoles do you see defined in the cluster?.</code></summary><br><b>

` kubectl get clusterroles --no-headers | wc -l  `

` kubectl get clusterrolebinding --no-headers  | wc -l `

` kubectl get clusterroles --no-headers -o json | jq '.items | length'`
</b></details>


<details>
<summary> Create Role & Rolebinding for `developer` to list pods .</code></summary><br><b>

` kubectl auth can-i list pods --as developer `

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: developer
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["list", “create”]

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-user-binding
  namespace: default
subjects:
# You can specify more than one "subject"
- kind: User
  name: dev-user # "name" is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:
  # "roleRef" specifies the binding to a Role / ClusterRole
  kind: Role #this must be Role or ClusterRole
  name: developer # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io

```
</b></details>


<details>
<summary> Create Clusterrole & clusterrolebinding for `new-user` to list nodes .</code></summary><br><b>

` kubectl auth can-i list nodes --as new-user `

` kubectl create clusterrole storage-admin --verb=get,list,watch,delete --resource=persistentvolumes --resource=storageclasses `

` kubectl create clusterrolebinding michelle-storage-admin --clusterrole=storage-admin --user=new-user `


```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  # "namespace" omitted since ClusterRoles are not namespaced
  name: new-user
rules:
- apiGroups: [""]
  #
  # at the HTTP level, the name of the resource for accessing Secret
  # objects is "secrets"
  resources: ["nodes"]
  verbs: ["list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-reader-new-user
subjects:
- kind: User
  name: manager # Name is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: new-user
  apiGroup: rbac.authorization.k8s.io
```
</b></details>


<details>
<summary> Create a taint on node01 with key of 'spray', value of 'mortein' and effect of 'NoSchedule'.
</code></summary><br><b>

` kubectl taint nodes node01 spray=mortein:NoSchedule `
</b></details>

<details>
<summary> Remove the taint on master, which currently has the taint effect of NoSchedule.</code></summary><br><b>

` kubectl taint nodes node01 spray=mortein:NoSchedule- `
</b></details>

<details>
<summary> Drain Node node02.</code></summary><br><b>

` kubectl drain node02 --ignore-daemonsets `
</b></details>

# ETCD

<details>
<summary>Update ETCD POD to use the new hostPath directory /var/lib/etcd-from-backup by modifying the pod definition file at /etc/kubernetes/manifests/etcd.yaml. 

* When this file is updated, the ETCD pod is automatically re-created as this is a static pod placed under the /etc/kubernetes/manifests directory.</summary><br><b>

Update volumes and volume mounts to point to new path

```yaml
 volumes:
  - hostPath:
      path: /var/lib/etcd-from-backup
      type: DirectoryOrCreate
    name: etcd-data
  - hostPath:
      path: /etc/kubernetes/pki/etcd
      type: DirectoryOrCreate
    name: etcd-certs
```

Note: as the ETCD pod has changed it will automatically restart, and also kube-controller-manager and kube-scheduler. Wait 1-2 to mins for this pods to restart. You can make a watch "docker ps | grep etcd" to see when the ETCD pod is restarted.

Note2: If the etcd pod is not getting Ready 1/1, then restart it by kubectl delete pod -n kube-system etcd-controlplane and wait 1 minute.


</b></details>


<details>
<summary>Take the backup of ETCD at the location /opt/etcd-backup.db on the master node.</summary><br><b>

ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot save /opt/etcd-backup.db
</b></details>

<details>
<summary>Restore ETCD Snapshot to a new folder.</summary><br><b>
Restore the snapshot to a new directory, note that the directory should NOT exists - it's created in the restore process. I'll fetch the cluster endpoint details from the current /etc/kubernetes/manifests/etcd.yaml file

`kubectl describe pods etcd-controlplane -n kube-system `

ETCDCTL_API=3 etcdctl etcdctl snapshot restore etcd.db \
--endpoints=https://127.0.0.1:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
--name=controlplane \
--data-dir /var/lib/etcd-from-backup \
--initial-cluster=controlplane=https://127.0.0.1:2380 \
--initial-cluster-token=etcd-cluster-1 \
--initial-advertise-peer-urls=https://127.0.0.1:2380 \

Deprecated: Use `etcdutl snapshot restore` instead.

Notice that ETCD is listening on two ports. Which of these have more client connections established?

` netstat -anp | grep etcd `

That's because 2379 is the port of ETCD to which all control plane components connect to. 

2380 is only for etcd peer-to-peer connectivity. When you have multiple master nodes.

</b></details>

<details>
<summary>Create a CertificateSigningRequest object with the name john with the contents of the john.csr file.</summary><br><b>


` openssl req -new -key john.key -out john.csr -config csr.conf `

`openssl x509 -req -in /etc/kubernetes/pki/apiserver-etcd-client.csr -CA /etc/kubernetes/pki/etcd/ca.crt -CAkey /etc/kubernetes/pki/etcd/ca.key -CAcreateserial -out /etc/kubernetes/pki/apiserver-etcd-client.crt `

` cat john.csr | base64 | tr -d "n" `

```yaml
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  request: #enter the bas64 value of .csr file #$(cat john.csr | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - server auth

```

` kubectl auth can-i  create pods --as dev-user `

` kubectl auth can-i  create pods `

` kubectl auth can-i list secrets --namespace deve --as test-user `

` kubectl get secret mynamespace-user-token-xxxxx -n mynamespace -o "jsonpath={.data.token}" | base64 -D `

</b></details>


<details>
<summary>CKA Useful Links </summary><br><b>

[CKA](https://prabhatsharma.in/blog/cka-practice-test-1/)

[CKA GUIDE](https://devopscube.com/cka-exam-study-guide/)

[CKA Simulator](https://killer.sh/course/preview/e84d0e31-4fff-4c42-8afd-be1bdbc0d994)


[CKAD-exercises](https://github.com/dgkanatsios/CKAD-exercises/blob/main/README.md)

</b></details>