import datetime

class system_monitor():
    # will probably go to c++
    def __init__(self):
        pass

    def get_cpu_temp(self):
        return "52°C"

    def get_time(self):
        return datetime.datetime.now()
