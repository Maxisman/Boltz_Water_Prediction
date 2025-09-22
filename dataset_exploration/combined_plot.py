import json
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load data
with open("../statistics/B_value_statistic_jun25.json", 'r') as f:
    B_values = json.load(f)
with open("../statistics/H_bonds_statistic_jun25.json", 'r') as f:
    H_bonds = json.load(f)

# Find common keys and prepare data
common_keys = sorted(list(set(B_values.keys()) & set(H_bonds.keys())))
B_factor_values = []
H_bond_values = []
for key in common_keys:
    if not math.isnan(B_values[key]):
        B_factor_values.append(B_values[key])
        H_bond_values.append(H_bonds[key])

# Create a DataFrame for easier plotting with seaborn
data = pd.DataFrame({
    'Number of Hydrogen Bonds': H_bond_values,
    'B-factor Value': B_factor_values
})

# Create a figure and axes object
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the violin plot on the axes
# `inner=None` removes the inner boxplot and quartile markers.
# `color='lightgray'` sets the color of the violin.
sns.violinplot(x='Number of Hydrogen Bonds', y='B-factor Value', data=data, ax=ax, inner=None, color='lightgray')

# Plot the swarm plot on the same axes
# `s=2` controls the size of the swarm points.
# `color='black'` makes the points stand out.
sns.swarmplot(x='Number of Hydrogen Bonds', y='B-factor Value', data=data, ax=ax, s=0.5, color='black')

# Set labels and title
ax.set_xlabel("Number of Hydrogen Bonds")
ax.set_ylabel("Z-value")
#ax.set_title("Z-value Distribution with Hydrogen Bonds")

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('combined_plot.png')
