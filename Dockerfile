FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set shell
SHELL ["/bin/bash", "-c"]

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    ca-certificates \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh

# Add conda to path
ENV PATH="/opt/conda/bin:${PATH}"

# Create conda environments from yml files
COPY environment.yml /app/environment.yml
RUN conda env create -f /app/environment.yml

# Set up entry point
COPY src /app/src
COPY data /app/data
COPY notebooks /app/notebooks

# Make entry point script executable
RUN chmod +x /app/src/main.py

# Set environment variable for GPU
ENV CUDA_VISIBLE_DEVICES=0

# Default command
CMD ["/bin/bash"]