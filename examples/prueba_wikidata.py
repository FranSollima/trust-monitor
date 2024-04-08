import requests
import os
import pickle
from trustmonitor import import_utils

def fetch_wikidata(params):
    url = 'https://www.wikidata.org/w/api.php'
    return requests.get(url, params=params)

def get_entidades_mencionadas(corpus_medio, libreria):
    entitiy_data = {}
    for article in corpus_medio.values():
        for entity in set(article.nlp_annotations.entities[libreria]):
            if entity not in entitiy_data:
                entitiy_data[entity] = {'count': 0}
            entitiy_data[entity]['count'] += 1
    for entity in entitiy_data:
        entitiy_data[entity]['count'] /= len(corpus_medio)
    return entitiy_data

# Cargamos el corpus
directory_path = os.path.join(import_utils.get_project_root(), "data", "raw")
pickle_file_path = os.path.join(directory_path, 'corpus.pkl')
with open(pickle_file_path, 'rb') as pickle_file:
    corpus = pickle.load(pickle_file)
print(f'Corpus loaded from {pickle_file_path}')
c = corpus.get_catalog()

# Entidades
entidades_por_medio = {}
for medio in c.medio.unique():
    print(f"Medio: {medio}")
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    # Frecuencia de entidades por medio
    entidades_por_medio[medio] = get_entidades_mencionadas(corpus_medio, libreria='stanza')

for medio in c.medio.unique():
    for entity in entidades_por_medio[medio]:
        wikidata_params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'es',
            'search': entity
        }
        data = fetch_wikidata(wikidata_params).json()
        entidades_por_medio[medio][entity]['wikidata'] = None
        if data['search']:
            entidades_por_medio[medio][entity]['wikidata'] = data['search'][0]
        break

# Examples
# wbsearchentities
wikidata_params = {
    'action': 'wbsearchentities',
    'format': 'json',
    'language': 'es',
    'search': 'Javier Gerardo Milei'
}
data = fetch_wikidata(wikidata_params).json()
print(data['search'])

# wbgetentities
wikidata_params = {
    'action': 'wbgetentities',
    'format': 'json',
    'ids': 'Q52395487'
}
data = fetch_wikidata(wikidata_params).json()
print(data["entities"]["Q52395487"]["labels"]["es"]["value"])
print(data["entities"]["Q52395487"]["descriptions"]["es"]["value"])
print(data["entities"]["Q52395487"]["aliases"]["es"])
