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

` kubectl autoscale deployment node-deploy --cpu-percent=50 --min=5 --max=8 `


