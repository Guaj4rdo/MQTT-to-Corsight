#!/bin/bash

# Configuration
IMAGE_NAME="mqtt-to-corsight"
CONTAINER_NAME="mqtt-to-corsight-prod"
PORT=8000

echo "Deploying $IMAGE_NAME..."

# Check for simulation mode
ENABLE_MQTT=True
if [[ "$1" == "--sim" ]]; then
    echo "SIMULATION MODE (MQTT Disabled)"
    ENABLE_MQTT=False
fi

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
    -e ENABLE_MQTT=$ENABLE_MQTT \
    $IMAGE_NAME

echo "Deployment complete!"
echo "Logs:"
docker logs $CONTAINER_NAME
