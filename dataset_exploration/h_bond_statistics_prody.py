from collections import Counter
from prody import *

import json
import csv
    

def calculate_hbonds_distribution(pdb_code, statistic):
    structure = parsePDB(pdb_code)
    if not structure.water:
        return
    bonding_waters = Counter()
    for water in structure.water:
        H_bond_participants = structure.select("protein and element N O S and within 3.5 of center", center = water.getCoords())
        if (H_bond_participants):
            bonding_waters[water.getIndex()] = len(H_bond_participants)
    statistic.update(bonding_waters.values())
    save_counter_as_json(statistic)
    
def save_counter_as_json(counter):
    with open("statistic.json", 'w') as f:
        json.dump(counter, f, indent=4)


def calculate_statistic(pdb_code = None):
    if pdb_code:
        calculate_hbonds_distribution(pdb_code, Counter())

    else:
        with open('list_file.txt', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            pdb_codes = list(csv_reader)[0]

        statistic = Counter()
        fail_count = 0

        for pdb_code in pdb_codes:
            try:
                calculate_hbonds_distribution(pdb_code, statistic)
            except Exception as e:
                fail_count += 1
                print(f"--- Error processing PDB code: {pdb_code} ---")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {e} \n")

        print(fail_count)

calculate_statistic()