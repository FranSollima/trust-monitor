import pandas as pd
from tqdm import tqdm

class Article():
    
    def __init__(self, news_dict, **kwargs):
        
        for key in news_dict:
            setattr(self, key, news_dict[key])      
                    
        for key in kwargs:
            setattr(self, key, kwargs[key])
            
    # def __repr__(self):
    #     pass

    # def __str__(self):
    #     pass
    
    def get_article_dict(self):
        return self.__dict__.copy()
    
    def get_article_attrs(self):
        return list(self.__dict__.keys())
    
    def _check_doc_attr(self):
        return hasattr(self, 'entities')
    
    def _check_entities_attr(self):
        return hasattr(self, 'entities')
    
    def analyze_cuerpo(self, nlp_processor):
        self.doc_cuerpo = nlp_processor.analyze(self.cuerpo)
        self.entities_cuerpo = dict(entities_list = nlp_processor.extract_entities(self.doc_cuerpo),
                                    entities_count = nlp_processor.count_entities(self.doc_cuerpo),
                                    entity_type_counts = nlp_processor.count_entity_types(self.doc_cuerpo))
    
    
    
class ArticlesCorpus():
    
    def __init__(self):
        self.articles = {}
        self.n_articles = 0
        
    # def __repr__(self):
    #     pass

    # def __str__(self):
    #     pass
        
    def load_articles(self, news, mode="list"):
        
        if mode == "list":
            self._load_articles_from_list(news)
            
        elif mode == "dict":
            self._load_articles_from_dict(news)
            
        else:
            raise ValueError("mode must be 'list' (list of dictionaries) or 'dict' (dictionary of Articles == corpus)")
            
        self._get_articles_catalog()
            
    def _load_articles_from_list(self, list_of_news):
        for news in list_of_news:
            self.articles[self.n_articles] = Article(news)
            self.n_articles += 1
            
    def _load_articles_from_dict(self, dict_of_news):  
        """Esta función permite cargar un corpus filtrado y generar un nuevo corpus"""                  
        for news in dict_of_news.values():
            self.articles[self.n_articles] = news
            self.n_articles += 1
            
            
        
    def _get_articles_catalog(self):
        news_list = [self.articles[index].get_article_dict() for index in self.articles.keys()]
        index_list = [index for index in self.articles.keys()]
        
        df = (pd.DataFrame(news_list)
              # Agregamos variables relevantes y damos formatos correctos.
              .assign(index = index_list,
                      fecha = lambda x: pd.to_datetime(x.fecha, format='%d/%m/%Y'),
                      # limpiamos los nombres de autores de las categorias.
                      categorias = lambda x: x.apply(lambda y: [i for i in y.categorias if i not in y.autor], axis=1))
              .assign(categorias = lambda x: x.categorias.apply(lambda y: '_'.join(y)),
                      etiquetas = lambda x: x.etiquetas.apply(lambda y: '_'.join(y)))
              [["index", "medio", "fecha", "categorias", "autor", "etiquetas", "titulo", "link_noticia"]]
              )
         
        self.catalog = df
        
    def get_corpus(self):
        return self.articles.copy()
    
    def get_catalog(self):
        return self.catalog.copy()
    
    def filter_by_catalog(self, filtered_catalog):
        index_list = filtered_catalog.index.tolist()
        return {index: self.articles[index] for index in index_list}
    
    def load_nlp_processor(self, nlp_processor):
        self.nlp_processor = nlp_processor
        print("NLP Processor loaded!")
        
    def analyze_corpus_cuerpo(self):
        if not hasattr(self, 'nlp_processor'):
            raise ValueError("nlp_processor not loaded")
        
        for article in tqdm(self.articles.values()):
            article.analyze_cuerpo(self.nlp_processor)
            
        print("Corpus analyzed!")
        self._corpus_cuerpo_analized = True
            
            
    def _update_catalog(self):
        
        pass
        