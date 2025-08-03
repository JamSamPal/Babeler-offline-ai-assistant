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
            subject = ""
            predicate = ""
            obj = ""
            for token in sent:
                # Find the subject
                if "subj" in token.dep_:
                    subject = token.text
                # Find the object
                if "obj" in token.dep_:
                    obj = token.text
                # Find the main verb (predicate)
                if token.dep_ == "ROOT":
                    predicate = token.text
            if subject and predicate and obj:
                triples.append(Triple(subject.lower(), predicate.lower(), obj.lower()))
        return triples
