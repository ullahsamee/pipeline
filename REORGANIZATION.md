# Repository Reorganization

This document summarizes the changes made to clean up and reorganize the repository by Karl Philip Lundquist.

## Directory Structure

### Created a proper project structure:

```
molecule_master/
├── data/                # Data files organized by type
│   ├── input/           # Input files for the pipeline
│   ├── output/          # Output files from each stage
│   ├── pdb/             # PDB files including target CD20 structure
│   └── results/         # Final results and rankings
├── src/                 # All source code in a single directory
│   ├── analysis/        # Scripts for analyzing and filtering designs
│   ├── proteinmpnn_af2/ # ProteinMPNN and AlphaFold2 integration
│   ├── rfdiffusion/     # RFDiffusion setup and configuration
│   ├── scripts/         # Shell scripts for pipeline execution
│   └── main.py          # Main orchestration script
├── notebooks/           # Jupyter notebooks for visualization
└── docs/                # Documentation files
```

## Code Reorganization

1. Created a central `main.py` script that orchestrates the complete pipeline
2. Moved Python analysis scripts from `run_inf_code/` to `src/analysis/`
3. Organized ProteinMPNN and AlphaFold2 code in `src/proteinmpnn_af2/`
4. Organized shell scripts in `src/scripts/`
5. Created proper Python packages with `__init__.py` files

## Documentation Improvements

1. Completely rewrote the README.md with:
   - Clear project overview
   - Installation instructions
   - Usage examples with command-line options
   - Detailed explanation of the design strategy
   - Advanced configuration options
   - Properly formatted references

2. Added proper documentation files:
   - CITATION.cff for citation information
   - LICENSE file (MIT License)
   - README.md files in subdirectories

## Cleanup

1. Removed unnecessary files:
   - progen2.md (unrelated to the main pipeline)
   - Duplicate files across directories
   
2. Standardized scripts:
   - Made all shell scripts executable
   - Improved path handling in Python scripts
   - Made main.py executable

## New Features

1. Created a setup script for RFDiffusion
2. Added command-line arguments to main.py for selective execution
3. Proper package structure for Python modules

## Future Improvements

1. Add unit tests
2. Add more detailed documentation
3. Create example notebooks for analysis
4. Add a requirements.txt file for Python dependencies