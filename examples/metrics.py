import os
import pickle
from trustmonitor import import_utils
from pprint import pprint
from tqdm import tqdm

# Cargamos el corpus
directory_path = os.path.join(import_utils.get_project_root(), "data", "raw")
pickle_file_path = os.path.join(directory_path, 'corpus.pkl')
with open(pickle_file_path, 'rb') as pickle_file:
    corpus = pickle.load(pickle_file)
print(f'Corpus loaded from {pickle_file_path}')
c = corpus.get_catalog()

def get_entidades_mencionadas(corpus_medio, libreria):
    entities_count = {}
    for article in corpus_medio.values():
        for entity in set(article.nlp_annotations.entities[libreria]):
            if entity not in entities_count:
                entities_count[entity] = 0
            entities_count[entity] += 1
    for entity in entities_count:
        entities_count[entity] /= len(corpus_medio)
    return entities_count

def get_labels_sentimiento(corpus_medio):
    sentimientos_count = {}
    for article in corpus_medio.values():
        label = article.nlp_annotations.sentiment['pysentimiento']['label']
        if label not in sentimientos_count:
            sentimientos_count[label] = 0
        sentimientos_count[label] += 1
    for label in sentimientos_count:
        sentimientos_count[label] /= len(corpus_medio)
    return sentimientos_count

def get_indice_sentimiento(corpus_medio):
    sentimientos = []
    for article in corpus_medio.values():
        scores = article.nlp_annotations.sentiment['pysentimiento']['scores']
        indice = scores['POS'] - scores['NEG']
        sentimientos.append(indice)
    return sum(sentimientos) / len(sentimientos)

def get_sentimiento_por_entidad(corpus_medio):
    # TODO: ignorar las que aparecen menos de X veces?
    lista_sentimientos_por_entidad = {}
    for article in corpus_medio.values():
        for entidad, sentimientos in article.nlp_annotations.entities_sentiment["stanza"].items():
            if entidad not in lista_sentimientos_por_entidad:
                lista_sentimientos_por_entidad[entidad] = []
            lista_sentimientos_por_entidad[entidad] += sentimientos
    sentimiento_por_entidad = {}
    for entidad in lista_sentimientos_por_entidad:
        sentimiento_por_entidad[entidad] = sum(lista_sentimientos_por_entidad[entidad]) / len(lista_sentimientos_por_entidad[entidad]) - 1
    return sentimiento_por_entidad

def aux_get_nro_palabras(article, libreria):
    if libreria == 'stanza':
        # TODO: esta bien usar num_tokens?
        return article.nlp_annotations.doc["stanza"].num_tokens
    elif libreria == 'spacy':
        # TODO: estamos usando lo mismo que stanza; esta bien?
        return article.nlp_annotations.doc["stanza"].num_tokens

def get_adjetivos(corpus_medio, libreria):
    # Devolvemos la cantidad de adjetivos dividido la cantidad de palabras
    adjetivos = 0
    nro_palabras = 0
    for article in corpus_medio.values():
        adjetivos += len(article.nlp_annotations.adjectives[libreria])
        nro_palabras += aux_get_nro_palabras(article, libreria)
    return adjetivos / nro_palabras

def get_adjetivos_cmp(corpus_medio, libreria):
    # Devolvemos la cantidad de adjetivos comparativos dividido la cantidad de adjetivos
    adjetivos_cmp = 0
    adjetivos = 0
    for article in corpus_medio.values():
        for adjetivo in article.nlp_annotations.adjectives[libreria]:
            adjetivos += 1
            if adjetivo['features'].get('Degree') == 'Cmp':
                adjetivos_cmp += 1
    return adjetivos_cmp / adjetivos


