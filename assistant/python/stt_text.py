class stt:
    """
    Microphone free "stt"
    """

    def __init__(self, *args, **kwargs):
        pass

    def listen(self):
        # prepend wake keyword to make typing easier
        return "hi " + input()
