from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations
from trustmonitor.import_utils import get_project_root
from spacy.matcher import Matcher

ROOT = get_project_root()
'''
# Load news from json file. 
corpus = ArticlesCorpus()
# corpus.load_articles(import_utils.import_news_from_json(f'{ROOT}/data/manual/noticias_demo.json'))
corpus.load_articles(import_utils.import_news_from_json(f'{ROOT}/scraper/data_noticias_lavoz_formatted.json'))

# Exportamos las noticias para label studio.
#corpus.export_articles(f"{ROOT}/label_studio/data/inputs/noticias_to_label_studio.json")

# Automatic NLP Annotations.
# Esto tendría que cambiar.
nlp = NLP('es','pysentimiento')
nlp._annotate_corpus(corpus)

# Importamos las anotaciones manuales y las cargamos al corpus.
#entities_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/outputs/annotations_entities_min.json", min_json=True)
#corpus.load_manual_annotations(manual_annotations=entities_annotations, author="jcc", annotated_attribute="entities")

# Importamos las anotaciones manuales y las cargamos al corpus.
#sources_annotations = import_manual_annotations(f"{ROOT}/label_studio/data/outputs/annotations_sources.json", min_json=False)
#corpus.load_manual_annotations(manual_annotations=sources_annotations, author="jcc", annotated_attribute="sources")

corpus.get_article(0).nlp_annotations.summary()
print("\n")
#corpus.get_article(0).manual_annotations.summary()
#print("\n")

# Save and load analyzed corpus.
corpus.save_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz.pkl")
'''

corpus2 = ArticlesCorpus().load_corpus(f"{ROOT}/data/pickle_files/corpus_lavoz.pkl")

def post_scrapp_processing(article_dict):
	rules = [('Redacción LAVOZ','\n')]

	for k in article_dict:
		if isinstance(article_dict[k], str):
			for rule in rules:
				article_dict[k] = article_dict[k].replace(rule[0],rule[1])
	return article_dict

# get atricle(1) to test customize entity spacy
#print(post_scrapp_processing(corpus2.get_article(1).get_article_dict()))

print(post_scrapp_processing(corpus2.get_article(1).get_article_dict()))

cuerpo = post_scrapp_processing(corpus2.get_article(1).get_article_dict())['cuerpo']

import spacy
from spacy.symbols import ORTH

# Load Spanish tokenizer
nlp = spacy.load("es_core_news_sm")

# Add special case to the tokenizer to handle closing quotes
special_case = [{ORTH: "”"}]
nlp.tokenizer.add_special_case("”", special_case)

# Initialize the Matcher with the shared vocabulary
matcher = Matcher(nlp.vocab)

# Define a pattern for capturing text within quotes
# Define two patterns
pattern1 = [
    {"ENT_TYPE": "PER"},    # Person entity
    {"POS": "VERB"},        # Verb
    {"IS_PUNCT": True, "OP": "*"},
    {"ORTH": "“"},  # Opening quote
    {"IS_PUNCT": False, "OP": "*"},  # Match any non-punctuation tokens between quotes
    {"ORTH": "”"}  # Exactly closing quote
]

pattern2 = [
    {"ENT_TYPE": "PER"},    # Person entity
    {"POS": "VERB"},        # Verb
    {"IS_PUNCT": True, "OP": "*"},
    {"ORTH": "“"},  # Opening quote
    {"IS_PUNCT": False, "OP": "*"},  # Match any non-punctuation tokens between quotes
    {"TEXT": {"REGEX": ".*”$"}}  # Token that ends with closing quote
]
# Define a pattern

# Add the pattern to the matcher
matcher.add("PERSON_VERB_QUOTE", [pattern1, pattern2])

# Create a document object
doc = nlp(cuerpo)

# Apply the matcher to the doc
matches = matcher(doc)

# Display the results
for match_id, start, end in matches:
    span = doc[start:end]  # The matched span
    print(f"Matched Span: {span.text}")


# Initialize a list to hold tokens, their entity types, and verb status
tokens_details = []

# Loop through each token in the document
for token in doc:
    # Get the entity type if the token is part of an entity
    entity_type = token.ent_type_ if token.ent_type_ else "No Entity"
    # Check if the token is a verb
    is_verb = "Yes" if token.pos_ == "VERB" else "No"
    # Append the token text, entity type, and verb status
    tokens_details.append((token.text, entity_type, is_verb))

# Print tokens, their corresponding entity types, and if they are verbs
for token, entity, verb in tokens_details:
    print(f"{token}: {entity}, Is Verb: {verb}")