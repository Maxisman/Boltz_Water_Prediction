from prody import *
import csv
import argparse


def remove_water_hydrogens(infile_path, outfile_path):
    with open(infile_path, 'r') as infile, open(outfile_path, 'w') as outfile:
        for line in infile:
            if not line.startswith("HETATM"):
                outfile.write(line)
                continue
            atom_type_str = line.split()[2]
            residue_type_str = line.split()[5]
            try:
                if atom_type_str == "H" and residue_type_str == "HOH":
                    continue
                else:
                    outfile.write(line)
            except ValueError:
                print(f"Warning: Could not parse atom index from HETATM line: {line.strip()}. Keeping line.")
                outfile.write(line)   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdblist", required=True) #required=False, default="./list_file_short.csv")
    parser.add_argument("--inputdir", required=True) #required=False, default = "/home/iwe78/Documents/PDBFiles/unfiltered_cif/")
    parser.add_argument("--outputdir", required=True) #required=False, default = "/home/iwe78/Documents/PDBFiles/filtered_cif/")
    args = parser.parse_args()

    with open(args.pdblist, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            pdb_codes = list(csv_reader)[0]

    fail_count = 0
    for pdb_code in pdb_codes:
            try:
                remove_water_hydrogens(args.inputdir + "filtered_" + pdb_code + ".cif", args.outputdir + "filtered_" + pdb_code + ".cif")
            except Exception as e:
                fail_count += 1
                print(f"--- Error processing PDB code: {pdb_code} ---")
                print(f"Error type: {type(e).__name__}")
                print(f"Error messstructuree: {e} \n")

