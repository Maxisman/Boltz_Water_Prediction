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

data_to_plot = [H_bond_values, B_factor_values]

fig, ax = plt.subplots()
positions = []
plot_data = []
x_tick_labels = []

for i in range(min(H_bond_values), max(H_bond_values) + 1):
    temp = []
    for j, value in enumerate(H_bond_values):
        if i == value:
            temp.append(B_factor_values[j])
    if(temp):
        plot_data.append(temp)
        positions.append(i)
        x_tick_labels.append(str(i))

ax.violinplot(plot_data, positions=positions, showmeans=True)
ax.set_xticks(positions)
ax.set_xticklabels(x_tick_labels)

ax.set_xlabel("Number of Hydrogen Bonds")
ax.set_ylabel("Z-value")
ax.set_title("Z-value Distribution for Different Numbers of Hydrogen Bonds")

plt.savefig('violinplot.png')
plt.show()