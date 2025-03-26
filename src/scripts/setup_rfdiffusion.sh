#!/bin/bash
# Setup script for RFDiffusion

set -e

# Clone RFDiffusion repository
echo "Cloning RFDiffusion repository..."
if [ ! -d "RFdiffusion" ]; then
    git clone https://github.com/RosettaCommons/RFdiffusion.git
else
    echo "RFDiffusion directory already exists, skipping clone."
fi

cd RFdiffusion

# Modify Dockerfile to fix compatibility issue
echo "Modifying Dockerfile..."
if ! grep -q "numpy==1.23.5" docker/Dockerfile; then
    # Add numpy version requirement to Dockerfile
    sed -i '' 's/RUN pip install numpy/RUN pip install numpy==1.23.5/g' docker/Dockerfile
    echo "Added numpy version requirement to Dockerfile"
else
    echo "Dockerfile already modified, skipping."
fi

# Build Docker container
echo "Building RFDiffusion Docker container..."
docker build -f docker/Dockerfile -t rfdiffusion .

echo "RFDiffusion setup complete!"