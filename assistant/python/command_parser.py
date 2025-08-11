import re
from assistant.python.semantics import Triple


class CommandParser:
    """
    Takes user input and then tells offline_assistant what function to call and any inputs it requires
    """

    def __init__(self):
        self.synonyms = {
            "time": ["time", "clock", "hour", "current time"],
            "name": ["name", "called"],
            "personality": ["personality", "mood", "character"],
            "has": ["have", "possess", "contain", "includes"],
            "is a": ["type of", "kind of", "sort of", "category", "are"],
            "remember": ["remember", "recall", "note"],
            "facts about": ["facts about", "information about", "tell me about"],
            "help": ["help", "commands", "what can you do", "list commands"],
        }
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
                r"^(?:set|change) your name to (.+)$", re.IGNORECASE
            ),
            "set_personality_to": re.compile(
                r"^(?:set|change) (?:my|your)? personality to (.+)$", re.IGNORECASE
            ),
            "set_and_parse_file": re.compile(
                r"^(?:parse|read|load)(?: the)? file (?:named )?(.+?)(?:\.txt)?$",
                re.IGNORECASE,
            ),
            # general
            "get_help": ["help", "what can you do", "commands", "list commands"],
        }
        # Every query must be written so as to capture a triple in the following order:
        #                "subject", "predicate", "object"
        # If one or more of these is absent they should still be captured but as a blank ()
        # Note, we call self.normalise(text) first so tenses and synonyms should be accounted
        # for there, e.g. "have" is already normalised to "has" to fit the format of memory.json
        self.queries = {
            # "is a knife a fork" capturing "knife", "is a", "fork"
            # also avoids capturing a question like "is it a type of animal?"
            # which utilises a contextual memory to fill in the noun and is dealt
            # with later
            "is_a_x_a_type_of_y": re.compile(
                r"^is (?:a[n]? )?(?!it\b)(\w+) a (is a) (\w+)\??$", re.IGNORECASE
            ),
            # "does a bird have wings" capturing "bird", "has", "wings"
            "does_a_x_have_y": re.compile(
                r"^does (?:a[n]? )?(?!it\b)(\w+) (has) (.+)\??$", re.IGNORECASE
            ),
            # "remember a banana has skin" capturing "banana", "has" and "skin"
            "remember_x_y_z": re.compile(
                r"^remember(?: a| an)? (\w+) (is a|has|\w+) (.+)$", re.IGNORECASE
            ),
            # "tell me facts about dogs" capturing "dog", "", ""   (note the blanks)
            "facts_about_x": re.compile(
                r"^(?:what are|tell me)(?: some)? facts about (?:the )?(\w+?)s?()()\??$"
            ),
            # "what things are mammals" capturing "", "is a", "mammal"
            "what_things_are_x": re.compile(
                r"^()what things (is a) (.+?)(?:s)?(?:\?)?$", re.IGNORECASE
            ),
            # "what things have fur" capturing "", "has", "fur"
            "what_things_have_x": re.compile(
                r"^()what things (has) (.+?)(?:\?)?$", re.IGNORECASE
            ),
            # "who discovered relativity" capturing "", "discovered" and "relativity"
            "who_x_y": re.compile(
                r"^()who (\w+) (?:the )?([\w\s]+)\??$", re.IGNORECASE
            ),
            # contextual questions
            # Will replace "it" with last subject user entered
            "does_it_have_x": re.compile(
                r"^()does it (has) (.+?)(?:\?)?$", re.IGNORECASE
            ),
            "is_it_a_type_of_x": re.compile(
                r"^()is it a (is a) (.+?)(?:\?)?$", re.IGNORECASE
            ),
        }

    def normalise_text(self, text):
        """
        Makes sure text is formatted to suit memory.json
        e.g. "have" is normalised to "has". Also deals with
        common synonyms
        """
        text = text.lower()
        # Replace longer synonyms first to avoid partial replacements
        for canonical, synonyms in sorted(
            self.synonyms.items(), key=lambda x: -max(len(s) for s in x[1])
        ):
            for syn in synonyms:
                # Word boundary to avoid partial word replacements
                pattern = rf"\b{re.escape(syn)}\b"
                text = re.sub(pattern, canonical, text)
        return text

    def parse(self, text):
        """
        Parses user input to either query memory.json
        or query personality.json
        """
        text = self.normalise_text(text)

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
