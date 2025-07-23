from head.stt import stt
from head.tts import tts
from head.command_parser import command_parser
from body.rf_scan import spectrum_analyser
from body.system_monitoring import system_monitor
import time
import platform
import subprocess

class Jarvis():

    def __init__(self, name = "Jarvis", personality = "fun"):
        # Personality - will eventually impact speech
        self.name = name
        self.personality = personality

        # Listening and speech functionalities (head)
        self.tts = tts()
        self.stt = stt()
        self.command_parser = command_parser()

        # Operations (body)
        self.rf_scanner = spectrum_analyser()
        self.monitor = system_monitor()

    def main(self):
        self.tts.speak("Hello, I am online and awaiting your command.")

        while True:
            try:
                command = self.stt.listen()
                parsed_action = self.command_parser.parse_command(command)

                if isinstance(parsed_action, tuple):
                    action, arg = parsed_action
                else:
                    action, arg = parsed_action, None

                if action == "help":
                    self.speak_help()

                elif action.startswith(("get_", "invoke_", "set_")):
                    method = getattr(self, action, None)
                    if callable(method):
                        if arg is not None:
                            result = method(arg)
                        else:
                            result = method()
                        if result is False:
                            break
                        elif result is not None:
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

    # --- Getters ---
    def get_temp(self):
        temp = self.monitor.get_cpu_temp()
        return f"The CPU temperature is {temp}"

    def get_time(self):
        time = self.monitor.get_time()
        return f"The current time is {time}"
    
    def get_name(self):
        return f"My name is {self.name}"
    
    def get_personality(self):
        return f"My personality is {self.personality}"
    
    # --- Setters --
    def set_name(self, new_name):
        self.name = new_name
        return f"Okay, I will call myself {new_name} from now on."

    def set_personality(self, new_personality):
        self.personality = new_personality
        return f"Okay, I will behave more {self.personality} from now on"
    
    # --- Invokers ---
    def invoke_rf_scan(self):
        self.tts.speak("Scanning the radio spectrum now.")
        self.rf_scanner.scan_spectrum()

    def invoke_fan(self):
        self.tts.speak("Activating fan... Done.")

    def invoke_shutdown(self):
        self.tts.speak("Goodbye.")
        return False