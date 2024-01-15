from NLP.nlp_stanza import NLP_STANZA as NLP
# from NLP.nlp_spacy import NLP_SPACY as NLP
from article_example import article

nlp = NLP('es')
doc = nlp.analyze(article['body'])
entities = nlp.extract_entities(doc)
entities_count = nlp.count_entities(doc)
adjectives = nlp.extract_adjectives(doc)
adjective_count = nlp.count_adjectives(doc)
# entities_V2 = nlp.extract_entities_v2(doc)  # TODO: qué es esto? | No implementado en spacy
entity_type_counts = nlp.count_entity_types(doc)
entity_sentiments = nlp.extract_entity_sentiments(doc)  # TODO: ver bien cómo es el output para ambas librerías
# place = nlp.extract_place(doc)
# date = nlp.extract_date(doc)  # TODO: está bien hecho? | No implementado en spacy
# sources = nlp.extract_sources(doc)  # TODO: está bien hecho? | No implementado en spacy
# links = nlp.extract_links(doc)  # TODO: está bien hecho? | No implementado en spacy

print(f'entities: {entities}')
print(f'entities_count: {entities_count}')
print(f'adjectives: {adjectives}')
print(f'adjective_count: {adjective_count}')
# print(f'entities_V2: {entities_V2}')
print(f'entity_type_counts: {entity_type_counts}')
print(f'entity_sentiments: {entity_sentiments}')
# print(f'place: {place}')
# print(f'date: {date}')
# print(f'sources: {sources}')
# print(f'links: {links}')
