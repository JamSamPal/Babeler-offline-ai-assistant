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
            "set_name_to": re.compile(
                r"^(?:set|change) (?:my|your)? name to (.+)$", re.IGNORECASE
            ),
            "set_personality_to": re.compile(
                r"^(?:set|change) (?:my|your)? personality to (.+)$", re.IGNORECASE
            ),
            "set_and_parse_file": re.compile(
                r"^(?:parse|read|load)(?: the)? file (?:named )?(.+?)(?:\.txt)?$",
                re.IGNORECASE,
            ),
            # general
            "help": ["help", "what can you do", "commands", "list commands"],
        }
        # Every query must be written so as to capture a triple in the following order:
        #                "subject", "predicate", "object"
        # If one or more of these is absent they should still be captured but as a blank ()
        self.queries = {
            # "is a knife a fork" capturing "knife", "type of", "fork"
            "is_a_x_a_type_of_y": re.compile(
                r"^is (?:a[n]? )?(\w+) a (type of) (\w+)\??$", re.IGNORECASE
            ),
            # "does a bird have wings" capturing "bird", "have", "wings"
            "does_a_x_have_y": re.compile(
                r"^does (?:a[n]? )?(\w+) (have) (.+)\??$", re.IGNORECASE
            ),
            # "remember a banana has skin" capturing "banana", "has" and "skin"
            "remember_x_y_z": re.compile(
                r"^remember(?: a| an)? (\w+) (\w+) (?:a |an )?(.+)$", re.IGNORECASE
            ),
            # "tell me facts about dogs" capturing "dog", "", ""   (note the blanks)
            "facts_about_x": re.compile(
                r"^(?:what are|tell me)(?: some)? facts about (?:the )?(\w+?)s?()()\??$"
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
        Parses user input to either query memory.json
        or query personality.json
        """
        text = text.strip().lower()

        # Check if the user input is a query of memory.json
        for type, pattern in self.queries.items():
            match = pattern.match(text)
            if match:
                return (type, Triple(*match.groups()))

        # Now check if user input is a query of personality.json
        for action, trigger_pattern in self.commands.items():
            # Set commands require an argument which we extract
            if action.startswith("set"):
                match = trigger_pattern.match(text)
                if match:
                    # For 'set' commands, the argument is the first captured group
                    return (action, match.group(1).strip())
            # Get commands have no argument to extract
            else:
                for trigger in trigger_pattern:
                    if trigger in text:
                        return (action, None)

        return ("unknown", None)
