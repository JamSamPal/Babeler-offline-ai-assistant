import subprocess

class tts():
    # This class speaks
    def __init__(self):
        pass

    def speak(self, text):
        # speaker logic goes here
        print(f"🗣️{text}")
        subprocess.run(["./body/apps/tts_speaker", text])
