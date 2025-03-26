# CD20 Protein Binder Design for the BioML Challenge 2024

## Summary
Participation in the BioML Challenge 2024: Bits to Binders competition, where we developed a computational pipeline to design novel protein binders targeting CD20 using RFDiffusion, ProteinMPNN, and AlphaFold2.

## Project Overview

This project was our team's submission to the BioML Challenge 2024: Bits to Binders competition organized by the University of Texas at Austin BioML Society. In a 5-week timeframe, we developed a comprehensive computational pipeline to design novel protein binders specifically targeting CD20, a membrane protein found on B cells and a key target for various immunotherapies. 

The competition challenged teams to design the antigen binding domain of a Chimeric Antigen Receptor (CAR) that would engage with CD20, with a strict constraint of 80 amino acids maximum length. Successful designs would activate a CAR-T cell killing and proliferation response, with all submissions being experimentally tested by LEAH Laboratories using their pooled CAR-T screening platform.

This work demonstrates the application of cutting-edge deep learning approaches and molecular simulation techniques to create functional proteins with potential therapeutic applications under real-world constraints.

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

## Results and Competition Status

Our computational design process yielded a collection of high-affinity protein binders specifically targeting the extracellular region of CD20. These final designs demonstrated strong predicted binding affinity, structural stability, and specificity for the target epitope while minimizing interaction with the cell membrane, all while meeting the competition's 80 amino acid length constraint.

Our designs have been submitted to the competition and are currently being tested by LEAH Laboratories. According to the competition organizers, approximately 12,000 proteins from all participating teams are being experimentally evaluated, with results expected in early 2025. The top three teams will be invited to present their methods based on how well their predicted designs bind to CD20, signal through a CAR, and activate a CAR-T cell proliferation and killing response.

The methodology we developed for this competition has broader implications beyond CD20. It provides a framework that could be adapted to design binders for other disease-relevant proteins, potentially leading to new therapeutic candidates for conditions where targeted protein binding is beneficial.

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

## Team and Competition Details

**Team Members:**
- Karl Philip Lundquist
- Abel Gurung
- Amardeep Singh
- Arjun Singh
- Dion Whitehead

**Competition:**
- **Event**: BioML Challenge 2024: Bits to Binders
- **Organizer**: University of Texas at Austin BioML Society
- **Design Phase**: August-September 2024 (5 weeks)
- **Target**: CD20 (B-cell surface protein)
- **Constraint**: 80 amino acids maximum length
- **Testing**: In progress by LEAH Laboratories
- **Results Expected**: Early 2025