import os, json
from os.path import join
from sys import path
from scipy.io import wavfile

path.append('.')
from models import DeepUaiDataset

def get_rate(ds: DeepUaiDataset):
    fname, _ = next(ds.samples(fnames=True))
    wavfilepath = join(ds.path, fname)
    rate, _ = wavfile.read(wavfilepath)
    return rate

def wav2json():
    new_ds_name = f'deglut-audios-json'
    new_ds_path = join('data', 'datasets', new_ds_name)
    if not os.path.isdir(new_ds_path): os.makedirs(new_ds_path)
    for fname, sample in ds.samples(fnames=True):
        fname = fname.split('.')[0]
        with open(join(new_ds_path, f'{fname}.json'), 'w') as file:
            json.dump(sample.tolist(), file)
    new_ds = DeepUaiDataset(name=new_ds_name)
    return new_ds

def wav2json_windows(ds: DeepUaiDataset, window_duration = 5): # seconds
    new_ds_name = f'{ds.name}-{window_duration}s'
    new_ds_path = DeepUaiDataset._get_path(new_ds_name)
    if not os.path.exists(new_ds_path): os.makedirs(new_ds_path)
    
    rate = get_rate(ds)
    window_size = int(rate * window_duration)
    step_size = window_size // 2
    for fname, sample in ds.samples(fnames=True):
        fname = fname.split('.')[0]
        i, start, stop = 0, 0, step_size
        while stop < len(sample):
            with open(join(new_ds_path, f'{fname}-{i}.json'), 'w') as file:
                json.dump(sample[start:stop].tolist(), file)
            i += 1
            start += step_size
            stop += step_size
    new_ds = DeepUaiDataset(name=new_ds_name, path=new_ds_path)
    return new_ds

ds_name = 'deglut-audios-wav-inliers'
ds = DeepUaiDataset(ds_name)
wav2json_windows(ds=ds)