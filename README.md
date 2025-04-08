# CD20 Protein Binder Design Pipeline

A computational pipeline for designing novel protein binders targeting CD20 using deep learning and molecular simulation approaches. Developed for the BioML Challenge 2024: Bits to Binders competition.

## Overview

This project implements a computational approach for designing protein binders that specifically target CD20, a membrane protein expressed on B cells and a key target for various immunotherapies. The pipeline integrates several state-of-the-art computational tools:

- **RFDiffusion** for de novo protein structure generation
- **ProteinMPNN** for deep learning-based protein sequence design
- **AlphaFold2** for protein structure prediction
- **Rosetta** for energy calculations and structural refinement
- **OpenMM** for molecular dynamics simulations
- **Prodigy** for binding affinity prediction

## Competition Context

This pipeline was developed for the BioML Challenge 2024: Bits to Binders competition organized by the University of Texas at Austin BioML Society. The competition required teams to:

- Design the antigen binding domain of a Chimeric Antigen Receptor (CAR) targeting CD20
- Adhere to an 80 amino acid length constraint (due to DNA synthesis limitations)
- Create designs that would activate CAR-T cell killing and proliferation responses
- Submit sequences for experimental testing by LEAH Laboratories

Our designs are currently in the testing stage with results expected in early 2025.

## Project Structure

```
cd20-binder-design/
├── data/
│   ├── input/           # Input files for the pipeline
│   ├── output/          # Output files from each stage
│   ├── pdb/             # PDB files including target CD20 structure
│   └── results/         # Final results and rankings
├── src/
│   ├── analysis/        # Scripts for analyzing and filtering designs
│   ├── proteinmpnn_af2/ # ProteinMPNN and AlphaFold2 integration
│   ├── rfdiffusion/     # RFDiffusion setup and configuration
│   ├── scripts/         # Shell scripts for pipeline execution
│   └── main.py          # Main orchestration script
├── notebooks/
│   └── view_pdbs.ipynb  # Jupyter notebook for visualizing PDB structures
├── Dockerfile           # Main Dockerfile for the project
├── CITATION.cff         # Citation information
├── LICENSE              # Project license
└── README.md            # This file
```

## Installation(Fedor 41) 



### Prerequisites

- Docker (for containerized execution)
- Python = 3.11 or 3.12.8
- CUDA = 12.6 configured GPU (recommended for AlphaFold2 and RFDiffusion)
- GCC = 14.2.1

### Docker(NVIDIA Container Toolkit) setup
 ```
curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | \
sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
sudo dnf install -y nvidia-container-toolkit

sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
   ```

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/klundquist/cd20-binder-design.git
   cd cd20-binder-design

   Download pyrosetta-2024.39+release.59628fb-cp311-cp311-linux_x86_64.whl
   from link: https://graylab.jhu.edu/download/PyRosetta4/archive/release/PyRosetta4.Release.python311.linux.cxx11thread.serialization.wheel/pyrosetta-2024.39+release.59628fb-cp311-cp311-linux_x86_64.whl
   place in /home/asus/biotools/cd20-binder-design/src/proteinmpnn_af2
   ```
2. make python virtual env
   ```bash
   cd /home/asus/biotools/cd20-binder-design
   source venv/bin/activate
   ```
4. Set up the environment:
   ```bash
   # Install RFDiffusion
   src/scripts/setup_rfdiffusion.sh
   
   # Install ProteinMPNN and AlphaFold2
   src/proteinmpnn_af2/setup.sh
   ```
5. Install remaining dependencies:
   ```bash
   pip install pandas matplotlib jupyter-lab mdanalysis biopython openmm nglview
   ```

## Usage

### Full Pipeline

Run the complete pipeline with:

```bash
python src/main.py
```

This will execute all steps in sequence:
1. Generate initial binder structures with RFDiffusion
2. Design sequences with ProteinMPNN and Rosetta FastRelax
3. Predict structures with AlphaFold2
4. Filter designs based on structural criteria
5. Run MD simulations and analyze binding energies
6. Rank and select top designs

### Selective Execution

You can skip specific steps using command-line flags:

```bash
# Skip RFDiffusion step (if you already have initial structures)
python src/main.py --skip-rfdiffusion

# Skip ProteinMPNN and AlphaFold2 (if you already have designed sequences and predicted structures)
python src/main.py --skip-proteinmpnn-af2

