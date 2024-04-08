import os
import json
import pickle
from pathlib import Path

def get_project_root() -> Path:
    """
    This function returns the project root path.

    Returns:
        Path: path to project root.
    """
    return os.path.normpath(Path(__file__).parent.parent)

def import_news_from_json(filepath: str) -> list:
    """
    This function imports news from a json file, creating a list of dictionaries.

    Args:
        filepath (str): json file path.

    Returns:
        list: list of dictionaries containing news.
    """
    with open(filepath, 'r', encoding="utf8") as f:
        news = json.load(f)
    return news

def import_news_from_pickle(filepath: str) -> list:
    with open(filepath, 'rb') as handle:
        news = pickle.load(handle)
    return news

def add_medio_to_news(news: list, medio:str) -> list:
    """
    This function adds a key 'medio' to each news in the list.

    Args:
        news (list): list of dictionaries containing news.
        medio (str): "medio" covering the news in the list (e.g. 'clarin').

    Returns:
        list: original list of dictionaries containing news with a new key 'medio'.
    """
    for new in news:
        new['medio'] = medio
    return news

def _news_keys_unification(news):

    for n in news:
        
        if 'categorias' not in n.keys():
            n['categorias'] = n.pop('categoria')
            if n['medio'] != 'infobae':
                n['categorias'] = [n['categorias']]
            
        if 'etiquetas' not in n.keys():
            n['etiquetas'] = n.pop('etiqueta')
            n['etiquetas'] = [n['etiquetas']]
            
    return news

def import_news_from_folder(data_path: str, medio: str) -> list:
    """
    This function creates a list of dictionaries containing news from a data path. Inside this directory 
    there should be a folder named after each news media ("medio"), containing json files with news.

    Args:
        data_path (str): path to directory containing news media folders.
        medio (str): folder names corresponding to each news media.

    Returns:
        list: list of dictionaries containing news with a key 'medio' included.
    """
    
    files_path = os.path.join(data_path, medio)
    
    news = []
    for file in os.listdir(files_path):
        n = import_news_from_json(os.path.join(files_path, file))
        news += n
    
    news = add_medio_to_news(news, medio)
    
    news = _news_keys_unification(news)
    
    return news


def check_news_keys(news: list):
    """
    This function checks that all news in the list have the same keys.

    Args:
        news (list): list of dictionaries containing news.

    Raises:
        Exception: if news have different keys.
    """
    
    k_list = ['hora',
              'link_noticia',
              'link_foto',
              'autor',
              'categorias',
              'cuerpo',
              'volanta',
              'fecha',
              'fecha_resumen',
              'etiquetas',
              'titulo',
              'resumen',
              'medio']

    
    #n_diff_keys = sum([not(list(n.keys()) == k_list) for n in news])
    n_diff_keys = sum([not(k in k_list) for n in news for k in n.keys()])

    if n_diff_keys != 0:
        print(news[0].keys())
        raise Exception('News with different keys')
    
    
    
# def import_entities_manual_annotations(filepath: str) -> list:
#     """
#     This function imports annotations from a json file, creating a list of dictionaries.

#     Args:
#         filepath (str): json file path.

#     Returns:
#         list: list of dictionaries containing annotations.
#     """
#     with open(filepath, 'r', encoding="utf8") as f:
#         annotations_data = json.load(f)
    
#     annotations = []
    
#     ent_label_conversion = {
#         'PER': 'Persona',
#         'ORG': 'Organización',
#         'LOC': 'Lugar',
#         'MISC': 'Misceláneo',
#         'GEN': 'Genérico'
#     }

#     for i in range(len(annotations_data)):
#         annotations.append({'titulo':annotations_data[i]['titulo'],
#                             'fecha':annotations_data[i]['fecha'],
#                             'link_noticia':annotations_data[i]['link_noticia'],
#                             'cuerpo':annotations_data[i]['cuerpo'],
#                             'entities':[]})
        
#         for d in annotations_data[i]['label']:
#             ent = ent_label_conversion[d['labels'][0]]
#             d = {'start_char': d['start'], 'end_char': d['end'], 'text': d['text'], 'type': ent}
#             annotations[i]['entities'].append(d)
        
        
#     # if annotated_attribute == "entities":


#     #     for i in range(len(annotations)):
#     #         for ent in annotations[i]["entities"]:
#     #             ent["type"] = ent_label_conversion[ent["type"]]
    
#     # # Post Processing of Entities annotations
#     # if annotated_attribute == "entities":
#     #     for i in range(len(annotations_data)):
#     #         for d in annotations[i][annotated_attribute]:                
#     #             d = {'text': d["text"], 'start_char': d["start"], 'end_char': d["end"], 'type': d["labels"][0]}
            

#     return annotations

