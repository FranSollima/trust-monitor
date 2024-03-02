import os
from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from pysentimiento import create_analyzer  # Import pysentimiento
from tqdm import tqdm

#ROOT = import_utils.get_project_root()
#noticias = import_utils.import_news_from_json(f'{ROOT}/data/manual/nuevas_noticias.json')
directory_path = os.path.join(import_utils.get_project_root(),"data", "raw")

medios = ['clarin','lanacion','infobae','pagina12']

corpus = ArticlesCorpus()

for medio in medios:
	corpus.load_articles(import_utils.import_news_from_folder(data_path=directory_path, medio=medio))

#print(corpus.get_catalog())

# maybe it is better to refactor this functio to some like this:
# analyze_corpus_cuerpo(stanza=True,spacy=False, pysentimiento=True)
# tha analyzer may retunr the output just the engines in the parametetrs.
#nlp = NLP('es', 'stanza')
#corpus.load_nlp_processor(nlp)
#corpus.analyze_corpus_cuerpo()

#article_id = 0
#print(corpus.get_article(article_id).entities_cuerpo)

#pysentimiento
nlp2 = NLP('es','pysentimiento')
nlp2._annotate_coprus(corpus)

#export corpus as pickle

import pickle

# Define the path where you want to save the pickle file
pickle_file_path = os.path.join(directory_path, 'corpus.pkl')

# Serialize the corpus object to a file
with open(pickle_file_path, 'wb') as pickle_file:
    pickle.dump(corpus, pickle_file)

print(f'Corpus exported to {pickle_file_path}')

# Deserialize the corpus object from the file
with open(pickle_file_path, 'rb') as pickle_file:
    loaded_corpus = pickle.load(pickle_file)

# Now, loaded_corpus contains the deserialized corpus object
print(f'Corpus loaded from {pickle_file_path}')