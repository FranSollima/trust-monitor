import pickle
import json
from trustmonitor import import_utils


ROOT = import_utils.get_project_root()

# Load the pickle file
file_path = f'{ROOT}/data/pickle_files/corpus_lavoz.pkl'

with open(file_path, 'rb') as f:
    data = pickle.load(f)


data.export_articles(f'{ROOT}/data/pickle_files/corpus_lavoz_annotated.json')
