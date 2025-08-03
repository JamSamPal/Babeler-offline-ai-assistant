from assistant.python.stt import stt
from assistant.python.tts import tts
from assistant.python.stt_text import stt as stt_text
from assistant.python.tts_text import tts as tts_text
from assistant.json.json_help import load_config, save_config_value
from assistant.python.command_parser import CommandParser
from assistant.python.semantics import Triple
from assistant.python.knowledge_base import KnowledgeBase
from assistant.python.document_parser import DocumentParser
import datetime

memory_path = "assistant/json/memory.json"
personality_path = "assistant/json/personality.json"
model_path = "assistant/voice_models/vosk-model-small-en-us-0.15"
text_bank_path = "assistant/text_bank"


class Assistant:
    """
    Main assistant class for handling user input, parsing commands,
    and interacting with TTS, STT, and memory modules.
    """

    def __init__(self, soundless=False):
        # Personality
        self.config = load_config(personality_path)
        self.name = self.config.get("name", "Jarvis")
        self.personality = self.config.get("personality", "default")
        self.soundless=soundless

        # Wake keywords
        # All commands must follow a wake keyword
        # except if you are using the soundless,
        # text-only mode
        self.WAKE_KEYWORDS = [
            f"{self.name} ",
            f"hey {self.name} ",
            "hey ",
            "hello ",
            "hi ",
        ]

        # Listening and speech functionalities
        if soundless:
            self.tts = tts_text(self.personality)
            self.stt = stt_text(model_path)
        else:
            self.tts = tts(self.personality)
            self.stt = stt(model_path)

        self.command_parser = CommandParser()
        self.knowledge_base = KnowledgeBase(memory_path)
        self.document_parser = DocumentParser()

    def main(self):
        """
        Run the loop of listen, query, reply
        """
        # Greet based on time
        self.tts.speak_greeting_by_time(datetime.datetime.now().hour)

        while True:
            try:
                command = self.stt.listen().lower()
                # print(f"[DEBUG] Heard: {command}")

                if self.soundless == False:
                    if not any(keyword in command for keyword in self.WAKE_KEYWORDS):
                        continue  # Ignore and keep listening

                    # Strip the keyword for cleaner command parsing
                    for keyword in self.WAKE_KEYWORDS:
                        if keyword in command:
                            command = command.replace(keyword, "").strip()

                # Get the command and optional argument (if no argument then arg = None)
                action, arg = self.command_parser.parse(command)

                if action == "help":
                    self.speak_help()

                elif action == "unknown":
                    self.tts.speak("Sorry, I didn’t understand.")

                elif action == "greeting":
                    self.tts.speak(self.tts.choose_random_reply("greeting"))
                else:
                    try:
                        method = getattr(self, action, None)
                        if arg is not None:
                            # handle setting a variable, e.g. name
                            # or querying data
                            result = method(arg)
                        else:
                            result = method()
                        
                        if result == "PENDING_FACT":
                            self.tts.speak("I don't know, would you like me to remember that for next time?")
                            reply = self.stt.listen().lower()
                            result = self.knowledge_base.possible_fact(reply)

                        self.tts.speak(result)
                    except:
                        self.tts.speak("Sorry, I didn't understand that.")

            except KeyboardInterrupt:
                self.tts.speak("Exiting now.")
                break

    ###############################
    # Queries of knowledge base
    ###############################

    def is_a_x_a_type_of_y(self, triple: Triple):
        return self.knowledge_base.get_answer(triple)

    def does_a_x_have_y(self, triple: Triple):
        return self.knowledge_base.get_answer(triple)

    def remember_x_y_z(self, triple: Triple, suppress_output=False):
        return self.knowledge_base.set_facts(triple, suppress_output=suppress_output)

    def facts_about_x(self, triple: Triple):
        return self.knowledge_base.get_facts(triple)

    def what_things_are_x(self, triple: Triple):
        return self.knowledge_base.get_inverse_answer(triple)

    def what_things_have_x(self, triple: Triple):
        return self.knowledge_base.get_inverse_answer(triple)

    def who_x_y(self, triple: Triple):
        return self.knowledge_base.get_inverse_answer(triple)

    ###############################
    # General queries
    ###############################

    def speak_help(self):
        cmds = list(self.command_parser.commands.keys())
        cmds_readable = [cmd.replace("_", " ") for cmd in cmds if cmd != "help"]
        help_text = "I can do the following commands: " + ", ".join(cmds_readable) + "."
        self.tts.speak(help_text)

    # --- Getters --
    def get_time(self):
        th = datetime.datetime.now().hour
        tm = datetime.datetime.now().minute
        return f"The current time is {th}:{tm}"

    def get_name(self):
        return f"My name is {self.name}"

    def get_personality(self):
        return f"My personality is {self.tts.personality}"

    # --- Setters --
    def set_and_parse_file(self, filename):
        path = text_bank_path + "/" + filename + ".txt"
        triples = self.document_parser.extract_triples(path)

        if not triples:
            return "invalid or empty file"
        for triple in triples:
            self.remember_x_y_z(triple, suppress_output=True)
        return f"{filename} parsed."

    def set_name_to(self, new_name):
        self.name = new_name
        save_config_value("name", new_name, self.config_path)
        return f"Okay, I will call myself {self.name} from now on."

    def set_personality_to(self, new_personality):
        all_personalities = load_config(personality_path)

        if new_personality not in all_personalities:
            available = ", ".join(all_personalities.keys())
            return f"I don't know how to act '{new_personality}'. Available personalities are: {available}."

        self.personality = new_personality
        self.tts.personality = new_personality
        self.tts.replies = self.tts.load_personality_replies()
        save_config_value("personality", new_personality, personality_path)
        return f"Okay, I will behave more {self.tts.personality} from now on"
