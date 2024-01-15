# nlp_base.py

class NLPBase:
    def __init__(self, language):
        self.language = language

    def analyze(self, text):
        raise NotImplementedError("Subclasses must implement the analyze method.")

    def extract_entities(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_entities method.")

    def extract_entities_v2(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_entities_v2 method.")

    def extract_adjectives(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_adjectives method.")

    def count_entity_types(self, doc):
        raise NotImplementedError("Subclasses must implement the count_entity_types method.")
    
    def extract_entity_sentiments(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_entity_sentiments method.")
    
    def extract_place(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_place method.")
    
    def extract_date(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_date method.")
    
    def extract_sources(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_sources method.")
    
    def extract_links(self, doc):
        raise NotImplementedError("Subclasses must implement the extract_links method.")
    
    def count_adjectives(self, doc):
        return len(self.extract_adjectives(doc))

    def count_entities(self, doc):
        return len(self.extract_entities(doc))
