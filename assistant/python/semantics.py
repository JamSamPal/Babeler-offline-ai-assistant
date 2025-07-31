from enum import Enum


class Predicate(Enum):
    """
    Enforce the valid predicates
    """

    IS_A = "is_a"
    HAS = "has"
    NONE = None

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


# Convert from natural language to internal types
predicate_map = {
    "is": Predicate.IS_A,
    "has": Predicate.HAS,
}


class Triple:
    """
    Structure to hold (subject, predicate, obj)
    """

    def __init__(self, subject, predicate, obj):
        self.subject = subject
        try:
            self.predicate = Predicate(predicate)
        except ValueError:
            raise ValueError(f"Invalid predicate: '{predicate}'")
        self.obj = obj

    def to_dict(self):
        return {
            "subject": self.subject,
            "predicate": self.predicate.value,
            "object": self.obj,
        }
