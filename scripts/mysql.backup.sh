#!/bin/bash


TODAY=`date +"%d%b%Y_%H_%M_%S"`
################## Update below values  ########################

DB_BACKUP_PATH='/var/mysql-db-backup/'
#DIR='mysql-db-backup'
MYSQL_HOST='localhost'
MYSQL_PORT='3306'
MYSQL_USER='username'
MYSQL_PASSWORD='password'
DATABASE_NAME='mysample'
BACKUP_RETAIN_DAYS=30   ## Number of days to keep local backup copy

#################################################################

sudo mkdir -p ${DB_BACKUP_PATH}
echo "Backup started for database - ${DATABASE_NAME}"


mysqldump -h ${MYSQL_HOST} \
   -P ${MYSQL_PORT} \
   -u ${MYSQL_USER} \
   -p${MYSQL_PASSWORD} \
   ${DATABASE_NAME} | gzip > ${DB_BACKUP_PATH}${DATABASE_NAME}-${TODAY}.sql.gz

if [ $? -eq 0 ]; then
  echo "Database backup successfully completed"
else
  echo "Error found during backup"
fi


##### Remove backups older than {BACKUP_RETAIN_DAYS} days  #####

DBDELDATE=`date +"%d%b%Y" --date="${BACKUP_RETAIN_DAYS} days ago"`

if [ ! -z ${DB_BACKUP_PATH} ]; then
      cd ${DB_BACKUP_PATH}
      if [ ! -z ${DBDELDATE} ] && [ -d ${DBDELDATE} ]; then
            rm -rf ${DBDELDATE}
      fi
fi

### End of script ####
