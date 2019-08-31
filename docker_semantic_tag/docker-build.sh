#!/usr/bin/bash

set -e

# the image tag to use, if it's empty, infer from the codebase (see belows)
IMAGE_TAG="$1"

# the name the docker image
IMAGE_NAME="registry.build4.fun/my-cool-project"

# path to the docker file
IMAGE_DOCKERFILE="$(pwd)/Dockerfile"

# docker build context
IMAGE_BUILDCTX="$(pwd)"

if [[ -z "$TAG" ]]
then
    date_version=$(date "+%Y%m%d")
    head_commit=$(git rev-parse --short HEAD)
    IMAGE_TAG="${date_version}-${head_commit}"
fi

docker build \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    -t "${IMAGE_NAME}:latest" \
    -f  "$IMAGE_DOCKERFILE" \
    "$IMAGE_BUILDCTX"
