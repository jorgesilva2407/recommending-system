#! /bin/bash

docker run --rm \
    -v ./data/2023_spotify_ds1.csv:/input/playlists.csv \
    -v ./pkl/:/output \
    -v ./model/params.json:/app/params.json \
    recommending-model
