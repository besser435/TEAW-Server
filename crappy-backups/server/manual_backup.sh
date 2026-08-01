#!/bin/bash

# Backup configuration
BACKUP_DIR="/home/temp_teaw_backups"
SOURCE_DIR="/var/opt/minecraft/crafty/crafty-4/servers/e97c3311-4330-4fb8-be4a-b74cfa6b734b"

# Timestamp for filename
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="${BACKUP_DIR}/manual_backup_${TIMESTAMP}.tar.zst"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

echo "Creating backup..."
echo "Source: $SOURCE_DIR"
echo "Destination: $BACKUP_FILE"

cd "$SOURCE_DIR" || {
    echo "Failed to enter source directory."
    exit 1
}


# Create compressed archive using all CPU cores
tar \
    --exclude='./bluemap' \
    --exclude='./logs' \
    --exclude='./plugins/CoreProtect/database.db' \
    -I 'zstd -T0 -1' \
    -cf "$BACKUP_FILE" .

if [ $? -eq 0 ]; then
    echo "Backup completed successfully:"
    echo "$BACKUP_FILE"
else
    echo "Backup failed."
    exit 1
fi