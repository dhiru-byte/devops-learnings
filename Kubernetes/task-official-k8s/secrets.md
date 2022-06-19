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

  The default key name is the filename. You can optionally set the key name using
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