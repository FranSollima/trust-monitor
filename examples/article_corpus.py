import os
from trustmonitor import import_utils
from trustmonitor.articles import Article, ArticlesCorpus

ROOT = import_utils.get_project_root()

print("\n------------------EJEMPLO ARTICULO------------------\n")
# Importamos una lista de noticias.
news_list = import_utils.import_news_from_file(f"{ROOT}/data/manual/nuevas_noticias.json")
print(f'Cantida de noticias: {len(news_list)}')

# Podemos tomar la primera de las noticias y transformarla en un Articulo.
# Esta clase luego puede tener métodos para analizar la noticia.
news_0 = news_list[0]
# Podemos ver las keys que tiene la noticia.
# Estas serán atributos en la clase Article.
print(news_0.keys())

article = Article(news_0)
# Vemos los atributos.
print(f'Atributos del articulo: {article.get_article_attrs()}')
# Podemos acceder a sus componentes llamando a los atributos.
print(f'Título del articulo: {article.titulo}')

print("\n------------------EJEMPLO CORPUS ARTICULOS------------------\n")

# Vemos los medios en el directorio de datos crudos.
medios = os.listdir(f'{ROOT}/data/raw')
print(f'Medios disponibles: {medios}')

# Guardamos las listas de noticias de los 4 medios.
noticias = []
for medio in medios:
    noticias += import_utils.import_news_from_folder(f"{ROOT}/data/raw/", medio)
    
print(f"Cantidad de noticias: {len(noticias)}")

# Instanciamos la clase ArticlesCorpus.
corpus = ArticlesCorpus()
# Cargamos la lista de noticias de todos los medios en el Corpus.
corpus.load_articles(noticias)

c = corpus.get_catalog()#assign(categorias2 = lambda df: df.categorias.apply(lambda x: '_'.join(x))).query('["DEPORTES", "TV"] in categorias2')
print("\n Muestra del Catalogo \n")
print(c.head())

fil_c = c[c["titulo"].str.contains('Buenos Aires') & c["categorias"].str.contains('DEPORTES')]
print("\n Catálogo Filtrado \n")
print(fil_c)

print("\n Corpus Filtrado \n")
print(corpus.filter_by_catalog(fil_c))

corpus.get_article(0).plot_entities_cuerpo()