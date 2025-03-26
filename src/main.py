#!/usr/bin/env python3
"""
CD20 Protein Binder Design Pipeline

This script orchestrates the full end-to-end pipeline for designing protein binders
targeting CD20. It combines RFDiffusion for initial structure generation, ProteinMPNN 
for sequence design, and AlphaFold2 for structure prediction and validation.

Author: Karl Philip Lundquist
Date: March 2025
"""

import os
import argparse
import subprocess
import sys
from pathlib import Path

# Add src directory to path
# Get the root directory of the project
project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

def create_directories():
    """Create necessary directories for pipeline execution."""
    directories = [
        "data/input",
        "data/output",
        "data/pdb",
        "data/results/round1",
        "data/results/final"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Created directory structure")

def run_rfdiffusion(args):
    """Run RFDiffusion to generate initial binder structures."""
    print("Starting RFDiffusion for initial binder generation...")
    script_path = os.path.join(src_dir, "scripts", "run_rfdiff.sh")
    
    # Ensure script is executable
    subprocess.run(["chmod", "+x", script_path])
    
    # Run the RFDiffusion script
    subprocess.run([script_path], check=True)
    print("RFDiffusion complete")

def run_proteinmpnn_af2(args):
    """Run ProteinMPNN for sequence design and AlphaFold2 for structure prediction."""
    print("Starting ProteinMPNN and AlphaFold2 pipeline...")
    
    # Setup the Docker environment if needed
    setup_script = os.path.join(src_dir, "proteinmpnn_af2", "setup.sh")
    subprocess.run(["chmod", "+x", setup_script])
    subprocess.run([setup_script], check=True)
    
    # Run the Docker container
    docker_script = os.path.join(src_dir, "proteinmpnn_af2", "run_docker.sh")
    subprocess.run(["chmod", "+x", docker_script])
    subprocess.run([docker_script], check=True)
    
    # Run ProteinMPNN
    mpnn_script = os.path.join(src_dir, "proteinmpnn_af2", "beta_model_mpnn.py")
    subprocess.run(["conda", "run", "-n", "proteinmpnn_binder_design", "python", mpnn_script], check=True)
    
    # Run AlphaFold2
    af2_script = os.path.join(src_dir, "proteinmpnn_af2", "beta_model_af2.py")
    subprocess.run(["conda", "run", "-n", "af2_binder_design", "python", af2_script], check=True)
    
    print("ProteinMPNN and AlphaFold2 complete")

def run_analysis(args):
    """Run analysis scripts to evaluate and rank designs."""
    print("Starting analysis of designed binders...")
    
    # Run analysis scripts in sequence
    scripts = [
        "filter_pdbs.py",
        "align.py",
        "run_md.py",
        "merge_energies.py",
        "collect_top_designs.py"
    ]
    
    for script in scripts:
        script_path = os.path.join(src_dir, "analysis", script)
        subprocess.run(["python", script_path], check=True)
    
    print("Analysis complete")

def main():
    parser = argparse.ArgumentParser(description="CD20 Protein Binder Design Pipeline")
    parser.add_argument("--skip-rfdiffusion", action="store_true", help="Skip RFDiffusion step")
    parser.add_argument("--skip-proteinmpnn-af2", action="store_true", help="Skip ProteinMPNN and AlphaFold2 steps")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip analysis steps")
    args = parser.parse_args()

    # Create directory structure
    create_directories()
    
    # Run pipeline components unless skipped
    if not args.skip_rfdiffusion:
        run_rfdiffusion(args)
    
    if not args.skip_proteinmpnn_af2:
        run_proteinmpnn_af2(args)
    
    if not args.skip_analysis:
        run_analysis(args)
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()