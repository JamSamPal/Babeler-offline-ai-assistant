from enum import Enum


class PredicateManager:
    def __init__(self):
        # Convert from natural language to internal types
        self.predicate_map = {
            "": "",
            "type of": "is_a",
            "are": "is_a",
            "is a": "is_a",
            "is": "is_a",
            "have": "has",
            "has": "has",
            "discovered": "discovered",
        }

    def add_predicate(self, key, value):
        self.predicates[key] = {value}

    def get_predicate(self, key):
        return self.predicates.get(key)


class Triple:
    """
    Structure to hold (subject, predicate, obj)
    """

    def __init__(self, subject, predicate, obj):
        self.subject = subject
        self.predicate = predicate
        self.obj = obj

    def to_dict(self):
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.obj,
        }
