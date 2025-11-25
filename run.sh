#!/bin/bash

echo "Initializing database..."
./database/initialize_db.sh

echo "Starting application..."
pipenv run python3.12 src/main.py -c config/Music_Streaming_Playlist_System_config.json
