import os, json, requests
from scipy.io import wavfile
from others import notion
from enum import Enum

DATASETS_NOTION = '69c1f6f272d349ed821d2b7e4cf24257'
NAME_PROP = 'Nome'
PATH_PROP = 'Caminho'
CLASSIFIED_PROP = 'Classificado?'
SIZE_PROP = '#Tamanho (MB)'
LEN_PROP = '#Quantidade de Itens'
LEN_CLASSES_PROP = '#Quantidade de Classes'
FTYPE_PROP = 'Tipo de Arquivo'
DATASET_ICON = {'type': 'external', 'external': {'url': 'https://www.notion.so/icons/database_blue.svg'}}

def read_json(fpath: str):
    with open(fpath, 'r') as file: return json.load(file)

class DeepUaiFTypes(str, Enum):
    json = 'json'
    mp3 = 'mp3'
    wav = 'wav'

class DeepUaiDataset:
    name: str
    path: str = None
    filepaths: list = None
    size: float = 0
    length: int = 0
    classified: bool = None
    classes: list = None
    ftype: DeepUaiFTypes = None
    notion_id: str = None
    
    @staticmethod
    def hello_world(): print('H3LL0 W0RLD')

    @staticmethod
    def available_datasets():
        path = os.path.join('data', 'datasets')
        return [os.path.basename(ds_path) for ds_path in os.listdir(path)]

    @staticmethod
    def _get_path(name: str):
        return os.path.join('data', 'datasets', name)
    
    def __str__(self) -> str:
        return f'{self.name}, {self.length} itens, {self.size} MB'
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.path = self._get_path(name=self.name)
        self.size, self.length = self._get_size_and_length()
        with os.scandir(self.path) as it:
            first = next(it)
            self.classified = first.is_dir()
            if self.classified:
                self.classes = os.listdir(self.path)
                self.ftype = os.listdir(first.path)[0].split('.')[-1]
            else:
                self.ftype = first.path.split('.')[-1]
        self.ensure_notion_ref()
    
    def _get_size_and_length(self, path=None):
        if not path: self.filepaths = []
        size, length = 0, 0
        with os.scandir(self.path if not path else path) as it:
            for entry in it:
                if entry.is_file():
                    length += 1
                    size += entry.stat().st_size / (1024**2)
                    self.filepaths.append(entry.path)
                elif entry.is_dir():
                    _size, _length = self._get_size_and_length(entry.path)
                    size += _size
                    length += _length
        return size, length

    def get_notion_ref(self):
        filter = {'property':NAME_PROP, 'title': {'equals': self.name}}
        pages = notion.get_pages(DATASETS_NOTION, filter=filter)['results']
        if len(pages) == 0: return None
        self.notion_id = pages[0]['id']
        return pages[0]

    def ensure_notion_ref(self):
        notion_ref = self.get_notion_ref()
        if notion_ref: return notion_ref
        props = {NAME_PROP: notion.to_title(self.name),
                 SIZE_PROP: {'number': self.size},
                 LEN_PROP: {'number': self.length},
                 CLASSIFIED_PROP: {'checkbox': self.classified}}
        if self.classified: props[LEN_CLASSES_PROP] = {'number': len(self.classes)}
        page = notion.create_page(DATASETS_NOTION, props, DATASET_ICON)
        self.notion_id = page['id']
        return page
    
    def samples(self, fnames=False):
        if self.ftype == DeepUaiFTypes.json: func = lambda fpath: read_json(fpath)
        elif self.ftype == DeepUaiFTypes.wav: func = lambda fpath: wavfile.read(fpath)[1]
        if fnames: return ((os.path.basename(fpath), func(fpath)) for fpath in self.filepaths)
        else: return (func(fpath) for fpath in self.filepaths)
    
    def _get_class(self, filepath:str):
        for cl in self.classes:
            if filepath.find(f'/{cl}/') >= 0:
                return self.classes.index(cl)
        ...
    def classified_samples(self):
        if self.ftype == DeepUaiFTypes.json: func = lambda fpath: read_json(fpath)
        elif self.ftype == DeepUaiFTypes.wav: func = lambda fpath: wavfile.read(fpath)[1]
        return (func(fpath) for fpath in self.filepaths), (self._get_class(fpath) for fpath in self.filepaths)
    
    @classmethod
    def sync_dataset(cls, host: str, name: str):
        path = cls._get_path(name)
        if os.path.exists(path): return
        os.makedirs(path)
        filepaths = requests.get(host + f'/ds/{name}/filepaths', verify=False)
        for filepath in filepaths:
            remote = requests.get(host + f'/{filepath}', stream=True, verify=False)
            with open(filepath, 'wb') as file:
                for chunk in remote.iter_content(): file.write(chunk)