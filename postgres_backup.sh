#!/bin/bash

# Database name for backup
DB_NAME="pvlppv"

# PostgreSQL user
DB_USER="postgres"

# Directory to save backups inside the container
CONTAINER_BACKUP_DIR="/var/lib/postgresql/backup"

# Host directories for backups
HOST_BACKUP_DIR="/root/pvlppv-website"

# Create the directory if it doesn't exist
mkdir -p $CONTAINER_BACKUP_DIR

# Perform pg_dump and save the dump
pg_dump -U $DB_USER $DB_NAME > $CONTAINER_BACKUP_DIR/$DB_NAME-$(date +\%Y-\%m-\%d).sql

# Copy the backup to host directories
cp $CONTAINER_BACKUP_DIR/$DB_NAME-$(date +\%Y-\%m-\%d).sql $HOST_BACKUP_DIR

# Remove backups older than 7 days from the container backup directory
find $CONTAINER_BACKUP_DIR -type f -name "*.sql" -mtime +7 -exec rm {} \;

# Remove backups older than 7 days from the host backup directory
find $HOST_BACKUP_DIR -type f -name "*.sql" -mtime +7 -exec rm {} \;
