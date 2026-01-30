# Interview Q/ACCESS

---------------------------------------------------------------------------------------


`1.What is difference between NACL & Security Group? `

`2. What is difference between NAT instance & NAT Gateway? `

`3.What Type of Traffic does NAT GAteway allows? `

`4. What does terraform init does? `

`5. What is the  use terraform state files? `

`6. What is use of count and interpolation in terraform? `

`7.What are k8s master components and their use? `

`8. Can we deploy a pod to specific node? Yes `

`9. How to allow  pod  A to access  pod B , only accessible to POD A? Using pod network policy. `

`10. Difference between Configmap & Secret? `

`11. Can we pass env variables to a pod using Configmap & Secret? Yes `

`12. Where to define env variables in deployment yaml file? `

`13. Pod affinity & Pod life cycle? `

`14. Different types of Docker Network ? Diff. between overlay & Bridge ? `

`15. Difference Between ADD & COPY , CMD & ENTRYPOINT . Can we override entrypoint as well ? Yes We can using docker run imagename --entrypoint flag . `

`16. Difference between Pod, Statefulset & Deployment.`

`17. 3 master node in Kubernetes ? what if 2 goes down what will happen.`

`18. Diff. between PV & PVC?. `

`19. what is terraform state file & terraform lock ?. `

`20. Can I rollback a node upgrade? `

`21.  What does serverless mean to you ?. `

 `Serverless computing is a cloud computing execution model in which the cloud provider allocates machine resources on demand, taking care of the servers on behalf of their customers.`

`22. What is continuous Integration? `

 `Continuous integration (CI) is the practice of automating the integration of code changes from multiple contributors into a single software project. `

`23. What is CIDR? `

`Classless inter-domain routing (CIDR), which stands for Classless Inter-Domain Routing, is an IP addressing scheme that improves the allocation of IP addresses. It replaces the old system based on classes A, B, and C. This scheme also helped greatly extend the life of IPv4 as well as slow the growth of routing tables. `

`24. What is init container? Why do we need it ?. `

`25. Pod restart policies available ?. `

`26. What is the use of replica set ?. `

`A ReplicaSet ensures that a specified number of pod replicas are running at any given time. However, a Deployment is a higher-level concept   that manages ReplicaSets and provides declarative updates to Pods along with a lot of other useful features. Therefore, we recommend using Deployments instead of directly using ReplicaSets, unless you require custom update orchestration or don't require updates at all.   This actually means that you may never need to manipulate ReplicaSet objects: use a Deployment instead, and define your application in the spec section. ` 

`27. What are the different storage classes ?. `

`28. Diff types of EC2 instances ?. `
 
  `General Purpose: The most popular; used for web servers, development environments, etc.`
  
  `Compute Optimized: Good for compute-intensive applications such as some scientific modeling or high-performance web servers. `
  
  `Memory Optimized: Used for anything that needs memory-intensive applications, such as real-time big data analytics, or running Hadoop or Spark. `
  
  `Accelerated Computing: Include additional hardware (GPUs, FPGAs) to provide massive amounts of parallel processing for tasks such as graphics processing. `
  
  `Storage Optimized: Ideal for tasks that require huge amounts of storage, specifically with sequential read-writes, such as log processing.`

`29. Is it possible to edit the specifications of existing pod for modifying the resource limits ?. `

`30. What are the different types of secrets available in Kubernetes ?. `
   https://kubernetes.io/docs/concepts/configuration/secret/ 
   
  `Opaque	arbitrary                    -  user-defined data `
  
  `kubernetes.io/service-account-token	-  service account token `
  
  `kubernetes.io/dockercfg             -  serialized ~/.dockercfg file `
 
  `kubernetes.io/dockerconfigjson	     -  serialized ~/.docker/config.json file. `
  
  `kubernetes.io/basic-auth	           -  credentials for basic authentication. `
   
  `kubernetes.io/ssh-auth	             -  credentials for SSH authentication. `
  
  `kubernetes.io/tls	                  -  data for a TLS client or server. `
  
  `bootstrap.kubernetes.io/token       - 	bootstrap token data. ` 

`31. What are the different ways you can apply probes, (liveness or readiness) for a container ?. `  https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

`32. How do you change the priority of a running process ?. `   https://www.thegeekstuff.com/2013/08/nice-renice-command-examples/

    `In this example, test.pl is launched with a nice value of 10.  $ nice -10 perl test.pl `

`33. Different taint effects ?.`  https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

`34. Suppose I have three nodes, one of the, I have labelled as LARGE and I want my data processing pod to go on the node which is labelled as LARGE what should be done ?. `

`35. How does Terraform load all the plugins ?. `

`36. What is VPC peering ?. `  https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html

`37. What is null resource in Terraform ?. ` 

`38. What is the difference between provider and provisioner in Terraform ?. `

`39. What are the different networks in Docker ?. `
https://docs.docker.com/network/ 

`40. What does docker run --network=none nginx do ?. `
 
`50. Different storage classes in AWS ?. `  
https://aws.amazon.com/s3/storage-classes/

`51. What is the difference between scaling and autoscaling ?. `

`52. What is K8S object that helps in autoscaling ?. `

`53. Diff. between fault tolerance and Disaster recovery ?. `

`54. Tell me about a time when you took on something significant outside your area of responsibility and why was that important ?. `

`55. `
