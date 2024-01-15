# trust-monitor
Our goal is to develop a prototype that uses AI to identify specific quality indicators within news stories within the newsroom environment. This AI Monitor will be tailored specifically for newsroom editors, helping them to identify issues such as a lack of sources, an excess of adjectives, or discrepancies in information that can be addressed using online tools such as Fact-Checker Explorer.

## Index

- [Installation](#instalation)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Installation
1. Clone the Repository
2. Navigate to the Project Directory
3. Create a Virtual Environment (Optional but Recommended):
```bash
python -m venv venv
```
Create a virtual environment named venv. To activate the virtual environment:
* On Windows:
```bash
.\venv\Scripts\activate
```
* On macOS and Linux:
```bash
source venv/bin/activate
```
4. Install Dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Execute the main script to run the project.
```bash
python main.py
```

Alternatively, you can try it in a Live Python Terminal, as follows:

```bash
from NLP.nlp_stanza import NLP_STANZA

nlp = NLP_STANZA('es')
doc = nlp.analyze("El presidente de la Cámara de Propietarios de la República Argentina aseguró...")
entities = nlp.extract_entities(doc)
entities_count = nlp.count_entities(doc)
adjectives = nlp.extract_adjectives(doc)
adjective_count = nlp.count_adjectives(doc)
entity_type_counts = nlp.count_entity_types(doc)
entity_sentiments = nlp.extract_entity_sentiments(doc)
```

## Project Structure

```bash
/NLP
    |-- nlp_base.py
    |-- nlp_spacy.py
    |-- nlp_stanza.py
|-- main.py
|-- requirements.txt
|-- README.md
```
