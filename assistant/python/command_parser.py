import re
from assistant.python.semantics import Triple, predicate_map


class CommandParser:
    """
    Takes user input and then tells offline_assistant what function to call and any inputs it requires
    """

    def __init__(self):
        self.commands = {
            # querying
            "get_time": ["time", "what time", "current time", "tell me the time"],
            "get_name": ["what is your name", "what's your name"],
            "get_personality": ["what is your personality", "what's your personality"],
            # setting variables
            "set_name": [
                "set name to",
                "set your name to",
                "change your name to",
                "change name to",
            ],
            "set_personality": [
                "set personality to",
                "set your personality to",
                "change personality to",
            ],
            # general
            "help": ["help", "what can you do", "commands", "list commands"],
        }
        self.queries = {
            "is a": re.compile(r"^is a (\w+) a (\w+)\??$", re.IGNORECASE),
            "has": re.compile(r"^does a (\w+) have (\w+)\??$", re.IGNORECASE),
            "facts": re.compile(
                r"^tell me facts about (?:the )?(\w+)(?:s)?\??$", re.IGNORECASE
            ),
            "remember": re.compile(r"^remember a (\w+) (\w+) (.+)$", re.IGNORECASE),
            "what": re.compile(
                r"^what (is|has) (?:a |an )?(.+?)(?:\?)?$", re.IGNORECASE
            ),
        }

    def parse(self, text):
        """
        User input will either lead to a query of memory.json or a query
        of personality.json
        """
        text = text.strip().lower()

        for type, pattern in self.queries.items():
            match = pattern.match(text)
            if match:
                return self.parse_query(type, match)

        return self.parse_command(text)

    def parse_query(self, type, match):
        if type == "facts":
            return (
                "get_facts",
                Triple(subject=match.group(1).lower(), predicate=None, obj=None),
            )
        elif type == "remember":
            return (
                "set_facts",
                Triple(
                    subject=match.group(1).lower(),
                    predicate=predicate_map[match.group(2).lower()],
                    obj=match.group(3).lower(),
                ),
            )

        elif type == "what":
            return (
                "get_inverse_answer",
                Triple(
                    subject=None,
                    predicate=predicate_map[match.group(1).lower()],
                    obj=match.group(2).lower(),
                ),
            )
        else:
            return (
                "get_answer",
                Triple(
                    subject=match.group(1).lower(),
                    predicate=predicate_map[type],
                    obj=match.group(2).lower(),
                ),
            )

    def parse_command(self, text):
        text = text.lower()

        if text == "":
            return ("greeting", None)

        for action, triggers in self.commands.items():
            for trigger in triggers:
                if trigger in text:
                    # finding value to "set"
                    if action.startswith("set"):
                        start = text.find(trigger) + len(trigger)
                        setter = text[start:].strip()
                        return (action, setter)
                    else:
                        return (action, None)

        return ("unknown", None)
