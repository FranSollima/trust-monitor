"""
Este script genera corpus procesados con NLP, agrega manual
 annotations y los guarda en formato json.
"""
import os
from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus, NLPAnnotations
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations

### PASO 1: Carga de noticias y exportación del Corpus inicial ###
# Importamos las noticias scrappeadas en formato json.
ROOT = import_utils.get_project_root()
filename = f'{ROOT}/label_studio/data/raw/data_noticias_lavoz_subset_formatted.json'
noticias = import_utils.import_news_from_json(filename)

# Cargamos las noticias en el Corpus.
corpus_001 = ArticlesCorpus()
corpus_001.load_articles(noticias)

# Exportamos el corpus sin modificaciones - 00.
corpus_001.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_001_00.json')

# Exportamos el corpus filtrado sin modificaciones - 00.
corpus_002 = corpus_001.filter_by_index([27, 57, 80, 89, 112], to_corpus=True)
corpus_002.reset_index()
corpus_002.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_002_00.json')


### PASO 2: Procesamiento de Corpus y exportación con NLP Annotations ###
# Anotamos automáticamente el corpus y calculamos las métricas.
nlp = NLP(language="es", libreria="pysentimiento")
nlp._annotate_corpus(corpus_001)

# Exportamos el corpus con anotaciones automáticas y métricas - 01.
corpus_001.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_001_01.json')

# Exportamos el corpus filtrado con anotaciones automáticas y métricas - 01.
corpus_002 = corpus_001.filter_by_index([27, 57, 80, 89, 112], to_corpus=True)
corpus_002.reset_index()
corpus_002.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_002_00.json')



### PASO 3: Carga y exportación de Corpus con Manual Annotations ###
# Cargamos las anotaciones manuales al corpus.
manual_annotations_files = os.listdir(f"{ROOT}/label_studio/data/outputs/")

for file in manual_annotations_files:
    author = file.split("_")[6].replace(".json", "")
    annotations = import_manual_annotations(f"{ROOT}/label_studio/data/outputs/{file}")
    corpus_001.load_manual_annotations(manual_annotations=annotations, author=author, annotated_attribute="sources")

# Exportamos el corpus con anotaciones automáticas y manuales - 02.
corpus_001.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_001_02.json')

# Exportamos el corpus filtrado con anotaciones automáticas y manuales - 02.
corpus_002 = corpus_001.filter_by_index([27, 57, 80, 89, 112], to_corpus=True)
corpus_002.reset_index()
corpus_002.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_002_00.json')