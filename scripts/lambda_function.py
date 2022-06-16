import boto3
import datetime

def lambda_handler(event, context):
    print("Connecting to RDS")
    client = boto3.client('rds')
    
    print("RDS snapshot backups stated at %s...\n" % datetime.datetime.now())
    client.create_db_cluster_snapshot(
        DBClusterIdentifier='adidas-prod-aurora-cluster', 
        DBClusterSnapshotIdentifier='adidas-prod-aurora-cluster-%s' % datetime.datetime.now().strftime("%y-%m-%d-%H"),
    )
    