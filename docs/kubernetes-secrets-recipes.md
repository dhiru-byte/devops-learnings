# Kubernetes Secret Recipes

- **Purpose:** procedural cards for creating and consuming Secrets.
- **Main guide:** [Kubernetes interview guide](kubernetes-interview-guide.md).
- **Safety:** never put real credentials in shell history, manifests, chat, or source control.
- **Concepts:** [Configuration and storage](kubernetes-interview-guide.md#configuration-and-storage) covers update semantics.
- **Protection:** [Secrets and etcd protection](kubernetes-interview-guide.md#secrets-and-etcd-protection) covers RBAC and encryption.

## Create with kubectl

Fastest path in a lab or exam. Docs:
[Managing Secrets using kubectl](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kubectl/)

```bash
kubectl create secret generic db-credentials \
  --from-file=username=./username.txt --from-file=password=./password.txt
kubectl create secret tls web-tls --cert=tls.crt --key=tls.key
```

- **Gotcha:** `--from-literal=username='app-user'` puts the value in shell
  history and in process arguments visible to other users on the host; prefer
  `--from-file`. `--dry-run=client -o yaml` previews the object, but that output
  still carries the value in base64.

## Registry credentials without a password in argv

`kubectl create secret docker-registry --docker-password=...` exposes the password
in argv and shell history. Log in with the container tool, then build the Secret
from the config file it wrote. Docs: [Pull an image from a private registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)

```bash
docker login registry.example.com --username ci --password-stdin < ./token.txt

kubectl create secret generic regcred \
  --from-file=.dockerconfigjson="$HOME/.docker/config.json" \
  --type=kubernetes.io/dockerconfigjson
```

- The key must be exactly `.dockerconfigjson` and the type exactly
  `kubernetes.io/dockerconfigjson`, or the kubelet ignores the Secret.
- **Gotcha:** `--password-stdin` belongs to `docker login`, not to kubectl.
  Podman writes `${XDG_RUNTIME_DIR}/containers/auth.json` instead — point
  `--from-file` at that path.
- **Gotcha:** the config file may hold credentials for other registries too;
  reference the Secret from `imagePullSecrets`, and scope it to one namespace.
- **Gotcha:** with a credential helper (`credsStore`) the file holds no token, so
  the Secret ends up empty — check `auths` in the config before creating it.

## Author declaratively

For GitOps, or when a task grades YAML. Docs: [Managing Secrets using a config file](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-config-file/)

```yaml
apiVersion: v1
kind: Secret
metadata: { name: app-config }
type: Opaque
stringData:
  config.yaml: |
    apiUrl: https://api.example.com/v1
    password: replace-me
```

- `stringData` takes plaintext and the API server encodes it into `data`;
  hand-encoding base64 is only needed under `data`.
- **Gotcha:** base64 is encoding, not encryption, and this file holds the
  credential in plaintext on disk. Use an encrypted Git workflow, a secrets
  operator, or an external manager rather than committing it directly.

## Generate with Kustomize

Rolls workloads automatically when a credential changes. Docs:
[Kustomization](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/) · [secretGenerator](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/secretgenerator/)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
secretGenerator:
  - name: db-credentials
    files: [username=username.txt, password=password.txt]
    literals: [environment=production]
```

- Render with `kubectl kustomize .` before applying with `kubectl apply -k .`.
- **Gotcha:** the generated name carries a content hash, so anything referencing
  the literal name breaks. `generatorOptions.disableNameSuffixHash` removes it,
  at the cost of the automatic rollout.

## Mount selected keys as files

Preferred consumption path. Docs: [Distribute credentials securely](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)

```yaml
spec:
  containers:
    - name: app
      image: nginx:stable
      volumeMounts: [{ name: credentials, mountPath: /var/run/app-secrets, readOnly: true }]
  volumes:
    - name: credentials
      secret:
        secretName: db-credentials
        defaultMode: 0400
        items: [{ key: username, path: username }, { key: password, path: password }]
```

- Omit `items` to project every key; include it to expose only what the container
  needs.
- **Gotcha:** mounted keys update eventually and the application must reload them,
  but a `subPath` mount **never** updates — that file stays frozen until the Pod
  is replaced.

## Read as environment variables

Only when the application cannot read files. Docs: [Secrets as environment variables](https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-environment-variables)

```yaml
env:
  - { name: DB_USERNAME, valueFrom: { secretKeyRef: { name: db-credentials, key: username } } }
envFrom:
  - { secretRef: { name: db-credentials } }
```

- **Gotcha:** environment values are fixed until the container is replaced and
  leak through `kubectl describe pod`, crash dumps, child processes, and
  `/proc/<pid>/environ`.
- **Gotcha:** `envFrom` silently skips keys that are not valid
  environment-variable names; explicit `secretKeyRef` entries fail loudly. A
  missing Secret leaves the Pod in `CreateContainerConfigError`, visible in the
  Pod events rather than the logs.

## Rotate a Secret

Replace the value and make workloads actually pick it up. Docs:
[Managing Secrets using kubectl](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kubectl/)

```bash
kubectl create secret generic db-credentials-v2 --from-file=password=./new-password.txt
kubectl set env deployment/app --from=secret/db-credentials-v2   # or edit the ref
kubectl rollout status deployment/app && kubectl delete secret db-credentials
```

- Prefer a **new name** or a Kustomize `secretGenerator` **content hash**: the
  reference change is what triggers the rollout.
- **Gotcha:** editing a Secret in place restarts nothing. Environment variables
  and `subPath` mounts keep the old value until the Pod is replaced; plain
  projected mounts refresh eventually but the app must reload them.
- **Gotcha:** after an in-place edit, force replacement with
  `kubectl rollout restart deployment/app`, and rotate at the source system too —
  the old credential stays valid until it is revoked there.

## Types and verification

Docs: [Secret types](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) · [ServiceAccount tokens](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/)

| Type | Use |
| :--- | :--- |
| `Opaque` | Arbitrary user data |
| `kubernetes.io/tls` | TLS certificate and private key |
| `kubernetes.io/dockerconfigjson` | Registry pull credentials |
| `kubernetes.io/basic-auth`, `kubernetes.io/ssh-auth` | Password or SSH key |
| `bootstrap.kubernetes.io/token` | Node bootstrap token |

```bash
kubectl auth can-i get secret/db-credentials -n default
kubectl describe secret db-credentials   # key names and sizes only
```

- Replace legacy `kubernetes.io/service-account-token` Secrets with short-lived
  projected tokens from the TokenRequest API.
- **Gotcha:** do not decode values during routine checks — verify key names,
  sizes, and access instead of printing the credential.
