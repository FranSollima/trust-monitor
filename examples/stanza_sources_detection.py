
# Modules

from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations
import logging
from tqdm import tqdm


# Functions

def normalize_ner(ner):
    if ner == "O":
        return "O"
    else:
        return ner.split("-")[1]
    

def flatten_stanza_tokens(stanza_doc):

    doc_tokens = []
    i = 0

    for sentence in stanza_doc.sentences:
        for token in sentence.tokens:
            t_abs_id = i
            t_id = token.id
            t_len = len(t_id)
            t_sent_id = int(sentence.sent_id)
            t_text = token.text
            t_start = token.start_char
            t_end = token.end_char
            t_ner = token.ner 
            t_norm_ner = normalize_ner(token.ner)
            t_checked = False
            
            if t_len == 1:
                t_lemma = token.words[0].lemma
                t_upos = token.words[0].upos
                t_xpos = token.words[0].xpos
                t_feats = token.words[0].feats
                t_head = token.words[0].head
                t_deprel = token.words[0].deprel
            
            else:
                t_lemma = "" #(token.words[0].lemma, token.words[1].lemma)
                t_upos = "" #(token.words[0].upos, token.words[1].upos)
                t_xpos = "" #(token.words[0].xpos, token.words[1].xpos)
                t_feats = "" #(token.words[0].feats, token.words[1].feats)
                t_head = "" #(token.words[0].head, token.words[1].head)
                t_deprel = "" #(token.words[0].deprel, token.words[1].deprel)
                
            new_token = dict(id_length = t_len, token_id = t_id, sent_id = t_sent_id, abs_id = t_abs_id, text = t_text, start_char = t_start, end_char = t_end, ner = t_ner, norm_ner = t_norm_ner, lemma = t_lemma, upos = t_upos, xpos = t_xpos, feats = t_feats, head = t_head, deprel = t_deprel, token_checked=t_checked)
            doc_tokens.append(new_token)
            i += 1
            
    return doc_tokens


def configure_logger():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    

def check_pattern_match(token, pattern):
    if pattern == "*":
        return True
    else:
        attribute_to_check = list(pattern.keys())[0]
        pattern_value = pattern[attribute_to_check] if type(pattern[attribute_to_check]) == list else [pattern[attribute_to_check]]
        return token[attribute_to_check] in pattern_value
        # if token[attribute_to_check] in pattern[attribute_to_check]:
        #     return True
        # else:
        #     return False
        
