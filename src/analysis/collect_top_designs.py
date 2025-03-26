import os
import csv
import shutil

def collect_and_sort_designs(rounds_dir, output_dir, top_n=300):
    all_data = []

    # Iterate over all rounds
    for round_folder in sorted(os.listdir(rounds_dir)):
        round_path = os.path.join(rounds_dir, round_folder)
        if not os.path.isdir(round_path):
            continue

        merged_csv_path = os.path.join(round_path, 'merged_energies_post.csv')  # Updated filename
        if not os.path.isfile(merged_csv_path):
            print(f"No merged_energies_post.csv in {round_path}")
            continue

        # Read merged_energies.csv
        with open(merged_csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Add round information to row
                row['Round'] = round_folder
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

    # Remove rows with invalid scores or missing binder_aligned_rmsd
    all_data = [row for row in all_data if row['Score'] is not None and row['binder_aligned_rmsd'] is not None]

    # Sort all data by Score (ascending)
    sorted_data = sorted(all_data, key=lambda x: x['Score'])

    # Take top N designs
    top_designs = sorted_data[:top_n]

    # Prepare output CSV data
    output_csv_rows = []
    output_csv_header = [
        'Rank', 'OutputName', 'Round', 'TotalEnergy_kJ/mol',
        'InteractionEnergy_kJ/mol', 'DeltaG_kcal/mol',
        'binder_aligned_rmsd', 'Rg', 'Score'
    ]

    # Create output directory for PDB files
    os.makedirs(output_dir, exist_ok=True)

    # For each top design, copy the PDB file and rename it
    for rank, row in enumerate(top_designs, start=1):
        output_name = row['OutputName']
        round_folder = row['Round']

        # Locate the PDB file in rounds/$i/md_output/
        pdb_filename = output_name + '.pdb'
        md_output_dir = os.path.join(rounds_dir, round_folder, 'md_output')
        pdb_path = os.path.join(md_output_dir, pdb_filename)

        if not os.path.isfile(pdb_path):
            print(f"PDB file {pdb_path} not found.")
            continue

        # Prepare new PDB filename with numerical prefix
        new_pdb_filename = f"{rank:03d}_{output_name}.pdb"
        dest_pdb_path = os.path.join(output_dir, new_pdb_filename)

        # Copy and rename the PDB file
        shutil.copyfile(pdb_path, dest_pdb_path)

        # Add rank to the row and collect for output CSV
        row['Rank'] = rank
        output_csv_rows.append(row)

    # Write the sorted designs and their data to a new CSV file
    output_csv_path = os.path.join(output_dir, 'top_designs.csv')
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output_csv_header)
        writer.writeheader()
        for row in output_csv_rows:
            writer.writerow({
                'Rank': row['Rank'],
                'OutputName': row['OutputName'],
                'Round': row['Round'],
                'TotalEnergy_kJ/mol': row['TotalEnergy_kJ/mol'],
                'InteractionEnergy_kJ/mol': row['InteractionEnergy_kJ/mol'],
                'DeltaG_kcal/mol': row['DeltaG_kcal/mol'],
                'binder_aligned_rmsd': row['binder_aligned_rmsd'],
                'Rg': row['Rg'],
                'Score': row['Score'],
            })

    print(f"Top {len(output_csv_rows)} designs have been copied and data saved to {output_csv_path}")

if __name__ == '__main__':
    # Set the path to the directory containing the rounds folders
    rounds_dir = 'rounds_old4'  # Adjust this if your rounds directory is named differently
    output_dir = 'top_designs_old'  # Directory to save top PDBs and CSV file
    collect_and_sort_designs(rounds_dir, output_dir, top_n=500)
    
    rounds_dir = 'rounds'  # Adjust this if your rounds directory is named differently
    output_dir = 'top_designs'  # Directory to save top PDBs and CSV file
    collect_and_sort_designs(rounds_dir, output_dir, top_n=1000)
