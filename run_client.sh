#!/bin/bash

docker run --rm \
    -v "./data/2023_spotify_new_songs.csv:/app/public/songs.csv" \
    -p 3000:3000 \
    -e REACT_APP_RECOMMENDATION_API_URL=http://localhost:50000/api/recommend \
    recommending-client
