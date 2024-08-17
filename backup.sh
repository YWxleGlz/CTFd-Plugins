#!/bin/bash

# Crontab example: 0 2 * * * /path/to/backup_script.sh >> /path/to/backup.log 2>&1

# Variables
BACKUP_SRC="/home/ubuntu/CTFd-Plugins/data"
BACKUP_DEST="/home/ubuntu/CTFd-Plugins/backups" # Feel free to move the backup folder to another location in order to have a real backup
DOCKER_COMPOSE_PATH="/home/ubuntu/CTFd-Plugins/"
BACKUP_COUNT=4  # Number of backups to keep
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_NAME="backup_$TIMESTAMP.tar.gz"

# Stop Docker stack
echo "Stopping Docker stack..."
cd $DOCKER_COMPOSE_PATH
docker compose stop

# Create backup
echo "Creating backup of $BACKUP_SRC..."
mkdir -p $BACKUP_DEST
tar -czf $BACKUP_DEST/$BACKUP_NAME $BACKUP_SRC

# Remove old backups
echo "Removing old backups, keeping the latest $BACKUP_COUNT..."
cd $BACKUP_DEST
ls -1tr | head -n -$BACKUP_COUNT | xargs -d '\n' rm -f --

cd $DOCKER_COMPOSE_PATH
docker compose start

echo "Backup completed successfully."