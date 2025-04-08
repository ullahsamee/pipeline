#!/bin/bash
set -e

echo "Running RFDiffusion Docker container with project paths..."

docker run --rm --gpus all \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data/pdb:/app/inputs \
  -v $(pwd)/data/output:/app/outputs \
  rfdiffusion \
  inference.output_prefix=/app/outputs/binder_design_rfdiff \
  inference.model_directory_path=/app/models \
  inference.input_pdb=/app/inputs/cd20.pdb \
  inference.num_designs=10 \
  inference.ckpt_override_path=/app/models/Complex_base_ckpt.pt \
  'contigmap.contigs=[C46-210/0 D46-210/0 80-80]' \
  'ppi.hotspot_res=[C168,C169,C170,C171,C172,C173,C174,C175,D168,D169,D170,D171,D172,D173,D174,D175]'
  # NO backslash on this last line ^

echo "RFDiffusion Docker container finished."
