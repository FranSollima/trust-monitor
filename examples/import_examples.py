import os
from trustmonitor import import_utils


# Podemos acceder a la raiz del proyecto con la función get_project_root()
# Importamos el json de noticias generadas manualmente.
filepath = os.path.join(import_utils.get_project_root(),"data", "manual", "nuevas_noticias.json")
news = import_utils.import_news_from_json(filepath)

# Imprimimos algunas características de las noticias.
print(f'Cantidad de noticias en el archivo: {len(news)}')
print(f'Características de las noticias: {list(news[0].keys())}')
for i, n in enumerate(news):
    print(f'Noticia {i+1} - Medio {n["medio"]} - {n["titulo"]}')
    
print("\n ------------------------------------ \n")

# Podemos importar las noticias de una carpeta entera.
# Esto importará todas las noticias de todos los archivos json de la carpeta.
directory_path = os.path.join(import_utils.get_project_root(),"data", "raw")
news = import_utils.import_news_from_folder(data_path=directory_path, medio='clarin')

# Imprimimos algunas características de las noticias.
print(f'Cantidad de noticias en el archivo: {len(news)}')
print(f'Características de las noticias: {list(news[0].keys())}')
for i in range(0, 6):
    print(f'Noticia {i+1} - Medio {news[i]["medio"]} - {news[i]["titulo"]}')
    
print("\n ------------------------------------ \n")

filepath = os.path.join(import_utils.get_project_root(),"data", "manual", "label_studio_annotations.json")
annotations = import_utils.import_label_studio_annotations(filepath)

for i, d in enumerate(annotations):
    print(d)
    if i == 5:
        break   