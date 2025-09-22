import argparse
import os
from prody import *
import statistics
import json
import numpy as np

class General_Statistic:
    def __init__(self):
        self.rmsd = []
        self.average_distance = []
        self.water_rmsd = []
        self.share_1 = []
        self.share_2 = []
        self.share_3 = []
        self.share_4 = []

    
    def step(self, rmsd, water_rmsd, average_distance, share_1, share_2, share_3, share_4):
        self.rmsd.append(rmsd)
        self.average_distance.append(average_distance)
        self.water_rmsd.append(water_rmsd)
        self.share_1.append(share_1)
        self.share_2.append(share_2)
        self.share_3.append(share_3)
        self.share_4.append(share_4)

    def finalize(self):
        object = {
        "name": "general",
        "rmsd": statistics.mean(self.rmsd),
        "average_distance": statistics.mean(self.average_distance),
        "water_rmsd": statistics.mean(self.water_rmsd),
        "share<0.5A": statistics.mean(self.share_1),
        "share<1.0A": statistics.mean(self.share_2),
        "share<5.0A": statistics.mean(self.share_3),
        "share<10.0A": statistics.mean(self.share_4)
        }
        print(object)
        return object

def evaluate_structure(prediction, target, general:General_Statistic):
    superimposition, mobile_mapped, target_mapped, seqi, overlap = matchAlign(prediction, target)
    rmsd = calcRMSD(mobile_mapped, target_mapped)
    
    average_distance, water_rmsd, share_1, share_2, share_3, share_4 = compute_overlap_measure(superimposition, target)
    object = {
        "name": str(prediction),
        "rmsd": rmsd,
        "average_distance": average_distance,
        "water_rmsd": water_rmsd,
        "share<0.5A": share_1,
        "share<1.0A": share_2,
        "share<5A": share_3,
        "share<10A": share_3
    }
    general.step(rmsd, water_rmsd, average_distance, share_1, share_2, share_3, share_4)

    return object

def compute_overlap_measure(superimposition, target):
    distances = []
    for water in superimposition.water:
        min_distance = 100000
        for target_water in target.water:
            sample_distance = calcDistance(water, target_water)
            if sample_distance < min_distance:
                min_distance = sample_distance
                #closest_atom = target_water #ADD FUNCTIONALITY
        distances.append(min_distance)
    
    average_distance = statistics.mean(distances)
    water_rmsd = np.sqrt(np.mean(np.array(distances) ** 2))
    share_1 = sum([1 for item in distances if item < 0.5]) / len(distances)
    share_2 = sum([1 for item in distances if item < 1.0]) / len(distances)
    share_3 = sum([1 for item in distances if item < 5.0]) / len(distances)
    share_4 = sum([1 for item in distances if item < 10.0]) / len(distances)

    return average_distance, water_rmsd, share_1, share_2, share_3, share_4


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictiondir", required=True)
    parser.add_argument("--targetdir", required=True)
    parser.add_argument("--resultpath", required=True)
    args = parser.parse_args()

    output = []
    general = General_Statistic()
    for file in os.listdir(args.predictiondir):
        try:
            predicted_structure = parseMMCIF(args.predictiondir + file)
            target_structure = parseMMCIF(args.targetdir + file)
            output.append(evaluate_structure(prediction=predicted_structure, target=target_structure, general=general))
        
        except Exception as e:
            print(f"--- Error processing file:" + file + "  ---")
            print(f"Error type: {type(e).__name__}")
            print(f"Error messstructuree: {e} \n")
        
    output.append(general.finalize())

    with open(args.resultpath, 'w') as f:
        json.dump(output, f, indent = 4)

        
