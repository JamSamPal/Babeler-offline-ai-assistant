import datetime
import subprocess

class system_monitor():
    # This class mainly returns status of system
    # will probably go to c++
    def __init__(self):
        pass

    def get(self, query):
        try:
            output = subprocess.check_output(["./body/apps/system_monitor", query]).decode().strip()
            return f"{output}"
        except Exception as e:
            print(f"Error calling get_{query}:", e)
            return None

    def get_time(self):
        return datetime.datetime.now()
