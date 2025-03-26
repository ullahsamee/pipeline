# CD20 Protein Binder Design

## Project Overview

This project was developed for the BioML Challenge 2024: Bits to Binders competition organized by the University of Texas at Austin BioML Society. The challenge tasked teams with designing protein sequences that could effectively bind to a cancer antigen target (CD20) within a 5-week timeframe. 

Our team created a computational pipeline for designing novel protein binders targeting CD20, a B-cell surface protein crucial for immunotherapies. By combining cutting-edge deep learning models with molecular simulation techniques, we developed a systematic approach to creating protein binders with high specificity and binding affinity.

The competition required designed proteins to be constrained to 80 amino acids (due to DNA synthesis limitations) and focused on creating the antigen binding domain of a Chimeric Antigen Receptor (CAR) that would engage with CD20. Successful designs would activate a CAR-T cell killing and proliferation response, resulting in a quantifiable increase in functional binders.

This repository contains our complete codebase, organized for clarity and reproducibility, as required by the competition's open-source mandate.

## Technical Approach

### Computational Innovation

Our pipeline integrates several state-of-the-art computational methods to solve the challenging problem of protein binder design:

1. **Structure Generation with RFDiffusion**
   - Leveraged diffusion models to generate backbone scaffolds matching target interfaces
   - Explored different binding interface strategies (hotspot-focused vs. broader interface designs)
   - Implemented constraints to ensure designed proteins would not intersect with the cell membrane

2. **Deep Learning-Based Sequence Design**
   - Applied ProteinMPNN to generate optimized amino acid sequences for our scaffolds
   - Fine-tuned sampling temperature to balance sequence diversity and stability
   - Integrated with Rosetta FastRelax for energetic optimization
   - Generated multiple sequence variants per scaffold to increase exploration

3. **Structure Validation with AlphaFold2**
   - Used AlphaFold2 to predict the 3D structures of designed sequences
   - Implemented filtering criteria based on prediction confidence scores
   - Excluded designs with poor prediction quality or structural misalignment

4. **Molecular Dynamics for Binding Assessment**
   - Developed custom MD simulation protocols for side-chain relaxation
   - Calculated binding energetics using OpenMM
   - Estimated binding free energies using Prodigy
   - Combined multiple energy metrics into a composite scoring function

5. **Iterative Optimization Strategy**
   - Implemented a multi-round design pipeline balancing exploration and exploitation
   - Carried forward top performers while generating new designs in each round
   - Applied progressive filtering based on energy thresholds and structural criteria

### Technical Challenges Overcome

1. **Membrane Compatibility**
   - Developed filters to ensure binders wouldn't protrude into the cell membrane
   - Implemented z-coordinate filtering to respect biological constraints

2. **Computational Efficiency**
   - Created a Docker-based architecture to ensure portability and reproducibility
   - Optimized the pipeline for GPU acceleration where applicable
   - Developed orchestration scripts to minimize manual intervention

3. **Scoring and Ranking**
   - Designed a comprehensive scoring function combining:
     - Total energy (stability)
     - Interface energy (binding strength)
     - Prodigy ΔG predictions (binding affinity)
     - Structural quality metrics

4. **Sequence-Structure Consistency**
   - Implemented RMSD filtering to ensure consistency between design intent and predicted structures
   - Balanced sequence optimization for both folding stability and binding affinity

## Technical Implementation

### Architecture

The pipeline is organized into several components:

1. **RFDiffusion Module**
   - Containerized environment for generating protein structures
   - Configurable contigs for targeting specific epitopes
   - Options for different diffusion model checkpoints

2. **ProteinMPNN-AF2 Module**
   - Integrated sequence design and structure prediction
   - Configurable sampling parameters
   - Built-in filtering for prediction quality

3. **Analysis Module**
   - Custom filtering and ranking algorithms
   - Molecular dynamics simulation integration
   - Energy calculation and binding assessment

