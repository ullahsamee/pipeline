import os
from pdbfixer import PDBFixer
from openmm.app import PDBFile
import openmm as mm
from openmm import app
from openmm import unit
import numpy as np
import csv
import sys
import textwrap

def fix_pdb(input_pdb_path, fixed_pdb_path):
    from pdbfixer import PDBFixer
    from openmm.app import PDBFile

    # Load the PDB file
    fixer = PDBFixer(filename=input_pdb_path)
    
    # Identify missing residues
    fixer.findMissingResidues()
    
    # Clear the missingResidues dictionary to prevent adding any missing residues
    fixer.missingResidues = {}
    
    # Do not call fixer.addMissingResidues()
    
    # Find and replace nonstandard residues
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    
    # Find missing atoms and add them
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    
    # Add missing hydrogens (pH 7.0)
    fixer.addMissingHydrogens(7.0)
    
    # Write the fixed PDB file
    with open(fixed_pdb_path, 'w') as outfile:
        PDBFile.writeFile(fixer.topology, fixer.positions, outfile)
    
    print(f"Fixed PDB written to {fixed_pdb_path}")

def run_minimization_and_md(input_pdb_path, output_pdb_path, energy_csv_path):
    
    # Load the PDB file
    pdb = app.PDBFile(input_pdb_path)
    
    # Define the force field
    forcefield = app.ForceField('amber14-all.xml')
    
    # Create a Modeller object
    modeller = app.Modeller(pdb.topology, pdb.positions)
    
    # Add missing hydrogens
    modeller.addHydrogens(forcefield)
    
    # Create the system
    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=app.NoCutoff,
        constraints=app.HBonds
    )
    
    # Identify atoms in Chain A
    chainA_atoms = [atom.index for atom in modeller.topology.atoms() if atom.residue.chain.id == 'A']
    
    # Identify atoms in Chains C and D
    chainCD_atoms = [atom.index for atom in modeller.topology.atoms() if atom.residue.chain.id in ['C', 'D']]
    
    # Find the NonbondedForce
    nonbonded_force = None
    for force in system.getForces():
        if isinstance(force, mm.NonbondedForce):
            nonbonded_force = force
            break
    if nonbonded_force is None:
        raise ValueError("No NonbondedForce found in the system.")
    
    expression = '4*sqrt(epsilon1*epsilon2)*((0.5*(sigma1 + sigma2)/r)^12 - (0.5*(sigma1 + sigma2)/r)^6) + (138.935456*q1*q2)/r'
    interaction_force = mm.CustomNonbondedForce(expression)
    interaction_force.addPerParticleParameter('q')
    interaction_force.addPerParticleParameter('sigma')
    interaction_force.addPerParticleParameter('epsilon')
    interaction_force.setNonbondedMethod(mm.CustomNonbondedForce.NoCutoff)
    interaction_force.addInteractionGroup(chainA_atoms, chainCD_atoms)
    
    # Add particles to the CustomNonbondedForce
    for index in range(system.getNumParticles()):
        charge, sigma, epsilon = nonbonded_force.getParticleParameters(index)
        interaction_force.addParticle([charge, sigma, epsilon])
    
    # Copy exclusions from NonbondedForce to CustomNonbondedForce
    for index in range(nonbonded_force.getNumExceptions()):
        p1, p2, chargeProd, sigma, epsilon = nonbonded_force.getExceptionParameters(index)
        interaction_force.addExclusion(p1, p2)
    
    # Assign a force group to the interaction force
    interaction_force.setForceGroup(1)
    
    # Add the interaction force to the system
    system.addForce(interaction_force)
    
    # Apply position restraints to backbone atoms
    backbone_atoms = [atom.index for atom in modeller.topology.atoms() if atom.name in ['N', 'CA', 'C', 'O']]
    force = mm.CustomExternalForce('0.5 * k * ((x - x0)^2 + (y - y0)^2 + (z - z0)^2)')
    force.addPerParticleParameter('x0')
    force.addPerParticleParameter('y0')
    force.addPerParticleParameter('z0')
    force.addGlobalParameter('k', 1000.0 * unit.kilojoule_per_mole / unit.nanometer**2)
    for index in backbone_atoms:
        position = modeller.positions[index]
        force.addParticle(index, position.value_in_unit(unit.nanometer))
    system.addForce(force)
    
    # Set up the integrator
    integrator = mm.LangevinIntegrator(
        300 * unit.kelvin,
        1.0 / unit.picoseconds,
        0.002 * unit.picoseconds
    )
    
    # Create the simulation object
    platform = mm.Platform.getPlatformByName('CUDA')  # Use 'CUDA' if available
    simulation = app.Simulation(modeller.topology, system, integrator, platform)
    
    # Set the initial positions
    simulation.context.setPositions(modeller.positions)
    
    # Minimize the energy
    print('Minimizing energy...')
    simulation.minimizeEnergy(maxIterations=1000)
    
    # Initialize velocities
    simulation.context.setVelocitiesToTemperature(300 * unit.kelvin)
    
    # Set up reporters (optional)
    # simulation.reporters.append(app.PDBReporter(output_pdb_path, 1000))  # Write the final structure
    
    # Run the simulation and compute interaction energy
    n_steps = 2000
    report_interval = 100
    
    for step in range(0, n_steps, report_interval):
        simulation.step(report_interval)
        
        # Get total potential energy
        state = simulation.context.getState(getEnergy=True)
        total_energy = state.getPotentialEnergy()
        
        # Get interaction energy
        interaction_state = simulation.context.getState(getEnergy=True, groups={1})
        interaction_energy = interaction_state.getPotentialEnergy()
        
        print(f"Step {simulation.currentStep}, Total Energy: {total_energy}, Interaction Energy (A - CD): {interaction_energy}")
    
    print(f'Simulation complete. Output written to {output_pdb_path}')
    final_state = simulation.context.getState(getPositions=True, getEnergy=True)

    positions = final_state.getPositions()
    with open(output_pdb_path, 'w') as f:
        app.PDBFile.writeFile(simulation.topology, positions, f)

    # Get final energies
    final_total_energy = final_state.getPotentialEnergy()
    final_interaction_state = simulation.context.getState(getEnergy=True, groups={1})
    final_interaction_energy = final_interaction_state.getPotentialEnergy()

    # Write energies to CSV
    output_name = os.path.splitext(os.path.basename(output_pdb_path))[0]  # Remove '.pdb' extension

    # Check if CSV file exists to write headers
    file_exists = os.path.isfile(energy_csv_path)
    with open(energy_csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            # Write header if file does not exist
            writer.writerow(['OutputName', 'TotalEnergy_kJ/mol', 'InteractionEnergy_kJ/mol'])
        writer.writerow([
            output_name,
            final_total_energy.value_in_unit(unit.kilojoule_per_mole),
            final_interaction_energy.value_in_unit(unit.kilojoule_per_mole)
        ])

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python run_md.py <input_pdb> <fixed_pdb> <output_md_pdb> <energy_csv>")
        sys.exit(1)

    input_pdb_path = sys.argv[1]
    fixed_pdb_path = sys.argv[2]
    output_pdb_path = sys.argv[3]
    energy_csv_path = sys.argv[4]

    # Ensure the output directories exist
    os.makedirs(os.path.dirname(fixed_pdb_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_pdb_path), exist_ok=True)

    # Check if input file exists
    if not os.path.isfile(input_pdb_path):
        print(f"Input PDB file not found: {input_pdb_path}")
        sys.exit(1)

    # Fix the PDB file
    try:
        fix_pdb(input_pdb_path, fixed_pdb_path)
    except Exception as e:
        print(f"Error fixing file {input_pdb_path}: {e}")
        sys.exit(1)

    # Run the MD simulation with the fixed PDB file
    try:
        run_minimization_and_md(fixed_pdb_path, output_pdb_path, energy_csv_path)
    except Exception as e:
        print(f"Error processing file {fixed_pdb_path}: {e}")
        sys.exit(1)
