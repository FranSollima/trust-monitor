from trustmonitor.import_utils import get_project_root, import_news_from_json
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations

ROOT = get_project_root()

# Load news from json file. 
corpus = ArticlesCorpus()
corpus = ArticlesCorpus().load_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz_politica_negocios_5.pkl")

# Automatic NLP Annotations.
# Esto tendría que cambiar.
nlp = NLP('es','pysentimiento')
nlp._annotate_corpus(corpus, file_name = 'out_json.json')

# Importamos las anotaciones manuales y las cargamos al corpus.
#entities_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/archive/annotations_entities_min.json", min_json=True)
#corpus.load_manual_annotations(manual_annotations=entities_annotations, author="jcc", annotated_attribute="entities")

# Importamos las anotaciones manuales y las cargamos al corpus.
#sources_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/archive/annotations_sources.json", min_json=False)
#corpus.load_manual_annotations(manual_annotations=sources_annotations, author="jcc", annotated_attribute="sources")

#print(corpus.get_article(0).nlp_annotations.sources)
print("\n")
print("\n")
#print(corpus.get_article(1).nlp_annotations.json)
print("\n")
print("\n")