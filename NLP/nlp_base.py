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

    def count_adjectives(self, doc):
        return len(self.extract_adjectives(doc))

    def count_entities(self, doc):
        return len(self.extract_entities(doc))
