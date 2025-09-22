from collections import Counter
from prody import *
import numpy as np

import json
import csv
    

def calculate_B_values_as_dict(pdb_code, statistic):
    structure = parsePDB(pdb_code)
    if not structure.water:
        return
    nparray = np.array(structure.water.getBetas())#added .water
    for water in structure.water:
        statistic[pdb_code + str(water.getIndex())] = (water.getBeta() - nparray.mean()) / nparray.std()
    save_dict_as_json(statistic)
    
def save_dict_as_json(counter):
    with open("B_value_statistic.json", 'w') as f:
        json.dump(counter, f, indent=4)


def calculate_statistic(pdb_code = None):
    if pdb_code:
        calculate_B_values_as_dict(pdb_code, {})

    else:
        with open('list_file.txt', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            pdb_codes = list(csv_reader)[0]

        statistic = Counter()
        fail_count = 0

        for pdb_code in pdb_codes:
            try:
                calculate_B_values_as_dict(pdb_code, statistic)
            except Exception as e:
                fail_count += 1
                print(f"--- Error processing PDB code: {pdb_code} ---")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {e} \n")

        print(fail_count)

calculate_statistic()