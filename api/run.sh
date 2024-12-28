#! /bin/bash

docker run --rm -v $(pwd)/association_rules.pkl:/app/model.pkl -p 5000:5000 recommendation-api