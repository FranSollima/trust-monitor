# nlp_base.py

class NLPBase:
    def __init__(self, language, library):
        self.language = language
        

    def analyze(self, text):
        raise NotImplementedError("Subclasses must implement the analyze method.")

    def count_adjectives(self, doc):
        raise NotImplementedError("Subclasses must implement the count_adjectives method.")

    def count_entities(self, doc):
        raise NotImplementedError("Subclasses must implement the count_entities method.")