4. **Orchestration Layer**
   - Main pipeline control script (main.py)
   - Command-line options for selective execution
   - Automated directory management

### Technical Skills Demonstrated

This project showcases proficiency in:

- **Computational Biology**: Protein design, molecular dynamics, binding energy calculations
- **Deep Learning Applications**: Use of diffusion models and transformer-based sequence design
- **Scientific Software Engineering**: Pipeline development, containerization, orchestration
- **Data Analysis**: Custom metrics, filtering algorithms, and evaluation protocols

## Results and Competition Status

Our pipeline successfully generated a diverse set of potential CD20 binders with the following characteristics:

- Strong predicted binding affinity to the CD20 extracellular domain
- Structural stability and proper folding
- Specificity for the target epitope
- Compatibility with membrane topology constraints
- Conformity to the 80 amino acid length constraint

Our team submitted these designed sequences to the BioML Challenge competition, where they are currently in the testing stage. LEAH Laboratories is conducting experimental validation using their pooled CAR-T screening platform to evaluate how well our designs bind to CD20, signal through a CAR, and activate CAR-T cell proliferation and killing responses. According to competition updates, approximately 12,000 proteins from all teams are being tested, with results expected in early 2025.

The methodology developed for this competition has broader applications beyond CD20, providing a framework for designing binders for other therapeutically relevant proteins. Our approach demonstrates how computational methods can accelerate the discovery of potential therapeutic proteins, reducing the need for extensive experimental screening.

## Future Directions

Several technical enhancements could further improve this pipeline:

1. **Integration with experimental data feedback loops**
   - Using experimental binding data to retrain models
   - Incorporating experimental structure data when available

2. **Enhanced sampling techniques**
   - Implementing replica exchange molecular dynamics for better conformational sampling
   - Exploring alternative sequence generation models

3. **Expanded scoring functions**
   - Adding immunogenicity predictions
   - Incorporating manufacturability metrics
   - Estimating in vivo stability

4. **Web interface and visualization tools**
   - Creating interactive visualizations for design analysis
   - Developing a web interface for non-programmers

## Technical Stack

- **Programming**: Python, Bash
- **Deep Learning**: RFDiffusion, ProteinMPNN, AlphaFold2
- **Molecular Modeling**: Rosetta, OpenMM, MDAnalysis
- **Containerization**: Docker
- **Visualization**: PyMOL, Jupyter notebooks

## Competition Participation

**Event**: BioML Challenge 2024: Bits to Binders  
**Organizer**: University of Texas at Austin BioML Society  
**Timeline**: August-September 2024 (5-week design phase)  
**Target**: CD20 (announced at competition kickoff)  
**Constraint**: 80 amino acids maximum length  
**Evaluation**: LEAH Laboratories' pooled CAR-T screening platform  
**Results**: Testing in progress, expected early 2025  

Our team's participation in this competition showcases our ability to rapidly develop and implement a sophisticated computational pipeline under real-world constraints and time pressure. The challenge provided valuable experience in applying cutting-edge AI methods to protein design for therapeutic applications.

## References

The technical approach builds upon several pioneering works in computational protein design:

1. Watson, J.L., et al. (2023). De novo design of protein structure and function with RFdiffusion. *Nature*, 620, 1089–1100.
2. Bennett, N.R., et al. (2023). Improving de novo protein binder design with deep learning. *Nature Communications*, 14, 2625.
3. Dauparas, J., et al. (2022). Robust deep learning–based protein sequence design using ProteinMPNN. *Science*, 378(6615), 49–56.
4. Jumper, J., et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*, 596(7873), 583–589.
5. Eastman, P., et al. (2017). OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. *PLOS Computational Biology*, 13(7), e1005659.
6. Vangone, A., & Bonvin, A.M.J.J. (2015). Contacts-based prediction of binding affinity in protein–protein complexes. *eLife*, 4, e07454.