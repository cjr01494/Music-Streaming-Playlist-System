#!/bin/bash
# ***************************************************
# Initialize the Music Database 
# ***************************************************

set -e  # Stop if any command fails
cd "$(dirname "$0")"  # Run from the script's own directory

MYSQL="/Applications/MAMP/Library/bin/mysql80/bin/mysql"
HOST="localhost"
PORT="8889"

echo "Dropping and recreating music_db ..."

$MYSQL -u root -p -h $HOST -P $PORT < drop_db.sql
$MYSQL -u root -p -h $HOST -P $PORT < create_db.sql
$MYSQL -u root -p -h $HOST -P $PORT < create_user.sql

echo "Creating tables and inserting data ..."
$MYSQL -u music_db_user -p -h $HOST -P $PORT music_db < create_tables.sql
$MYSQL -u music_db_user -p -h $HOST -P $PORT music_db < insert_test_data.sql

echo "music_db initialized successfully!"

