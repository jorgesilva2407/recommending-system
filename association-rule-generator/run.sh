#! /bin/bash

docker run --rm -v ./2023_spotify_ds1.csv:/input/playlists.csv -v ./output/:/output -v ./params.json:/app/params.json association-rule-generator
