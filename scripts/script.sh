#!/bin/bash

echo "Let Create Kubernetes Resources"

curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > install-helm.sh

chmod a+x install-helm.sh

./install-helm.sh

kubectl -n kube-system create serviceaccount tiller

kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller

helm init --service-account tiller

helm install stable/nginx-ingress -n nginx-ingress

kubectl create -f mstackxStage.yaml

kubectl create -f mstackxProd.yaml

#To test Horizontal Pod Autoscaler by putting load on to frontend service using a load generator
kubectl run -i --tty load-generator --image=busybox /bin/sh
