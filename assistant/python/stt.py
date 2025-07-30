from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import queue


class stt:
    """
    See, e.g. https://github.com/alphacep/vosk-api/blob/master/python/example/test_microphone.py
    """

    def __init__(self, model_path):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.device = None
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def listen(self):
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.callback,
            device=self.device,
        ):
            print("🎤 Listening...")
            while True:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        print(f"🧠 Heard: {text}")
                        return text
