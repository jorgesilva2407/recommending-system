#! /bin/bash

docker run --rm -v ./pkl/model.pkl:/app/model.pkl -p 5001:5000 api
