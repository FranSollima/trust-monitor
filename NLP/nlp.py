# nlp_base.py
import spacy
import stanza

class NLP:
    ### GENERALES ###
    def __init__(self, language, libreria):
        self.language = language
        self.libreria = libreria
        if self.libreria not in ('spacy', 'stanza'):
            raise NotImplementedError("Librería no implementada")
        if self.libreria == 'spacy':
            self._init_spacy()
        elif self.libreria == 'stanza':
            self._init_stanza()

    def analyze(self, text):
        if self.libreria == 'spacy':
            return self._analyze_spacy(text)
        elif self.libreria == 'stanza':
            return self._analyze_stanza(text)

    def extract_entities(self, doc):
        if self.libreria == 'spacy':
            return self._extract_entities_spacy(doc)
        elif self.libreria == 'stanza':
            return self._extract_entities_stanza(doc)

    def extract_entities_v2(self, doc):
        if self.libreria == 'spacy':
            return self._extract_entities_v2_spacy(doc)
        elif self.libreria == 'stanza':
            return self._extract_entities_v2_stanza(doc)

    def extract_adjectives(self, doc):
        if self.libreria == 'spacy':
            return self._extract_adjectives_spacy(doc)
        elif self.libreria == 'stanza':
            return self._extract_adjectives_stanza(doc)

    def count_entity_types(self, doc):
        if self.libreria == 'spacy':
            return self._count_entity_types_spacy(doc)
        elif self.libreria == 'stanza':
            return self._count_entity_types_stanza(doc)

    def extract_entity_sentiments(self, doc):
        if self.libreria == 'spacy':
            return self._extract_entity_sentiments_spacy(doc)
        elif self.libreria == 'stanza':
            return self._extract_entity_sentiments_stanza(doc)

    def extract_place(self, doc):
        raise NotImplementedError("extract_place not implemented")

    def extract_date(self, doc):
        raise NotImplementedError("extract_date not implemented")

    def extract_sources(self, doc):
        raise NotImplementedError("extract_sources not implemented")

    def extract_links(self, doc):
        raise NotImplementedError("extract_links not implemented")

    def count_adjectives(self, doc):
        return len(self.extract_adjectives(doc))

    def count_entities(self, doc):
        return len(self.extract_entities(doc))

    ### SPACY ###
    def _init_spacy(self):
        self.nlp = spacy.load(f'{self.language}_core_news_sm')

    def _analyze_spacy(self, text):
        return self.nlp(text)

    def _extract_entities_spacy(self, doc):
        entities = []
        for entity in doc.ents:
            entities.append(entity.text)
        return entities

    def _extract_entities_v2_spacy(self, doc):
        # Para cada entidad devolver el texto y el tipo y la posicion
        # Ver equivalencia de tipos entre spacy y stanza
        raise NotImplementedError("_extract_entities_v2_spacy not implemented")

    def _extract_adjectives_spacy(self, doc):
        adjectives = []
        for token in doc:
            if token.pos_ == 'ADJ':
                adjectives.append(token.text)
        return adjectives

    def _count_entity_types_spacy(self, doc):
        entity_classification = {}
        for entity in doc.ents:
            if entity.label_ not in entity_classification:
                entity_classification[entity.label_] = 1
            else:
                entity_classification[entity.label_] += 1
        return entity_classification

    def _extract_entity_sentiments_spacy(self, doc):
        raise Exception("No implementado para spacy - por ahora")
        entity_sentiments = {}
        for entity in doc.ents:
            if entity.text not in entity_sentiments:
                entity_sentiments[entity.text] = [entity.sentiment]
            else:
                entity_sentiments[entity.text].append(entity.sentiment)
        return entity_sentiments

    ### STANZA ###
    def _init_stanza(self):
        self.nlp = stanza.Pipeline(self.language, processors='tokenize,ner,sentiment,pos')

    def _analyze_stanza(self, text):
        return self.nlp(text)

    def _extract_entities_stanza(self, doc):
        entities = []
        for sentence in doc.sentences:
            for entity in sentence.ents:
                entities.append(entity.text)
        return entities

    def _extract_entities_v2_stanza(self, doc):
        # Para cada entidad devolver el texto y el tipo y la posicion
        # Ver equivalencia de tipos entre spacy y stanza
        print(*[f'token: {token.text}\tner: {token.ner}' for sent in doc.sentences for token in sent.tokens], sep='\n')

    def _extract_adjectives_stanza(self, doc):
        adjectives = []
        for sentence in doc.sentences:
            for word in sentence.words:
                # print(word,word.upos)
                if word.upos == 'ADJ':
                    adjectives.append(word.text)
        return adjectives

    def _count_entity_types_stanza(self, doc):
        entity_classification = {}
        for sentence in doc.sentences:
            for entity in sentence.ents:
                if entity.type not in entity_classification:
                    entity_classification[entity.type] = 1
                else:
                    entity_classification[entity.type] += 1
        return entity_classification

    def _extract_entity_sentiments_stanza(self, doc):
        entity_sentiments = {}
        for sentence in doc.sentences:
            for entity in sentence.ents:
                if entity.text not in entity_sentiments:
                    entity_sentiments[entity.text] = [sentence.sentiment]
                else:
                    entity_sentiments[entity.text].append(sentence.sentiment)
        return entity_sentiments
