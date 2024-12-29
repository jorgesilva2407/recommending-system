#! /bin/bash

docker run --rm \
    -v ./pkl/model.pkl:/app/model.pkl \
    -p 50000:5000 \
    recommending-api
