# nlp_stanza.py
import stanza
from NLP.nlp_base import NLPBase

class NLP_STANZA(NLPBase):
    def __init__(self, language):
        super().__init__(language)
        self.nlp = stanza.Pipeline(self.language, processors='tokenize,ner,sentiment,pos')

    def analyze(self, text):
        return self.nlp(text)

    def extract_entities(self, doc):
        entities = []
        for sentence in doc.sentences:
            for entity in sentence.ents:
                entities.append(entity.text)
        return entities

    def extract_entities_v2(self, doc):
        print(*[f'token: {token.text}\tner: {token.ner}' for sent in doc.sentences for token in sent.tokens], sep='\n')

    def extract_adjectives(self, doc):
        adjectives = []
        for sentence in doc.sentences:
            for word in sentence.words:
                # print(word,word.upos)
                if word.upos == 'ADJ':
                    adjectives.append(word.text)
        return adjectives

    def count_entity_types(self, doc):
        entity_classification = {}
        for sentence in doc.sentences:
            for entity in sentence.ents:
                if entity.type not in entity_classification:
                    entity_classification[entity.type] = 1
                else:
                    entity_classification[entity.type] += 1
        return entity_classification

    def extract_entity_sentiments(self, doc):
        entity_sentiments = {}
        for sentence in doc.sentences:
            for entity in sentence.ents:
                if entity.text not in entity_sentiments:
                    entity_sentiments[entity.text] = sentence.sentiment
        return entity_sentiments

    def extract_place(self, doc):
        raise NotImplementedError("extract_place not implemented")

    def extract_date(self, doc):
        try:
            date = doc.sentences[0].tokens[0].misc['Date']
        except TypeError:
            date = None
        return date

    def extract_sources(self, doc):
        sources = []
        for sentence in doc.sentences:
            for token in sentence.tokens:
                if token.misc is not None and 'Source' in token.misc:
                    sources.append(token.misc['Source'])
        return sources

    def extract_links(self, doc):
        links = []
        for sentence in doc.sentences:
            for token in sentence.tokens:
                if token.misc is not None and 'Link' in token.misc:
                    links.append(token.misc['Link'])
        return links
