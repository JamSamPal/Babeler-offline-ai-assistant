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
        and attributes: "does a dog have fur?". It will recursively search
        asking broader and broader questions e.g.:
        "is a dog an animal?" ->
        ("I know a dog is a mammal") ->
        "is a mammal an animal?" ->
        ("I know a mammal is an animal so a dog must be) ->
        "yes"
        """
        triple_bank = [triple]
        old_triples = set()

        while triple_bank:
            current_triple = triple_bank.pop()

            if current_triple in old_triples:
                continue
            old_triples.add(current_triple)

            facts = self.by_subject.get(current_triple.subject, [])
            for pred, obj in facts:
                if (current_triple.predicate, current_triple.obj) == (pred, obj):
                    return "Yes."
                elif pred == "is a":
                    next_triple = Triple(
                        obj, current_triple.predicate, current_triple.obj
                    )
                    triple_bank.append(next_triple)
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
        """
        # uses pre-computed index for speed
        subjects = self.by_predicate_object.get((triple.predicate, triple.obj), [])
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
        # Check for duplicate fact
        potential_duplicate_facts = self.by_subject.get(triple.subject, [])
        if (
            triple.predicate,
            triple.obj,
        ) in potential_duplicate_facts:
            return "I already know that fact"

        # Add to memory
        self.memory.append(
            {
                "subject": triple.subject,
                "predicate": triple.predicate,
                "object": triple.obj,
            }
        )

        # Update indexes
        self.by_subject[triple.subject].append((triple.predicate, triple.obj))
        self.by_predicate_object[(triple.predicate, triple.obj)].append(triple.subject)

        # Save to disk
        save_memory(self.config_path, self.memory)

        if suppress_output:
            return

        return f"Okay, I will remember that for next time"
