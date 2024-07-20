from flask import Flask, request, jsonify
import json
import os
from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus, NLPAnnotations
from trustmonitor.nlp import NLP
from trustmonitor.manual_annotations_utils import import_manual_annotations

app = Flask(__name__)

# Initialize the NLP model
nlp = NLP(language="es", libreria="pysentimiento")

@app.route('/process', methods=['POST'])
def process_corpus():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Assuming data is a list of dictionaries representing the corpus
        corpus = ArticlesCorpus()
        corpus.load_articles(data)

        # Annotate the corpus
        nlp._annotate_corpus(corpus)

        corpus_out = corpus.to_dict(include_annotations = True)

        response = corpus_out

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)