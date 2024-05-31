
# Modules

from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations
from tqdm import tqdm
from trustmonitor.matcher import Matcher


def get_explicit_sources(doc, matches):    

    sources_list = []

    for detection in matches:
        
        # Texto General.
        start_char = detection["start_char"]
        end_char = detection["end_char"]
        length = detection["length"]
        pattern = detection["pattern"]
        text = doc.text[start_char:end_char]
        
        source = {'text':text,
                'start_char':start_char,
                'end_char':end_char,
                'length':length,
                'pattern':pattern,
                'explicit':True,
                'components':{}}
        
        # Obtenemos la lista de tokens de la afirmación y del resto para la cita.
        abs_id_quote = [t["abs_id"] for t in detection["detection"] if t["text"] == '“' or t["text"] == '”']
        token_list_quote = [t for t in detection["detection"] if t["abs_id"] >= abs_id_quote[0] and t["abs_id"] <= abs_id_quote[1]]
        token_list_else = [t for t in detection["detection"] if t["abs_id"] < abs_id_quote[0] or t["abs_id"] > abs_id_quote[1]]
        
        # Afirmación.
        start_char = token_list_quote[0]["start_char"]
        end_char = token_list_quote[-1]["end_char"]
        text = doc.text[start_char:end_char]
        label = "Afirmacion"
        
        source['components']['afirmacion'] = {'text':text, 'start_char':start_char, 'end_char':end_char, 'label':label}
        
        # Conector.
        # Asume 1 solo conector.
        # Asume que siempre tiene que haber conector
        token_conector = [t for t in token_list_else if t["upos"] == "VERB"][0]
        start_char = token_conector["start_char"]
        end_char = token_conector["end_char"]
        text = doc.text[start_char:end_char]
        label = "Conector"
        
        source['components']['conector'] = {'text':text, 'start_char':start_char, 'end_char':end_char, 'label':label}
        
        # Conector.
        # Asume persona en orden consecutivo.
        # Puede no encontrar un referenciado.
        token_src = [t for t in token_list_else if t["norm_ner"] == "PER"]
        if len(token_src) > 0:
            start_char = token_src[0]["start_char"]
            end_char = token_src[-1]["end_char"]
            text = doc.text[start_char:end_char]
            label = "Referenciado"
            
            source['components']['referenciado'] = {'text':text, 'start_char':start_char, 'end_char':end_char, 'label':label}
        
        sources_list.append(source)
    
    return sources_list






# # Configure the logger
# logger = logging.getLogger(__name__)
# if logger.hasHandlers():
#     logger.handlers.clear()
# configure_logger()

ROOT = import_utils.get_project_root()
#corpus = ArticlesCorpus().load_corpus(f"{ROOT}/label_studio/data/raw/corpus_lavoz_politica_negocios_nlp_srcs.pkl")
corpus = ArticlesCorpus().load_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz_politica_negocios_5.pkl")

pattern1 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"upos":"VERB"},
    {"norm_ner":"PER"},
]

pattern2 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"upos":"VERB"},
    #{"norm_ner":"PER"},
]

pattern3 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"upos":"VERB"},
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
]

pattern4 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"text":[",", ":"]},
    {"upos":"VERB"},
]

pattern5 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"text":[",", ":"]},
    {"upos":"VERB"},   
    {"norm_ner":"PER"},
]

pattern6 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"text":[",", ":"]},
    {"upos":"VERB"},
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
]

pattern7 = [
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":"“"},
    "*",
    {"text":"”"}
]

pattern8 = [
    {"upos":"VERB"},
    {"text":"“"},
    "*",
    {"text":"”"}
    #{"norm_ner":"PER"},
]

pattern9 = [
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":"“"},
    "*",
    {"text":"”"}
]

pattern10 = [
    {"upos":"VERB"},
    {"text":[",", ":"]},
    {"text":"“"},
    "*",
    {"text":"”"},
]

pattern11 = [
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":[",", ":"]},
    {"text":"“"},
    "*",
    {"text":"”"}
]

pattern12 = [
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":[",", ":"]},
    {"text":"“"},
    "*",
    {"text":"”"}
]

patterns = {"QVP":pattern1, 
            "QV":pattern2, 
            "QVPP":pattern3, 
            "Q.V":pattern4, 
            "Q.VP":pattern5,
            "Q.VPP":pattern6,
            "PVQ":pattern7,
            "VQ":pattern8,
            "PPVQ":pattern9,
            "V.Q":pattern10,
            "PV.Q":pattern11,
            "PPV.Q":pattern12
            }

#doc = corpus.get_article(2).nlp_annotations.doc["stanza"]

for article in tqdm(corpus.get_articles()):
    
    #logger.info(f"Processing article {article.index} - {article.titulo}")
    doc = article.nlp_annotations.doc["stanza"]
    
    matcher = Matcher(patterns=patterns, debug=False)
    matches = matcher.run(doc)

    # doc_tokens = flatten_stanza_tokens(doc)

    # detection_list = matcher(doc_tokens, patterns, debug=False)

    # detection_list = postprocess_matches(detection_list)

    # sources_list = get_explicit_sources(doc, detection_list)
    
    sources_list = get_explicit_sources(doc, matches)
    
    article.nlp_annotations.sources["stanza"] = sources_list
    #article.nlp_annotations.doc = {}
    
    
corpus.save_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz_politica_negocios_5_srcs.pkl")