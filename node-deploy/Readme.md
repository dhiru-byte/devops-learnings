### Task Explaination

[Dockerfile](node-deploy/Dockerfile)



For Creating Docs from Docker config json file.

` kubectl create secret generic regcred --from-file=.dockerconfigjson=/home/ubuntu/.docker/config.json --type=kubernetes.io/dockerconfigjson `