# Skip analysis (if you just want to generate designs)
python src/main.py --skip-analysis
```

### Visualization

Use the provided Jupyter notebook to visualize PDB structures:

```bash
jupyter notebook notebooks/view_pdbs.ipynb
```

## Design Strategy

The pipeline implements an iterative optimization strategy balancing exploration and exploitation:

1. **Initial Structure Generation**: RFDiffusion creates scaffolds with complementary binding interfaces to CD20
2. **Sequence Design**: ProteinMPNN optimizes sequences for both stability and binding
3. **Structure Validation**: AlphaFold2 predicts structures to ensure design accuracy
4. **Filtering**: Removes designs with poor predictions or impractical structural properties
5. **Binding Assessment**: MD simulations and energy calculations evaluate binding stability
6. **Iterative Optimization**: Top designs are carried forward through multiple rounds

Multiple design strategies were explored:
- Hotspot-focused designs targeting specific CD20 residues (168-175)
- Broader interface designs covering larger regions (residues 46-210)
- Beta-model variants with enhanced structural constraints

## Results

The pipeline generated a collection of high-affinity protein binders specifically targeting the extracellular region of CD20, with strong predicted binding affinity, structural stability, and specificity for the target epitope while minimizing interaction with the cell membrane.

Our designs have been submitted to the BioML Challenge and are currently being experimentally tested alongside approximately 12,000 other designs from participating teams. Results are expected in early 2025.

## Advanced Configuration

### RFDiffusion Parameters

Different contig configurations can be used to target specific regions:

```bash
# Target specific hotspot residues
contigmap.contigs=[C168-175/0 D168-175/0 80-80]

# Target broader interface
contigmap.contigs=[C46-210/0 D46-210/0 80-80]

# Use beta model for enhanced structural constraints
inference.ckpt_override_path=$HOME/models/Complex_beta_ckpt.pt
```

### ProteinMPNN Options

Modify sequence design parameters in `src/proteinmpnn_af2/beta_model_mpnn.py`:

```python
# Number of sequence designs per scaffold
num_seq_per_target = 4  

# Temperature for sampling (higher = more diverse)
sampling_temp = 0.1
```

## References

- **RFDiffusion**:
  - Watson, J.L., Juergens, D., Bennett, N.R. et al. (2023). De novo design of protein structure and function with RFdiffusion. Nature, 620, 1089–1100. https://doi.org/10.1038/s41586-023-06415-8

- **ProteinMPNN & AlphaFold2**:
  - Bennett, N.R., Coventry, B., Goreshnik, I. et al. (2023). Improving de novo protein binder design with deep learning. Nat Commun 14, 2625. https://doi.org/10.1038/s41467-023-38328-5
  - Dauparas, J., Anishchenko, I., Bennett, N., et al. (2022). Robust deep learning–based protein sequence design using ProteinMPNN. Science, 378(6615), 49–56. https://doi.org/10.1126/science.add2187
  - Jumper, J., Evans, R., Pritzel, A., et al. (2021). Highly accurate protein structure prediction with AlphaFold. Nature, 596(7873), 583–589. https://doi.org/10.1038/s41586-021-03819-2

- **Molecular Dynamics & Energy Analysis**:
  - Eastman, P., Swails, J., Chodera, J.D., et al. (2017). OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. PLOS Computational Biology, 13(7), e1005659. https://doi.org/10.1371/journal.pcbi.1005659
  - Vangone, A., & Bonvin, A.M.J.J. (2015). Contacts-based prediction of binding affinity in protein–protein complexes. eLife, 4, e07454. https://doi.org/10.7554/eLife.07454
  - Xue, L.C., Rodrigues, J.P., Kastritis, P.L., Bonvin, A.M.J.J., & Vangone, A. (2016). PRODIGY: a web server for predicting the binding affinity of protein–protein complexes. Bioinformatics, 32(23), 3676–3678. https://doi.org/10.1093/bioinformatics/btw514

## Team

- Karl Philip Lundquist
- Abel Gurung
- Amardeep Singh
- Arjun Singh
- Dion Whitehead

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this code in your research, please cite this repository:

```bibtex
@software{lundquist2025cd20,
  author = {Lundquist, Karl Philip and Gurung, Abel and Singh, Amardeep and Singh, Arjun and Whitehead, Dion},
  title = {CD20 Protein Binder Design Pipeline},
  year = {2025},
  url = {https://github.com/klundquist/cd20-binder-design}
}
```
