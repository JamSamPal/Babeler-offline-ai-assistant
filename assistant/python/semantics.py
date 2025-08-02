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
