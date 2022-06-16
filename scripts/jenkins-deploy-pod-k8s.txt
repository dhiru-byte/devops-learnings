#Jenkins Pipeline to deploy on kubernentes

pipeline {
  agent {
    kubernetes {
      //cloud 'kubernetes'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: default
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
    
"""
    }
  }

  stages {
    stage('echo') {
      steps {
        container('nginx') {
          sh 'echo Hello World'
        }
      }
    }
  }
}

