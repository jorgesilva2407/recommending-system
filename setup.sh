#! /bin/bash
set -x

minikube start
minikube mount /Users/jlsilva:/Users/jlsilva &> /dev/null &
# ./build_model.sh
# ./build_api.sh
# ./build_client.sh
# minikube image load recommending-model
# minikube image load recommending-api
# minikube image load recommending-client

kubectl create namespace jorgesilva
kubectl -n jorgesilva apply -f pv.yml
kubectl -n jorgesilva apply -f pvc.yml

kubectl -n jorgesilva apply -f model/job.yml
kubectl -n jorgesilva apply -f api/deployment.yml
kubectl -n jorgesilva apply -f api/service.yml
kubectl -n jorgesilva apply -f client/deployment.yml
kubectl -n jorgesilva apply -f client/service.yml

sleep 5

kubectl -n jorgesilva get all
