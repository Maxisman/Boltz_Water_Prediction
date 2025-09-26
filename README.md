This repository offers supplementary material for Maximilian Kleineberg's bachelor thesis "Extending the capabilities of AI structure prediction tools to reconstruct the locations of water molecules". It contains files that were used for dataset exploration, dataset curation, training, and evaluation. Also it contains several figures from the dataset exploration.

Contents:
filterWaters.py: filter a directory of .cif files and remove waters as specified in the thesis
training_parameters.yaml: training configurations for finetuning
figures: figures created for dataset exploration
evaluation:
  evaluate_predictions.py: evaluate a directory of predicted structures on rmsd, average_distance, water_rmsd, share,0.5, share<1.0, share,5.0, share<10.0
  fix_predictions.py: fix the problem with corrupted predictions
  ids_successful_Boltz-1_evaluation: PDB ids of Boltz-1 predictions that could be aligned
  ids_successful_modified-Boltz_evaluation: PDB ids of modified-Boltz predictions that could be aligned
  evaluation_results: .json files with the results from running prediction on Casp/test dataset, with modified-Boltz (trained) and Boltz-1 (untrained) on 30 or N waters
dataset_exploration:
  B_value_statistic: File that describes B values (normalized over all atoms) of all water molecules in the sample (+ Python script to create it)
  H_bonds_statistic: File that describes number of hydrogen bonds for each water in the sample (+ Python script to create it)
  combined_plot.py: code to create a plot combining violin and swarm plot
  h_bond_statistics_prody.py: saves figure of distribution of hydrogen bonds per water
  histogram_normalized_B_value.py: save figure of distribution of normalized B_values
  list_file: PDB ids of the sample in .txt and .csv format
  *plot.py: create the corresponding plot from the statistics data
