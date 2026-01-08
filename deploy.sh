#!/bin/bash

# Configuration
IMAGE_NAME="mqtt-to-corsight"
CONTAINER_NAME="mqtt-to-corsight-prod"
PORT=8000

echo "Deploying $IMAGE_NAME..."

# 1. Stop and remove existing container
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# 2. Build Image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# 3. Run Container
echo "Running container..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    --network="host" \
    --env-file .env \
    $IMAGE_NAME

echo "Deployment complete!"
echo "Logs:"
docker logs -f $CONTAINER_NAME
