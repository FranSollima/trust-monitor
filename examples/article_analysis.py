from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP


ROOT = import_utils.get_project_root()
noticias = import_utils.import_news_from_file(f'{ROOT}/data/manual/nuevas_noticias.json')

corpus = ArticlesCorpus()
corpus.load_articles([noticias[0]])

print(corpus.get_catalog())

nlp = NLP('es', 'stanza')
corpus.load_nlp_processor(nlp)
corpus.analyze_corpus_cuerpo()

article_id = 0
print(corpus.get_article(article_id).entities_cuerpo)