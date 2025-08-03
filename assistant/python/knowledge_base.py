from collections import defaultdict
from assistant.json.json_help import load_config, save_memory
from assistant.python.semantics import Triple


class KnowledgeBase:
    """
    Reads and writes to memory.json allowing us to query the memory
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.memory = load_config(config_path)
        self.by_subject = defaultdict(list)
        self.by_predicate_object = defaultdict(list)
        self.pending_fact = None
        self.index_triples()

    def normalise_predicate(self, pred: str):
        """
        Accounting for tenses - in the future
        this will also deal with synonyms
        """
        pred = pred.lower().strip()
        if pred in {"is", "are", "type of"}:
            return "is a"
        elif pred in {"has", "have"}:
            return "has"
        return pred

    def index_triples(self):
        """
        Build indexes for quick lookup by subject and by (predicate, object).
        """
        for fact in self.memory:
            s, p, o = fact["subject"], fact["predicate"], fact["object"]
            self.by_subject[s].append((p, o))
            self.by_predicate_object[(p, o)].append(s)

    def get_answer(self, triple: Triple):
        """
        Queries and answers questions on inheritance: "is a dog a mammal?"
        and attributes: "does a dog have fur?" Essentially looks up predicate
        and object given subject.
        """
        facts = self.by_subject.get(triple.subject, [])
        if (self.normalise_predicate(triple.predicate), triple.obj) in facts:
            return "Yes."
        else:
            self.pending_fact = triple
            return "PENDING_FACT"
    
    def possible_fact(self, reply: str):
        if self.pending_fact and reply in {"yes", "sure", "ok", "yeah"}:
            response = self.set_facts(self.pending_fact)
            self.pending_fact = None
            return response

        elif self.pending_fact and reply in {"no", "nah", "not really"}:
            self.pending_fact = None
            return "Okay, I won't remember it."

        return "PENDING_FACT"

    def get_inverse_answer(self, triple: Triple):
        """
        Queries and answers questions like: "what is a mammal?", "what has fur"
        Essentially looks up subject given predicate and object
        """
        # uses pre-computed index for speed
        subjects = self.by_predicate_object.get(
            (self.normalise_predicate(triple.predicate), triple.obj), []
        )
        if not subjects:
            return f"I don't know."
        elif len(subjects) == 1:
            return f"{subjects[0]}"
        else:
            joined = ", ".join(subjects)
            return f"{joined}."

    def get_facts(self, triple: Triple):
        """
        Returns all the information on a subject in a human
        readable format
        """
        facts = self.by_subject.get(triple.subject, [])
        if not facts:
            return f"I don't know anything about {triple.subject}."
        return self.facts_to_text(triple.subject, facts)

    def facts_to_text(self, subject: str, facts: str):
        lines = []
        for predicate, obj in facts:
            if predicate == "is a":
                lines.append(f"A {subject} is a {obj}.")
            elif predicate == "has":
                lines.append(f"A {subject} has {obj}.")
            else:
                lines.append(f"{subject} {predicate} {obj}.")
        return " ".join(lines)

    def set_facts(self, triple: Triple, suppress_output: bool = False):
        """
        Writes a triple to memory.json
        """
        # Normalise Predicate
        normalised_predicate = self.normalise_predicate(triple.predicate)

        # Check for duplicate fact
        potential_duplicate_facts = self.by_subject.get(triple.subject, [])
        if (
            normalised_predicate,
            triple.obj,
        ) in potential_duplicate_facts:
            return "I already know that fact"

        # Add to memory
        self.memory.append(
            {
                "subject": triple.subject,
                "predicate": normalised_predicate,
                "object": triple.obj,
            }
        )

        # Update indexes
        self.by_subject[triple.subject].append((normalised_predicate, triple.obj))
        self.by_predicate_object[(normalised_predicate, triple.obj)].append(
            triple.subject
        )

        # Save to disk
        save_memory(self.config_path, self.memory)

        if suppress_output:
            return

        return f"Okay, I will remember that for next time"
