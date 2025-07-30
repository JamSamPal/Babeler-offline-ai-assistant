import re
from assistant.python.babbeler import Triple


class command_parser:
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
            "set_name": ["set name", "set your name", "change name", "call you"],
            "set_personality": [
                "set personality",
                "set your personality",
                "change personality",
                "act",
            ],
            # general
            "help": ["help", "what can you do", "commands", "list commands"],
            "greeting": ["hi", "good day", "good morning", "good afternoon"],
            "blank": [""],  # In case user just says "Hey"
        }
        self.queries = {
            "is_a": re.compile(r"^is a (\w+) a (\w+)\??$", re.IGNORECASE),
            "has": re.compile(r"^does a (\w+) have (\w+)\??$", re.IGNORECASE),
            "facts": re.compile(
                r"^tell me facts about (?:the )?(\w+)(?:s)?\??$", re.IGNORECASE
            ),
            "remember": re.compile(r"^remember a (\w+) (\w+) (\w+)$", re.IGNORECASE),
        }

    def parse(self, text):
        """
        User input will either lead to a query of memory.json or a query
        of personality.json
        """
        text = text.strip().lower()

        for predicate, pattern in self.queries.items():
            match = pattern.match(text)
            if match:
                return self.parse_query(predicate, match)

        return self.parse_command(text)

    def parse_query(self, predicate, match):
        if predicate == "facts":
            return (
                "get_facts",
                Triple(subject=match.group(1).lower(), predicate=None, obj=None),
            )
        elif predicate == "remember":
            return ("set_facts", Triple(*[_.lower() for _ in match.groups()]))
        else:
            return (
                "get_answer",
                Triple(
                    subject=match.group(1).lower(),
                    predicate=predicate,
                    obj=match.group(2).lower(),
                ),
            )

    def parse_command(self, text):
        text = text.lower()

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
