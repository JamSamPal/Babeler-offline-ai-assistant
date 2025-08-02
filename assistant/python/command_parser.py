import re
from assistant.python.semantics import Triple


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
            "set_name_to": [
                "set name to",
                "set your name to",
                "change your name to",
                "change name to",
            ],
            "set_personality_to": [
                "set personality to",
                "set your personality to",
                "change personality to",
            ],
            "set_and_parse_file": ["parse file"],
            # general
            "help": ["help", "what can you do", "commands", "list commands"],
        }
        # Every query must be written so as to capture a triple: "subject", "predicate", "object"
        # If one or more of these is absent they should still be captured but as a blank ()
        # New predicates must be updated in PredicateManager
        self.queries = {
            # "is a knife a fork" capturing "knife", "type_of", "fork"
            "is_a_x_a_type_of_y": re.compile(
                r"^is a[n]? (\w+) a (type of) (\w+)\??$", re.IGNORECASE
            ),
            # "does a bird have wings" capturing "bird", "have", "wings"
            "does_a_x_have_y": re.compile(
                r"^does a[n]? (\w+) (have) (.+)\??$", re.IGNORECASE
            ),
            # "remember a banana has skin" capturing "banana", "has" and "skin"
            "remember_x_y_z": re.compile(
                r"^remember(?: a| an)? (\w+) (\w+) (?:a |an )?(.+)$", re.IGNORECASE
            ),
            # "tell me facts about dogs" capturing "dog", "", ""   (note the blanks)
            "facts_about_x": re.compile(
                r"^tell me(?: some)? facts about (?:the )?(\w+?)s?()()\??$"
            ),
            # "what things are mammals" capturing "", "are", "mammal"
            "what_things_are_x": re.compile(
                r"^()what things (are) (\w+?)(?:s)?(?:\?)?$", re.IGNORECASE
            ),
            # "what things have fur" capturing "", "have", "fur"
            "what_things_have_x": re.compile(
                r"^()what things (have) (\w+?)(?:\?)?$", re.IGNORECASE
            ),
            # "who discovered relativity" capturing "", "discovered" and "relativity"
            "who_x_y": re.compile(
                r"^()who (\w+)(?: the)? ([\w\s]+?)(?:\?)?$", re.IGNORECASE
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
                return (type, Triple(*map(str.lower, match.groups())))

        return self.parse_command(text)

    def parse_command(self, text):
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
