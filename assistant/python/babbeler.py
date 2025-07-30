from collections import defaultdict
from assistant.json.json_help import load_config, save_memory

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
            "object": self.obj
        }

class babbeler():
    """
    Reads and writes to memory.json allowing us to query the memory
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.memory= load_config(config_path)
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
        and attributes: "does a dog have fur?"
        """
        facts = self.by_subject.get(triple.subject, [])
        if (triple.predicate, triple.obj) in facts:
            return "Yes."
        elif any(p == triple.predicate for (p, _) in facts):
            return f"I know some things about {triple.subject}, but not that."
        else:
            return "I don't know."

    def get_facts(self, subject: str):
        """
        Returns all the information on a subject in a human
        readable format
        """
        facts = self.by_subject.get(subject, [])
        if not facts:
            return f"I don't know anything about {subject}."
        return self.facts_to_text(subject, facts)
    
    
    def facts_to_text(self, subject, facts):
        lines = []
        for predicate, obj in facts:
            if predicate == "is_a":
                lines.append(f"A {subject} is a {obj}.")
            elif predicate =="has":
                lines.append(f"A {subject} has {obj}.")
            else:
                lines.append(f"A {subject} {predicate.replace('_', ' ')} {obj}.")
        return " ".join(lines)
    
    
    def set_facts(self, triple:Triple):
        """
        Writes a triple to memory.json
        """
        fact = triple.to_dict()

        # Add to memory
        self.memory.append(fact)

        # Update indexes
        self.by_subject[triple.subject].append((triple.predicate, triple.obj))
        self.by_predicate_object[(triple.predicate, triple.obj)].append(triple.subject)

        # Save to disk
        save_memory(self.config_path, self.memory)

    
    


        


