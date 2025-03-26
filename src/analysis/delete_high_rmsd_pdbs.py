import os
import sys

def delete_high_rmsd_pdbs(af2_score_path, pdb_dirs, rmsd_threshold=6.0):
    # Read af2 score file (out_*.sc) to identify high RMSD designs
    high_rmsd_designs = []
    with open(af2_score_path, 'r') as af2_file:
        header = None
        for line in af2_file:
            line = line.strip()
            if not line.startswith('SCORE:'):
                continue
            parts = line.split()
            if 'binder_aligned_rmsd' in line and 'description' in line:
                # This is the header line
                header = parts[1:]  # Skip 'SCORE:'
                # Find the index of 'binder_aligned_rmsd' and 'description'
                try:
                    rmsd_index = header.index('binder_aligned_rmsd')
                    description_index = header.index('description')
                except ValueError as e:
                    print(f"Error: Column not found in header: {e}")
                    sys.exit(1)
                continue
            elif header is not None:
                # This is a data line
                data = parts[1:]  # Skip 'SCORE:'
                # Ensure the data has enough columns
                if len(data) < max(rmsd_index, description_index) + 1:
                    print(f"Warning: Incomplete data line skipped: {line}")
                    continue
                try:
                    binder_aligned_rmsd = float(data[rmsd_index])
                    description = data[description_index]
                    if binder_aligned_rmsd > rmsd_threshold:
                        high_rmsd_designs.append(description)
                except ValueError as e:
                    print(f"Error parsing line: {line}. Error: {e}")
                    continue
            else:
                print("Warning: Data line encountered before header. Skipping line.")
                continue

    # Delete corresponding PDB files from specified directories
    for design in high_rmsd_designs:
        for pdb_dir in pdb_dirs:
            pdb_path = os.path.join(pdb_dir, design + '.pdb')
            if os.path.isfile(pdb_path):
                os.remove(pdb_path)
                print(f"Deleted {pdb_path}")
            else:
                print(f"PDB file {pdb_path} not found.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python delete_high_rmsd_pdbs.py <af2_score_path> <pdb_dir1> [<pdb_dir2> ...]")
        sys.exit(1)

    af2_score_path = sys.argv[1]
    pdb_dirs = sys.argv[2:]

    delete_high_rmsd_pdbs(af2_score_path, pdb_dirs)
