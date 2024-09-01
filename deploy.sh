#!/bin/bash

# Log in to Amazon ECR
$(aws ecr get-login-password --region us-east-2) | docker login --username AWS --password-stdin 481665086534.dkr.ecr.us-east-2.amazonaws.com

# Pull the latest Docker image from ECR
docker pull 481665086534.dkr.ecr.us-east-2.amazonaws.com/my-python-app:latest

# Stop the currently running container
docker stop my-python-app || true
docker rm my-python-app || true

# Run the new Docker container
docker run -d --name my-python-app -p 80:80 481665086534.dkr.ecr.us-east-2.amazonaws.com/my-python-app:latest
