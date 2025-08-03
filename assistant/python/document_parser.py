import spacy
from assistant.python.semantics import Triple


class DocumentParser:
    """
    Extracts triples from a given file and saves them to memory
    """

    def __init__(self):
        # Load the English model
        self.nlp = spacy.load("en_core_web_sm")

    def extract_text(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            return text
        except FileNotFoundError:
            return

    def extract_triples(self, path):
        text = self.extract_text(path)

        if not text:
            return []

        doc = self.nlp(text)
        triples = []

        for sent in doc.sents:
            subjects = []
            predicates = []
            objects = []

            for token in sent:
                # Identify subjects
                if "nsubj" in token.dep_ or "csubj" in token.dep_:
                    subjects.append(token.text.lower())

                # Identify main verbs (predicates)
                if token.dep_ == "ROOT" and token.pos_ == "VERB":
                    predicates.append(token.text.lower())

                # Identify direct objects
                if "dobj" in token.dep_:
                    objects.append(token.text.lower())

            if subjects and predicates and objects:
                for s in subjects:
                    for p in predicates:
                        for o in objects:
                            triples.append(Triple(s, p, o))

        return triples
