from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from pysentimiento import create_analyzer  # Import pysentimiento
from tqdm import tqdm

ROOT = import_utils.get_project_root()
noticias = import_utils.import_news_from_json(f'{ROOT}/data/manual/nuevas_noticias.json')

corpus = ArticlesCorpus()
corpus.load_articles([noticias[0]])

print(corpus.get_catalog())


# maybe it is better to refactor this functio to some like this:
# analyze_corpus_cuerpo(stanza=True,spacy=False, pysentimiento=True)
# tha analyzer may retunr the output just the engines in the parametetrs.
nlp = NLP('es', 'stanza')
corpus.load_nlp_processor(nlp)
corpus.analyze_corpus_cuerpo()


article_id = 0
print(corpus.get_article(article_id).entities_cuerpo)

#pysentimiento
nlp2 = NLP('es','pysentimiento')
nlp2._init_pysentimiento()
nlp2._extract_corpus_sentiment(corpus)
print(corpus)

for article in tqdm(corpus.articles.values()):
    print(article.nlp_annotations.general_sentiment['pysentimiento'])



