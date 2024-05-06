from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations

ROOT = import_utils.get_project_root()

# Load news from json file. 
corpus = ArticlesCorpus()
# corpus.load_articles(import_utils.import_news_from_json(f'{ROOT}/data/manual/noticias_demo.json'))
corpus.load_articles(import_utils.import_news_from_json(f'{ROOT}/scraper/data_noticias_lavoz_formatted.sample.json'))

# Exportamos las noticias para label studio.
#corpus.export_articles(f"{ROOT}/label_studio/data/archive/noticias_to_label_studio.json")

# Automatic NLP Annotations.
# Esto tendría que cambiar.
nlp = NLP('es','pysentimiento')
nlp._annotate_corpus(corpus)

# Importamos las anotaciones manuales y las cargamos al corpus.
#entities_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/archive/annotations_entities_min.json", min_json=True)
#corpus.load_manual_annotations(manual_annotations=entities_annotations, author="jcc", annotated_attribute="entities")

# Importamos las anotaciones manuales y las cargamos al corpus.
#sources_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/archive/annotations_sources.json", min_json=False)
#corpus.load_manual_annotations(manual_annotations=sources_annotations, author="jcc", annotated_attribute="sources")

corpus.get_article(0).nlp_annotations.summary()
print("\n")
#corpus.get_article(0).manual_annotations.summary()
#print("\n")

# Save and load analyzed corpus.
corpus.save_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz.pkl")

corpus2 = ArticlesCorpus().load_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz.pkl")
corpus2.get_article(0).nlp_annotations.summary()