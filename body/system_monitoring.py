import datetime
import subprocess

class system_monitor():
    # This class mainly returns status of system
    # will probably go to c++
    def __init__(self):
        pass

    def get_cpu_temp(self):
        try:
            output = subprocess.check_output(["./body/apps/get_temp"]).decode().strip()
            return f"{output}°C"
        except Exception as e:
            print("Error calling get_temp:", e)
            return None

    def get_time(self):
        return datetime.datetime.now()