# Metricas
metricas = {}
for medio in c.medio.unique():
    print(f"Medio: {medio}")
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    metricas[medio] = {}
    # Frecuencia de entidades por medio
    metricas[medio]['entidades_mencionadas_stanza'] = get_entidades_mencionadas(corpus_medio, libreria='stanza')
    metricas[medio]['entidades_mencionadas_spacy'] = get_entidades_mencionadas(corpus_medio, libreria='spacy')
    # Labels sentimiento por medio
    metricas[medio]['labels_sentimiento'] = get_labels_sentimiento(corpus_medio)
    # Indice de sentimiento por medio
    metricas[medio]['indice_sentimiento'] = get_indice_sentimiento(corpus_medio)
    # Frecuencia de sentimiento por entidad-medio
    metricas[medio]['sentimiento_por_entidad'] = get_sentimiento_por_entidad(corpus_medio)
    # Frecuencia de adjetivos
    metricas[medio]['adjetivos_stanza'] = get_adjetivos(corpus_medio, libreria='stanza')
    metricas[medio]['adjetivos_spacy'] = get_adjetivos(corpus_medio, libreria='spacy')
    # Frecuencia de adjetivos Degree=Cmp vs adjetivos por medio
    metricas[medio]['adjetivos_degree_cmp_stanza'] = get_adjetivos_cmp(corpus_medio, libreria='stanza')
    metricas[medio]['adjetivos_degree_cmp_spacy'] = get_adjetivos_cmp(corpus_medio, libreria='spacy')
    print(f"Metricas calculadas para {medio}")

print(metricas['clarin']['labels_sentimiento'])
print(metricas['infobae']['labels_sentimiento'])
print(metricas['lanacion']['labels_sentimiento'])
print(metricas['pagina12']['labels_sentimiento'])

print(metricas['clarin']['indice_sentimiento'])
print(metricas['infobae']['indice_sentimiento'])
print(metricas['lanacion']['indice_sentimiento'])
print(metricas['pagina12']['indice_sentimiento'])

print(metricas['clarin']['adjetivos_stanza'])
print(metricas['infobae']['adjetivos_stanza'])
print(metricas['lanacion']['adjetivos_stanza'])
print(metricas['pagina12']['adjetivos_stanza'])

print(metricas['clarin']['adjetivos_spacy'])
print(metricas['infobae']['adjetivos_spacy'])
print(metricas['lanacion']['adjetivos_spacy'])
print(metricas['pagina12']['adjetivos_spacy'])

print(metricas['clarin']['adjetivos_degree_cmp_stanza'])
print(metricas['infobae']['adjetivos_degree_cmp_stanza'])
print(metricas['lanacion']['adjetivos_degree_cmp_stanza'])
print(metricas['pagina12']['adjetivos_degree_cmp_stanza'])

print(metricas['clarin']['adjetivos_degree_cmp_spacy'])
print(metricas['infobae']['adjetivos_degree_cmp_spacy'])
print(metricas['lanacion']['adjetivos_degree_cmp_spacy'])
print(metricas['pagina12']['adjetivos_degree_cmp_spacy'])

entidades_top_10 = sorted(metricas['clarin']['entidades_mencionadas_stanza'].items(), key=lambda x: -x[1])[:10]
sentimientos_frecuencias_top_10 = [(elem[0], elem[1], metricas['clarin']['sentimiento_por_entidad'][elem[0]]) for elem in entidades_top_10]
pprint(sentimientos_frecuencias_top_10)

entidades_top_10 = sorted(metricas['infobae']['entidades_mencionadas_stanza'].items(), key=lambda x: -x[1])[:10]
sentimientos_frecuencias_top_10 = [(elem[0], elem[1], metricas['infobae']['sentimiento_por_entidad'][elem[0]]) for elem in entidades_top_10]
pprint(sentimientos_frecuencias_top_10)

entidades_top_10 = sorted(metricas['lanacion']['entidades_mencionadas_stanza'].items(), key=lambda x: -x[1])[:10]
sentimientos_frecuencias_top_10 = [(elem[0], elem[1], metricas['lanacion']['sentimiento_por_entidad'][elem[0]]) for elem in entidades_top_10]
pprint(sentimientos_frecuencias_top_10)

entidades_top_10 = sorted(metricas['pagina12']['entidades_mencionadas_stanza'].items(), key=lambda x: -x[1])[:10]
sentimientos_frecuencias_top_10 = [(elem[0], elem[1], metricas['pagina12']['sentimiento_por_entidad'][elem[0]]) for elem in entidades_top_10]
pprint(sentimientos_frecuencias_top_10)

entidades_top_10 = sorted(metricas['pagina12']['entidades_mencionadas_stanza'].items(), key=lambda x: -x[1])[:10]
pprint(entidades_top_10)
entidades_top_10 = sorted(metricas['pagina12']['entidades_mencionadas_spacy'].items(), key=lambda x: -x[1])[:10]
pprint(entidades_top_10)


"""
EXTRA
"""
from trustmonitor.articles import ArticlesCorpus

