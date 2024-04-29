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


filename = f'{ROOT}/scraper/links_noticias_subset.txt'

with open(filename, 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]

ROOT = import_utils.get_project_root()
noticias = import_utils.import_news_from_json(f'{ROOT}/scraper/data_noticias_lavoz_subset.json')

# Reorder noticias list based on the order of the links
noticias_ordered = []
for line in lines:
    for news in noticias:
        if news['link'] == line:
            noticias_ordered.append(news)
            break

noticias = noticias_ordered

#noticias = post_scrapp_processing(noticias)
noticias = post_scrapp_processing_fecha(noticias)
noticias = post_scrapp_processing_medio(noticias)
#noticias = post_scrapp_processing_paragraph(noticias)

filename = f'{ROOT}/label_studio/data/raw/data_noticias_lavoz_formatted.json'
   
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(noticias, f, ensure_ascii=False, indent=4)
    
# Load news from json file. 
corpus = ArticlesCorpus()
corpus.load_articles(noticias)

# Filter por categorias negocios y política.
df = corpus.get_catalog().query("seccion.str.contains('Política') | seccion.str.contains('Negocios')")

corpus2 = corpus.filter_by_catalog(df, to_corpus=True)
corpus2.reset_index()
corpus2.export_articles(f"{ROOT}/label_studio/data/raw/data_noticias_lavoz_politica_negocios.json")

corpus2.save_corpus(f"{ROOT}/label_studio/data/raw/corpus_lavoz_politica_negocios.pkl")

n_blocks = 10
n_news_per_block = 20

for i in range(n_blocks):
    s = i*n_news_per_block
    e = i*n_news_per_block + n_news_per_block
    index_range = np.arange(s, e)
    
    corpus_to_export = corpus2.filter_by_index(index_range, to_corpus=True)
    corpus_to_export.export_articles(f'{ROOT}/label_studio/data/inputs/data_noticias_lavoz_{s}_{e-1}.json')