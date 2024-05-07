import os, shutil
from sklearn.base import OutlierMixin
from models import DeepUaiDataset
from models.mlns import MLNS, Y_PROP
from others import notion

HOST = 'http://localhost:8000'

class DeepUaiOutlierDetection(MLNS):
    clf: OutlierMixin = None
    y: list = None
    
    def __init__(self, name: str, ds_name: str, clf: OutlierMixin) -> None:
        super().__init__(name, ds_name)
        self.clf = clf
    
    def execute(self):
        x = list(self.ds.samples())
        self.y = self.clf.fit_predict(x)
        fname, fpath = self.save_result(self.y)
        self.create_notion_ref()
        notion_file = {'name': fname, 'external': {'url': f'{HOST}/{fpath}'}}
        notion.update_page(self.notion_id, {Y_PROP: {'files': [notion_file]}})
        return self.y
    
    def create_inliers_ds(self):
        if self.y is None: raise Exception('Modelo não treinado.')
        ds_name = self.ds.name + '-inliers'
        ds_path = DeepUaiDataset._get_path(ds_name)
        if not os.path.exists(ds_path): os.makedirs(ds_path)
        for i, filepath in enumerate(self.ds.filepaths):
            fname = os.path.basename(filepath)
            if self.y[i] < 0: continue
            shutil.copyfile(filepath, os.path.join(ds_path, fname))
        return DeepUaiDataset(ds_name)
    
    def create_classified_ds(self):
        if self.y is None: raise Exception('Modelo não treinado.')
        ds_name = self.ds.name + '-classified'
        ds_path = DeepUaiDataset._get_path(ds_name)
        if not os.path.exists(ds_path):
            os.makedirs(ds_path)
            os.makedirs(os.path.join(ds_path, 'inliers'))
            os.makedirs(os.path.join(ds_path, 'outliers'))
        for i, filepath in enumerate(self.ds.filepaths):
            fname = os.path.basename(filepath)
            new_filepath = os.path.join(ds_path, 'inliers' if self.y[i]<0 else 'outliers',fname)
            shutil.copyfile(filepath, new_filepath)
        return DeepUaiDataset(ds_name)