from sys import path
from os.path import join

path.append('.')

from models.datasets import LocalDataset, RemoteDataset
datasets = ('deglut-audios-5s', 'deglut-audios-json', 'deglut-audios-statistics1',
            'deglut-audios-wav', 'deglut-audios-wav-classified1', 'deglut-audios-wav-inliers')
for dataset_name in datasets:
    dataset_path = join('data', 'datasets', dataset_name)
    local_dataset = LocalDataset(name=dataset_name, path=dataset_path)
    remote_dataset = RemoteDataset.ensure_ref(local_dataset)