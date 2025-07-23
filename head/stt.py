import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

class stt:
    def __init__(self):
        pass

    def listen(self):
        return input("🧠 Type your command: ")