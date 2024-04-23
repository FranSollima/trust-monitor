"""
Este script permite la generación de bloques de noticias a partir
de un conjunto mayor de noticias del medio LaVoz. Estos bloques pueden 
ser anotados manualmente usando label studio.
"""

import json
import numpy as np
from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus


ROOT = import_utils.get_project_root()
noticias = import_utils.import_news_from_json(f'{ROOT}/scraper/data_noticias_lavoz.json')

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

for news in noticias:
    news['medio'] = 'lavoz'
    
    fecha, fecha_hora = news["fecha_hora"].split(",")
    fecha = fecha.split(" de ")
    fecha = f"{fecha[0]}/{month_mapping[fecha[1]]}/{fecha[2]}"
    
    news["fecha_hora"] = fecha_hora
    news["fecha"] = fecha
    
filename = f'{ROOT}/label_studio/data/raw/data_noticias_lavoz_formatted.json'
   
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(noticias, f, ensure_ascii=False, indent=4)
    
    
# Load news from json file. 
corpus = ArticlesCorpus()
corpus.load_articles(noticias)

n_blocks = 10
n_news_per_block = 20

for i in range(n_blocks):
    s = i*n_news_per_block
    e = i*n_news_per_block + n_news_per_block
    index_range = np.arange(s, e)
    
    corpus_to_export = corpus.filter_by_index(index_range, to_corpus=True)
    corpus_to_export.export_articles(f'{ROOT}/label_studio/data/inputs/data_noticias_lavoz_{s}_{e}.json')