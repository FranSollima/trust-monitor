from NLP.nlp import NLP
from article_example import article

nlp = NLP('es', 'spacy')
doc = nlp.analyze(article['body'])
entities = nlp.extract_entities(doc)
entities_count = nlp.count_entities(doc)
adjectives = nlp.extract_adjectives(doc)
adjective_count = nlp.count_adjectives(doc)
# entities_V2 = nlp.extract_entities_v2(doc) # TODO: No implementado en spacy | reformular para stanza
entity_type_counts = nlp.count_entity_types(doc)
# entity_sentiments = nlp.extract_entity_sentiments(doc) # TODO: No implementado en spacy | igualar el output de ambas librerias

print(f'entities: {entities}')
print(f'entities_count: {entities_count}')
print(f'adjectives: {adjectives}')
print(f'adjective_count: {adjective_count}')
# print(f'entities_V2: {entities_V2}')
print(f'entity_type_counts: {entity_type_counts}')
# print(f'entity_sentiments: {entity_sentiments}')
