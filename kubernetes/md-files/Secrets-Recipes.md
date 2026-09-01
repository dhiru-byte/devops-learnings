# Kubernetes Secret Recipes

These are procedural examples. Do not place real credentials in shell history,
manifests, chat, or source control.

Conceptual coverage lives in the main guide: how Secrets compare to ConfigMaps
and how mounted data updates is in
[Kubernetes.md](Kubernetes.md#configmap-versus-secret), and protection through
RBAC, encryption at rest, and external secret managers is in
[Kubernetes.md](Kubernetes.md#protecting-secrets-and-etcd).

## Create a generic Secret

From literals:

```bash
kubectl create secret generic db-credentials \
  --from-literal=username='app-user' \
  --from-literal=password='replace-me'
```

From files, with explicit key names:

```bash
kubectl create secret generic db-credentials \
  --from-file=username=./username.txt \
  --from-file=password=./password.txt
```

Preview a manifest without sending it to the API server:

```bash
kubectl create secret generic db-credentials \
  --from-literal=username='app-user' \
  --from-literal=password='replace-me' \
  --dry-run=client -o yaml
```

## Declarative Secret

Prefer `stringData` when authoring by hand; the API server converts it to
base64-encoded `data`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-config
type: Opaque
stringData:
  config.yaml: |
    apiUrl: https://api.example.com/v1
    username: replace-me
    password: replace-me
```

```bash
kubectl apply -f secret.yaml
```

The file still contains plaintext. Use an encrypted Git workflow, an external
secret manager, or a secrets operator rather than committing it directly.

## Generate with Kustomize

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
secretGenerator:
  - name: db-credentials
    files:
      - username=username.txt
      - password=password.txt
    literals:
      - environment=production
```

```bash
kubectl apply -k .
```

Kustomize adds a content hash to the generated name by default, allowing a
changed Secret to trigger rollout when workload references are transformed.

## Mount selected keys as files

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-demo
spec:
  containers:
    - name: app
      image: nginx:stable
      volumeMounts:
        - name: credentials
          mountPath: /var/run/app-secrets
          readOnly: true
  volumes:
    - name: credentials
      secret:
        secretName: db-credentials
        items:
          - key: username
            path: username
          - key: password
            path: password
```

Mounted Secret updates are eventually reflected unless mounted with `subPath`.
The application must reload changed files.

## Read one key as an environment variable

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-demo
spec:
  containers:
    - name: app
      image: nginx:stable
      env:
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
```

Environment variables do not update until the container is replaced and can be
exposed through process diagnostics. Prefer mounted files when the application
supports them.

## Import all keys as environment variables

```yaml
envFrom:
  - secretRef:
      name: db-credentials
```

Every key must be a valid environment-variable name or it will be skipped.
Explicit `secretKeyRef` entries make dependencies clearer.

## Common built-in Secret types

| Type | Use |
| --- | --- |
| `Opaque` | Arbitrary user data |
| `kubernetes.io/tls` | TLS certificate and private key |
| `kubernetes.io/dockerconfigjson` | Registry credentials |
| `kubernetes.io/basic-auth` | Username/password |
| `kubernetes.io/ssh-auth` | SSH private key |
| `bootstrap.kubernetes.io/token` | Node bootstrap token |

Legacy long-lived `kubernetes.io/service-account-token` Secrets should usually
be replaced with short-lived projected ServiceAccount tokens from the Token
Request API.

## Verify access without revealing data

```bash
kubectl auth can-i get secret/db-credentials -n default
kubectl get secret db-credentials -o jsonpath='{.metadata.name}{"\n"}'
```

Avoid printing or decoding Secret values during routine verification.
