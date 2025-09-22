import argparse
from prody import *
import numpy as np
import csv
import re

H_BOND_DISTANCE_CUTOFF = 3.5
METAL_BOND_CUTOFF = 3

def set_normalized_betas(structure):
    nparray = np.array(structure.getBetas())
    mean = nparray.mean()
    std = nparray.std()
    for index, entry in enumerate(nparray):
        nparray[index] = (entry - mean) / std

    structure.setBetas(nparray)

def set_bond_numbers(structure):
    water_hydrogen_bonds = np.full([structure.numAtoms()], -1, dtype = int)
    for water in structure.water:
        H_bond_participants = structure.select("not water and element N O S and within " + str(H_BOND_DISTANCE_CUTOFF) + " of center", center = water.getCoords())

        if H_bond_participants == None:
            water_hydrogen_bonds[water.getIndex()] = 0
            continue

        water_hydrogen_bonds[water.getIndex()] = len(H_bond_participants)

    structure.setData("water_hydrogen_bonds", water_hydrogen_bonds)

def set_metal_bond_numbers(structure):
    water_metal_bonds = np.full([structure.numAtoms()], -1, dtype = int)
    for water in structure.water:
        metal_neighborhood = structure.select("(ion or element MN FE CO NI CU ZN CA NA K MG) and within " + str(METAL_BOND_CUTOFF) + " of center", center = water.getCoords())
        water_metal_bonds[water.getIndex()] = 0 if metal_neighborhood == None else len(metal_neighborhood)
    structure.setData("water_metal_bonds", water_metal_bonds)

def remove_designated_waters(infile_path, outfile_path, atoms_to_be_removed):
    indices = atoms_to_be_removed.getIndices()
    with open(infile_path, 'r') as infile, open(outfile_path, 'w') as outfile:
        for line in infile:
            if not line.startswith("HETATM"):
                outfile.write(line)
                continue

            atom_index_str = line.split()[1]
            try:
                atom_index = int(atom_index_str)
                if atom_index in indices:
                    continue
                else:
                    outfile.write(line)
            except ValueError:
                print(f"Warning: Could not parse atom index from HETATM line: {line.strip()}. Keeping line.")
                outfile.write(line)



def select_good_waters(pdb_code, origin_file_directory, save_file_directory):
    structure = parseMMCIF(origin_file_directory + pdb_code.lower() + ".cif")
    if not structure.water:
        print("no water in " + pdb_code)
        return
    
    set_normalized_betas(structure)
    set_bond_numbers(structure)
    set_metal_bond_numbers(structure)

    #final selection
    filtered_structure = structure.select(  "not water or ("
                                                "beta < 0.5 and occupancy >= 1.0 and (" \
                                                    "water_hydrogen_bonds >= 2 or water_metal_bonds >= 1" \
                                                ")" \
                                            ")")
    remove_designated_waters(origin_file_directory + pdb_code.lower() + ".cif", save_file_directory + "/filtered_" + pdb_code + ".cif", (~filtered_structure))

#    writeMMCIF(save_file_directory + "/filtered_" + pdb_code, filtered_structure, autoext=True)


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
            select_good_waters(pdb_code, args.inputdir, args.outputdir)
        except Exception as e:
            fail_count += 1
            print(f"--- Error processing PDB code: {pdb_code} ---")
            print(f"Error type: {type(e).__name__}")
            print(f"Error messstructuree: {e} \n")

    print("Errors encountered:" + str(fail_count))
