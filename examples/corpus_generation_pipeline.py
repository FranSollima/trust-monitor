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
corpus_002.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_002_01.json')



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
corpus_002.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_002_02.json')



### CORPUS 3 - 1153: Procesamiento de Corpus y exportación con NLP Annotations ###

def post_scrapp_processing(news_list):
    
    rules = [('Redacción LAVOZ','\n')]
 
    for news in news_list:
        for k in news:
            if isinstance(news[k], str):
                for rule in rules:
                    news[k] = news[k].replace(rule[0],rule[1])
                    
    return news_list

def post_scrapp_processing_fecha(news_list):

    month_mapping = {"enero":1,
                     "febrero":2,
                     "marzo":3,
                     "abril":4,
                     "mayo":5,
                     "junio":6,
                     "julio":7,
                     "agosto":8,
                     "septiembre":9,
                     "octubre":10,
                     "noviembre":11,
                     "diciembre":12}

    for news in news_list:
        
        fecha, fecha_hora = news["fecha_hora"].split(",")
        fecha = fecha.split(" de ")
        fecha = f"{fecha[0]}/{month_mapping[fecha[1]]}/{fecha[2]}"
        
        news["fecha_hora"] = fecha_hora
        news["fecha"] = fecha
        
    return news_list

def post_scrapp_processing_medio(news_list):
    
    for news in news_list:
        news['medio'] = 'lavoz'

    return news_list

def post_scrapp_processing_paragraph(news_list):
 
    for news in news_list:
        
        text_list = list(news["cuerpo"])
                    
        for i in range(len(text_list)-1):
            if text_list[i] == "." and text_list[i+1] != " " and not (text_list[i-1].isdigit() and text_list[i+1].isdigit()) and text_list[i+1].isupper() :
                text_list[i] = ".\n"
                
        news["cuerpo"] = ''. join(text_list)
                    
    return news_list


# filename = f'{ROOT}/scraper/links_noticias_subset.txt'

# with open(filename, 'r') as file:
#     lines = file.readlines()
#     lines = [line.strip() for line in lines]

# ROOT = import_utils.get_project_root()
# noticias = import_utils.import_news_from_json(f'{ROOT}/scraper/data_noticias_lavoz_subset.json')

# # Reorder noticias list based on the order of the links
# noticias_ordered = []
# for line in lines:
#     for news in noticias:
#         if news['link'] == line:
#             noticias_ordered.append(news)
#             break

# noticias = noticias_ordered

### PASO 1: Carga de noticias y exportación del Corpus inicial ###
# Importamos las noticias scrappeadas en formato json.
ROOT = import_utils.get_project_root()
filename = f'{ROOT}/scraper/data_noticias_lavoz.json'
noticias = import_utils.import_news_from_json(filename)

#noticias = post_scrapp_processing(noticias)
noticias = post_scrapp_processing_fecha(noticias)
noticias = post_scrapp_processing_medio(noticias)

# Cargamos las noticias en el Corpus.
corpus_003 = ArticlesCorpus()
corpus_003.load_articles(noticias)

corpus_003.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_003_00.json')

### PASO 2: Procesamiento de Corpus y exportación con NLP Annotations ###
# Anotamos automáticamente el corpus y calculamos las métricas.
nlp = NLP(language="es", libreria="pysentimiento")
nlp._annotate_corpus(corpus_003)

# Exportamos el corpus con anotaciones automáticas y métricas - 01.
corpus_003.to_json(f'{ROOT}/data/json_files/corpus_lavoz_pn_003_01.json')