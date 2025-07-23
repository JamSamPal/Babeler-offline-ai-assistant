import numpy as np
import matplotlib.pyplot as plt

class spectrum_analyser():
    # will eventually use rf attachment, probably go to c++
    def __init__(self):
        pass

    def scan_spectrum(self):
        # Simulate a signal peak
        freqs = np.linspace(88e6, 108e6, 1000)
        power = np.random.normal(-90, 2, len(freqs))
        power[200:210] += 30  # Simulated spike at 92 MHz

        plt.plot(freqs / 1e6, power)
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Signal Power (dB)")
        plt.title("Simulated RF Spectrum")
        plt.grid(True)
        plt.show()