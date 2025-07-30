from assistant.python.stt import stt
from assistant.python.tts import tts
from assistant.python.stt_text import stt as stt_text
from assistant.python.tts_text import tts as tts_text
from assistant.python.command_parser import command_parser
import json
import datetime

config_path="assistant/json/config.json"
personality_path="assistant/json/personality_replies.json"
model_path="assistant/voice_models/vosk-model-small-en-us-0.15"

class Assistant():

    def __init__(self, soundless = False):
        # Personality
        self.config = self.load_config(config_path)
        self.name = self.config.get("name", "Jarvis")
        self.personality = self.config.get("personality", "default")

        # Listening and speech functionalities
        if soundless:
            self.tts = tts_text(self.personality)
            self.stt = stt_text(model_path)
        else:
            self.tts = tts(self.personality)
            self.stt = stt(model_path)

        self.command_parser = command_parser()

    def main(self):
        # Greet based on time
        self.tts.speak_greeting_by_time( datetime.datetime.now().hour )

        while True:
            try:
                command = self.stt.listen().lower()
                #print(f"[DEBUG] Heard: {command}")

                # Check for wake keyword
                WAKE_KEYWORDS = ["jarvis", "hey jarvis", "hey", "hello", "hi"]
                # All commands must follow a wake keyword with the exception
                # of sleep commands which can be said on their own
                SLEEP_KEYWORDS = ["bye", "goodbye", "goodnight", "see you"]

                if any(keyword in command for keyword in SLEEP_KEYWORDS):
                    self.tts.speak(self.tts.choose_random_reply("goodbye"))
                    break

                if not any(keyword in command for keyword in WAKE_KEYWORDS):
                    continue  # Ignore and keep listening

                # Strip the keyword for cleaner command parsing
                for keyword in WAKE_KEYWORDS:
                    if keyword in command:
                        command = command.replace(keyword, "").strip()

                parsed_action = self.command_parser.parse_command(command)

                if isinstance(parsed_action, tuple):
                    action, arg = parsed_action
                else:
                    action, arg = parsed_action, None

                if action == "help":
                    self.speak_help()

                if action == "greeting" or action == "blank":
                    self.tts.speak(self.tts.choose_random_reply("greeting"))

                elif action.startswith(("get_", "invoke_", "set_")):
                    method = getattr(self, action, None)
                    if callable(method):
                        if arg is not None:
                            result = method(arg)
                        else:
                            result = method()
                        if result is not None:
                            self.tts.speak(result)
                    else:
                        self.tts.speak(f"Sorry, I don't know how to {action.replace('_', ' ')}.")
                else:
                    self.tts.speak("Sorry, I didn't understand that.")


            except KeyboardInterrupt:
                self.tts.speak("Exiting now.")
                break

    def speak_help(self):
        cmds = self.command_parser.list_commands()
        cmds_readable = [cmd.replace("_", " ") for cmd in cmds if cmd != "help"]
        help_text = "I can do the following commands: " + ", ".join(cmds_readable) + "."
        self.tts.speak(help_text)

    def load_config(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_config_value(self, key, value, path):
        try:
            with open(path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        config[key] = value
        with open(path, "w") as f:
            json.dump(config, f, indent=2)

    # --- Getters ---
    def get_temp(self):
        temp = self.monitor.get("temp")
        return f"The CPU temperature is {temp} degrees celcius"
    
    def get_cpu_usage(self):
        use = self.monitor.get("memory")
        return f"{use}"

    def get_time(self):
        time = self.monitor.get_time()
        return f"The current time is {time}"
    
    def get_name(self):
        return f"My name is {self.name}"
    
    def get_personality(self):
        return f"My personality is {self.tts.personality}"
    
    # --- Setters --
    def set_name(self, new_name):
        self.name = new_name
        self.save_config_value("name", new_name, config_path)
        return f"Okay, I will call myself {self.name} from now on."

    def set_personality(self, new_personality):
        all_personalities = self.load_config(personality_path)

        if new_personality not in all_personalities:
            available = ", ".join(all_personalities.keys())
            return f"I don't know how to act '{new_personality}'. Available personalities are: {available}."

        self.personality = new_personality
        self.tts.personality = new_personality
        self.tts.replies = self.tts.load_personality_replies()
        self.save_config_value("personality", new_personality, config_path)
        return f"Okay, I will behave more {self.tts.personality} from now on"
