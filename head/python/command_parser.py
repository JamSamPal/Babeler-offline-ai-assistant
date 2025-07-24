class command_parser():
    def __init__(self):
        # Improve with more natural parsing, e.g. goodbye is a subset of bye
        # Ontology style thing
        self.commands = {
            # actions
            "invoke_rf_scan": ["scan spectrum", "radio scan", "look for signals"],
            "invoke_activate_fan": ["turn on fan", "activate fan", "start fan", "fan on"],
            "invoke_shutdown": ["shutdown", "turn off", "goodbye", "power down"],

            # querying
            "get_temp": ["temperature", "cpu temp", "how hot", "what's the temperature", "temp"],
            "get_time": ["time", "what time", "current time", "tell me the time"],
            "get_name": ["what is your name", "what's your name"],
            "get_personality": ["what is your personality", "what's your personality"],

            # setting variables
            "set_name": ["set name", "set your name", "change name", "call you"],
            "set_personality": ["set personality", "set your personality", "change personality", "act"],

            # general
            "help": ["help", "what can you do", "commands", "list commands"],
            "greeting":["hi", "good day", "good morning", "good afternoon"],
            "blank":[""] # In case user just says "Hey" or "Hey Jarvis"
        }

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
    
    def list_commands(self):
        return list(self.commands.keys())