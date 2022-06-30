 # To Setup PostgreSQL & Cronjob to take Backups

` kubectl create -f pgsql-cm.yaml `

### Step 2. Replace your Database creds.
Replace database creds in [pgsql-cm.yaml]
!Attention: This is for simplicity these should be replaced with Secrets.

### Step 3. Create the resources

` kubectl create -f pgsql-deploy.yaml `

` kubectl create -f cronjob-pv.yaml `

` kubectl create -f cronjob-deployment.yaml `

` kubectl create -f minio-pv.yaml `

 ` POSTGRES_DB: awesomedb `
 ` POSTGRES_USER: amazinguser `
 ` POSTGRES_PASSWORD: perfectpassword `
## Contributing and Modifying

1. Make your desired changes and build the container:

` docker build -t dhirujackal/postgresql7:12.3.1 . `

2. Test it locally by executing the command below:

` docker run -v /d/backup:/pg_backup dhirujackal/postgresql7:12.3.1 `

### Step 1. Pull the image

` docker push dhirujackal/postgresql7:12.3.1 `

### Step 2. Run and map to your drive (e.g. /d/backup)
` docker run -v /host/backup:/pg_backup dhirujackal/postgresql7:12.3.1 `


## To setup NFS Server On Centos And use nfs type Persistent Volume

` yum install nfs-utils `

` mkdir /var/nfsshare `

` chmod -R 755 /var/nfsshare `

` vi /etc/exports `

` systemctl start rpcbind `

` systemctl start nfs-server  `

` systemctl start nfs-lock `

` systemctl start nfs-idmap `


## Initializing Postgres as terraform Backend to store Terraform State Files.


`terraform workspace list `

`terraform workspace new dhirendra `

`terraform init -backend-config='conn_str=postgres://amazinguser:perfectpassword@node-ip:31186/terraform_backend?sslmode=disable' `
 
`kubectl exec -it postgresql-postgresql-0 -- psql -h 10.91.3.57 -U postgres --password -p 30311 postgres `

`sudo -u postgres psql -d terraform_backend `

`CREATE DATABASE sonar; `

`DROP DATABASE terraform_backend; `

`sudo passwd postgres `

`\dt * `

`\l+ terraform_backend `

`./mc config host add minio-local http://10.91.2.3:31311 AKIAIOSFODNN7EXAMPLE wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY --api S3v4 `

`./mc ls minio-local `

`./mc mb minio-local/pgsql-nfs `

`. ~/bash_profile `

`export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE `

`export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY `

`Restic password: Empirix@123 `

`restic -r s3:http://minio-server-ip:31311/pgsql-nfs init `

`restic -r s3:http://minio-server-ip:31311/pgsql-nfs --verbose backup /var/data/pgsqldumpdata `

