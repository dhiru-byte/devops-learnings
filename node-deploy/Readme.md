### Task Explaination

* `Dockerfile` to containerized the nodejs app.

* ` docker build -t dhirendrabyte/node-server:latest . ` : build the image from dockerfile usign this command.

* ` docker push dhirendrabyte/node-server:latest ` : push the image to registry.

### Deploy to Kubernetes

Deploy the node app by applying `deployment.yaml`

 `kubectl apply -f deployment.yaml` .

### Create  Secret for pulling images from private repo in Kubernetes.

` kubectl create secret generic regcred --from-file=.dockerconfigjson=/home/ubuntu/.docker/config.json --type=kubernetes.io/dockerconfigjson `


### Create HPA(Horizontal Pod Autoscaler) for autoscaling the deployment using metrics like CPU or Memory.

### for CPU
` kubectl autoscale deployment node-deploy --cpu-percent=50 --min=5 --max=8 `

OR

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: node-cpu-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: node-deploy
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```




### For Memory

```yaml
apiVersion: autoscaling/v2beta2 
kind: HorizontalPodAutoscaler
metadata:
  name: node-memory-hpa 
spec:
  scaleTargetRef:
    apiVersion: apps/v1 
    kind: Deployment 
    name: node-deploy
  minReplicas: 1 
  maxReplicas: 10 
  metrics: 
  - type: Resource
    resource:
      name: memory 
      target:
        type: Utilization 
        averageValue: 10Mi
```        