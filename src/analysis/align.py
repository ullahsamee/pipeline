import os
import sys
import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.core.universe import Merge

def align_and_write(pdb1_path, pdb2_path, cd20_path, output_pdb_path):
    # Load the PDB files into MDAnalysis Universes
    u_rf = mda.Universe(pdb1_path, guess_bonds=False, topology_format='PDB', guess_element=True)
    u_af = mda.Universe(pdb2_path, guess_bonds=False, topology_format='PDB', guess_element=True)
    u_cd20 = mda.Universe(cd20_path, guess_bonds=False, topology_format='PDB', guess_element=True)
    
    # Align chain A from PDB2 to chain A from PDB1 using backbone atoms
    chainA_rf = u_rf.select_atoms("chainID A")  # Chain A from PDB1 (reference)
    chainA_af = u_af.select_atoms("chainID A")  # Chain A from PDB2 (mobile)

    align.alignto(chainA_af, chainA_rf, select="backbone")
    
    # Align protein parts of chains C and D from cd20_path to chain B from PDB1 using backbone atoms
    chainB_rf = u_rf.select_atoms("chainID B")  # Chain B from PDB1 (reference)
    
    # Select only protein residues from chains C and D in cd20_path
    chainsCD_cd20 = u_cd20.select_atoms("(chainID C or chainID D) and protein")
    
    # Align the protein parts of chains C and D to chain B of PDB1 using backbone atoms
    align.alignto(chainsCD_cd20, chainB_rf, select="backbone")
    
    # Merge the aligned chain A from PDB2 and the aligned protein parts of chains C and D from cd20_path
    merged = Merge(chainA_af, chainsCD_cd20)
    
    # Write the merged structure to the output PDB file
    merged.atoms.write(output_pdb_path)
    
    print(f"Aligned PDB written to {output_pdb_path}")

def find_matching_af_pdb(af_folder, base_name):
    matching_files = [f for f in os.listdir(af_folder) if f.startswith(base_name) and f.endswith('.pdb')]
    
    if len(matching_files) == 0:
        raise FileNotFoundError(f"No matching AF2 PDB file found for {base_name} in {af_folder}")
    elif len(matching_files) > 1:
        raise Exception(f"Multiple matching AF2 PDB files found for {base_name} in {af_folder}: {matching_files}")
    
    return matching_files[0]

def process_folders(rf_folder, af_folder, cd20_path, output_folder):
    rf_files = {f for f in os.listdir(rf_folder) if f.endswith('.pdb')}
    
    for rf_file in rf_files:
        base_name = rf_file.split('.')[0]  # e.g., binder_design_0
        
        try:
            matching_af_file = find_matching_af_pdb(af_folder, base_name)
        except Exception as e:
            print(e)
            continue
        
        rf_pdb_path = os.path.join(rf_folder, rf_file)
        af_pdb_path = os.path.join(af_folder, matching_af_file)
        output_pdb_path = os.path.join(output_folder, f"{base_name}_aligned.pdb")
        
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Call the align_and_write function
        try:
            align_and_write(rf_pdb_path, af_pdb_path, cd20_path, output_pdb_path)
        except Exception as e:
            print(f"Error processing {base_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python align.py <rf_folder> <af_folder> <cd20_path> <output_folder>")
        sys.exit(1)
    
    rf_folder = sys.argv[1]
    af_folder = sys.argv[2]
    cd20_path = sys.argv[3]
    output_folder = sys.argv[4]

    if not os.path.isdir(rf_folder) or not os.path.isdir(af_folder):
        print("Error: One or both input folders are invalid.")
        sys.exit(1)
    
    if not os.path.isfile(cd20_path):
        print(f"Error: CD20 PDB file not found: {cd20_path}")
        sys.exit(1)

    process_folders(rf_folder, af_folder, cd20_path, output_folder)
