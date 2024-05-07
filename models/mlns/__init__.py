# Machine Learning Não Supervisionado
import os, json
from os.path import join
from others import notion
from models import DeepUaiDataset

MLNS_NOTION = '589048c0e98f4b50ab25892398cc0fa6'
NAME_PROP = 'Nome'
DS_PROP = 'Dataset Alvo'
Y_PROP = 'Y'

class MLNS:
    name: str
    ds_name: str
    notion_id: str | None = None
    ds: DeepUaiDataset = None

    def __init__(self, name: str, ds_name: str) -> None:
        self.name = name
        self.ds_name = ds_name
        self.ds = DeepUaiDataset(name=self.ds_name)
    
    def save_result(self, y: list, fname='y'):
        fname += '.json'
        predictions_path = join('data', 'predictions', self.name)
        if not os.path.isdir(predictions_path): os.makedirs(predictions_path)
        final_path = join(predictions_path, fname)
        with open(final_path, 'w') as file:
            json.dump([float(_y) for _y in y], file)
        return fname, final_path
    
    def create_notion_ref(self):
        props = {NAME_PROP: notion.to_title(self.name),
                 DS_PROP: notion.to_relation(self.ds.notion_id)}
        page = notion.create_page(MLNS_NOTION, props)
        self.notion_id = page['id']
        return page