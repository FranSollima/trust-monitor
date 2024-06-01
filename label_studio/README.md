# Label Studio

Este sector del repositorio contiene la generación de noticias para anotaciones en Label Studio.

## Origen de Datos

Los datos originales para etiquetar son un subset de 200 noticias de política y negocios que se encuentra en el directorio `scraper`. Las noticias son `data_noticias_lavoz_subset.json` y su origen es el archivo de links `links_noticias_subset.txt`. 

## Procesamiento

El procesamiento de los datos originales se produce con el script `label_studio_setup.py`. Este script genera algunos archivos en el directorio `data/raw/`:

- `data_noticias_lavoz_subset_formatted.json`: Contiene las noticias del archivo `data_noticias_lavoz_subset.json` con la fecha normalizada y el atributo medio completo.
  
- `data_noticias_lavoz_politica_negocios.json`: Contiene las noticias del archivo `data_noticias_lavoz_subset_formatted.json` pasados por el Corpus y con el filtro de categorías de política y negocios (no es necesario porque los links ya pertenecen a esta categoría).

- `corpus_lavoz_politica_negocios.pkl`: El corpus de noticias seleccionadas guardado en pickle.

## Estructura de directorios

- `configs/`: Contiene las configuraciones en xml para crear el proyecto de anotación en label studio.
- `data/`
  - `raw/`: Datos procesados para la anotación.
  - `inputs/`: Bloques de 20 noticias generados a partir del corpus procesado previamente para la anotación.
  - `output/`: Anotaciones exportadas desde label studio.