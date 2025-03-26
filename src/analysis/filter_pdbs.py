# filter_pdbs.py

import os
import sys

def delete_if_z_positive(pdb_file):
    with open(pdb_file, 'r') as file:
        for line in file:
            if line.startswith("ATOM"):
                chain = line[21]  # Chain identifier is in column 22 (index 21)
                z_coord = float(line[46:54].strip())  # z-coordinate is in columns 47-54
                if chain == 'A' and z_coord > 0:
                    print(f"Deleting {pdb_file} as an atom in chain A has z > 0")
                    os.remove(pdb_file)
                    return

def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdb'):
            pdb_file_path = os.path.join(folder_path, file_name)
            delete_if_z_positive(pdb_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filter_pdbs.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory")
        sys.exit(1)
    
    process_folder(folder_path)
