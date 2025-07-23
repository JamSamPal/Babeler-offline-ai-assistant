class command_parser():
    def __init__(self):
        # Improve with more natural parsing, e.g. goodbye is a subset of bye
        self.commands = {
            "invoke_rf_scan": ["scan spectrum", "radio scan", "look for signals"],
            "invoke_activate_fan": ["turn on fan", "activate fan", "start fan", "fan on"],
            "invoke_shutdown": ["shutdown", "turn off", "goodbye", "power down"],
            "get_temp": ["temperature", "cpu temp", "how hot", "what’s the temperature"],
            "get_time": ["time", "what time", "current time", "tell me the time"]
        }

    def parse_command(self, text):
        text = text.lower()

        for action, triggers in self.commands.items():
            if any(trigger in text for trigger in triggers):
                return action

        return "unknown"