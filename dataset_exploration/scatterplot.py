import json
import math
import matplotlib.pyplot as plt
import numpy as np

with open("../statistics/B_value_statistic_jun25.json", 'r') as f:
    B_values = json.load(f)
with open("../statistics/H_bonds_statistic_jun25.json", 'r') as f:
    H_bonds = json.load(f)
common_keys = sorted(list(set(B_values.keys()) & set(H_bonds.keys())))


B_factor_values = []
H_bond_values = []
for key in common_keys:
    #in some files there is no B value data
    if math.isnan(B_values[key]):
        continue
    B_factor_values.append(B_values[key])
    H_bond_values.append(H_bonds[key])

correlation = np.corrcoef(B_factor_values, H_bond_values)[0,1]
print(correlation)


# Determine the maximum value to set the upper limit for bins
plt.figure(figsize=(10, 6)) # Set figure size for better readability


plt.scatter(B_factor_values, H_bond_values, alpha=0.2, color='skyblue', edgecolors='w', s=5) # s is marker size
#plt.hexbin(B_factor_values, H_bond_values, gridsize=250, cmap="viridis", mincnt=1)


#plt.xticks(range(1,2))

plt.title("Z-values and number of hydrogen bonds per water molecule")
plt.ylabel("number of hydrogen bonds")
plt.xlabel("Z-values")
#plt.grid(True, linestyle='--', alpha=0.6) # Add a grid for easier reading
plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.text(0.02, 0.98, f"Correlation: {correlation:.4f}",
             transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5))

# Save the plot
plt.savefig('scatterplot.png')
plt.show