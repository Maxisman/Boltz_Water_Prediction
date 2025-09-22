import json
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns # Import seaborn

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

# Create a DataFrame for easier plotting with seaborn
import pandas as pd
data = pd.DataFrame({
    'Number of Hydrogen Bonds': H_bond_values,
    'B-factor Value': B_factor_values
})

# Create a figure and an axes object
plt.figure(figsize=(10, 6)) # Adjust figure size as needed

# Create the swarm plot
sns.swarmplot(x='Number of Hydrogen Bonds', y='B-factor Value', data=data, s=0.2) # s controls marker size

# Add labels and title for clarity
plt.xlabel("Number of Hydrogen Bonds")
plt.ylabel("Z-value")
plt.title("Z-value Distribution for Different Numbers of Hydrogen Bonds (Swarm Plot)")

plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.savefig('swarmplot.png')
plt.show()