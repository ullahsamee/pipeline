# Use a base image with Python
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# Set up the working directory
WORKDIR /app

# Set bash as default shell early
SHELL ["/bin/bash", "-c"]

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

# Copy the repository files (build context assumed to be project root)
COPY . .

# Copy the PyRosetta wheel file (assumes it's in src/proteinmpnn_af2/ in the build context)
COPY src/proteinmpnn_af2/pyrosetta-*.whl /tmp/

# Set up the conda environments using correct paths and names
# IMPORTANT: Assumes the corresponding YML files have had '- pyrosetta' removed/commented out
RUN conda env create -f dl_binder_design/include/proteinmpnn_fastrelax.yml -n proteinmpnn_binder_design && conda clean -afy
RUN conda env create -f dl_binder_design/include/af2_binder_design.yml -n af2_binder_design && conda clean -afy

# Install PyRosetta from wheel file into the first environment
RUN echo "Installing PyRosetta wheel in proteinmpnn_binder_design env..." && \
    conda run -n proteinmpnn_binder_design pip install /tmp/pyrosetta-*.whl

# Install PyRosetta from wheel file into the second environment
# WARNING: Ensure this environment uses Python 3.10 for cp310 wheel compatibility
RUN echo "Installing PyRosetta wheel in af2_binder_design env..." && \
    conda run -n af2_binder_design pip install /tmp/pyrosetta-*.whl

# Clean up the wheel file after installation
RUN rm /tmp/pyrosetta-*.whl

# Download AlphaFold2 model weights (Keep this section from original)
# Note: This happens *inside* the image, making it large.
RUN cd dl_binder_design/af2_initial_guess && \
    mkdir -p model_weights/params && \
    cd model_weights/params && \
    wget https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar && \
    tar --extract --verbose --file=alphafold_params_2022-12-06.tar && \
    rm alphafold_params_2022-12-06.tar

# Add conda-forge channel and install biopython=1.79 (Keep this section)
RUN echo "Configuring conda channels and installing biopython..." && \
    /opt/conda/bin/conda config --add channels conda-forge && \
    /opt/conda/bin/conda install -y biopython=1.79 -n af2_binder_design && conda clean -afy

# Install specific numpy versions (Keep this section)
RUN echo "Installing numpy=1.23.5..." && \
    conda install -y -n proteinmpnn_binder_design numpy=1.23.5 && conda clean -afy
RUN conda install -y -n af2_binder_design numpy=1.23.5 && conda clean -afy

# Set environment variables (Ensure correct env names are used)
ENV PATH /opt/conda/envs/af2_binder_design/bin:/opt/conda/envs/proteinmpnn_binder_design/bin:$PATH

# Default command (Keep this section)
CMD ["bash"]
