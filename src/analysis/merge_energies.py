import os
import sys
import csv

def merge_csv_files(energies_csv_path, prodigy_csv_path, output_csv_path):
    # Read energies.csv into a dictionary
    energies_dict = {}
    with open(energies_csv_path, 'r') as energies_file:
        energies_reader = csv.DictReader(energies_file)
        for row in energies_reader:
            output_name = row['OutputName']
            energies_dict[output_name] = {
                'TotalEnergy_kJ/mol': float(row['TotalEnergy_kJ/mol']),
                'InteractionEnergy_kJ/mol': float(row['InteractionEnergy_kJ/mol'])
            }

    # Read prodigy_scores.csv into a dictionary
    prodigy_dict = {}
    with open(prodigy_csv_path, 'r') as prodigy_file:
        prodigy_reader = csv.DictReader(prodigy_file)
        for row in prodigy_reader:
            file_name = row['File']
            # Remove file extension if present
            base_name = os.path.splitext(file_name)[0]
            prodigy_dict[base_name] = {
                'DeltaG_kcal/mol': float(row['DeltaG (kcal/mol)'])
            }

    # Merge the dictionaries
    merged_data = []
    for output_name in energies_dict:
        total_energy = energies_dict[output_name]['TotalEnergy_kJ/mol']
        interaction_energy = energies_dict[output_name]['InteractionEnergy_kJ/mol']

        # Match the names between energies_dict and prodigy_dict
        if output_name in prodigy_dict:
            deltaG_kcal = prodigy_dict[output_name]['DeltaG_kcal/mol']
            # Convert DeltaG from kcal/mol to kJ/mol
            deltaG_kJ = deltaG_kcal * 4.184
        else:
            # Handle missing DeltaG values
            deltaG_kcal = None
            deltaG_kJ = 0.0  # Assuming zero if DeltaG is missing

        # Calculate Score
        if total_energy > -9500:
            score = 0
        else:
            if deltaG_kcal is not None:
                score = interaction_energy + deltaG_kJ * 50
            else:
                score = None  # Or set a default value if preferred

        # Prepare the merged row
        merged_row = {
            'OutputName': output_name,
            'TotalEnergy_kJ/mol': total_energy,
            'InteractionEnergy_kJ/mol': interaction_energy,
            'DeltaG_kcal/mol': deltaG_kcal,
            'Score': score
        }
        merged_data.append(merged_row)

    # Write the merged data to a new CSV file
    with open(output_csv_path, 'w', newline='') as output_file:
        fieldnames = ['OutputName', 'TotalEnergy_kJ/mol', 'InteractionEnergy_kJ/mol', 'DeltaG_kcal/mol', 'Score']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_energies.py <energies_csv_path> <prodigy_csv_path> <output_csv_path>")
        sys.exit(1)

    energies_csv_path = sys.argv[1]
    prodigy_csv_path = sys.argv[2]
    output_csv_path = sys.argv[3]

    merge_csv_files(energies_csv_path, prodigy_csv_path, output_csv_path)
    print(f"Merged data written to {output_csv_path}")
