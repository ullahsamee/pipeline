#!/bin/bash

# Clone the repository
REPO_URL="https://github.com/nrbennet/dl_binder_design.git"
CLONE_DIR="dl_binder_design"

# Check if the directory already exists
if [ -d "$CLONE_DIR" ]; then
    echo "Directory $CLONE_DIR already exists. Pulling the latest changes."
    cd $CLONE_DIR && git pull
else
    echo "Cloning the repository..."
    git clone $REPO_URL
    cd $CLONE_DIR
fi

# Clone ProteinMPNN
MPNN_DIR="mpnn_fr/ProteinMPNN"
if [ -d "$MPNN_DIR" ]; then
    echo "ProteinMPNN directory already exists. Pulling the latest changes."
    cd $MPNN_DIR && git pull && cd ../../
else
    echo "Cloning ProteinMPNN repository..."
    git clone https://github.com/dauparas/ProteinMPNN.git mpnn_fr/ProteinMPNN
fi

# Specify the path to the Dockerfile if it's not in the root directory
DOCKERFILE_PATH="/home/btb/karl/dl_binder_design/Dockerfile"  # Update this if your Dockerfile is in a subdirectory

# Build the Docker image
echo "Building the Docker image..."
docker build -t dl_binder_design -f $DOCKERFILE_PATH .

echo "Setup complete. You can now run the container using the run_design.sh script."
