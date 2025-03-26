# CD20 Protein Binder Design

## Summary
Development of a computational pipeline to design novel protein binders targeting CD20 using RFDiffusion, ProteinMPNN, and AlphaFold2.

## Project Overview

In this project, we developed a comprehensive computational pipeline to design novel protein binders specifically targeting CD20, a membrane protein found on B cells and a key target for various immunotherapies. This work demonstrates the application of cutting-edge deep learning approaches and molecular simulation techniques to create functional proteins with potential therapeutic applications.

## The Challenge

Designing proteins that can specifically bind to targets like CD20 represents a significant frontier in therapeutic development. Traditional methods rely on experimental screening of vast libraries—a process that consumes extensive time and resources. Our team sought to address this limitation by developing a computational approach that could dramatically accelerate protein binder design, leveraging recent advances in AI and molecular simulation techniques.

CD20 is a critical protein found on B-cell surfaces and serves as a key target for numerous immunotherapies. Our goal was to create a systematic pipeline that could design novel protein binders with high specificity and affinity for this therapeutic target.

## Our Approach

We began by implementing RFDiffusion to generate initial protein binder structures complementary to the CD20 target region. This phase involved extensive parameter exploration to optimize the binding interface. We tested different configurations, including hotspot-focused designs targeting specific CD20 residues (168-175), broader interface designs covering larger regions (residues 46-210), and beta-model variants with enhanced structural constraints.

For sequence optimization, we applied ProteinMPNN, a deep learning model designed specifically for protein sequence generation. Working with Rosetta FastRelax for structural refinement, we optimized each design for both stable protein folding and strong complementarity with the CD20 extracellular domain.

Structure prediction served as our critical validation step. Using AlphaFold2, we predicted the 3D structures of our designed sequences and implemented filtering criteria to eliminate designs with poor confidence scores or structures that would protrude into the cell membrane when properly aligned with CD20. These practical constraints ensured that our designs would be functional in a biological context.

## Refinement Process

Assessing binding stability emerged as one of the most nuanced aspects of our project. We developed a workflow incorporating energy minimization and molecular dynamics simulations for side-chain relaxation. This approach allowed us to evaluate binding stability through multiple metrics: total energy calculations, non-bonded interaction energy between binder and CD20, and binding free energy estimation using Prodigy.

Our process evolved into a multi-round design strategy that balanced exploration and exploitation. We carried forward the top-performing designs through progressive iterations while continuously generating new variants to maintain diversity. Designs meeting our criteria for energy thresholds and RMSD advanced through rounds, each iteration improving stability and affinity. This iterative approach allowed us to effectively navigate the vast protein design space, systematically improving our binders' qualities while maintaining a computationally feasible search.

## Results and Impact

Our computational design process yielded a collection of high-affinity protein binders specifically targeting the extracellular region of CD20. These final designs demonstrated strong predicted binding affinity, structural stability, and specificity for the target epitope while minimizing interaction with the cell membrane.

The methodology we developed has broader implications beyond CD20. It provides a framework that could be adapted to design binders for other disease-relevant proteins, potentially leading to new therapeutic candidates for conditions where targeted protein binding is beneficial.

## Key Technologies

- **RFDiffusion** for de novo protein structure generation
- **ProteinMPNN** for deep learning-based protein sequence design
- **AlphaFold2** for protein structure prediction
- **Rosetta** for energy calculations and structural refinement
- **OpenMM** for molecular dynamics simulations
- **Prodigy** for binding affinity prediction
- **Docker** for environment containerization
- **Python** for data processing and analysis
- **Jupyter** for interactive visualization

## Repository

[GitHub Repository](https://github.com/klundquist/cd20-binder-design)

## Team

- Karl Philip Lundquist
- Abel Gurung
- Amardeep Singh
- Arjun Singh
- Dion Whitehead