import os
import sys
import csv
import re
from Bio.PDB import PDBParser
import numpy as np

def extract_base_design_name(name):
    # Remove prefixes
    name = re.sub(r'^rnd\d+_binder_design_', 'binder_design_', name)
    name = re.sub(r'^rnd\d+_', '', name)
    # Remove suffixes
    name = re.sub(r'_aligned_md$', '', name)
    name = re.sub(r'_aligned$', '', name)
    name = re.sub(r'_md$', '', name)
    name = re.sub(r'_fixed$', '', name)
    name = re.sub(r'_dldesign_.*$', '', name)
    name = re.sub(r'_cycle.*$', '', name)
    name = re.sub(r'_af2pred$', '', name)
    return name

def compute_radius_of_gyration(pdb_file_path, chain_id='A'):
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure('structure', pdb_file_path)
    except Exception as e:
        print(f"Error reading PDB file {pdb_file_path}: {e}")
        return None

    coords = []
    for model in structure:
        for chain in model:
            if chain.id == chain_id:
                for residue in chain:
                    for atom in residue:
                        coords.append(atom.get_coord())
                break  # Only process the specified chain

    if not coords:
        print(f"No coordinates found for chain {chain_id} in {pdb_file_path}")
        return None

    coords = np.array(coords)
    center_of_mass = np.mean(coords, axis=0)
    rg_squared = np.mean(np.sum((coords - center_of_mass) ** 2, axis=1))
    radius_of_gyration = np.sqrt(rg_squared)
    return radius_of_gyration

def merge_csv_files(energies_csv_path, prodigy_csv_path, af2_score_path, output_csv_path, pdb_dir, rg_multiplier):
    # Build energies_dict
    energies_dict = {}
    with open(energies_csv_path, 'r') as energies_file:
        energies_reader = csv.DictReader(energies_file)
        for row in energies_reader:
            output_name = row['OutputName']
            base_name = extract_base_design_name(output_name)
            energies_dict[base_name] = {
                'OutputName': output_name,
                'TotalEnergy_kJ/mol': float(row['TotalEnergy_kJ/mol']),
                'InteractionEnergy_kJ/mol': float(row['InteractionEnergy_kJ/mol'])
            }

    # Build prodigy_dict
    prodigy_dict = {}
    with open(prodigy_csv_path, 'r') as prodigy_file:
        prodigy_reader = csv.DictReader(prodigy_file)
        for row in prodigy_reader:
            file_name = row['File']
            base_name_full = os.path.splitext(file_name)[0]
            base_name = extract_base_design_name(base_name_full)
            prodigy_dict[base_name] = {
                'DeltaG_kcal/mol': float(row['DeltaG (kcal/mol)'])
            }

    # Build af2_dict
    af2_dict = {}
    with open(af2_score_path, 'r') as af2_file:
        header = None
        for line in af2_file:
            line = line.strip()
            if not line.startswith('SCORE:'):
                continue
            parts = line.split()
            if 'binder_aligned_rmsd' in line and 'description' in line:
                # Header line
                header = parts[1:]  # Skip 'SCORE:'
                rmsd_index = header.index('binder_aligned_rmsd')
                description_index = header.index('description')
                continue
            elif header is not None:
                # Data line
                data = parts[1:]  # Skip 'SCORE:'
                if len(data) <= max(rmsd_index, description_index):
                    continue
                binder_aligned_rmsd = float(data[rmsd_index])
                description = data[description_index]
                base_name = extract_base_design_name(description)
                af2_dict[base_name] = {
                    'binder_aligned_rmsd': binder_aligned_rmsd
                }

    # Merge dictionaries and compute Rg
    merged_data = []
    for base_name, energy_data in energies_dict.items():
        total_energy = energy_data['TotalEnergy_kJ/mol']
        interaction_energy = energy_data['InteractionEnergy_kJ/mol']
        output_name = energy_data['OutputName']

        # Get DeltaG
        deltaG_kcal = prodigy_dict.get(base_name, {}).get('DeltaG_kcal/mol', None)
        deltaG_kJ = deltaG_kcal * 4.184 if deltaG_kcal is not None else 0.0

        # Get binder_aligned_rmsd
        binder_aligned_rmsd = af2_dict.get(base_name, {}).get('binder_aligned_rmsd', None)

        # Exclude designs with missing or high RMSD
        if binder_aligned_rmsd is None or binder_aligned_rmsd >= 6.0:
            continue

        # Compute Radius of Gyration
        pdb_filename = output_name + '.pdb'
        pdb_file_path = os.path.join(pdb_dir, pdb_filename)
        rg = compute_radius_of_gyration(pdb_file_path, chain_id='A')
        if rg is None:
            continue  # Skip if Rg could not be computed

        # Calculate Score
        if total_energy > -9000:
            score = 5000
        else:
            if deltaG_kcal is not None:
                score = interaction_energy + deltaG_kJ * 50 + (rg - 10) * rg_multiplier
            else:
                score = None  # Or set to a default high value

        # Prepare merged row
        merged_row = {
            'OutputName': output_name,
            'TotalEnergy_kJ/mol': total_energy,
            'InteractionEnergy_kJ/mol': interaction_energy,
            'DeltaG_kcal/mol': deltaG_kcal,
            'binder_aligned_rmsd': binder_aligned_rmsd,
            'Rg': rg,
            'Score': score
        }
        merged_data.append(merged_row)

    # Write merged data
    with open(output_csv_path, 'w', newline='') as output_file:
        fieldnames = [
            'OutputName', 'TotalEnergy_kJ/mol', 'InteractionEnergy_kJ/mol',
            'DeltaG_kcal/mol', 'binder_aligned_rmsd', 'Rg', 'Score'
        ]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_data)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python merge_energies_post.py <energies_csv> <prodigy_csv> <af2_score_file> <output_csv> <pdb_dir>")
        sys.exit(1)
    energies_csv_path = sys.argv[1]
    prodigy_csv_path = sys.argv[2]
    af2_score_path = sys.argv[3]
    output_csv_path = sys.argv[4]
    pdb_dir = sys.argv[5]

    # Define the Rg multiplier (adjust this value as needed)
    rg_multiplier = 500.0  # You can change this value later

    # Ensure that Biopython is installed
    try:
        from Bio.PDB import PDBParser
    except ImportError:
        print("Biopython is required for PDB parsing. Install it using 'pip install biopython'.")
        sys.exit(1)

    merge_csv_files(energies_csv_path, prodigy_csv_path, af2_score_path, output_csv_path, pdb_dir, rg_multiplier)
    print(f"Merged data written to {output_csv_path}")
