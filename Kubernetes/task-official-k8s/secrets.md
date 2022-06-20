### Managing Secrets using kubectl

```shell
echo -n 'admin' > ./username.txt
echo -n '1f2d1e2e67df' > ./password.txt
```


The `kubectl create secret` command packages these files into a Secret and creates
the object on the API server.

```shell
kubectl create secret generic db-user-pass \
  --from-file=./username.txt \
  --from-file=./password.txt
```

* The default key name is the filename. You can optionally set the key name using
`--from-file=[key=]source`. For example:

```shell
kubectl create secret generic db-user-pass \
  --from-file=username=./username.txt \
  --from-file=password=./password.txt
```

```shell
echo -n 'admin' | base64 
echo -n '1f2d1e2e67df' | base64
```

* Write a `Secret` config file that looks like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
```

* Note that the name of a Secret object must be a valid

You could store this in a Secret using the following definition:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
stringData:
  config.yaml: |
    apiUrl: "https://my.api.com/api/v1"
    username: <user>
    password: <password>
```

### Create the `Secret` object

```shell
kubectl apply -f ./secret.yaml
```


### Managing Secrets using Kustomize

You can generate a Secret by defining a secretGenerator in a kustomization.yaml file that references other existing files. For example, the following kustomization file references the ./username.txt and the ./password.txt files:

```yaml
secretGenerator:
- name: db-user-pass
  files:
  - username.txt
  - password.txt
```

You can also define the `secretGenerator` in the `kustomization.yaml`
file by providing some literals.
For example, the following `kustomization.yaml` file contains two literals
for `username` and `password` respectively:

```yaml
secretGenerator:
- name: db-user-pass
  literals:
  - username=admin
  - password=1f2d1e2e67df
```

You can also define the `secretGenerator` in the `kustomization.yaml`
file by providing `.env` files.
For example, the following `kustomization.yaml` file pulls in data from
`.env.secret` file:

```yaml
secretGenerator:
- name: db-user-pass
  envs:
  - .env.secret
```

* Note that in all cases, you don't need to base64 encode the values.

### Create the Secret

```shell
kubectl apply -k .
```

#### Create a Pod that has access to the secret data through a Volume.

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
  # The secret data is exposed to Containers in the Pod through a Volume.
  volumes:
    - name: secret-volume
      secret:
        secretName: test-secret
```

#### Define container environment variables using Secret data.

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
          name: backend-user
          key: backend-username
```
#### Define container environment variables with data from multiple Secrets.

```shell
` kubectl create secret generic backend-user --from-literal=backend-username='backend-admin' `
` kubectl create secret generic db-user --from-literal=db-username='db-admin' `
```

```yaml
apiVersion: v1   
kind: Pod   
metadata:   
  name: envvars-multiple-secrets   
spec:   
  containers:   
  - name: envars-test-container   
    image: nginx   
    env:   
    - name: BACKEND_USERNAME   
      valueFrom:   
        secretKeyRef:   
          name: backend-user   
          key: backend-username   
    - name: DB_USERNAME   
      valueFrom:   
        secretKeyRef:   
          name: db-user   
          key: db-username
```

#### Configure all key-value pairs in a Secret as container environment variables.

```shell
` kubectl create secret generic test-secret --from-literal=username='my-app' --from-literal=password='39528$vdg7Jb' `
```

```yaml
apiVersion: v1
    
kind: Pod    
metadata:    
  name: envfrom-secret    
spec:    
  containers:    
  - name: envars-test-container    
    image: nginx    
    envFrom:    
    - secretRef:    
        name: test-secret    
```