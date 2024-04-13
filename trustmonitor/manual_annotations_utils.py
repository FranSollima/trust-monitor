import json
import os

def import_manual_annotations(file_path, min_json=False):
    """
    EL PREPROCESAMIENTO PODRÍA ESTAR ACA Y NO EN EL CORPUS.
    ESTO ASEGURA QUE EL FORMATO DE LAS ANOTACIONES SEA CORRECTO
    AGREGAR EL ARGUMENTO annotated_attribute PARA QUE EL USUARIO PUEDA ELEGIR SI QUIERE LAS ENTIDADES O LAS FUENTES
    AGREGAR EL ARGUEMNTO DE JSON COMPLETO O MIN (PARA FUENTES UNICAMENTE ACEPTAR COMPLETO).
    """
    file_path = os.path.normpath(file_path)
    
    with open(file_path, 'r', encoding="utf8") as f:
        manual_annotations = json.load(f)
        
    manual_annotations = preprocess_manual_annotations(manual_annotations, min_json)
        
    return manual_annotations


def _preprocess_manual_annotations_min(manual_annotations):
    """ ESTO EN REALIDAD IMPORTA JSON MIN"""

    manual_annotations_formated = {}

    for article in manual_annotations:            
        manual_annotations_formated[article['index']] = {'annotations': [], 
                                                         'titulo': article['titulo']}

        for annotation in article['label']:               
            manual_annotations_formated[article['index']]['annotations'].append({'text': annotation['text'],
                                                                                 'type': annotation['labels'][0],
                                                                                 'start_char': annotation['start'],
                                                                                 'end_char': annotation['end']})
            
    return manual_annotations_formated


def _preprocess_manual_annotations_full(manual_annotations):
    """ ESTO EN REALIDAD IMPORTA JSON COMPLETO"""
    manual_annotations_formated = {}

    for article in manual_annotations:
        manual_annotations_formated[article['data']['index']] = {'titulo':article['data']['titulo'],
                                                                'annotations':[]}
        
        for annotation in article['annotations'][0]['result']:
            if 'value' in annotation.keys():
                manual_annotations_formated[article['data']['index']]['annotations'].append({'start_char': annotation['value']['start'],
                                                                                            'end_char': annotation['value']['end'],
                                                                                            'text': annotation['value']['text'],
                                                                                            'type': annotation['value']['labels'][0],
                                                                                            'id': annotation['id'],
                                                                                            'label_type':'region'})
                
            if 'from_id' in annotation.keys():
                manual_annotations_formated[article['data']['index']]['annotations'].append({'from_id': annotation['from_id'],
                                                                                            'to_id': annotation['to_id'],
                                                                                            'direction': annotation['direction'],
                                                                                            'label_type':'relation'})
                
    return manual_annotations_formated


def preprocess_manual_annotations(manual_annotations, min_json=False):
    
    if min_json:
       manual_annotations_formated = _preprocess_manual_annotations_min(manual_annotations)
    else:
         manual_annotations_formated = _preprocess_manual_annotations_full(manual_annotations)
        
    return manual_annotations_formated




