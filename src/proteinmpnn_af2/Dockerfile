# Use a base image with Python
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# Set up the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh
ENV PATH=/opt/conda/bin:$PATH

# Copy the repository files
COPY . .

# Set up the conda environment for ProteinMPNN-FastRelax
RUN conda env create -f include/proteinmpnn_fastrelax.yml -n proteinmpnn_binder_design && conda clean -afy
RUN conda env create -f include/af2_binder_design.yml -n af2_binder_design && conda clean -afy

# Install PyRosetta using the installer
RUN pip install pyrosetta-installer && \
    python -c 'import pyrosetta_installer; pyrosetta_installer.install_pyrosetta()'

# Download AlphaFold2 model weights
RUN cd af2_initial_guess && \
    mkdir -p model_weights/params && \
    cd model_weights/params && \
    wget https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar && \
    tar --extract --verbose --file=alphafold_params_2022-12-06.tar && \
    rm alphafold_params_2022-12-06.tar

# Install PyRosetta in the proteinmpnn_fastrelax environment
RUN /opt/conda/bin/conda run -n proteinmpnn_binder_design pip install pyrosetta-installer && \
    /opt/conda/bin/conda run -n proteinmpnn_binder_design python -c 'import pyrosetta_installer; pyrosetta_installer.install_pyrosetta()'

# Install PyRosetta in the af2_binder_design environment
RUN /opt/conda/bin/conda run -n af2_binder_design pip install pyrosetta-installer && \
    /opt/conda/bin/conda run -n af2_binder_design python -c 'import pyrosetta_installer; pyrosetta_installer.install_pyrosetta()'

# Add conda-forge channel and install biopython=1.79
RUN /opt/conda/bin/conda config --add channels conda-forge && \
    /opt/conda/bin/conda install biopython=1.79 -n af2_binder_design

RUN conda install -n proteinmpnn_binder_design numpy=1.23.5
RUN conda install -n af2_binder_design numpy=1.23.5

# Set environment variables
ENV PATH /opt/conda/envs/af2_binder_design/bin:/opt/conda/envs/proteinmpnn_fastrelax/bin:$PATH

# Default command
CMD ["bash"]
