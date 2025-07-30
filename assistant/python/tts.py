import subprocess
import random
import json

class tts():
    """
    tts implemented using "espeak" library
    """
    def __init__(self, personality="default"):
        self.personality = personality
        self.replies = self.load_personality_replies()

    def speak(self, text):
        try:
            # must have espeak installed
            command = f'espeak "{text}" --stdout | paplay'
            subprocess.run(command, shell=True)
        except Exception as e:
            print(f"{e} \n speech failed - check espeak is installed and then check audio device")
    

    def speak_greeting_by_time(self, hour):
        if 5 <= hour < 12:
            type_ = "morning"
        elif 12 <= hour < 20:
            type_ = "evening"
        else:
            type_ = "night"
        self.speak(self.choose_random_reply(type_))

    def load_personality_replies(self):
        # Load JSON with all personality replies
        try:
            with open("assistant/json/personality_replies.json", "r") as f:
                all_replies = json.load(f)
            return all_replies.get(self.personality, {})
        except Exception as e:
            print(f"Failed to load personality replies: {e}")
            return {}

    def choose_random_reply(self, type_):
        """Get a random reply for a given type (morning, evening, greeting, etc.)"""
        options = self.replies.get(type_, [])
        return random.choice(options)