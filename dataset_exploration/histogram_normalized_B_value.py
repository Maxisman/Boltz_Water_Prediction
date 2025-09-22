import json
import matplotlib.pyplot as plt
import numpy as np

with open("B_value_statistic.json", 'r') as f:
    data = json.load(f)

values = list(data.values())

# Determine the maximum value to set the upper limit for bins
max_value = max(values)
bins = np.arange(-5,5, 0.5) # Bins from 0 to max_value, in steps of 10

plt.figure(figsize=(10, 6))
plt.hist(values, bins=bins, edgecolor='black')
plt.title('Normalized Distribution of B-Values over all waters')
plt.xlabel('Value Categories')
plt.ylabel('Frequency')
plt.xticks(bins)
plt.grid(axis='y', alpha=0.75)

# Save the plot
plt.savefig("normalized_value_distribution_B_values_all_waters.png")