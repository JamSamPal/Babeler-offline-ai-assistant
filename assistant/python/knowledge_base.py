from collections import defaultdict
from assistant.json.json_help import load_config, save_memory, save_config_value
from assistant.python.semantics import Triple


class KnowledgeBase:
    """
    Reads and writes to memory.json allowing us to query the memory
    """

    def __init__(self, config_path: str, predicate_map_path: str):
        self.config_path = config_path
        self.predicate_map_path = predicate_map_path
        self.memory = load_config(config_path)
        self.predicate_map = load_config(predicate_map_path)
        self.by_subject = defaultdict(list)
        self.by_predicate_object = defaultdict(list)
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
        and attributes: "does a dog have fur?" Essentially looks up predicate
        and object given subject.
        """
        facts = self.by_subject.get(triple.subject, [])
        if (self.predicate_map[triple.predicate], triple.obj) in facts:
            return "Yes."
        elif facts:
            return f"I know some things about {triple.subject}, but not that."
        else:
            return "I don't know."

    def get_inverse_answer(self, triple: Triple):
        """
        Queries and answers questions like: "what is a mammal?", "what has fur"
        Essentially looks up subject given predicate and object
        """
        # uses pre-computed index for speed
        subjects = self.by_predicate_object.get(
            (self.predicate_map[triple.predicate], triple.obj), []
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

    def set_facts(self, triple: Triple, surpress_output: bool = False):
        """
        Writes a triple to memory.json
        """
        # Check for duplicate fact
        potential_duplicate_facts = self.by_subject.get(triple.subject, [])
        if any(
            p == self.predicate_map[triple.predicate]
            for (p, _) in potential_duplicate_facts
        ):
            return "I already know that fact"

        # Check predicate
        if triple.predicate not in self.predicate_map:
            self.predicate_map[triple.predicate] = triple.predicate
            save_config_value(
                triple.predicate, triple.predicate, self.predicate_map_path
            )

        # Add to memory
        self.memory.append(
            {
                "subject": triple.subject,
                "predicate": self.predicate_map[triple.predicate],
                "object": triple.obj,
            }
        )

        # Update indexes
        self.by_subject[triple.subject].append(
            (self.predicate_map[triple.predicate], triple.obj)
        )
        self.by_predicate_object[
            (self.predicate_map[triple.predicate], triple.obj)
        ].append(triple.subject)

        # Save to disk
        save_memory(self.config_path, self.memory)

        if surpress_output:
            return

        return f"Okay, I will remember that for next time"