# Articulo más negativo
max_pos = 0
max_article = None
for medio in c.medio.unique():
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    for article in corpus_medio.values():
        scores = article.nlp_annotations.sentiment['pysentimiento']['scores']
        if scores['POS'] > max_pos:
            max_pos = scores['POS']
            max_article = article

# Articulo más positivo
max_neg = 0
max_article = None
for medio in c.medio.unique():
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    for article in corpus_medio.values():
        scores = article.nlp_annotations.sentiment['pysentimiento']['scores']
        if scores['NEG'] > max_neg:
            max_neg = scores['NEG']
            max_article = article

# Articulo más neutral
max_neu = 0
max_article = None
for medio in c.medio.unique():
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    for article in corpus_medio.values():
        scores = article.nlp_annotations.sentiment['pysentimiento']['scores']
        if scores['NEU'] > max_neu:
            max_neu = scores['NEU']
            max_article = article

# Con mas adjetivos (segun stanza)
max_adj = 0
max_article = None
for medio in c.medio.unique():
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    for article in corpus_medio.values():
        adjetivos = len(article.nlp_annotations.adjectives['stanza'])
        nro_palabras = aux_get_nro_palabras(article, 'stanza')
        if nro_palabras < 50: # Solo articulos con mas de 50 palabras en el cuerpo
            continue
        if nro_palabras and adjetivos / nro_palabras > max_adj:
            max_adj = adjetivos / nro_palabras
            max_article = article

# Con menos adjetivos
min_adj = 1
min_article = None
for medio in c.medio.unique():
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    for article in corpus_medio.values():
        adjetivos = len(article.nlp_annotations.adjectives['stanza'])
        nro_palabras = aux_get_nro_palabras(article, 'stanza')
        if nro_palabras < 50: # Solo articulos con mas de 50 palabras en el cuerpo
            continue
        if nro_palabras and adjetivos / nro_palabras < min_adj:
            min_adj = adjetivos / nro_palabras
            min_article = article
            
# Con mas adj comp
max_adj = 0
max_article = None
for medio in c.medio.unique():
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    for article in corpus_medio.values():
        adjetivos_cmp = 0
        for adjetivo in article.nlp_annotations.adjectives['stanza']:
            if adjetivo['features'].get('Degree') == 'Cmp':
                adjetivos_cmp += 1
        nro_palabras = aux_get_nro_palabras(article, 'stanza')
        if nro_palabras < 50: # Solo articulos con mas de 50 palabras en el cuerpo
            continue
        if nro_palabras and adjetivos_cmp / nro_palabras > max_adj:
            max_adj = adjetivos_cmp / nro_palabras
            max_article = article

# Con menos adj comp
min_adj = 1
min_article = None
for medio in c.medio.unique():
    corpus_medio = corpus.filter_by_catalog(c[c.medio == medio])
    for article in corpus_medio.values():
        adjetivos_cmp = 0
        for adjetivo in article.nlp_annotations.adjectives['stanza']:
            if adjetivo['features'].get('Degree') == 'Cmp':
                adjetivos_cmp += 1
        nro_palabras = aux_get_nro_palabras(article, 'stanza')
        if nro_palabras < 50: # Solo articulos con mas de 50 palabras en el cuerpo
            continue
        if nro_palabras and adjetivos_cmp / nro_palabras < min_adj:
            min_adj = adjetivos_cmp / nro_palabras
            min_article = article


# Filtro (solo consideramos articulos con mas de 50 palabras en el cuerpo)
titulares_filtro = (
    'Los secretos de Federer: por qué vuelve a la Argentina y por qué no es de Boca pese al intento de Del Potro', # Mas positivo
    'Epidemia de lesiones del Real Madrid: 10 jugadores en la enfermería en tres meses', # Mas negativo
    'Superclásico: Más de 2 millones de dólares de recaudación|Los socios e hinchas de River colmarán el Monumental', # Mas neutral
    'Sol Pérez celebró la llegada de la Primavera (y sus seguidores también)', # Mas adjetivos
    'Las 30 mejores fotos de la gala de los premios The Best', # Sin adjetivos
    'Martín Fierro de Moda 2019: cuáles son las categorías y cómo es el sistema de votación', # Mas adjetivos comparativos
    'Primavera: por qué este año empezó el 23 de septiembre', # Sin adjetivos comparativos
)

corpus_para_pkl = ArticlesCorpus()
corpus_filtrado = corpus.filter_by_catalog(c[c.titulo.isin(titulares_filtro)])
corpus_para_pkl.load_articles(corpus_filtrado, mode='dict')

