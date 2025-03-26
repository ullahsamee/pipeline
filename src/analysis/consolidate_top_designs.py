import os
import csv
import shutil
from Bio.PDB import PDBParser, PPBuilder

def consolidate_designs(
    top_designs_dirs,
    output_dir,
    consolidated_top_n=500,
    pdb_subfolder='',
    csv_filename='top_designs.csv'
):
    all_data = []

    # Iterate over the provided top_designs directories
    for designs_dir in top_designs_dirs:
        csv_path = os.path.join(designs_dir, csv_filename)
        if not os.path.isfile(csv_path):
            print(f"No {csv_filename} in {designs_dir}")
            continue

        # Read the top_designs.csv file
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Add source folder information to row
                row['SourceFolder'] = os.path.basename(designs_dir)
                # Store the original rank from the source folder
                row['SourceRank'] = row['Rank']
                all_data.append(row)

    # Convert energies to floats and handle missing or invalid data
    for row in all_data:
        try:
            row['Score'] = float(row['Score'])
        except (ValueError, TypeError):
            row['Score'] = None  # Handle invalid scores
        # Convert other energy fields as needed
        for key in ['TotalEnergy_kJ/mol', 'InteractionEnergy_kJ/mol', 'DeltaG_kcal/mol', 'binder_aligned_rmsd', 'Rg']:
            try:
                row[key] = float(row[key])
            except (ValueError, TypeError):
                row[key] = None  # Handle missing or invalid values

    # Remove rows with invalid scores
    all_data = [row for row in all_data if row['Score'] is not None]

    # Sort all data by Score (ascending)
    sorted_data = sorted(all_data, key=lambda x: x['Score'])

    # Take top N designs
    top_designs = sorted_data[:consolidated_top_n]

    # Prepare output CSV data
    output_csv_rows = []
    output_csv_header = [
        'Rank', 'OutputName', 'SourceFolder', 'SourceRank', 'Round', 'TotalEnergy_kJ/mol',
        'InteractionEnergy_kJ/mol', 'DeltaG_kcal/mol', 'binder_aligned_rmsd', 'Rg', 'Score'
    ]

    # Create output directory for PDB files
    os.makedirs(output_dir, exist_ok=True)

    # Prepare to extract sequences
    parser = PDBParser(QUIET=True)
    ppb = PPBuilder()
    fasta_lines = []

    # For each top design, copy the PDB file and rename it
    for rank, row in enumerate(top_designs, start=1):
        output_name = row['OutputName']
        source_folder = row['SourceFolder']
        source_rank = int(row['SourceRank'])  # Use the original rank from the source folder
        round_folder = row.get('Round', '')
        source_designs_dir = os.path.join(source_folder, pdb_subfolder)

        # Construct the PDB filename using the source rank
        pdb_filename = f"{source_rank:03d}_{output_name}.pdb"
        source_pdb_path = os.path.join(source_folder, pdb_filename)

        # If the PDB file is not found in the source folder, try to locate it
        if not os.path.isfile(source_pdb_path):
            # Try to find the PDB in the source designs directory
            source_pdb_path = os.path.join(source_folder, pdb_subfolder, pdb_filename)
            if not os.path.isfile(source_pdb_path):
                print(f"PDB file {pdb_filename} not found in {source_folder}.")
                continue

        # Prepare new PDB filename with numerical prefix and source folder identification
        new_pdb_filename = f"{rank:03d}_{source_folder}_{output_name}.pdb"
        dest_pdb_path = os.path.join(output_dir, new_pdb_filename)

        # Copy and rename the PDB file
        shutil.copyfile(source_pdb_path, dest_pdb_path)

        team_name = "Molecule_Masters"
        # Extract the sequence of chain A
        try:
            structure = parser.get_structure(output_name, dest_pdb_path)
            for model in structure:
                for chain in model:
                    if chain.id == 'A':
                        sequence = ''.join(str(pp.get_sequence()) for pp in ppb.build_peptides(chain))
                        fasta_lines.append(f">{rank:03d}_{team_name}\n{sequence}")
                        break  # Only process chain A
        except Exception as e:
            print(f"Error extracting sequence from {dest_pdb_path}: {e}")
            continue

        # Prepare row for output CSV
        row_copy = row.copy()  # Create a copy to avoid modifying the original row
        row_copy['Rank'] = rank  # Update rank to consolidated rank
        output_csv_rows.append(row_copy)

    # Write the sorted designs and their data to a new CSV file
    output_csv_path = os.path.join(output_dir, 'top_designs.csv')
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output_csv_header)
        writer.writeheader()
        for row in output_csv_rows:
            writer.writerow({
                'Rank': row['Rank'],
                'OutputName': row['OutputName'],
                'SourceFolder': row['SourceFolder'],
                'SourceRank': row['SourceRank'],
                'Round': row.get('Round', ''),
                'TotalEnergy_kJ/mol': row['TotalEnergy_kJ/mol'],
                'InteractionEnergy_kJ/mol': row['InteractionEnergy_kJ/mol'],
                'DeltaG_kcal/mol': row['DeltaG_kcal/mol'],
                'binder_aligned_rmsd': row['binder_aligned_rmsd'],
                'Rg': row['Rg'],
                'Score': row['Score'],
            })

    # Write the sequences to a FASTA file
    fasta_output_path = os.path.join(output_dir, 'top_designs_sequences.fasta')
    with open(fasta_output_path, 'w') as fasta_file:
        fasta_file.write('\n'.join(fasta_lines))

    print(f"Top {len(output_csv_rows)} designs have been consolidated and data saved to {output_csv_path}")
    print(f"FASTA file of chain A sequences saved to {fasta_output_path}")

if __name__ == '__main__':
    # Directories containing the top designs
    top_designs_dirs = ['top_designs', 'top_designs_old']

    # Directory to save consolidated top designs
    output_dir = 'top_designs_consolidated'

    # Number of top designs to consolidate
    consolidated_top_n = 500  # Adjust this as needed

    consolidate_designs(top_designs_dirs, output_dir, consolidated_top_n)
