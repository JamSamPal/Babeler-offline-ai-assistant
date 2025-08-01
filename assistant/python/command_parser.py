import re
from assistant.python.semantics import Triple, predicate_map


class CommandParser:
    """
    Takes user input and then tells offline_assistant what function to call and any inputs it requires
    """

    def __init__(self):
        self.commands = {
            # querying
            "get_time": [
                "time",
                "what time",
                "current time",
                "tell me the time",
                "get time",
            ],
            "get_name": ["what is your name", "what's your name", "get name"],
            "get_personality": [
                "what is your personality",
                "what's your personality",
                "get personality",
            ],
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
            # "is a knife a fork" capturing "knife", "fork"
            "is_a_x_a_y": re.compile(r"^is a (\w+) a (\w+)\??$", re.IGNORECASE),
            # "does a bird have wings" capturing "bird", "wings"
            "does_a_x_have_y": re.compile(
                r"^does a (\w+) have (.+)\??$", re.IGNORECASE
            ),
            # "tell me facts about dogs" capturing "dog"
            "facts_about_x": re.compile(r"^tell me facts about (?:the )?(\w+?)s?\??$"),
            # "remember a banana has skin" capturing "banana", "has" and "skin"
            "remember_a_x_y_z": re.compile(
                r"^remember a (\w+) (\w+) (.+)$", re.IGNORECASE
            ),
            # "what things are mammals" capturing "mammal"
            "what_things_are_x": re.compile(
                r"^what things are (\w+?)(?:s)?(?:\?)?$", re.IGNORECASE
            ),
            # "what things have fur" capturing "fur"
            "what_things_have_x": re.compile(
                r"^what things have (\w+?)(?:\?)?$", re.IGNORECASE
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
        handlers = {
            "facts_about_x": lambda m: (
                "get_facts",
                Triple(subject=m.group(1).lower(), predicate=None, obj=None),
            ),
            "remember_a_x_y_z": lambda m: (
                "set_facts",
                Triple(
                    subject=m.group(1).lower(),
                    predicate=predicate_map[m.group(2).lower()],
                    obj=m.group(3).lower(),
                ),
            ),
            "what_things_are_x": lambda m: (
                "get_inverse_answer",
                Triple(
                    subject=None,
                    predicate=predicate_map["are"],
                    obj=m.group(1).lower(),
                ),
            ),
            "what_things_have_x": lambda m: (
                "get_inverse_answer",
                Triple(
                    subject=None,
                    predicate=predicate_map["have"],
                    obj=m.group(1).lower(),
                ),
            ),
            "is_a_x_a_y": lambda m: (
                "get_answer",
                Triple(
                    subject=m.group(1).lower(),
                    predicate=predicate_map["is a"],
                    obj=m.group(2).lower(),
                ),
            ),
            "does_a_x_have_y": lambda m: (
                "get_answer",
                Triple(
                    subject=m.group(1).lower(),
                    predicate=predicate_map["has"],
                    obj=m.group(2).lower(),
                ),
            ),
        }

        try:
            return handlers[type](match)
        except KeyError:
            raise ValueError(f"No handler for query type: {type}")

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
