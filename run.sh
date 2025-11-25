#!/bin/bash

echo "Initializing database..."
cd database
./initialize_db.sh
cd ..

echo "Starting application..."
pipenv run python3 src/main.py -c config/Music_Streaming_Playlist_System_config.json
