import os
import pandas as pd

def load_files(directory, start_at, end_at):
    all_entries = os.listdir(directory)
    files = [entry for entry in all_entries if os.path.isfile(os.path.join(directory, entry))]
    datasets = {}
    for i in range(len(files)):
        datasets[files[i]] = wash_data(pd.read_csv(directory + '/' + files[i]), start_at, end_at)
    return datasets

def wash_data(dataset, start_at, end_at):
    data_subset = dataset.loc[
            (dataset["time"] >= start_at) & (dataset["time"] <= end_at)]
    washed_data = data_subset.interpolate()
    return washed_data
