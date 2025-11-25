#!/bin/bash
# ***************************************************
# Initialize the Music Database 
# **************************************************

set -e  # Stop script if any command fails

# Move to directory where this script is located
cd "$(dirname "$0")"

# MySQL binary (MAMP 8.0)
MYSQL="/Applications/MAMP/Library/bin/mysql80/bin/mysql"

HOST="localhost"
PORT="8889"
ROOT_PW="root"

echo "Dropping and recreating music_db..."

$MYSQL -u root -p"$ROOT_PW" -h $HOST -P $PORT < drop_db.sql
$MYSQL -u root -p"$ROOT_PW" -h $HOST -P $PORT < create_db.sql

echo "Creating database user (if applicable)..."
$MYSQL -u root -p"$ROOT_PW" -h $HOST -P $PORT < create_user.sql || true

echo "Creating tables..."
$MYSQL -u root -p"$ROOT_PW" -h $HOST -P $PORT music_db < create_tables.sql

echo "Inserting test data..."
$MYSQL -u root -p"$ROOT_PW" -h $HOST -P $PORT music_db < insert_test_data.sql

echo "music_db initialized successfully!"

