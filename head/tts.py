import subprocess
import random

class tts():
    # This class speaks
    def __init__(self):
        # Predefined random replies for common phrases
        self.replies = {
            "greeting": ["Hello!", "Hi there!", "Greetings!", "Hey!", "Nice to see you!"],
            "morning": ["Good morning!", "Morning sunshine!", "Hope you slept well!", "Rise and shine!"],
            "afternoon": ["Good afternoon!", "Afternoon mate!", "Good day"],
            "night": ["Hello night owl", "What are you doing up at this time"],
            "goodbye": ["Goodbye!", "See you later!", "Shutting down.", "Until next time!", "Farewell!"]
        }

    def speak(self, text):
        # speaker logic goes here
        print(f"🗣️{text}")
        subprocess.run(["./body/apps/tts_speaker", text])
    
    def choose_random_reply(self, category):
        reply = random.choice(self.replies[category])
        self.speak(reply)

