from head.stt import stt
from head.tts import tts
from head.command_parser import command_parser
from body.rf_scan import spectrum_analyser
from body.system_monitoring import system_monitor
import time
import platform
import subprocess

class Jarvis():

    def __init__(self):
        self.tts = tts()
        self.stt = stt()
        self.command_parser = command_parser()
        self.rf_scanner = spectrum_analyser()
        self.monitor = system_monitor()

    def main(self):
        self.tts.speak("Hello, I am online and awaiting your command.")

        while True:
            try:
                command = self.stt.listen()
                action = self.command_parser.parse_command(command)

                if action.startswith("get_"):
                    what = action.split("get_")[1]
                    response = self.get_value(what)
                    self.tts.speak(response)

                elif action.startswith("invoke_"):
                    what = action.split("invoke_")[1]
                    should_continue = self.invoke_action(what)
                    if should_continue is False:
                        break
                else:
                    self.tts.speak("Sorry, I didn't understand that.")


            except KeyboardInterrupt:
                self.tts.speak("Exiting now.")
                break

    def get_value(self, what):
        getters = {
            "temp": self.monitor.get_cpu_temp,
            "time": self.monitor.get_time
        }

        if what in getters:
            value = getters[what]()
            return f"The {what} is {value}"
        else:
            return "I don't know how to get that yet."


    def invoke_action(self, what):
        if what == "rf_scan":
            self.tts.speak("Scanning the radio spectrum now.")
            self.rf_scanner.scan_spectrum()

        elif what == "fan":
            self.tts.speak("Activating fan... Done.")

        elif what == "shutdown":
            self.tts.speak("Goodbye.")
            return False

        else:
            self.tts.speak("Unknown action.")
