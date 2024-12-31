#!/bin/bash
set -x

current_dir=$(pwd)
docker_hub_user=silvajorge
api_image_name=recommending-api
model_image_name=recommending-model
client_image_name=recommending-client
tagged_api_image_name=$docker_hub_user/$api_image_name:latest
tagged_model_image_name=$docker_hub_user/$model_image_name:latest
tagged_client_image_name=$docker_hub_user/$client_image_name:latest

cd_build_tag_push() {
    cd $1
    docker build -t $2 .
    docker tag $2 $3
    docker rmi $2
    docker push $3
}

cd_build_tag_push $current_dir/api $api_image_name $tagged_api_image_name
cd_build_tag_push $current_dir/model $model_image_name $tagged_model_image_name
cd_build_tag_push $current_dir/client $client_image_name $tagged_client_image_name