def matcher(doc_tokens, patterns, debug=False):
    
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        
    detection_list = []
        
    for token in doc_tokens:
        logger.debug(f"Token analizado {token['abs_id']} - {token['text']}")
        
        for pattern_name, pattern in patterns.items():
            logger.debug(f"Pattern analizado {pattern}")
            # Cuando se cumple el primer patrón, se agrega el token a la lista de fuentes
            
            if check_pattern_match(token, pattern[0]):
                
                detection = [token]
                detection_check = [True]
                start_index = token["abs_id"]

                logger.debug(f"Deteccion token entrada {token['abs_id']} - {token['text']}")
                logger.debug(f"Se evalua el prox token  {doc_tokens[start_index + 1]['abs_id']} - {doc_tokens[start_index + 1]['text']}")
                                
                i = 1
                
                for j, p in enumerate(pattern[1:], 1):
                    
                    
                    # Si todavía no se llegó al final del documento:
                    if (start_index + i) < len(doc_tokens):
                    
                        logger.debug(f"token número -> {start_index + i} de {len(doc_tokens)}")
                        logger.debug(f"Se evalua el token  {doc_tokens[start_index + i]['abs_id']} - {doc_tokens[start_index + i]['text']} con la regla {p}")
                        
                        # En este lugar tendría que tener el próximo patrón
                        # Agregar todas las palabras hasta que se cumpla el próximo patrón
                        # Ir avanzando en el índice de tokens
                        if p == "*":
                            logger.debug("Entra en *")
                            while not check_pattern_match(doc_tokens[start_index + i], pattern[j+1]):
                                logger.debug(f"Evalua el próximo token {doc_tokens[start_index + i]['abs_id']} -  {doc_tokens[start_index + i]['text']} pattern {pattern[j+1]}")
                                detection.append(doc_tokens[start_index + i])
                                detection_check.append(True)
                                i += 1
                                if i == len(doc_tokens):
                                    break
                            
                            i -= 1
                            logger.debug(f"FIN Next token {doc_tokens[start_index + i]['abs_id']} -  {doc_tokens[start_index + i]['text']} pattern {pattern[j+1]}")
                        #     while                  
                        
                        # elif list(p.keys())[0] == "norm_ner":
                        #     print("Entra en NER")
                        #     print(f"Evalua el próximo token {doc_tokens[start_index + i]['abs_id']} - {doc_tokens[start_index + i]['text']} pattern {p}")
                        #     while check_pattern_match(doc_tokens[start_index + i], p):
                        #         print(f"Dentro NER se evalua el próximo token {doc_tokens[start_index + i]['abs_id']} - {doc_tokens[start_index + i]['text']} pattern {p}")
                        #         detection.append(doc_tokens[start_index + i])
                        #         detection_check.append(True)
                        #         i += 1
                        #         if i == len(doc_tokens):
                        #             break
                                
                        #     i -= 1
                        #     print(f"FIN NER Next token {doc_tokens[start_index + i]['abs_id']} - {doc_tokens[start_index + i]['text']} pattern {p}")
                        
                        elif check_pattern_match(doc_tokens[start_index + i], p):
                            logger.debug(f"Evalua el próximo token {doc_tokens[start_index + i]['abs_id']} -  {doc_tokens[start_index + i]['text']} pattern {p}")
                            detection.append(doc_tokens[start_index + i])
                            detection_check.append(True)
                            
                        else:
                            logger.debug("NO SE CUMPLE LA REGLA")
                            detection_check.append(False) 
                            break
                            
                        i += 1
                        
                    else:
                        logger.debug("NO HAY MAS TOKENS")
                        detection_check.append(False)
                        break
                        
                if all(detection_check): 
                    logger.debug("SE CUMPLE LA REGLA")
                    detection_list.append({'pattern': pattern_name,
                                           'start_char':detection[0]['start_char'],
                                           'end_char':detection[-1]['end_char'],
                                           'length':detection[-1]['end_char'] - detection[0]['start_char'],
                                           'detection':detection})
                    
            else:
                continue
    
    logger.info([(d["pattern"], d["start_char"], d["end_char"]) for d in detection_list])
    
    return detection_list

def postprocess_matches(matches):
    
    drops = []
    
    print("Initial Matches")
    print([(d["pattern"], d["start_char"], d["end_char"]) for d in matches])

    for i, match in enumerate(matches):
        start = match["start_char"]
        end = match["end_char"]
        length = match["length"]
        match_drops = []
        matches_left = [m for j,m in enumerate(matches) if j != i] 
        
        for other_match in matches_left:
            
            if start >= other_match["start_char"] and start <= other_match["end_char"]:
                if length <= other_match["length"]:
                    match_drops.append(1)
            elif end >= other_match["start_char"] and end <= other_match["end_char"]: 
                if length <= other_match["length"]:
                    match_drops.append(1)
            else:
                match_drops.append(0)
        
        drops.append(sum(match_drops))
        
    matches = [m for i, m in enumerate(matches) if drops[i] == 0]

    print("Final Matches")
    print([(d["pattern"], d["start_char"], d["end_char"]) for d in matches])
    
    return matches


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






# Configure the logger
logger = logging.getLogger(__name__)
if logger.hasHandlers():
    logger.handlers.clear()
configure_logger()

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
    
    logger.info(f"Processing article {article.index} - {article.titulo}")
    doc = article.nlp_annotations.doc["stanza"]

    doc_tokens = flatten_stanza_tokens(doc)

    detection_list = matcher(doc_tokens, patterns, debug=False)

    detection_list = postprocess_matches(detection_list)

    sources_list = get_explicit_sources(doc, detection_list)
    
    article.nlp_annotations.sources["stanza"] = sources_list
    #article.nlp_annotations.doc = {}
    
    
corpus.save_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz_politica_negocios_5_srcs.pkl")