#!/bin/bash

# Ensure script exits on error
set -e

# Define clone directory relative to script execution path (project root)
REPO_URL="https://github.com/nrbennet/dl_binder_design.git"
CLONE_DIR="dl_binder_design"

if [ -d "$CLONE_DIR" ]; then
    echo "Directory $CLONE_DIR already exists. Pulling the latest changes."
    (cd $CLONE_DIR && git pull) # Use subshell for git pull
else
    echo "Cloning the repository..."
    git clone $REPO_URL $CLONE_DIR # Clone into specific directory name
fi

# Define ProteinMPNN dir relative to project root
MPNN_DIR="mpnn_fr/ProteinMPNN"
MPNN_PARENT_DIR="mpnn_fr" # Parent dir for ProteinMPNN

if [ -d "$MPNN_DIR" ]; then
    echo "ProteinMPNN directory already exists. Pulling the latest changes."
    (cd $MPNN_DIR && git pull) # Use subshell for git pull
else
    echo "Cloning ProteinMPNN repository..."
    # Ensure parent directory exists
    mkdir -p $MPNN_PARENT_DIR
    git clone https://github.com/dauparas/ProteinMPNN.git $MPNN_DIR
fi

# Build the image using the corrected LOCAL Dockerfile
# Assumes this script is run from the project root (cd20-binder-design)
# The build context '.' is the project root, containing dl_binder_design and mpnn_fr
echo "Building the dl_binder_design image using local Dockerfile..."
docker build -t dl_binder_design -f src/proteinmpnn_af2/Dockerfile .

echo "Setup complete. You can now run the container using the run_design.sh script (or the pipeline script)."
