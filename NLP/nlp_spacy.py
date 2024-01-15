# nlp_spacy.py
import spacy
from NLP.nlp_base import NLPBase

class NLP_SPACY(NLPBase):
    def __init__(self, language):
        super().__init__(language)
        self.nlp = spacy.load(f'{self.language}_core_news_sm')

    def analyze(self, text):
        return self.nlp(text)

    def extract_entities(self, doc):
        entities = []
        for entity in doc.ents:
            entities.append(entity.text)
        return entities

    def extract_entities_v2(self, doc):
        raise NotImplementedError("extract_entities_v2 not implemented")

    def extract_adjectives(self, doc):
        adjectives = []
        for token in doc:
            if token.pos_ == 'ADJ':
                adjectives.append(token.text)
        return adjectives

    def count_entity_types(self, doc):
        entity_classification = {}
        for entity in doc.ents:
            if entity.label_ not in entity_classification:
                entity_classification[entity.label_] = 1
            else:
                entity_classification[entity.label_] += 1
        return entity_classification
        
    def extract_entity_sentiments(self, doc):
        entity_sentiments = {}
        for entity in doc.ents:
            if entity.text not in entity_sentiments:
                entity_sentiments[entity.text] = [entity.sentiment]
            else:
                entity_sentiments[entity.text].append(entity.sentiment)
        return entity_sentiments

    def extract_place(self, doc):
        raise NotImplementedError("extract_place not implemented")

    def extract_date(self, doc):
        raise NotImplementedError("extract_date not implemented")

    def extract_sources(self, doc):
        raise NotImplementedError("extract_sources not implemented")

    def extract_links(self, doc):
        raise NotImplementedError("extract_links not implemented")
