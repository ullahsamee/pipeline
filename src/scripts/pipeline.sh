#!/bin/bash

# Set up necessary directories and files
mkdir -p rfdiff_in rfdiff_out
cp $HOME/inputs/cd20.pdb ./rfdiff_in/

## Step 1: Run script 1 with the rfdiffusion container
docker run --rm --gpus all \
   -v $HOME/models:/app/models \
   -v ./rfdiff_in:/app/inputs \
   -v ./rfdiff_out:/app/outputs \
   rfdiffusion \
   inference.output_prefix=/app/outputs/binder_design \
   inference.model_directory_path=/app/models \
   inference.input_pdb=/app/inputs/cd20.pdb \
   inference.num_designs=100 \
   inference.ckpt_override_path=/app/models/Complex_beta_ckpt.pt \
   'contigmap.contigs=[C46-210/0 D46-210/0 80-80]' \
   'ppi.hotspot_res=[C171,C174,C175,D171,D174,D175]'

## Step 2: Run script 2 with the dl_binder_container and proteinmpnn_binder_design environment

# Create output directory
mkdir -p mpnn_out

# Run Docker command
docker run --rm --gpus all \
  --entrypoint /bin/bash \
  -v "$(pwd)/rfdiff_out:/app/inputs" \
  -v "$(pwd)/mpnn_out:/app/outputs" \
  dl_binder_design -c "
    source /opt/conda/etc/profile.d/conda.sh && \
    conda activate proteinmpnn_binder_design && \
    python -u /app/mpnn_fr/dl_interface_design.py \
      -pdbdir /app/inputs \
      -relax_cycles 0 \
      -seqs_per_struct 4 \
      -outpdbdir /app/outputs
  "

## Step 3: Run script 3 with the dl_binder_container and af2_binder_design environment
mkdir -p af2_out
docker run --rm --gpus all \
  -v "$(pwd)/mpnn_out:/app/inputs" \
  -v "$(pwd)/af2_out:/app/outputs" \
  dl_binder_design bash -c "
    source /opt/conda/etc/profile.d/conda.sh && \
    conda activate af2_binder_design && \
    python -u /app/af2_initial_guess/predict.py \
      -pdbdir /app/inputs \
      -outpdbdir /app/outputs
  "

## Notify user that the pipeline has finished
echo "Pipeline execution complete."
