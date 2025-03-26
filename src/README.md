# Source Code Organization

This directory contains the source code for the CD20 Protein Binder Design Pipeline. The code is organized into several modules:

## Main Script

- `main.py`: Orchestrates the complete pipeline, providing command-line options to control execution flow

## Modules

- **analysis/**: Scripts for filtering, analyzing, and ranking protein binder designs
  - `align.py`: Aligns protein complexes using MDAnalysis
  - `collect_top_designs.py`: Collects and ranks the best designs
  - `consolidate_top_designs.py`: Merges top designs from multiple sources
  - `delete_high_rmsd_pdbs.py`: Removes structures with high RMSD values
  - `filter_pdbs.py`: Filters out designs that would protrude into the membrane
  - `merge_energies.py`: Combines energetics data for final scoring
  - `run_md.py`: Performs molecular dynamics simulations to assess binding stability

- **proteinmpnn_af2/**: Components for sequence design and structure prediction
  - `beta_model_mpnn.py`: Implements ProteinMPNN for optimizing protein sequences
  - `beta_model_af2.py`: Uses AlphaFold2 to predict structures
  - `Dockerfile`: Docker configuration for containerized execution
  - `setup.sh`: Setup script for environment preparation
  - `run_docker.sh`: Script to launch the Docker container

- **rfdiffusion/**: Components for initial binder structure generation
  - `Dockerfile`: Docker configuration for RFDiffusion

- **scripts/**: Shell scripts for pipeline automation
  - `pipeline.sh`: Main pipeline execution script
  - `run_pipeline.sh`: Wrapper for pipeline.sh with nohup
  - `run_rfdiff.sh`: Script to run RFDiffusion
  - `setup_rfdiffusion.sh`: Script to set up RFDiffusion environment