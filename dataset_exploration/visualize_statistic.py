from matplotlib import pyplot as plt
import json


fig, ax = plt.subplots()
#counts = [1,2,3,4,5,6,7,8]
with open("./statistics/statistic_jun24_3.5A.json", 'r') as f:
    counter = json.load(f)

sorted_items = sorted(counter.items(), key=lambda item: int(item[0]))
sorted_keys = [item[0] for item in sorted_items]
sorted_values = [item[1] for item in sorted_items]

p = ax.bar(sorted_keys, sorted_values, label=sorted_keys)
ax.bar_label(p, label_type='edge')

ax.set_ylabel('number of occurences')
ax.set_xlabel('number of hydrogen bonds')
#ax.set_title('distribution of number of water-biomolecule hydrogen bonds per water in a random pdb sample')
#ax.legend(title='number of h_bonds per water')
plt.savefig("distribution.png")