import os, json, numpy as np, librosa
from os.path import join
from sys import path

path.append('.')
from models import DeepUaiDataset

def compute_statistics1(filepath: str):
    y, _ = librosa.load(filepath, sr=None)
    mean = np.mean(y)
    std_dev = np.std(y)
    min_val = np.min(y)
    max_val = np.max(y)
    median = np.median(y)
    q1 = np.percentile(y, 25)
    q3 = np.percentile(y, 75)
    energy = np.sum(y ** 2)
    statistics = {'Mean': mean, 'Standard Deviation': std_dev,
                  'Minimum': min_val, 'Maximum': max_val,
                  'Median': median, 'Q1': q1, 'Q3': q3,
                  'Energy': energy}
    
    return [float(s) for s in statistics.values()]

new_ds_name = 'deglut-audios-statistics2'
new_ds_path = join('data', 'datasets', new_ds_name)
if not os.path.isdir(new_ds_path): os.makedirs(new_ds_path)

ds = DeepUaiDataset('deglut-audios-wav')
for filepath in ds.filepaths:
    fname = os.path.basename(filepath).split('.')[0]
    with open(join(new_ds_path, f'{fname}.json'), 'w') as file:
        json.dump(compute_statistics1(filepath), file)

new_ds = DeepUaiDataset(name=new_ds_name)