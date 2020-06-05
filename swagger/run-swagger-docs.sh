#!/bin/bash
# https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/installation.md
# https://hub.docker.com/r/swaggerapi/swagger-ui/tags

API_VER=$(curl -s https://api.github.com/repos/OasisLMF/OasisPlatform/tags | jq -r '( first ) | .name')
API_URL="https://github.com/OasisLMF/OasisPlatform/releases/download/$API_VER/openapi-schema-$API_VER.json"

export SWAGGER_SCHEMA="openapi-schema-$API_VER.json"
export SWAGGER_LINK="oasis-api-schema.json"
export SWAGGER_IMAGE="swaggerapi/swagger-ui"
export SWAGGER_TAG="v3.24.2"

wget $API_URL -O $SWAGGER_SCHEMA
rm $SWAGGER_LINK
ln -s $SWAGGER_SCHEMA $SWAGGER_LINK
docker-compose up -d
