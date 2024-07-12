from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations
import re

ROOT = import_utils.get_project_root()

'''
# Load news from json file. 
corpus = ArticlesCorpus()
# corpus.load_articles(import_utils.import_news_from_json(f'{ROOT}/data/manual/noticias_demo.json'))
corpus.load_articles(import_utils.import_news_from_json(f'{ROOT}/scraper/data_noticias_lavoz_formatted.json'))

# Exportamos las noticias para label studio.
#corpus.export_articles(f"{ROOT}/label_studio/data/archive/noticias_to_label_studio.json")

# Automatic NLP Annotations.
# Esto tendría que cambiar.

nlp._annotate_corpus(corpus)

# Importamos las anotaciones manuales y las cargamos al corpus.
#entities_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/archive/annotations_entities_min.json", min_json=True)
#corpus.load_manual_annotations(manual_annotations=entities_annotations, author="jcc", annotated_attribute="entities")

# Importamos las anotaciones manuales y las cargamos al corpus.
sources_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/archive/annotations_sources.json", min_json=False)
corpus.load_manual_annotations(manual_annotations=sources_annotations, author="jcc", annotated_attribute="sources")

corpus.get_article(0).nlp_annotations.summary()
print("\n")
#corpus.get_article(0).manual_annotations.summary()
#print("\n")

# Save and load analyzed corpus.
corpus.save_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz.pkl")
'''
nlp = NLP('es','pysentimiento')
corpus2 = ArticlesCorpus().load_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz.pkl")
nlp.calculate_corpus_metrics(corpus2)
nlp._build_frontend_json(corpus2)
corpus2.export_articles(f"{ROOT}/data/corpus_demo/corpus_lavoz.json")
print(corpus2.get_article(0).nlp_annotations.sources)

import pandas as pd
import json

# File path
file_path = f"{ROOT}/data/corpus_demo/corpus_lavoz.json"

# Load JSON data from file
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

data_out = []

for ele in data:
	data_out.append(ele['nlp_annotations']['metrics'])

# Convert JSON data to pandas DataFrame
df = pd.json_normalize(data_out)


print(df.shape)
# File path for the Excel file
excel_file_path = f"{ROOT}/data/corpus_demo/corpus_lavoz.xlsx"

# Export the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)

# Print the DataFrame to the console
print(df.head())